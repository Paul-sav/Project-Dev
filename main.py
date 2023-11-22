import config
import machine
import time
import socket


def setup_udp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))  # Bind to all available interfaces
    print(f"UDP server started on port {port}")
    return server_socket  # Return the socket object


def move_forward():
    wheel_B1.value(1)
    wheel_B2.value(0)
    wheel_A1.value(0)
    wheel_A2.value(1)


def move_backward():
    wheel_B1.value(0)
    wheel_B2.value(1)
    wheel_A1.value(1)
    wheel_A2.value(0)


def turn_left():
    wheel_B1.value(0)
    wheel_B2.value(1)
    wheel_A1.value(0)
    wheel_A2.value(1)


def turn_right():
    wheel_B1.value(1)
    wheel_B2.value(0)
    wheel_A1.value(1)
    wheel_A2.value(0)


def stop_robot():  # Sets all outputs to LOW
    wheel_B1.value(0)
    wheel_B2.value(0)
    wheel_A1.value(0)
    wheel_A2.value(0)
    afwd.value(0)
    arev.value(0)


def actuator_up():  # Raises actuator for 1s
    afwd.value(0)
    arev.value(1)
    time.sleep(1)
    afwd.value(0)
    arev.value(0)


def actuator_down():  # Lowers actuator for 1s
    afwd.value(1)
    arev.value(0)
    time.sleep(1)
    afwd.value(0)
    arev.value(0)


# Map commands to functions
command_functions = {
    'w': move_forward,
    's': move_backward,
    'a': turn_left,
    'd': turn_right,
    'x': stop_robot,
    'q': actuator_up,
    'e': actuator_down
}

# region Pin initialization
# Actuator initialization
afwd = machine.Pin(4, machine.Pin.OUT)
afwd.value(0)
arev = machine.Pin(15, machine.Pin.OUT)
arev.value(0)

# PWM for motor wheels
wheel_PWM_B = machine.PWM(machine.Pin(25))
wheel_PWM_B.freq(20000)
wheel_PWM_B.duty(700)

wheel_PWM_A = machine.PWM(machine.Pin(26))
wheel_PWM_A.freq(20000)
wheel_PWM_A.duty(650)

# Wheel initialization
wheel_B1 = machine.Pin(12, machine.Pin.OUT)
wheel_B1.value(0)
wheel_B2 = machine.Pin(27, machine.Pin.OUT)
wheel_B2.value(0)
wheel_A1 = machine.Pin(13, machine.Pin.OUT)
wheel_A1.value(0)
wheel_A2 = machine.Pin(14, machine.Pin.OUT)
wheel_A2.value(0)
wheel_stby = machine.Pin(33, machine.Pin.OUT)
wheel_stby.value(1)
# endregion

UDP_PORT = 8080
server_socket = setup_udp_server(UDP_PORT)

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print("Received:", data.decode('utf-8'), "from", addr)

    if message.strip() == 'exit':
        break
    if message.strip().lower() == 'esp32 discovery':  # Filter out the discovery message
        continue
        
    command = message.strip().lower()
    command_function = command_functions.get(command)
    if command_function:
        command_function()
    else:
        print("Unknown command:", message)

    # Respond with the ESP32's IP address upon receiving a broadcast message
    if message.strip().lower() == 'esp32 discovery':
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        response_data = str(addr[0]).encode()
        response_address = (addr[0], UDP_PORT)  # Send the response to the sender's IP address
        try:
            udp.sendto(response_data, response_address)
        except Exception as e:
            print("Error occurred during send:", str(e))

server_socket.close()
print("UDP server stopped")

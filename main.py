import config
import machine
import time
import socket


def handle_command(command):
    if isinstance(command, bytes):
        command = command.decode('utf-8').strip().lower()  # Decode bytes to string and normalize

    if command == 'esp32 discovery':
        # Get the ESP32 unique ID
        esp32_unique_id = machine.unique_id()
        esp32_unique_id_hex = ''.join('{:02x}'.format(x) for x in esp32_unique_id)
        server_socket.sendto(esp32_unique_id_hex.encode(), ('<broadcast>', UDP_PORT))
    elif command == 'exit':
        global server_running
        server_running = False
    else:
        # Process other commands or simply print the received message for debugging
        print("Received:", command)


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

server_running = True

while server_running:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Received: {message} from {addr}")

    # Process the command
    handle_command(message)

server_socket.close()
print("UDP server stopped")

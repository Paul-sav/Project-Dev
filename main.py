import config
import machine
import time
import socket

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

ip_address = config.IP_ADDRESS
netmask = config.NETMASK
UDP_PORT = 8080


# region Movement functions
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
    time.sleep(1.3)
    afwd.value(0)
    arev.value(0)


def actuator_down():  # Lowers actuator for 1s
    afwd.value(1)
    arev.value(0)
    time.sleep(2)
    afwd.value(0)
    arev.value(0)


def speed_up():
    if wheel_PWM_A.duty() < 1000 and wheel_PWM_B.duty() < 1000:
        wheel_PWM_A.duty(wheel_PWM_A.duty() + 50)
        wheel_PWM_B.duty(wheel_PWM_B.duty() + 50)


def speed_down():
    if wheel_PWM_A.duty() > 400 and wheel_PWM_B.duty() > 400:
        wheel_PWM_A.duty(wheel_PWM_A.duty() - 50)
        wheel_PWM_B.duty(wheel_PWM_B.duty() - 50)


# endregion


def handle_command(command):
    try:
        if isinstance(command, bytes):
            command = command.decode('utf-8').strip().lower()

        print("Received command:", command)  # Print the received command

        commands = {
            'w': move_forward,
            's': move_backward,
            'a': turn_left,
            'd': turn_right,
            '': stop_robot,
            'q': actuator_up,
            'e': actuator_down,
            'z': speed_up,
            'x': speed_down
        }
        if command in commands:
            commands[command]()
        else:
            print("Unknown command:", command)

    except Exception as error:
        print("Exception occurred:", error)


def calculate_broadcast_address(ip_address, netmask):
    parts = list(map(int, ip_address.split('.')))
    netmask = list(map(int, netmask.split('.')))
    broadcast = [part | ~netmask[index] & 0xff for index, part in enumerate(parts)]
    broadcast_address = '.'.join(map(str, broadcast))
    return broadcast_address


def setup_udp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))  # Bind to all available interfaces
    print(f"UDP server started on port {port}")
    return server_socket  # Return the socket object


BROADCAST_ADDRESS = calculate_broadcast_address(ip_address, netmask)
server_socket = setup_udp_server(UDP_PORT)

discovery_handled = False  # Flag to track if discovery command has been handled

while True:
    try:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        # print(f"Received: {message} from {addr}")

        if message.startswith('CMD:'):
            command = message[4:]  # Extract the command without the prefix
            handle_command(command)
            continue

        if message == 'ESP32 Discovery' and not discovery_handled:
            handle_command(message)
            discovery_handled = True  # Set the flag indicating discovery command handled

    except Exception as error:
        print("Exception occurred:", error)

server_socket.close()
print("UDP server stopped")

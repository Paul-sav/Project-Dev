import config
import machine
import time
import socket
import network

# region Pin initialization
# Actuator initialization
afwd = machine.Pin(4, machine.Pin.OUT)
afwd.value(0)
arev = machine.Pin(15, machine.Pin.OUT)
arev.value(0)

# PWM for motor wheels
wheel_PWM_B = machine.PWM(machine.Pin(25))
wheel_PWM_B.freq(20000)
wheel_PWM_B.duty(500)

wheel_PWM_A = machine.PWM(machine.Pin(26))
wheel_PWM_A.freq(20000)
wheel_PWM_A.duty(500)

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

# region WiFi settings
# Access Point Settings
UDP_PORT = 8080
AP_SSID = "Pallet Robot"
AP_PASS = "12345"

# Disables WiFi and enables Access Point
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
sta_ap = network.WLAN(network.AP_IF)
sta_ap.active(True)
sta_ap.config(essid=AP_SSID, password=AP_PASS, authmode=network.AUTH_WPA2_PSK, hidden=False)
ap_ip = sta_ap.ifconfig()[0]
ap_broadcast = ap_ip[:ap_ip.rfind('.')] + '.255'
# endregion


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


def actuator_up():  # Raises actuator for 1.3s, any higher risks the supports uncoupling
    global actuator_flag
    if not actuator_flag:
        afwd.value(1)
        arev.value(0)
        time.sleep(1.3)
        afwd.value(0)
        arev.value(0)
        actuator_flag = True


def actuator_down():  # Lowers actuator for 2s
    global actuator_flag
    afwd.value(0)
    arev.value(1)
    time.sleep(2)
    afwd.value(0)
    arev.value(0)
    actuator_flag = False  # Resets flag


def speed_up():
    if wheel_PWM_A.duty() < 1000 and wheel_PWM_B.duty() < 1000:
        wheel_PWM_A.duty(wheel_PWM_A.duty() + 50)
        wheel_PWM_B.duty(wheel_PWM_B.duty() + 50)


def speed_down():
    if wheel_PWM_A.duty() > 300 and wheel_PWM_B.duty() > 300:
        wheel_PWM_A.duty(wheel_PWM_A.duty() - 50)
        wheel_PWM_B.duty(wheel_PWM_B.duty() - 50)


# endregion


# region UDP and IP address functions
def handle_command(command):
    try:
        if isinstance(command, bytes):
            # Checks if command is in bytes and decodes it to a lowercase string
            command = command.decode('utf-8').strip().lower()

        print("Received command:", command)  # Print the received command

        commands = {  # Dictionary for possible commands
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


def setup_udp_server(port, ip_address):
    # Turns on UDP server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip_address, port))  # Bind to all available interfaces
    print(f"UDP server started on port {port}")
    afwd.value(1)  # Raises actuator for 500ms to show it started the server
    arev.value(0)
    time.sleep(0.5)
    afwd.value(0)
    arev.value(1)
    time.sleep(0.5)
    afwd.value(0)
    arev.value(0)
    return server_socket  # Return the socket object


def send_ip(client_socket, client_addr, broadcast):
    # Send the ESP32's IP address to the discovered client
    ip_message = f"ESP_IP:{ap_ip}"
    print(f"Sending {ip_message}")
    client_socket.sendto(ip_message.encode(), (broadcast, UDP_PORT))


# endregion

server_socket = setup_udp_server(UDP_PORT, ap_ip)

discovery_flag = False  # Flag to track if discovery command has been handled

actuator_flag = False  # Flag to prevent actuator from going up twice

while True:
    try:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode('utf-8')  # Decodes bytes received to string

        if message.startswith('CMD:'):
            command = message[4:]  # Extract the command without the prefix
            if command == 'l':  # Closes the server if stop is received
                break

            handle_command(command)
            continue

        if message == 'ESP Discovery' and not discovery_flag:
            print(f"Received: {message} from {addr}")
            send_ip(server_socket, addr, ap_broadcast)  # Send the ESP IP to the client
            discovery_flag = True  # Set the discovery true

    except Exception as error:
        print("Exception occurred:", error)

server_socket.close()
print("UDP server stopped")

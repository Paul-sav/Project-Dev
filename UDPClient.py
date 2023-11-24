import socket

BROADCAST_PORT = 8080  # Replace with the actual port
BROADCAST_ADDRESS = '192.168.108.255'  # Replace with current broadcast address


def send_command(command, client_socket, esp_ip, esp_port):  # Sends command to ESP
    try:
        client_socket.sendto(f"CMD:{command}".encode(), (esp_ip, esp_port))

    except Exception as error:
        print("Error sending command:", error)


def discover_esp():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(('0.0.0.0', BROADCAST_PORT))  # Bind to listen for responses
    # Sends discovery message to broadcast address
    client_socket.sendto('ESP Discovery'.encode(), (BROADCAST_ADDRESS, BROADCAST_PORT))

    client_socket.settimeout(5)  # Timeout to wait for replies

    try:
        while True:
            data, addr = client_socket.recvfrom(1024)
            message = data.decode('utf-8')  # Receive the IP address sent by the ESP
            print(f"Received: {message}")

            if message.startswith('ESP_IP:'):
                esp_ip = message.split(':')[1]  # Extract the IP address part
                print(f"ESP found at: {esp_ip}")
                ESP_PORT = 8080  # Replace with the actual port

                while True:  # Allows user to input commands after connecting
                    user_input = input("Enter a command: ")
                    if user_input.lower() == 'exit':
                        break  # Exit loop on 'exit' command
                    send_command(user_input, client_socket, esp_ip, ESP_PORT)
                break

    except socket.timeout:
        print("Discovery complete")

    return esp_ip if 'esp_ip' in locals() else None  # Returns non if no ESP is found


esp_ip = discover_esp()

if esp_ip is None:
    print("ESP not found")

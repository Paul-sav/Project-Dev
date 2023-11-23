import socket

def send_command(command, client_socket, esp_ip, esp_port):
    try:
        client_socket.sendto(f"CMD:{command}".encode(), (esp_ip, esp_port))
        # print(f"Sent command: {command}")
        
    except Exception as error:
        print("Error sending command:", error)

BROADCAST_PORT = 8080
BROADCAST_ADDRESS = '10.0.0.255'

def discover_esp():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(('0.0.0.0', BROADCAST_PORT))  # Bind to listen for responses

    client_socket.sendto('ESP32 Discovery'.encode(), (BROADCAST_ADDRESS, BROADCAST_PORT))

    client_socket.settimeout(5)  # Set a timeout to wait for replies

    try:
        while True:
            # data, addr = client_socket.recvfrom(1024)
            esp_ip = '10.0.0.27'  # Update the IP from the received address
            print(f"ESP found at: {esp_ip}")

            # Perform subsequent communication with ESP here
            ESP_PORT = 8080  # Replace with the actual port

            client_socket.settimeout(5)  # Set timeout for receiving responses

            while True:
                user_input = input("Enter a command: ")
                if user_input.lower() == 'exit':
                    break  # Exit loop on 'exit' command
                send_command(user_input, client_socket, esp_ip, ESP_PORT)

            # Once interaction with ESP is done, break the discovery loop
            break

    except socket.timeout:
        print("Discovery complete")

    return esp_ip if 'esp_ip' in locals() else None

esp_ip = discover_esp()

if esp_ip is None:
    print("ESP not found")

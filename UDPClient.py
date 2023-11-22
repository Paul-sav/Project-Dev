import socket
import time

def send_command(command, client_socket, esp_ip, esp_port):
    client_socket.sendto(command.encode(), (esp_ip, esp_port))
    print(f"Sent: {command}")

    # Listen for a response from the ESP32
    try:
        data, addr = client_socket.recvfrom(1024)
        print(f"Received response: {data.decode('utf-8')} from {addr}")
    except socket.timeout:
        print("No response received")

# Broadcasting discovery message to find ESP32
BROADCAST_PORT = 8080
BROADCAST_ADDRESS = '10.0.0.255'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.bind(('0.0.0.0', BROADCAST_PORT))  # Bind to listen for responses

client_socket.sendto('ESP32 Discovery'.encode(), (BROADCAST_ADDRESS, BROADCAST_PORT))

# Listen for replies
client_socket.settimeout(5)  # Set a timeout to wait for replies

try:
    while True:
        data, addr = client_socket.recvfrom(1024)
        esp_ip = addr[0]  # Update the IP from the received address
        print(f"ESP found at: {esp_ip}")

        # Sending a dummy command to check if ESP32 is responsive
        send_command('test', client_socket, esp_ip, BROADCAST_PORT)
        break  # Once a reply is received, stop listening
except socket.timeout:
    print("Discovery complete")

# Loop for user interaction after discovery
if 'esp_ip' in locals():
    ESP_PORT = 8080  # Replace with the actual port
    client_socket.settimeout(5)  # Set timeout for receiving responses

    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() == 'exit':
            break  # Exit loop on 'exit' command
        send_command(user_input, client_socket, esp_ip, ESP_PORT)

    client_socket.close()
else:
    print("ESP not found")

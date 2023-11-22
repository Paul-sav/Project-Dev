import socket

# Broadcast discovery message to find ESP32
BROADCAST_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.sendto('ESP32 Discovery'.encode(), ('<broadcast>', BROADCAST_PORT))

# Listen for replies
client_socket.settimeout(5)  # Set a timeout to wait for replies
try:
    while True:
        data, addr = client_socket.recvfrom(1024)
        esp_ip = data.decode('utf-8')
        if esp_ip.startswith("b'"):  # Check for the 'b' prefix indicating bytes literal
            esp_ip = esp_ip[2:-1]  # Remove the 'b' and single quotes
        print(f"ESP found at: {esp_ip}")
        break  # Once a reply is received, stop listening
except socket.timeout:
    print("Discovery complete")
finally:
    client_socket.close()

# Send commands to the discovered ESP32
if 'esp_ip' in locals():  # Check if the ESP32 was found
    ESP_IP = esp_ip  # Use the discovered ESP32's IP address
    ESP_PORT = 8080  # Replace with the UDP port your ESP32 is listening on

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Function to send commands to ESP32
    def send_command(command):
        client_socket.sendto(command.encode(), (ESP_IP, ESP_PORT))
        print(f"Sent: {command}")

    # Send commands after Enter is pressed
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() == 'exit':
            break  # Exit loop on 'exit' command
        send_command(user_input)

    # Close the socket when done
    client_socket.close()
else:
    print("ESP not found")
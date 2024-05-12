import machine
import socket
import time

# Set up PIR sensor
PIR_PIN = 16  # GPIO pin number where the PIR sensor is connected
BUZZER_PIN = 14  # GPIO pin connected to the buzzer
pir = machine.Pin(PIR_PIN, machine.Pin.IN)
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

# Server details
server_ip = '192.168.47.185'  # Replace with the server's IP address
server_port = 65000

# Establish socket connection with the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    # Read PIR sensor status
    motion_detected = pir.value()
    print('Motion detected:', motion_detected)

    # Send motion detection status to the server
    client_socket.sendall(str(motion_detected).encode())

    # Receive action from the server
    action = client_socket.recv(1024).decode()
    print('Received action from the server:', action)

    # Process the action and perform necessary operations
    if action == 'buzzer_on':
        buzzer.on()
        time.sleep(5)
        buzzer.off()
    else:
        buzzer.off()

    time.sleep(2)

# Close the connection
client_socket.close()


import socket
import threading
import logging
import tkinter as tk

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server details
server_ip = '192.168.47.185'  # Server IP address
server_port = 65000

# Function to handle client connections
def handle_client(client_socket, client_address):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()

        if data:
            logging.info(f'Received data from {client_address[0]}: {data}')
            if client_address[0] == '192.168.47.250':  # Replace with the actual IP address of Client 1
                # Handle data from Client 1 (motion detection)
                motion_detected = int(data)
                print('Motion detected:', motion_detected)

                # Determine action based on motion detection
                action = ""
                if motion_detected == 1:
                    action = "buzzer_on"
                else:
                    action = "buzzer_off"
                print('Action:', action)

                # Update GUI with received data and action
                update_gui(client1_label, motion_label1, None, None, action_label1, client_address[0], motion_detected, None, None, action)

                # Send action to Client 1
                client_socket.sendall(action.encode())
                logging.info(f'Sent action to {client_address[0]}: {action}')

            elif client_address[0] == '192.168.47.240':  # Replace with the actual IP address of Client 2
                # Handle data from Client 2 (temperature and CO2 level)
                temperature, co2_level = data.split(',')
                print('Temperature:', temperature)
                print('CO2 Level:', co2_level)

                # Determine actions based on temperature and CO2 level
                actions = []
                if float(temperature) > 25:
                    actions.append("led_on")
                else:
                    actions.append("led_off")

                if int(co2_level) == 1:
                    actions.append("buzzer_on")
                else:
                    actions.append("buzzer_off")

                print('Actions:', actions)

                # Update GUI with received data and actions
                update_gui(client2_label, None, temperature_label2, co2_label2, action_label2, client_address[0], None, temperature, co2_level, actions)

                # Send actions to Client 2
                client_socket.sendall(','.join(actions).encode())
                logging.info(f'Sent actions to {client_address[0]}: {actions}')

    # Close the client socket
    client_socket.close()

# Function to update the GUI labels
def update_gui(client_label, motion_label, temperature_label, co2_label, action_label, client, motion_detected, temperature, co2_level, action):
    client_label.config(text=f'Client: {client}')
    if motion_label:
        motion_label.config(text=f'Motion Detected: {motion_detected}')
    if temperature_label:
        temperature_label.config(text=f'Temperature: {temperature}')
    if co2_label:
        co2_label.config(text=f'CO2 Level: {co2_level}')
    if action_label:
        action_label.config(text=f'Action: {action}')

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(5)
print(f'Server listening on {server_ip}:{server_port}')

# Create the root window
root = tk.Tk()
root.title('Industrial Monitoring and Control')
root.geometry('600x300')

# Set background colors
root.configure(bg='lightgray')

# Create a label for the title
title_label = tk.Label(root, text='Industrial Monitoring and Control', font=('Arial', 16), bg='lightgray')

# Add the title label to the root window
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create a frame for Client 1
frame1 = tk.Frame(root, bg='white', padx=10, pady=10)
frame1.grid(row=1, column=0, sticky='nsew')

# Create labels for Client 1
client1_label = tk.Label(frame1, text='Client: -', font=('Arial', 12), bg='white')
motion_label1 = tk.Label(frame1, text='Motion Detected: -', font=('Arial', 12), bg='white')
action_label1 = tk.Label(frame1, text='Action: -', font=('Arial', 12), bg='white')

# Add labels to the frame
client1_label.grid(row=0, column=0, pady=5)
motion_label1.grid(row=1, column=0, pady=5)
action_label1.grid(row=2, column=0, pady=5)

# Create a frame for Client 2
frame2 = tk.Frame(root, bg='white', padx=10, pady=10)
frame2.grid(row=1, column=1, sticky='nsew')

# Create labels for Client 2
client2_label = tk.Label(frame2, text='Client: -', font=('Arial', 12), bg='white')
temperature_label2 = tk.Label(frame2, text='Temperature: -', font=('Arial', 12), bg='white')
co2_label2 = tk.Label(frame2, text='CO2 Level: -', font=('Arial', 12), bg='white')
action_label2 = tk.Label(frame2, text='Action: -', font=('Arial', 12), bg='white')

# Add labels to the frame
client2_label.grid(row=0, column=0, pady=5)
temperature_label2.grid(row=1, column=0, pady=5)
co2_label2.grid(row=2, column=0, pady=5)
action_label2.grid(row=3, column=0, pady=5)

# Configure grid weights to utilize remaining space
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Function to start the server
def start_server():
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        # Create a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Create a thread to start the server
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Start the tkinter event loop
root.mainloop()

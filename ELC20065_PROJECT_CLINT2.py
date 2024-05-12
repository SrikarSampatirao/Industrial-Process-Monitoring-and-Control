import RPi.GPIO as GPIO
import Adafruit_DHT
import socket
import time

# Set up GPIO mode and define GPIO pin numbers
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED_PIN = 23
BUZZER_PIN = 24
DHT_PIN = 4
MQ2_ANALOG_PIN = 17
MQ2_DIGITAL_PIN = 27

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MQ2_DIGITAL_PIN, GPIO.IN)

# Define DHT11 sensor type
sensor = Adafruit_DHT.DHT11

# Server details
server_ip = '192.168.147.185'  # Replace with the server's IP address
server_port = 65000

def read_temperature():
    # Read temperature from the DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    return temperature

def read_gas_level():
    # Read gas level from the MQ-2 sensor
    gas_level = GPIO.input(MQ2_DIGITAL_PIN)
    return gas_level

# Establish socket connection with the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    # Read temperature and gas level
    temperature = read_temperature()
    gas_level = read_gas_level()
    print('Temperature:', temperature)
    print('Gas Level:', gas_level)

    # Create an array of sensor data
    sensor_data = [temperature, gas_level]

    # Send sensor data to the server as an array
    client_socket.sendall(','.join(str(data) for data in sensor_data).encode())

    # Receive action from the server as an array
    action = client_socket.recv(1024).decode().split(',')
    print('Received action from the server:', action)

    # Process the action and perform necessary operations
    if 'led_on' in action:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(LED_PIN, GPIO.LOW)
    elif 'buzzer_on' in action:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    time.sleep(5)

# Close the connection
client_socket.close()


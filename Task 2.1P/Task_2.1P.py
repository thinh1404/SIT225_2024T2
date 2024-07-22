import serial
import csv 
from datetime import datetime
import time

# Create a serial communication
s = serial.Serial(port = "COM7", baudrate = 9600, timeout=20)

filename = "DHT_22.data.csv"

with open(filename,"a", newline ="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Timestamp","Humidity","Temperature"])
    
    while True:
        line = s.readline().decode("utf-8").strip()
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # Split the line into humidity and temperature
        try:
            humidity, temperature = line.split(',')
            csv_writer.writerow([timestamp, humidity, temperature])
            csvfile.flush()  # Ensure data is written to file
        except ValueError:
            print(f"Data format error: {line}")
        time.sleep(1);    
    
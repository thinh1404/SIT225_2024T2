import serial
import csv
from datetime import datetime
import time

# Create serial communication objects for both Arduinos
s1 = serial.Serial(port="COM7", baudrate=9600, timeout=20)  # Accelerometer (X, Y, Z)
s2 = serial.Serial(port="COM12", baudrate=9600, timeout=20) # Temperature, Sound frequency

filename = "Fan_Motor.csv"

# Open the CSV file and write the header row
with open(filename, "a", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Timestamp", "Temperature", "Sound Frequency", "Accel_X", "Accel_Y", "Accel_Z"])

    while True:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        try:
            # Read and process data from COM12 (Temperature and Sound frequency)
            line_s2 = s2.readline().decode("utf-8").strip()
            temperature, sound_frequency = line_s2.split(',')

            # Read and process data from COM7 (Accelerometer X, Y, Z)
            line_s1 = s1.readline().decode("utf-8").strip()
            accel_x, accel_y, accel_z = line_s1.split(',')

            # Write data to CSV
            csv_writer.writerow([timestamp, temperature, sound_frequency, accel_x, accel_y, accel_z])
            csvfile.flush()  # Ensure data is written to the file

        except ValueError as e:
            print(f"Data format error: {e}")

        time.sleep(1)  # Adjust the delay as needed
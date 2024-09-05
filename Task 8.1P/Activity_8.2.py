import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime
import time

DEVICE_ID = "d2d8a108-d4c3-4794-bf15-271885269210"
SECRET_KEY = "YyuZ6b3CQZHTJC#TGX@@H7AiP"

# File for logging data
file = open('accelerometer_data.csv', 'a')

# Initialize buffers for x, y, z axis
data_buffer = {
    'x': [],
    'y': [],
    'z': []
}

# Function to log data to CSV
def log_data():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_string = f"{timestamp}, {data_buffer['x'][-1]}, {data_buffer['y'][-1]}, {data_buffer['z'][-1]}\n"
    file.write(csv_string)
    file.flush()
    print(f"Data logged: {csv_string.strip()}")

# Callback functions for accelerometer axis value changes
def on_x_acc_changed(client, value):
    data_buffer['x'].append(value)
    log_data()

def on_y_acc_changed(client, value):
    data_buffer['y'].append(value)
    log_data()

def on_z_acc_changed(client, value):
    data_buffer['z'].append(value)
    log_data()

def main():
    print("main() function")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with 'x', 'y', 'z' cloud variables
    # and listen on their value changes
    client.register("x", value=None, on_write=on_x_acc_changed)
    client.register("y", value=None, on_write=on_y_acc_changed)
    client.register("z", value=None, on_write=on_z_acc_changed)

    # Start cloud client
    client.start()

if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
    finally:
        file.close()


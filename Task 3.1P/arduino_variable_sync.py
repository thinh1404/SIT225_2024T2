import sys
import traceback
import random
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime
import time
DEVICE_ID = "dc2f7bd5-5a26-4cd6-91df-c72bcdbdede1"
SECRET_KEY = "SahriqBTzzP09PvP5Q62yyThg"


# Callback function on temperature change event.
# 
# Open the file in append mode once at the start
file = open('temperature_data.csv', 'a')

def on_temperature_changed(client, value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_string = f"{timestamp}, {value}\n"
    file.write(csv_string)
    file.flush()  # Ensure data is written to the file immediately
    print(f"New temperature logged: {csv_string.strip()}")


def main():
    print("main() function")
    try:
        

        # Instantiate Arduino cloud client
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
        )

        # Register with 'temperature' cloud variable
        # and listen on its value changes in 'on_temperature_changed'
        # callback function.
        # 
        client.register(
            "temperature", value=None, 
            on_write=on_temperature_changed)

        # start cloud client
        client.start()
        # Keep the script running for 10 minutes to log data
        time.sleep(600)
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()

    finally:
        # Close the file at the end of the execution
        file.close()

if __name__ == "__main__":
    try:
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
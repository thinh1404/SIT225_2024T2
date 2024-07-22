import random as rd
import time
import serial
from datetime import datetime

# Set the baud rate
baud_rate = 9600

# Create a serial port communication
s = serial.Serial(port = "COM7", baudrate = baud_rate, timeout=20)

while True:
    # SENDING STAGE
    # Random times blink of LED
    timesBlink = rd.randint(1,5)
    
    # Get the sending timestamp
    sendTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"{sendTime} Send >>> {timesBlink} blink times")
    
    # Send the data to Arduino
    s.write(bytes(str(timesBlink),"utf-8"))
    time.sleep(timesBlink)
    # RECEIVING STAGE
    
    # Receive the sleep time from Arduino
    sleepTime = s.readline().decode("utf-8").strip()
    # Receive timestamp
    recvTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{recvTime} Receive <<< {sleepTime} sleeping seconds")
    
    
   
    # Sleeping stage
    sleepTime = int(sleepTime)
    time.sleep(sleepTime)
    
    # Time stamp that python finishes sleeping
    wakeupTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"{wakeupTime} wake up")
    
    print("=" * 10)
    print()
   

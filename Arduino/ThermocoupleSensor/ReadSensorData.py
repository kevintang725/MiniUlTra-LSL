# Read, Record, and Save Data from AntNeuro Amplifier
# Author: Kai Wing Kevin Tang, 2023
# Requires sampling rate >=4096Hz in AntNeuro to pick up TTL

import pandas as pd
import time
import serial
import os

# Define COM Ports
arduino_port = '/dev/cu.usbmodem1301'

def write(x):
    arduino.write(bytes(x, 'utf-8'))

def read():
    receive = arduino.readline().decode("utf-8")
    try:
        l = list(receive)
    except:
        print("error")
    return receive


def main():

    # Main Loop
    print("-------------------------------------------------------------------------")
    print("Setting up serial communication with I/O...")
    print("-------------------------------------------------------------------------")

    # Establish serial communication with arduino
    try:
        arduino = serial.Serial(arduino_port,timeout=1, baudrate=115200)
    except:
        print('Unable to connect to arduino')
    
    # create dataframe to store streamed raw temperature data
    df = pd.DataFrame()
    
    # request file name input from user
    file_name = input('Please enter the filename to save as: ')

    # request total recording time to stream
    trial_duration = input('Please enter trial duration to record in seconds: ')
    
    # Begin timer
    start = time.time()
    while True:
        temperature = arduino.readline().decode("utf-8")
        # compute elapsed time
        elapsed_time = time.time() - start
        print("Elapsed Time (s): " + str(elapsed_time) + " | Temperature (C): " + str(temperature), end='\r')
        # append data to the dataframe
        #df = df.append({'Temperature (C)': temperature}, ignore_index=True)
        df = pd.concat([df, pd.DataFrame([{'Time (s)': elapsed_time, 'Temperature (C)': float(temperature)}])], ignore_index=True)

        # Check if recorded time has reached user input's total time desired
        if elapsed_time > int(trial_duration):
            # terminate and exit loop
            break
    
    # display dataframe store
    print(df)   
    print("Saving Data...")

    # save to csv
    df.to_csv(file_name + '.csv')
    print("Done")


if __name__ == '__main__':
    main()

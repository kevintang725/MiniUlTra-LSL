# Main Code
# Author: Kai Wing Kevin Tang, 2023

import serial
import time

# Import RehaMove3 Library
from rehamove import *

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    #time.sleep(0.05)
    #data = arduino.readline()

def read():
    receive = arduino.readline().decode("utf-8");
    print(receive)
    #print(value) # printing the value
    return receive

def FES_Parameters():
    FES_Current = 5         # mA
    FES_PulseWidth = 200    # us
    FES_Channel = "blue"    # Channel
    return FES_Channel, FES_Current, FES_PulseWidth

# Define COM Ports
arduino_port = '/dev/cu.usbmodem11401'
reha_port = 'COM3'

# Establish serial communication with arduino
try:
    arduino = serial.Serial(arduino_port,timeout=1, baudrate=115200)
except:
    print('Unable to connect to arduino')

# Establish serial communication with RehaMove3 and Set Parameters
try:
    FES_Channel, FES_Current, FES_PulseWidth = FES_Parameters()
    reha_move = Rehamove(reha_port)
    reha_move.version()
    reha_move.battery()
    reha_move.pulse(FES_Channel, FES_Current, FES_PulseWidth) # Sends pulse
except:
    print('Unable to connect to RehaMove3')
    pass

# Main Loop
print("-------------------------------------------------------------------------")
print("Main Terminal")
print("tFUS+FES+EEG Experiment v1")
print("User: Kevin Tang")
print("-------------------------------------------------------------------------")

while True:
    try:
        # Wait for initialization
        time.sleep(1)

        prompt = arduino.readline().decode("utf-8")

        userinput = input(prompt) # Taking input from user
        write(userinput)
        while True:
            trigger = read()
    except KeyboardInterrupt:
        write('0')
        time.sleep(1)
        trigger = read()
        pass
    


    

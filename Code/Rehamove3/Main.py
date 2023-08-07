# Main Code
# Author: Kai Wing Kevin Tang, 2023
# For Windows, only Python 3.7 Works

import serial
import time
import os


from rehamove import *

def write(x):
    arduino.write(bytes(x, 'utf-8'))

def read():
    receive = arduino.readline().decode("utf-8")
    try:
        l = list(receive)
        FUS_Trigger = l[0]
        FES_Trigger = l[1]
        # Check conditions for triggers
        if (l[0] == "1" and l[1] == "0") or (l[0] == "1" and l[1] == "1") or (l[0] == "0" and l[1] == "0") :
            print(FUS_Trigger + "," + FES_Trigger)
        else:
            print(receive)          
    except IndexError:
        print(receive)
        FUS_Trigger = "N"
        FES_Trigger = "N"
        pass
    except:
        FUS_Trigger = "N"
        FES_Trigger = "N"
    return receive, FUS_Trigger, FES_Trigger

def FES_Parameters():
    FES_Current = 5         # mA
    FES_PulseWidth = 200    # us
    FES_Channel = "blue"    # Channel
    return FES_Channel, FES_Current, FES_PulseWidth

def char_boolean(char):
    if (char == "1"):
        return True
    if (char == "0"):
        return False

# Define COM Ports
arduino_port = 'COM4'
reha_port = 'COM5'

# Main Loop
print("-------------------------------------------------------------------------")
print("Setting up serial communication with I/O...")
print("-------------------------------------------------------------------------")

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
    #reha_move.pulse(FES_Channel, FES_Current, FES_PulseWidth) # Sends pulse
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
            trigger, FUS, FES = read()
            # Check if FES Trigger is true, if so send pulse
            try:
                condition_FES = char_boolean(FES)
                if (condition_FES == True):
                    reha_move.pulse(FES_Channel, FES_Current, FES_PulseWidth) # Sends pulse
            except:
                print("Error: Cannot send FES Pulse")

    except KeyboardInterrupt:
        write('0')
        time.sleep(1)
        trigger, FUS, FES = read()
        pass
    


    

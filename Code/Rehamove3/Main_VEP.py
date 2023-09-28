# Main Code
# Author: Kai Wing Kevin Tang, 2023
# For Windows, only Python 3.7 Works
# Set AntNeuro Sampling Rate Fs = 512Hz

import serial
import time
import os
import pygame,time


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
        #if (l[0] == "1" and l[1] == "0") or (l[0] == "1" and l[1] == "1") or (l[0] == "0" and l[1] == "0") :
            #print(FUS_Trigger + "," + FES_Trigger)
        #else:
        #    print(receive)          
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
    FES_Current = 12         # mA
    FES_PulseWidth = 200    # us
    FES_Channel = "blue"    # Channel
    FES_Counter = 0         # Initialize FES Counts
    FES_Total_Count = 2   # Total Stimuli Count Limit
    return FES_Channel, FES_Current, FES_PulseWidth, FES_Counter, FES_Total_Count

def char_boolean(char):
    if (char == "1"):
        return True
    if (char == "0"):
        return False


# Define COM Ports
arduino_port = '/dev/cu.usbmodem1401'
reha_port = 'COM6'

# Photic Stimulation Parameters
Photic_Frequency = 25           # Hz

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
    FES_Channel, FES_Current, FES_PulseWidth, FES_Counter, FES_Total_Count = FES_Parameters()
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

pygame.init()
scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN )
r=1
while True:
    try:
        # Wait for initialization
        time.sleep(1)

        prompt = arduino.readline().decode("utf-8")

        #userinput = input(prompt) # Taking input from user
        #write(userinput)
        write('1')
        while True:
            trigger, FUS, FES = read()
            # Check if FES Trigger is true, if so send pulse
            try:
                condition_FES = char_boolean(FES)
                if (condition_FES == True and FES_Counter < FES_Total_Count):
                    reha_move.pulse(FES_Channel, FES_Current, FES_PulseWidth) # Sends pulse
                    FES_Counter += 1
                    print("FES Count: " + str(FES_Counter))

                    while (r < Photic_Frequency):
                        scr.fill(pygame.Color('black'))
                        pygame.display.update()
                        time.sleep(1/Photic_Frequency/2)
                        scr.fill(pygame.Color('white'))
                        pygame.display.update()
                        time.sleep(1/Photic_Frequency/2)
                        r+=1
                    scr.fill(pygame.Color('black'))
                    pygame.display.update()
                    r = 0
                if (FES_Counter >= FES_Total_Count):
                    write('0')
                    time.sleep(1)
                    trigger, FUS, FES = read()
                    pygame.quit()
            except:
                print("Error: Cannot send FES Pulse")

                

    except KeyboardInterrupt:
        write('0')
        time.sleep(1)
        trigger, FUS, FES = read()
        pass


    
    
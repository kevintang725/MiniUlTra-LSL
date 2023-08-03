# RehaMove3 Functional Electrical Stimulation
# Author: Kai Wing Kevin Tang, 2023

# Python code transmits a byte to Arduino /Microcontroller
import serial
import time


port = 'COM3'

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    #time.sleep(0.05)
    #data = arduino.readline()

def read():
    print(arduino.readline().decode("utf-8"))
    #print(value) # printing the value

# Establish serial communication with arduino
try:
    arduino = serial.Serial(port,timeout=1, baudrate=115200)
except:
    print('Unable to connect to arduino')

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
            read()
    except KeyboardInterrupt:
        write('0')
        time.sleep(1)
        read()
        pass
    


    

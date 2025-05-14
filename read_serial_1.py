import serial
import subprocess
import os
import sys
ser = serial.Serial(port='COM7', baudrate=230400, bytesize=8, parity='N', stopbits=1, timeout=5)
print(ser.name)

bytesToRead = 50 * 1024# 50 kilobytes
chunkSize = 500 # 500 bytes
file_1 = open("raw_ADC_values.data", "ab")

while (bytesToRead > 0):
    x = ser.read(min(chunkSize, bytesToRead)) # in case bytesToRead < chunkSize then read for remaining bytes
    file_1.write(x)
    bytesToRead -= len(x)
file_1.close()

compileResult = subprocess.getstatusoutput(f"gcc ADCtoWAV.c -o ADCtoWAV") #compiles the c program and generates the executable file
codeOutput = subprocess.getstatusoutput(f"ADCtoWAV raw_ADC_values.data recording.wav") #runs the executable with command line arguments
print(compileResult[0]) #prints 0 if compiled with no issues
print(compileResult[1]) #prints compilation errors, if any
print(codeOutput[0]) #prints 0 if the C program could run without any errors
print(codeOutput[1]) #prints any output displayed onto the terminal by the C program
ser.close()
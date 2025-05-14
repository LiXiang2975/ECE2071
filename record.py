import serial
import time
import subprocess
import os
import sys

#set serial UART parameters (note that baudrate should be higher than ADC sampling rate)
ser = serial.Serial(port = "COM6",baudrate = 230400, bytesize = 8,parity="N",stopbits = 1, timeout = 5)
#check whether the serial communication is active
print(ser.name)

chunkSize = 500 # 500 bytes


mode = input("1 for normal operating mode or 2 for distance trigger mode: ")

ser.write(mode.encode())

mode = int(mode)

if mode == 1:
    print("System in Manual Recording Mode.\n")
    duration = input("Enter duration for audio recording: ")
    #send duration to stm
    # duration = int(duration)
    # ser.write(duration.encode())
    duration = float(duration)
    #calculate end time
    end_time = time.time() + duration

    fileSize = int(6400 * 16 / 8 * duration)


    #open te binary file to write the raw ADC values
    if os.path.exists("raw_ADC_values.data"):
        os.remove("raw_ADC_values.data")

    file_1 = open("raw_ADC_values.data","wb")
    while time.time() <end_time:
        x = ser.read(min(chunkSize, fileSize)) #read 5000 bytes over UART
        file_1.write(x) #write 5000 bytes to file
        fileSize -= len(x)
        # print("1")

elif mode == 2:
    print("System in Distance Trigger Mode.\n")
    fileSize = 0

    #open te binary file to write the raw ADC values
    if os.path.exists("raw_ADC_values.data"):
        os.remove("raw_ADC_values.data")

    file_1 = open("raw_ADC_values.data","wb")
   
    while True:
        try:
            x = ser.read(chunkSize) #read 5000 bytes over UART
            file_1.write(x) #write 5000 bytes to file
            fileSize += len(x)
        #     generate = input("Enter 1 to generate file: ")
        #     generate = int(generate)

        #     if  generate == 1:
               


        #     number = int(user_input)
        #     print(f"You entered: {number}")

        except KeyboardInterrupt:
            print("ok wait ahh\n")
            break
        #     print("Invalid input! Please enter a valid number.")
                #         break
 

    # x = ser.read(50000) #read 5000 bytes over UART
    # file_1.write(x) #write 5000 bytes to file

# while (bytesToRead > 0):
#     x = ser.read(min(chunkSize, bytesToRead)) # in case bytesToRead < chunkSize then read for remaining bytes
#     file_1.write(x)
#     bytesToRead -= len(x)
# file_1.close()




compileResult = subprocess.getstatusoutput(f"gcc ADCtoWAV.c -o ADCtoWAV") #compiles the c program and generates the executable file
codeOutput = subprocess.getstatusoutput(f"ADCtoWAV raw_ADC_values.data recording.wav {fileSize}") #runs the executable with command line arguments
print(compileResult[0]) #prints 0 if compiled with no issues
print(compileResult[1]) #prints compilation errors, if any
print(codeOutput[0]) #prints 0 if the C program could run without any errors
print(codeOutput[1]) #prints any output displayed onto the terminal by the C program    
file_1.close()
ser.close()
print("exiting program liao")
    
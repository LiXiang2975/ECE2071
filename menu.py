import serial
import time
import subprocess
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

## Global Variables
chunkSize = 500 # 500 bytes
sampleRate = 6400
channel = 1
bitsPerSample = 16
byteToBits = 8
outputFile = "raw_ADC_values.data"
teamID = "Group 6"
vin = 3.3  # 3.3 V into the STM

#set serial UART parameters (note that baudrate should be higher than ADC sampling rate)
ser = serial.Serial(port = "COM7",baudrate = 230400, bytesize = 8,parity="N",stopbits = 1, timeout = 5)
#check whether the serial communication is active
print(ser.name)

def manual_recording_mode():
    print("-------------------System operating in Manual Recording Mode-------------------\n")
    duration = float(input("Enter duration for audio recording: "))

    # Define starting time and ending time
    endTime = time.time() + duration

    fileSize = int(sampleRate * bitsPerSample / byteToBits * duration)

    remove_existing_file()

    fptr = open(outputFile,"wb")
    limited_recording(endTime, fileSize, fptr)
    print("\nRecording Completed...\n")

    outputFormat = output_format_menu(fileSize)

    fptr.close()
    print("Returning to Main Menu...\n")
    main_menu()

def distance_trigger_mode():
    print("-------------------System operating in Distance Trigger Mode-------------------\n")

    outputFormat = output_format_menu()
    distance = int(input("Enter the detection range of the ultrasonic sensor (Default 10 cm): "))

    remove_existing_file()

    fptr = open(outputFile,"wb")

    fileSize = unlimited_recording(fptr)
    outputFormat = output_format_menu(fileSize)

    fptr.close()
    print("Returning to Main Menu...\n")
    main_menu()

def output_format_menu(fileSize):
    while True:
        print("\nAudio Data Output Format")
        print("1: Generate WAV File")
        print("2: Plot Waveform PNG")
        print("3: Export CSV Data")
        print("4: Perform FFT Analysis")
        print("5: Exit to Main Menu")
        try:
            outputFormat = int(input("Enter number for desired output format: "))
            if outputFormat not in [1, 2, 3, 4, 5]:
                print("\nEnter number 1 to 5 la babi, so bad ke ur math!??")
            elif outputFormat == 1:
                generate_WAV(fileSize)
            elif outputFormat == 2:
                generate_PNG()
            elif outputFormat == 3:
                generate_CSV()
            elif outputFormat == 4:
                perform_FFT()
            elif outputFormat == 5:
                print("Exiting to Main Menu....")
                main_menu()
            else:
                return outputFormat
        except KeyboardInterrupt:
            print("\nWhy quit la aiyoooooooo cannot finish the code meh?????????")
            exit()
        except ValueError:
            print("\nEnter number 1 to 5 la babi, so bad ke ur math!??")

def remove_existing_file():
    if os.path.exists("raw_ADC_values.data"):
        os.remove("raw_ADC_values.data") 

def limited_recording(endTime, fileSize, fptr):
    while time.time() < endTime:
        try:
            x = ser.read(min(chunkSize, fileSize)) #read 5000 bytes over UART
            fptr.write(x) #write 5000 bytes to file
            fileSize -= len(x)
        except KeyboardInterrupt:
            print("Recording interrupted by the user...")
            break

def unlimited_recording(fptr):
    fileSize = 0
    startTime = time.time()
    while True:
        try:
            x = ser.read(chunkSize) #read 5000 bytes over UART
            fptr.write(x) #write 5000 bytes to file
            fileSize += len(x)
        except KeyboardInterrupt:
            print("Recording Completed...\n")
            return fileSize

def generate_WAV(fileSize):
    compileResult = subprocess.getstatusoutput(f"gcc ADCtoWAV.c -o ADCtoWAV") #compiles the c program and generates the executable file
    codeOutput = subprocess.getstatusoutput(f"ADCtoWAV raw_ADC_values.data recording.wav {fileSize}") #runs the executable with command line arguments
    print(compileResult[0]) #prints 0 if compiled with no issues
    print(compileResult[1]) #prints compilation errors, if any
    print(codeOutput[0]) #prints 0 if the C program could run without any errors
    print(codeOutput[1]) #prints any output displayed onto the terminal by the C program    

def generate_PNG():
    amplitude = read_values(outputFile, vin)
    
    # plot amplitude vs time
    plt.plot(amplitude)
    plt.title(outputFile)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude (V)")
    plt.grid(True)
    plt.savefig(f"ADC_Plot_{teamID}_{sampleRate}.png") # [Plot name][Group ID][Sampling rate]
    plt.show()

    process(amplitude)

def generate_CSV():
    return 0
    # ahhhhhhh

def perform_FFT():
    return 0
    # spider man spider man save the world fuck ur ass

def read_values(filename, vin): 
    raw = np.fromfile(filename, dtype=np.uint16) # assume binary 12 bit sample size in 16 bit format
    amplitude = (raw / 4095.0) * vin # find amplitude (voltage at time)
    return amplitude

def process(amplitude):
    with open("ADC_Processed.csv", mode='w', newline='') as file: # write into a csv file the processed data
        writer = csv.writer(file)
        writer.writerow(['Sample Rate (Hz)', sampleRate])  # write sample rate into first row
        writer.writerow(['Time (ms)', 'Amplitude (V)'])  # write headers into second row
        for i, value in enumerate(amplitude): # write index (time) and amplitude into following rows
            writer.writerow([i, value])

def main_menu():
    while True:
        print("\n-----------------------------------Main Menu-----------------------------------")
        print("1: Manual Recording Mode")
        print("2: Distance trigger Mode")
        print("3: Quit")
        print("-------------------------------------------------------------------------------")

        try:
            mode = int(input("Select Mode: "))
            if mode == 1:
                print("\n\nEntering Manual Recording Mode...\n")
                manual_recording_mode()
                break
            elif mode == 2:
                print("\n\nEntering Distance Trigger Mode...\n")
                distance_trigger_mode()
                break
            elif mode == 3:
                print("\nWhy you so boring, run the function then now wan quit alamak\n")
                exit()
            else:
                print("\nInvalid mode selected!")
                print("Select 1 to 3 la babi, dunno how to count isit ==> one two three, okay????\n")
        except ValueError:
            print("Brother, only numbers from 1 to 3 la, cant read???")
        except KeyboardInterrupt:
            print("\n\nChill la, cannot enter 3 to exit isit")
            print("Exiting...\n")
            exit()
    

if __name__ == "__main__":
    main_menu()


    
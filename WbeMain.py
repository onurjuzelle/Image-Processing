########################################################################
#
#    @File:    WbeMain.py
#
#    @Author:  İbrahim Alan
#              Onur Güzel
#
#    @Mail:    ibrahimalan996@gmail.com
#              onurguzel4@gmail.com
#
#    @Description:  The aim of this project is to design and 
#                   build a product that, on activation, 
#                   autonomously cleans a whiteboard.
#
#    @Note:    Version 1.0.0 (Library version) - 13 APR 2020
#
#    Created on 13 APR 2020 - MON, 09.47
#
#    @Version	1.0.0 - Modified Date : 13 APR 2020
#
########################################################################

#!/usr/bin/env python

# Import Libraries
try:
    import os
    import time
    import binascii
    import struct
    import multiprocessing
    
    import threading
    
    import WbeInformation
    import WbeGlobalVariables
    #import WbeSerialPort
    import WbeImageOperations
    import WbeEraser
except ImportError:
    print("Some required files could not be found for program in Main...",
          "\nPlease contact with the manufacturer!")
          
          
# Multiprocessing definitions    
input_queue_serial = multiprocessing.Queue()
output_queue_serial = multiprocessing.Queue()


# Class definitions
Information = WbeInformation.InformationClass()
#SerialPort = WbeSerialPort.SerialPortClass(input_queue_serial, output_queue_serial)


def mainLoop():
    
    print("Coordinates are calculating, please wait...")
    
    # Get input image
    input_image = WbeImageOperations.getImage()
    
    # Convert HSV image
    hsv_image   = WbeImageOperations.convertColorSpace(input_image)
    
    # Apply mask to image
    output_image = WbeImageOperations.applyMask(input_image, hsv_image)
    
    # Find objects to erase
    erase_image = WbeEraser.findEraseObjects(output_image)
    
    # Find coordinates to delete
    #WbeEraser.findEraseCoordinates(erase_image)
    
    # Find object corners
    coordinates_list = WbeEraser.findEraseObjectCorners(erase_image)
    
    # Print coordinates
    WbeEraser.printListOfCoordinates(coordinates_list)
    
    while True:
        try:
            #print("Main Loop!")
            time.sleep(5)
        except Exception as err:
            print("Main Loop Error!", err)


# Not used 
def mainThread():
    while True:
        try:
            #print("Main Thread!")
            time.sleep(1)
        except Exception as err:
            print("Main Thread Error!", err)


# Main
if __name__ == "__main__":
    
    # Initialization Messages
    Information.PrintInformation()
    Information.PrintInformationLibrary()
    
    #SerialPort.SerialPortOpen() # Open Serial Port
    #SerialPort.daemon = True
    #SerialPort.start()
    
    mainLoopThread = threading.Thread(target = mainThread)
    mainLoopThread.daemon = True
    mainLoopThread.start()
    
    mainLoop()
    

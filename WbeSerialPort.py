########################################################################
#
#    @File:    WbeSerialPort.py
#
#    @Author:  İbrahim Alan
#              Onur Güzel
#
#    @Mail:    ibrahimalan996@gmail.com
#              onurguzel4@gmail.com   
#
#    @Description:  This module encapsulates the access for the serial 
#                   port. It provides backends for Python running on 
#                   Windows, OSX, Linux, BSD etc.
#
#    For more detail; 
#        https://pyserial.readthedocs.io/en/latest/pyserial.html 
#
#    @Note:    Version 1.0.0 (Library version) - 16 APR 2020
#
#    Created on 16 APR 2020 - THU, 16.14
#
#    @Version	1.0.0 - Modified Date : 16 APR 2020
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
    import serial
    
    import WbeGlobalVariables
except ImportError:
    print("Some required files could not be found for program in Serial Port...",
          "\nPlease contact with the manufacturer!")


# Serial Port Class
class SerialPortClass(multiprocessing.Process):
    def __init__(self, input_queue_serial, output_queue_serial):
        multiprocessing.Process.__init__(self)
        
        self.input_queue_serial = input_queue_serial
        self.output_queue_serial = output_queue_serial
        
        self.number_of_messages_sent = 0
        self.number_of_messages_received = 0
        
        # Change this to match your local settings
        self.serialPortName     = 'COM7'
        self.serialPortBaudrate = 115200
        self.serialPort = self.SerialPortConfiguration(serial.Serial(), self.serialPortName, self.serialPortBaudrate)

    # Serial port configuration
    def SerialPortConfiguration(self, serialPort, portName, baud):
        serialPort = serial.Serial(
            port = portName,    # Device name or None
            baudrate = baud,    # Baud rate

            bytesize = serial.EIGHTBITS,    # Number of data bits
            parity = serial.PARITY_NONE,    # Disable parity checking
            stopbits = serial.STOPBITS_ONE, # Number of stop bits.

            timeout = 0.01,     # Set a read timeout value
            writeTimeout = 0.01, # Set a write timeout value 
            xonxoff = False,	# Disable software flow control
            rtscts = False,     # Disable hardware flow control (RTS/CTS)
            dsrdtr = False      # Disable hardware flow control (DSR/DTR)
        )
        return serialPort

    # Open serial port
    def SerialPortOpen(self):
        try:
            self.serialPort.open()
            return True
        except Exception as e:
            if(WbeGlobalVariables.info_print_allowed == 1):
                print("Error open serial port : " + str(e))
            return False

    # Check open/close status of serial port
    def SerialPortCheckStatus(self):
        if(self.serialPort.isOpen()):
            if(WbeGlobalVariables.info_print_allowed == 1):
                print("Port is Available!")
            return True
        else:
            if(WbeGlobalVariables.info_print_allowed == 1):
                print("Port is Not Available!")
            return False

    # Close serial port
    def SerialPortClose(self):
        try:
            self.serialPort.close()
        except Exception as e:
            if(WbeGlobalVariables.info_print_allowed == 1):
                print("Error Close Serial Port : " + str(e))

    # Write to serial port
    def SerialWrite(self, data):
        self.serialPort.flushInput()
        self.serialPort.write(data)
        self.number_of_messages_sent = self.number_of_messages_sent + 1
        
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Number Of Messages Sent :" + str(self.number_of_messages_sent))
        
        #print("Writing to Serial Port:")
        #print(data)

    # Read from serial port
    def SerialRead(self):
        try:
            coming_data = self.serialPort.read(100)
            return coming_data
        except Exception as err:
            if(WbeGlobalVariables.info_print_allowed == 1):
                print("No message")

    # Scheduler
    def run(self):
        while True:
            try:
                # look for incoming tornado request
                if not self.input_queue_serial.empty():
                    data = self.input_queue_serial.get()
                    # send it to the serial device
                    self.SerialWrite(data)

                # look for incoming serial data
                if (self.serialPort.inWaiting() > 0):
                    data = self.SerialRead()
                    self.output_queue_serial.put(data)
                    
                    self.number_of_messages_received = self.number_of_messages_received + 1
                    
                    if(WbeGlobalVariables.info_print_allowed == 1):
                        print("Number Of Messages Received :" + str(self.number_of_messages_received))
                        print("Coming Message From Serial Port:")
                        print(binascii.hexlify(data))
                    
            except Exception as err:
                print("Serial Run Error")



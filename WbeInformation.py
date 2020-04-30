########################################################################
#
#    @File:    WbeInformation.py
#
#    @Author:  İbrahim Alan
#              Onur Güzel
#
#    @Mail:    ibrahimalan996@gmail.com
#              onurguzel4@gmail.com
#
#    @Description:  This library prints general information to user 
#                   about software.
#
#    @Note:    Version 1.0.0 (Library version) - 14 APR 2020
#
#    Created on 14 APR 2020 - TUE, 10.11
#
#    @Version	1.0.0 - Modified Date : 14 APR 2020
#
########################################################################


#!/usr/bin/env python


# Import Libraries
try:
    import WbeGlobalVariables
except ImportError:
    print("Some required files could not be found for program in Information...",
          "\nPlease contact with the manufacturer!")


# Information Class
class InformationClass:
    def __init__(self):
        self.information_message = """
                             Bahcesehir University
                             

    Description : The aim of this project is to design and build a product
                  that, on activation, autonomously cleans a whiteboard.

    Project     : Autonomous Whiteboard Eraser
    Board       : Raspberry Pi 3

    Author      : 
    
    Version     : 1.0.0
    """

        self.information_library = """
    Imported Libraries:
        -> WbeInformation.py
        -> WbeGlobalVariables.py
        -> WbeImageOperations.py
        -> WbeEraser.py
        -> WbeSerialPort.py
        
    """

    # Print info about aim of program
    def PrintInformation(self):
        if(WbeGlobalVariables.info_print_allowed==1):
            print(self.information_message)

    # Print info about imported libraries
    def PrintInformationLibrary(self):
        if(WbeGlobalVariables.info_print_allowed==1):
            print(self.information_library)

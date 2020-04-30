########################################################################
#
#    @File:    WbeGetInput.py
#
#    @Author:  İbrahim Alan
#              Onur Güzel
#
#    @Mail:    ibrahimalan996@gmail.com
#              onurguzel4@gmail.com
#
#    @Description:  This library perform delete operations
#
#    @Note:    Version 1.0.0 (Library version) - 17 APR 2020
#
#    Created on 17 APR 2020 - FRI, 10.24
#
#    @Version	1.0.0 - Modified Date : 17 APR 2020
#
########################################################################


#!/usr/bin/env python


# Import Libraries
try:
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    
    import WbeGlobalVariables  
except ImportError:
    print("Some required files could not be found for program...",
        "\nPlease contact with the manufacturer!")


# Find all pixels to delete
def findEraseCoordinates(ers_img):
    try:
        #print("Image size : ", ers_img.shape)

        lower_red = np.array([0,0,250])  # BGR-code of your lowest red
        upper_red = np.array([0,0,255])   # BGR-code of your highest red 
        
        mask_ers_img = cv2.inRange(ers_img, lower_red, upper_red)  
        
        cv2.imshow("Red shapes", mask_ers_img)
        cv2.waitKey(0)
        
        findEraseObjectCorners(mask_ers_img)
        
        # Get all non zero values
        list_coordinates = []
        coordinates = cv2.findNonZero(mask_ers_img)
        
        np.set_printoptions(threshold = np.inf) #BU KISIM TUM ARRAYI PRINT ETMEK ICIN 
        print(ers_img[60][152]) #bizim resimin tutuldugu array ise once y sonra x seklinde tutuluyor
        
        for j in range(len(coordinates)):
            list_coordinates.append(coordinates[j][0])#once x sonra y ekseni seklinde piksel degerlerini print ediyor 
            print(list_coordinates[j])
            
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Get Image Error : " + str(e))
        return False
        

# Find corner coodinates of shapes
def findEraseObjectCorners(ers_img):
    try:
        #print("Image size : ", ers_img.shape)

        lower_red = np.array([0,0,250])  # BGR-code of your lowest red
        upper_red = np.array([0,0,255])   # BGR-code of your highest red 
        
        gry_img = cv2.inRange(ers_img, lower_red, upper_red)  
        
        font = cv2.FONT_HERSHEY_COMPLEX

        rgb_img = cv2.cvtColor(gry_img, cv2.COLOR_GRAY2RGB)
        
        # Converting image to a binary image 
        # ( black and white only image). 
        _, threshold = cv2.threshold(gry_img, 110, 255, cv2.THRESH_BINARY) 

        # Detecting contours in image. 
        contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        list_coordinates = [[0 for x in range(20)] for x in range(int(len(contours)))] 
        shape_counter = 0
        
        # Going through every contours found in the image. 
        for cnt in contours : 
  
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
  
            # draws boundary of contours. 
            cv2.drawContours(gry_img, [approx], 0, (0, 0, 255), 5)  
  
            # Used to flatted the array containing 
            # the co-ordinates of the vertices. 
            n = approx.ravel()  
            i = 0
            
            coordinate_counter = 0

            for j in n : 
                if(i % 2 == 0): 
                    x = n[i] 
                    y = n[i + 1] 
                    
                    # String containing the coordinates. 
                    string = str(x) + " " + str(y)
                    
                    list_coordinates[shape_counter][coordinate_counter] = string
                    coordinate_counter+=1
  
                    if(i == 0): 
                        # Text on topmost coordinate. 
                        #cv2.putText(rgb_img, "Shape", (x, y), font, 0.2, (255, 0, 0))
                        #cv2.circle(image, center_coordinates, radius, color, thickness) 
                        cv2.circle(rgb_img, (x, y), 2, (255, 0, 0), 2) 
                    else: 
                        # Text on remaining coordinates. 
                        #cv2.putText(rgb_img, string, (x, y), font, 0.2, (0, 0, 255))
                        cv2.circle(rgb_img, (x, y), 2, (255, 0, 0), 2) 
                    
                    #list_coordinates[i].extend([(x, y)])
                i = i + 1
            shape_counter+=1
  
        # Showing the final image. 
        plt.subplot(111),plt.imshow(rgb_img),plt.title('Coordinates')
    
        plt.show() 

            
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Erase Object Corners Error : " + str(e))
        return False
        
    return list_coordinates
    

# Find objects to erase
def findEraseObjects(out_img):
    try:
		# Convert to gray scale
        gry_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2GRAY)

        # Apply threshold on gray image
        ret,threshold_img = cv2.threshold(gry_img, 127, 255, 1)

        # Find contours
        contours, h = cv2.findContours(threshold_img, 1, 2)

        for contour in contours:
            
            approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
            
            if len(approx) == 5:
                #print ("Pentagon")
                cv2.drawContours(out_img, [contour], 0, 255, -1)
            elif len(approx) == 3:
                #print ("Triangle")
                pass
            elif len(approx) == 2:
                #print ("Line")
                cv2.drawContours(out_img, [contour], 0, (0,0,255), -1)
            elif len(approx) == 4:
                #print ("Square")
                cv2.drawContours(out_img, [contour], 0, (0,0,255), -1)
            elif len(approx) == 9:
                #print ("Half circle")
                cv2.drawContours(out_img, [contour], 0, (255, 255, 0), -1)
            elif len(approx) > 10:
                #print ("Circle")
                cv2.drawContours(out_img, [contour], 0, (0, 0, 255), -1)
                
        plt.subplot(111),plt.imshow(out_img),plt.title('Found objects')
    
        plt.show()
        
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Get Image Error : " + str(e))
        return False
        
    return out_img
    

# Print coordinates to screen
def printListOfCoordinates(coordinate_list):
    try:
        for i in range(len(coordinate_list)):
            print("Shape ", i+1, " : \n", coordinate_list[i])
    
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Print List Coordinates Error : " + str(e))
        return False

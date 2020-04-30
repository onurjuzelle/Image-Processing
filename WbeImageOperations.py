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
#    @Description:  This library gets input to use
#
#    @Note:    Version 1.0.0 (Library version) - 15 APR 2020
#
#    Created on 15 APR 2020 - WED, 13.54
#
#    @Version	1.0.0 - Modified Date : 15 APR 2020
#
########################################################################


#!/usr/bin/env python


# Import Libraries
try:
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt  
    
    import WbeGlobalVariables
    import WbeEraser
except ImportError:
    print("Some required files could not be found for program in Input...",
        "\nPlease contact with the manufacturer!")
        

# Get test image from local folder   
def getImage():
    try:
        img = cv2.imread("capstone.png")
        if img is None:
            print("Could not open or find the image!")
            
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Get Image Error : " + str(e))
        return False
    
    return img
    

# To convert color space
def convertColorSpace(src_img):
    try:
        # Convert the Gray Scale
        gry_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        
        # Convert the HSV 
        hsv_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)
    
        # Mask image using HSV
        msk_img = cv2.inRange(hsv_img, (36, 25, 25), (70, 255,255))
    
        showStartupImages(src_img, gry_img, hsv_img, msk_img)
    
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Convery Color Space Error : " + str(e))
        return False
    
    return hsv_img
    

# Apply mask
def applyMask(src_img, hsv_img):
    try:
        color_mask = cv2.inRange(hsv_img, (36, 25, 25), (70, 255,255))
        masked_image = np.zeros_like(src_img)
        cv2.drawContours(masked_image, findContours(color_mask), 0, (255,255,255), -1) 
        output_image = np.zeros_like(src_img)
        
        output_image[masked_image == (0,0,0)] = src_img[masked_image == 0]
        
        showMaskedImages(src_img, color_mask, masked_image, output_image)

    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Convery Color Space Error : " + str(e))
        return False
    
    return output_image
    

# Find contours
def findContours(mask):
    try:
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Convert Color Space Error : " + str(e))
        return False
    
    return contours


# To show images 
def showStartupImages(src_img, gry_img, hsv_img, msk_img):
    try:
        plt.subplot(221),plt.imshow(src_img),plt.title('Source')
        plt.subplot(222),plt.imshow(gry_img,'gray'),plt.title('Gray')
        plt.subplot(223),plt.imshow(hsv_img,'hsv'),plt.title('Hsv')
        plt.subplot(224),plt.imshow(msk_img,),plt.title('Masked')
    
        plt.show()
        
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Get Image Error : " + str(e))
        return False
        

# To show images 
def showMaskedImages(src_img, color_mask, masked_image, output_image):
    try:
        plt.subplot(221),plt.imshow(src_img),plt.title('Source')
        plt.subplot(222),plt.imshow(color_mask),plt.title('Color Masked')
        plt.subplot(223),plt.imshow(masked_image),plt.title('Masked')
        plt.subplot(224),plt.imshow(output_image),plt.title('Output')
    
        plt.show()
        
    except Exception as e:
        if(WbeGlobalVariables.info_print_allowed == 1):
            print("Get Image Error : " + str(e))
        return False

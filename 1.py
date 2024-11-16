import cv2
import numpy as np
import pyautogui
import time
import random as rd

# set the window size and position of the Minecraft game
win_width = 1920
win_height = 1080
win_x = 50
win_y = 50

# set the coordinates of the region of interest (ROI) containing the slider
roi_x = 350
roi_y = 520
roi_width = 1100
roi_height = 50

# set the color thresholds for red and yellow
red_thresh = [0, 100, 100]
red_max = [10, 255, 255]
yellow_thresh = [20, 100, 100]
yellow_max = [40, 255, 255]

# set the coordinates of the space bar
space_x = 650
space_y = 900

# set the refresh rate of the screen capture (in milliseconds)
refresh_rate = 50

while True:
    timeun = rd.randint(1, 5)
    timedn = rd.randint(1, 59)

    # Sleep for a random time
    time.sleep(timeun + timedn / 60.0)
    start_time = time.time()
    timeout = 60  # secondes

    a=5
    pyautogui.click(button='right')


    # loop until the user presses the 'q' key
    while a>1:
        if time.time() - start_time > timeout:
            print("La boucle a été arrêtée après 30 secondes.")
            b=False
        # capture the screenshot of the Minecraft game window
        screenshot = pyautogui.screenshot(region=(win_x, win_y, win_width, win_height))

        # convert the screenshot to a numpy array and BGR format
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # extract the ROI containing the slider
        roi = screenshot[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width, :]

        # convert the ROI to HSV color space
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # create masks for the red and yellow sections of the slider
        red_mask = cv2.inRange(hsv, np.array(red_thresh), np.array(red_max))
        yellow_mask = cv2.inRange(hsv, np.array(yellow_thresh), np.array(yellow_max))

        # create a white mask by thresholding the grayscale image
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, white_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

        # pad the white mask to make it 2 pixels larger than the real size of the slider
        white_mask = cv2.copyMakeBorder(white_mask, 1, 1,0 , 0, cv2.BORDER_CONSTANT, value=0)

        # find the position of the slider by finding the center of mass of the white pixels

        # create masks for the red and yellow sections of the slider
        red_mask = cv2.inRange(hsv, np.array(red_thresh), np.array(red_max))
        yellow_mask = cv2.inRange(hsv, np.array(yellow_thresh), np.array(yellow_max))

        # create a white mask by thresholding the grayscale image
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, white_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

        # pad the white mask to make it 2 pixels larger than the real size of the slider
        white_mask = cv2.copyMakeBorder(white_mask, 1, 1, 0, 0, cv2.BORDER_CONSTANT, value=0)
        if time.time() - start_time > timeout:
            print("La boucle a été arrêtée après 30 secondes.")
            a=0

        # find the position of the slider by finding the center of mass of the white pixels
        moments = cv2.moments(white_mask, False)
        print("White mask moments m00:", moments["m00"])  # Debugging output
        if moments["m00"] != 0.0:
            slider_x = int(moments["m10"] / moments["m00"])
            slider_y = int(moments["m01"] / moments["m00"])

            # find the center of the red section by finding the center of mass of the red pixels
            moments_red = cv2.moments(red_mask, False)
            print("Red mask moments m00:", moments_red["m00"])  # Debugging output
            if moments_red["m00"] != 0.0:
                red_x = int(moments_red["m10"] / moments_red["m00"])
                red_y = int(moments_red["m01"] / moments_red["m00"])
                print("Center of red section: ({}, {})".format(red_x, red_y))
                print("Center of white section: ({}, {})".format(slider_x, slider_y))

                # check if the slider is in the red or yellow section of the bar
                if red_x != 0 and slider_x != 0:
                    print(red_x/slider_x)
                    print(slider_x/red_x)
                    if ((red_x / slider_x) <1.0 and (slider_x/red_x)<1.1) or ((red_x / slider_x) <1.0 and (slider_x/red_x)<1.1):
                        # simulate the space bar press
                        pyautogui.press('space')
                        print("vu")
                        print("Space bar pressed")
                        time.sleep(0.1)
                        a=0



        # display the red, yellow, and white masks
        cv2.imshow('Red Mask', red_mask)
        cv2.imshow('Yellow Mask', yellow_mask)
        cv2.imshow('White Mask', white_mask)

        # wait for a key press to close the windows
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # wait for the next refresh cycle
        time.sleep(refresh_rate / 1000.0)

    # close all open windows
    cv2.destroyAllWindows()
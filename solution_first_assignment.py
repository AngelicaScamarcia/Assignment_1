from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py solutions/exercise3_solution.py

"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

gold_dist = 0.8
""" float: distance that the robot can't pass once golden token is recognised"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

def dir_golden():
    right_dist=150
    left_dist=150
    for token in R.see():
        if (token.info.marker_type is MARKER_TOKEN_GOLD): #if golden token is detected from R.see function
	    if token.rot_y<110 and token.rot_y>80: # gold token is on its right
	        if token.dist <= right_dist:
		    right_dist = token.dist 
            elif -110 < token.rot_y < -80: # gold token is on its left
                if token.dist <= left_dist:
		        left_dist = token.dist 
    return right_dist, left_dist
   

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=50
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

while 1:
    dist_g, rot_g = find_golden_token()
    dist_s, rot_s = find_silver_token()
    
    if dist_g < gold_dist and abs(rot_g)<80: # stay far from boxes on l&r and go on
        print("golden token is nearby")
	print(dist_s, abs(rot_s))  
	
        if dist_s < 1 and abs(rot_s)<90: 
            print("silver token is here, grab it")
            
            if -a_th <= rot_s <= a_th: # if the robot is well aligned with the token, we go forward
	        print("Ah, that'll do.")
		if dist_s < d_th:
		    R.grab() # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
           	    print("Gotcha!")
  		    turn(30,2)
	    	    R.release() # release the silver token that you grabed
	   	    drive(-10,0.5)
	    	    turn(-30,2)
	    	else:
		    drive(20, 0.5)
		    
            elif rot_s < -a_th: # if the robot is not well aligned with the token, we move it on the left 
                print("Left a bit...")
        	turn(-2, 0.5)
    	    elif rot_s > a_th: # if the robot is not well aligned with the token, we move it on the right
                print("Right a bit...")
        	turn(+2, 0.5)
	    
        else:
            right_dist,left_dist = dir_golden() # calling the function to get the distance on the right and the left
	    print("golden token detected, turn around") 
	    
	    if (right_dist > left_dist):
	        print ("turn right")
	        while (abs (rot_g)<90): 
	            dist_g, rot_g = find_golden_token() # get the distance and the angle between the golden token and the robot by the function find_golden_tocken()
		    turn(5,0.5)
 	        drive(20,0.5)
	    elif(right_dist < left_dist):
	        print ("turn left")
	        while (abs (rot_g)<90): 
	            dist_g, rot_g = find_golden_token()  
		    turn(-5,0.5)
	        drive(20,0.5)
	   
    else:
        print("golden token is far from me")
	print(dist_s, abs(rot_s))
	if dist_s < 1 and abs(rot_s)<90:
	    print("silver token is here, grab it")	
		
	    if -a_th <= rot_s <= a_th: # if the robot is well aligned with the token, we go forward
	        print("Ah, that'll do.")
                if dist_s < d_th:
                    R.grab() # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
           	    print("Gotcha!")
		    turn(30,2)
	    	    R.release()
	   	    turn(-30,2)
	        else:
	            drive(20,0.5)
            elif rot_s < -a_th: # if the robot is not well aligned with the token, we move it on the left 
                print("Left a bit...")
                turn(-2, 0.5)
    	    elif rot_s > a_th: # if the robot is not well aligned with the token, we move it on the right
                print("Right a bit...")
                turn(+2, 0.5)
        else: 
            print("no taken detected")
	    drive (20,0.5)
        			

    				
        				
		

#Route Runner
import smbus			#import SMBus module of I2C
from time import sleep          #import
import numpy as np
import RPi.GPIO as GPIO
import datetime
import pandas as pd   
import RPi.GPIO as GPIO
import sys

#initialze variables to use as registers for accelertometer
accel_x_out_reg = 0x3B
accel_y_out_reg = 0x3D
accel_z_out_reg = 0x3F
d_address = 0x68

#universal variables
margin = 5
mov_fac = 15

def initialize_accel():

    #sets up the registers for reading from the accelerometer
    bus.write_byte_data(d_address, 0x19, 7)
    bus.write_byte_data(d_address, 0x6B, 1)
    bus.write_byte_data(d_address, 0x1A, 0)
    bus.write_byte_data(d_address, 0x1B, 24)
    bus.write_byte_data(d_address, 0x38, 1)

def read_data_from_accel(addr):

        #reads in raw data from accelerometer
        first = bus.read_byte_data(d_address, addr)
        second = bus.read_byte_data(d_address, addr+1)
        #combines the two registers
        data = ((first << 8) | second)
        
        #subtracts by the max value if less then half the value to make a signed integer
        if(data > 32768):
                data = data - 65536
        return data
    
def get_angles():
    
    #initializes values for use in system
    c_sph_pp_i = [0,0] #what will be returned
    Ax = 0
    Ay = 0
    Az = 0

    #reads in data over enough time to remove excessive noise
    for i in range(0,100):
        acc_x = int(read_data_from_accel(accel_x_out_reg)/300)
        acc_y = int(read_data_from_accel(accel_y_out_reg)/300)
        acc_z = int(read_data_from_accel(accel_z_out_reg)/300)
        
        Ax = acc_x + Ax
        Ay = acc_y + Ay
        Az = acc_z + Az
        
    #averages all data of time collected
    Ax = Ax/100
    Ay = Ay/100
    Az = Az/100

    #gets the phi value for sphereical coordinates                                                                                                                                            
    phi = np.arctan((np.sqrt((Ax**2)+(Ay**2))) / Az) 
    
    #gets theta value for spherical coordinates
    if(Ax > 0)                                                                                                            :
        theta = (np.arctan(Ay/Ax))
    elif(Ax == 0):
            if(Ay > 0):
                theta = np.pi/2
            else:
                theta = -np.pi/2
    else:
       theta = (np.arctan(Ay/Ax) + np.pi)
        
    #covnverts from traditional spherical to my coordinate system
    c_sph_pp_i[1] = -1 * (np.arctan((np.sin(phi) * np.cos(theta)) / np.cos(phi))) * (180/np.pi)
    c_sph_pp_i[0] = (np.arctan((np.sin(phi) * np.sin(theta)) / np.cos(phi))) * (180/np.pi)
    
    return c_sph_pp_i


#all the movement patterns for linear actuators
def moveforward_x(active):
        
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, active)
    status_fx = active
    return status_fx

def movebackward_x(active):
        
    GPIO.output(backward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(backward_channel_x, active)
    status_bx = active
    return status_bx

def moveforward_y(active):
        
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, active)
    status_fy = active
    return status_fy

def movebackward_y(active):
        
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, active)
    status_by = active
    return status_by

def stop():
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.LOW)
    return
    
def in_pos(x_goal, y_goal):
    value = False
    cur_pos_i = get_angles()

    
    if (((cur_pos_i[0] >= (x_goal - margin)) and (cur_pos_i[0] <= (x_goal + margin))) and ((cur_pos_i[1] >= (y_goal - margin)) and (cur_pos_i[1] <= (y_goal + margin)))):
        value = True
    else:
        value = False
    #print(value)  
    return value
    
def run_route():
    df = pd.read_csv('//home//pi//HLT_Shared//Route Data//Scanning_Route.csv')
    point_list = df.values.tolist()
    cur_pos = get_angles()
    print(df)
    print(point_list)
    
    for i in point_list: # increments through the list of points

        x_goal = i[0] #sets my goal points
        y_goal = i[1]
        print(x_goal)
        print(y_goal)
        
        print(get_angles())
        
        while(not(in_pos(x_goal, y_goal))): # checks to make sure both positons are correct if not it continues the loop
            
            cur_pos = get_angles() #updates position
            if((cur_pos[0] <= (x_goal - margin)) or (cur_pos[0] >= (x_goal + margin))): #checks x position and moves
                if (cur_pos[0] <= (x_goal - margin)): #if we are behind the goal move towards it
                    moveforward_x(1)
                    delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                    sleep(delta_x)
                    stop()
                elif (cur_pos[0] >= (x_goal + margin)): # if we are in front move towards it
                    movebackward_x(1)
                    delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                    sleep(delta_x)
                    stop()
                else: #stops movment when in postion
                    stop()
                    
                sleep(0.25)
                
            #print((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin)))
            cur_pos = get_angles() #updates postion to check again
            if((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin))): #checks y position and moves
                if (cur_pos[1] <= (y_goal - margin)): #if we are behind the goal move towards it
                    moveforward_y(1)
                    delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                    sleep(delta_y)
                    stop()
                elif (cur_pos[1] >= (y_goal + margin)): # if we are in front move towards it
                    movebackward_y(1)
                    delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                    sleep(delta_y)
                    stop()
                else: #stops movment when in postion
                    stop()
                    
                sleep(0.75)
                cur_pos = get_angles() #updates postion to check again
                
            print("Phi_x = ", cur_pos[0], "Phi_y = ", cur_pos[1])
            
        stop()
        sleep(3)
        #still with in all the points but I have gotten to the point where we need to collect data
        #write to file saying collect data
        with open('//home//pi//HLT_Shared//Route Data//Signal_Processing_Key.txt', 'w') as c:
            c.write('1')
        check_val = 1 #sets check values to 1 so it knows to go
        
        
        #sleep cycle waiting for something saying done collecting data
        while(check_val):
            with open('//home//pi//HLT_Shared//Route Data//Signal_Processing_Key.txt', 'r') as c:
                check_val = int(c.readlines()[0]) # checks to see if check_val is 0 yet
            print(check_val)
            print("sleepy_scan")
            sleep(15)
        #contiues to next postion and repeats
        
        
    #once we have moved to all the points it updates this file saying it has moved
    with open('//home//pi//HLT_Shared//Route Data//Route_Key.txt', 'w') as c:
            c.write('1')   
        
    
def go_to(x, y):
    while(not(in_pos(x_goal, y_goal))): # checks to make sure both positons are correct if not it continues the loop
            
        cur_pos = get_angles() #updates position
        if((cur_pos[0] <= (x_goal - margin)) or (cur_pos[0] >= (x_goal + margin))): #checks x position and moves
            if (cur_pos[0] <= (x_goal - margin)): #if we are behind the goal move towards it
                moveforward_x(1)
                delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                sleep(delta_x)
                stop()
            elif (cur_pos[0] >= (x_goal + margin)): # if we are in front move towards it
                movebackward_x(1)
                delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                sleep(delta_x)
                stop()
            else: #stops movment when in postion
                stop()
                    
        sleep(0.25)
                
            #print((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin)))
        cur_pos = get_angles() #updates postion to check again
        if((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin))): #checks y position and moves
            if (cur_pos[1] <= (y_goal - margin)): #if we are behind the goal move towards it
                moveforward_y(1)
                delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                sleep(delta_y)
                stop()
            elif (cur_pos[1] >= (y_goal + margin)): # if we are in front move towards it
                movebackward_y(1)
                delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                sleep(delta_y)
                stop()
            else: #stops movment when in postion
                stop()
                    
        sleep(0.75)
        cur_pos = get_angles() #updates postion to check again
    
    stop()
    print("At Home")        
    stop()
#initialization for all of the different linear actuators and accelertometer
status_fx = False
status_bx = False
status_fy = False
status_by = False

forward_channel_x = 24
backward_channel_x = 27
forward_channel_y = 22
backward_channel_y = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(forward_channel_x, GPIO.OUT)
GPIO.setup(backward_channel_x, GPIO.OUT)
GPIO.setup(forward_channel_y, GPIO.OUT)
GPIO.setup(backward_channel_y, GPIO.OUT)
           
GPIO.output(forward_channel_y, GPIO.LOW)
GPIO.output(backward_channel_y, GPIO.LOW)
GPIO.output(forward_channel_x, GPIO.LOW)
GPIO.output(backward_channel_x, GPIO.LOW)
    
bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

initialize_accel()


moveforward_x(True)
sleep(0.25)
stop()
sleep(0.25)
movebackward_x(True)
sleep(0.5)
stop()
sleep(0.25)
moveforward_x(True)
sleep(0.25)
stop()
sleep(0.25)
moveforward_y(True)
sleep(0.25)
stop()
sleep(0.25)
movebackward_y(True)
sleep(0.5)
stop()
sleep(0.25)
moveforward_y(True)
sleep(0.25)
stop()
    
try:
    
    while(True):
        with open('//home//pi//HLT_Shared//Route Data//Route_Key.txt') as c:
            write_check = c.readlines()
        
        #print(write_check)
        if (write_check[0] == '0'):
            run_route()
    
        print("sleepy_route")
        sleep(10)
        
except:
    stop()
    print("Error")
    sys.exit()
    

    
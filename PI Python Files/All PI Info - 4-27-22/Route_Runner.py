#Route Runner
import smbus			#import SMBus module of I2C
import time         #import
import numpy as np
import RPi.GPIO as GPIO
import datetime
import pandas as pd   
import RPi.GPIO as GPIO
import sys
import signal_processing as sig

#initialze variables to use as registers for accelertometer
accel_x_out_reg = 0x3B
accel_y_out_reg = 0x3D
accel_z_out_reg = 0x3F
d_address = 0x68

#universal variables
margin = 2
mov_fac = 15
start_time = 0
x_cal = 0
y_cal = 0

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
    global x_cal
    global y_cal
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
    c_sph_pp_i[1] = ((-1 * (np.arctan((np.sin(phi) * np.cos(theta)) / np.cos(phi))) * (180/np.pi)) + y_cal)
    c_sph_pp_i[0] = -1 * (((np.arctan((np.sin(phi) * np.sin(theta)) / np.cos(phi))) * (180/np.pi)) + x_cal)
    
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
    global margin
    
    for i in point_list: # increments through the list of points
        adjusted = time_adjust(2, i)
        x_goal = adjusted[0] #sets my goal points
        y_goal = adjusted[1]
        
        print(x_goal)
        print(y_goal)
        
        print(get_angles())
        
        while(not(in_pos(x_goal, y_goal))): # checks to make sure both positons are correct if not it continues the loop
            
            time.sleep(0.25)
            cur_pos = get_angles() #updates position
            time.sleep(0.25)
            
            if((cur_pos[0] <= (x_goal - margin)) or (cur_pos[0] >= (x_goal + margin))): #checks x position and moves
                if (cur_pos[0] <= (x_goal - margin)): #if we are behind the goal move towards it
                    delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                    movebackward_x(1)
                    time.sleep(delta_x)
                    stop()
                elif (cur_pos[0] >= (x_goal + margin)): # if we are in front move towards it
                    delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                    moveforward_x(1)
                    time.sleep(delta_x)
                    stop()
                else: #stops movment when in postion
                    stop()
                    
                time.sleep(0.25)
                
            #print((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin)))
            cur_pos = get_angles() #updates postion to check again
            
            time.sleep(0.25)
            
            if((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin))): #checks y position and moves
                if (cur_pos[1] <= (y_goal - margin)): #if we are behind the goal move towards it
                    moveforward_y(1)
                    delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                    time.sleep(delta_y)
                    stop()
                elif (cur_pos[1] >= (y_goal + margin)): # if we are in front move towards it
                    movebackward_y(1)
                    delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                    time.sleep(delta_y)
                    stop()
                else: #stops movment when in postion
                    stop()
                    
                time.sleep(0.75)
                cur_pos = get_angles() #updates postion to check again
                
            print("Phi_x = ", cur_pos[0], "Phi_y = ", cur_pos[1])
            
        stop()
        time.sleep(5)
        
        #UNCOMMENT
        sig.read_signal()
        print("Signal Read")
        #still with in all the points but I have gotten to the point where we need to collect data
        #write to file saying collect data
        '''with open('//home//pi//HLT_Shared//Route Data//Signal_Processing_Key.txt', 'w') as c:
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
        '''
        
    #once we have moved to all the points it updates this file saying it has moved
     
        
    
def go_to(x, y):
    x_goal = x
    y_goal = y
    
    smargin = 0.2
    cur_pos = get_angles()
    
    while(not((((cur_pos[0] >= (x_goal - smargin)) and (cur_pos[0] <= (x_goal + smargin))) and ((cur_pos[1] >= (y_goal - smargin)) and (cur_pos[1] <= (y_goal + smargin)))))): # checks to make sure both positons are correct if not it continues the loop
            
        cur_pos = get_angles() #updates position
        if((cur_pos[0] <= (x_goal - smargin)) or (cur_pos[0] >= (x_goal + smargin))): #checks x position and moves
            if (cur_pos[0] <= (x_goal - smargin)): #if we are behind the goal move towards it
                delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                movebackward_x(1)
                time.sleep(delta_x)
                stop()
            elif (cur_pos[0] >= (x_goal + smargin)): # if we are in front move towards it
                
                delta_x = (abs(cur_pos[0] - x_goal))/mov_fac
                moveforward_x(1)
                time.sleep(delta_x)
                
                stop()
            else: #stops movment when in postion
                stop()
                    
        time.sleep(0.25)
                
            #print((cur_pos[1] <= (y_goal - margin)) or (cur_pos[1] >= (y_goal + margin)))
        cur_pos = get_angles() #updates postion to check again
        if((cur_pos[1] <= (y_goal - smargin)) or (cur_pos[1] >= (y_goal + smargin))): #checks y position and moves
            if (cur_pos[1] <= (y_goal - smargin)): #if we are behind the goal move towards it
                moveforward_y(1)
                delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                time.sleep(delta_y)
                stop()
            elif (cur_pos[1] >= (y_goal + smargin)): # if we are in front move towards it
                movebackward_y(1)
                delta_y = (abs(cur_pos[1] - y_goal))/mov_fac
                time.sleep(delta_y)
                stop()
            else: #stops movment when in postion
                stop()
                    
        time.sleep(0.75)
        cur_pos = get_angles() #updates postion to check again
    
    stop()
    print("At Home")
    print("Phi_x: ", cur_pos[0], "Phi_y: ", cur_pos[1])
    stop()
    
def time_adjust(mode_num, target_point):
    global start_time
    
    if(mode_num == 1):
        start_time = time.time()
        
    elif(mode_num == 2):
        t_elapsed = (time.time() - start_time)
        angle_shift = t_elapsed * (1/240)
        target_point[0] = target_point[0] + angle_shift
        
    elif(mode_num == 3):
        start_time = 0
    
    return target_point
    

#initialization for all of the different linear actuators and accelertometer
status_fx = False
status_bx = False
status_fy = False
status_by = False

forward_channel_x = 25
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

"""
moveforward_x(True)
time.sleep(0.25)
stop()
time.sleep(0.25)
movebackward_x(True)
time.sleep(0.5)
stop()
time.sleep(0.25)
moveforward_x(True)
time.sleep(0.25)
stop()
time.sleep(0.25)
moveforward_y(True)
time.sleep(0.25)
stop()
time.sleep(0.25)
movebackward_y(True)
time.sleep(0.5)
stop()
time.sleep(0.25)
moveforward_y(True)
time.sleep(0.25)
stop()
"""


try:
    #go_to(0,0)
    while(True):
        #print("in while statement")
        go_to(0,0)
        time_wait = 1 #the time in seconds in between scans
        
        with open('//home//pi//HLT_Shared//Route Data//Route_Key.txt') as c:
            write_check = c.readlines()
        with open('//home//pi//HLT_Shared//Route Data//RPA_Key.txt') as d:
            rpa_check = d.readlines()
        with open('//home//pi//HLT_Shared//Route Data//Duration_Key.txt') as e:
            dur_key = int(e.readlines()[0])
        #print(write_check)
        dur_key = dur_key * 5 #converts hours to seconds
        
        if(write_check[0] == "0"):
            # sig.clear_folder('//home//pi//HLT_Shared//Scan Graphs')
            
            with open('//home//pi//HLT_Shared//Signal Data//Signal_Key.txt', 'w') as g:
                g.write('0')
                
            if(dur_key != 0):
                sig.write_blank_files()
                if(rpa_check == 1):#rpa
                    with open('//home//pi//HLT_Shared//Route Data//RPA_Key.txt') as d:
                        rpa_check = d.readlines()
            
                    time_adjust(1, [0, 0])
            
                    while(dur_key > 0):
                        run_route()
                        time.sleep(time_wait)
                        dur_key = dur_key - time_wait
            
                    time_adjust(3, [0, 0])#time adjust doesnt reset after ever run
                
                else:
                    while(dur_key > 0): #2 dim & one dim sweep
                        time_adjust(1, [0,0])
                        run_route()
                        time_adjust(3, [0, 0])#time adust does reset after every run
                        time.sleep(time_wait)
                        dur_key = dur_key - time_wait
              
            else:#2 dim array
                sig.write_blank_files()
                time_adjust(1, [0,0])
                run_route()
                time_adjust(3, [0, 0])
                
            with open('//home//pi//HLT_Shared//Signal Data//Signal_Key.txt', 'w') as g:
                g.write('1')
        
        
        
        with open('//home//pi//HLT_Shared//Route Data//Route_Key.txt', 'w') as c:
            c.write('1')
            
        print("sleepy_route")
        time.sleep(10)
        
except Exception as e:
    stop()
    print("Error: ", e)
    sys.exit()


    
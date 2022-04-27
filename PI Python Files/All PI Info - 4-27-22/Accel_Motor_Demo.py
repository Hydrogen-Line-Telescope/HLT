#Route Runner
import smbus			#import SMBus module of I2C
from time import sleep         #import
import numpy as np
import RPi.GPIO as GPIO
import datetime
import pandas as pd   
import RPi.GPIO as GPIO
import sys
#import signal_processing as sig
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
theta = 0

dev = 0.2
mov_fac = 20

def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
    
def get_angles():
    
    c_sph_pp_i = [0,0]
    Ax = 0
    Ay = 0
    Az = 0

    for i in range(0,100):
        acc_x = int(read_raw_data(ACCEL_XOUT_H)/300)
        acc_y = int(read_raw_data(ACCEL_YOUT_H)/300)
        acc_z = int(read_raw_data(ACCEL_ZOUT_H)/300)
        
        Ax = acc_x + Ax
        Ay = acc_y + Ay
        Az = acc_z + Az
        
            
    Ax = Ax/100
    Ay = Ay/100
    Az = Az/100
                                                                                                                                                 
    phi = np.arctan((np.sqrt((Ax**2)+(Ay**2))) / Az) 
    
    if(Ax > 0)                                                                                                            :
        theta = (np.arctan(Ay/Ax))
    elif(Ax == 0):
            if(Ay > 0):
                theta = np.pi/2
            else:
                theta = -np.pi/2
    else:
       theta = (np.arctan(Ay/Ax) + np.pi)
        
    
    c_sph_pp_i[1] = (-1 * (np.arctan((np.sin(phi) * np.cos(theta)) / np.cos(phi))) * (180/np.pi) - 0.3)
    c_sph_pp_i[0] = (((np.arctan((np.sin(phi) * np.sin(theta)) / np.cos(phi))) * (180/np.pi)) - 0.63) 
    
    return c_sph_pp_i

def moveforward_x(active):
        
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.HIGH)
    status_fx = active
    return status_fx

def movebackward_x(active):
        
    GPIO.output(backward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(backward_channel_x, GPIO.HIGH)
    status_bx = active
    return status_bx

def moveforward_y(active):
        
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.HIGH)
    status_fy = active
    return status_fy

def movebackward_y(active):
        
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.HIGH)
    status_by = active
    return status_by

def stop():
    GPIO.output(backward_channel_x, GPIO.LOW)
    GPIO.output(forward_channel_y, GPIO.LOW)
    GPIO.output(forward_channel_x, GPIO.LOW)
    GPIO.output(backward_channel_y, GPIO.LOW)
    return
    
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

MPU_Init()

'''
moveforward_x(True)
sleep(0.25)
stop()
movebackward_x(True)
sleep(0.5)
stop()
moveforward_x(True)
sleep(0.25)
stop()
moveforward_y(True)
sleep(0.25)
stop()
movebackward_y(True)
sleep(0.5)
stop()
moveforward_y(True)
sleep(0.25)
stop()'''

try:
    
    if((input("Success?: ")) == "y"):
        print("Linear Actuators Ready")
    ct = get_angles()

    print("Phi X: ", int(ct[0]), "Phi Y: ", int(ct[1]))
    if((input("Success?: ")) == "y"):
        print("Accel Ready")


    test = 1
    angle_x = 0
    angle_y = 0
    
    while(test != "q"):
        #get intital angle
        
        ca = get_angles()
        while((ca[0] > (angle_x + dev)) or (ca[0] < (angle_x - dev)) or (ca[1] > (angle_y + dev)) or (ca[1] < (angle_y - dev))):
            if((ca[0] > (angle_x + dev)) or (ca[0] < (angle_x - dev))):
                #ca = get_angles()
                if(ca[0] < (angle_x - dev)):
                    status_fx = moveforward_x(True)
                    delta_x = (abs(ca[0] - angle_x))/mov_fac
                    sleep(delta_x)
                    stop()
                elif(ca[0] > (angle_x + dev)):
                    status_bx = movebackward_x(True)
                    delta_x = (abs(ca[0] - angle_x))/mov_fac
                    sleep(delta_x)
                    stop()
                stop()
                #sleep(0.25)
                #stop()
                #sleep(0.25)
                sleep(0.5)
                ca = get_angles()
                #print("Phi_x = ", int(ca[0]), "Phi_y = ", int(ca[1]))
    
            stop()
            sleep(0.02)
            ca = get_angles()
            
            if((ca[1] > (angle_y + dev)) or (ca[1] < (angle_y - dev))):
                #ca = get_angles()
                if(ca[1] < (angle_y - dev)):
                    status_fy = moveforward_y(True)
                    delta_y = (abs(ca[1] - angle_y))/mov_fac
                    sleep(delta_y)
                    stop()
                elif(ca[1] > (angle_y + dev)):
                    status_by = movebackward_y(True)
                    delta_y = (abs(ca[1] - angle_y))/mov_fac
                    sleep(delta_y)
                    stop()
                    
                stop()
                #sleep(0.25)
                #stop()
                #sleep(0.25)
                sleep(0.02)
                ca = get_angles()
                #print("Phi_x = ", int(ca[0]), "Phi_y = ", int(ca[1]))
    
            stop()
            sleep(0.02)
            print("Phi_x = ", ca[0], "Phi_y = ", ca[1])
    
        test = input("Type q to quit: ")
        angle_x = float(input("Please input integer X angle: "))
        angle_y = float(input("Please input integer Y angle: "))
except Exception as e:
    stop()
    print("Error: ", e)
    sys.exit()
    


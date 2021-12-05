import smbus		
from time import sleep   
import numpy as np
import RPi.GPIO as GPIO
#import used libraries


#initialze variables to use as registers for accelertometer
accel_x_out_reg = 0x3B
accel_y_out_reg = 0x3D
accel_x_out_reg = 0x3F
d_address = 0x68


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
    c_sph_pp_i[0] = (np.arctan((np.sin(phi) * np.cos(theta)) / np.cos(phi))) * (180/np.pi)
    c_sph_pp_i[1] = (np.arctan((np.sin(phi) * np.sin(theta)) / np.cos(phi))) * (180/np.pi)
    
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


#initialization for all of the different linear actuators and accelertometer
status_fx = False
status_bx = False
status_fy = False
status_by = False

forward_channel_x = 27
backward_channel_x = 22
forward_channel_y = 24
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


#move actuators to make sure they are working
moveforward_x(True)
sleep(2)
movebackward_x(True)
sleep(2)
moveforward_y(True)
sleep(2)
movebackward_y(True)
sleep(2)

#check for motor movement
stop()
if((input("Success?: ")) == "y"):
    print("Linear Actuators Ready")
ct = get_angles()

#checks accelermeter is read correctly
print("Phi X: ", int(ct[0]), "Phi Y: ", int(ct[1]))
if((input("Success?: ")) == "y"):
    print("Accel Ready")

#a way to quit
test = input("Type q to quit: ")

test loop
while(test != "q"):
    #get intital angle
    angle_x = int(input("Please input integer X angle: "))
    angle_y = int(input("Please input integer Y angle: "))
    ca = get_angles()

    #checks if both angles are correct
    while((ca[0] > (angle_x + 5)) or (ca[0] < (angle_x - 5)) or (ca[1] > (angle_y + 5)) or (ca[1] < (angle_y - 5))):
        
        #checks if x angle is correct
        while((ca[0] > (angle_x + 5)) or (ca[0] < (angle_x - 5))):

            #if it is smaller it increases the x linear actuator
            if(ca[0] < (angle_x - 5)):
                status_fx = moveforward_x(True)
            #if it is bigger it decreases the x lineaer actuator
            elif(ca[0] > (angle_x + 5)):
                status_bx = movebackward_x(True)
            
            #get angles again and then repeats if it is still not correct
            ca = get_angles()
            print("Phi_x = ", int(ca[0]), "Phi_y = ", int(ca[1]))

        #stops the linear actuators
        stop()
    
        #repeats the same thing above for y axis
        while((ca[1] > (angle_y + 5)) or (ca[1] < (angle_y - 5))):
            if(ca[1] < (angle_y - 5)):
                status_fy = moveforward_y(True)
            elif(ca[1] > (angle_y + 5)):
                status_by = movebackward_y(True)
            ca = get_angles()
            print("Phi_x = ", int(ca[0]), "Phi_y = ", int(ca[1]))
    
        stop()

        #gets angles one last time and the repeats until both are with in desired area.
        ca = get_angles()
    
    
    test = input("Type q to quit: ")
    
                 
    


import smbus			#import SMBus module of I2C
from time import sleep          #import
import numpy as np

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
        
    
    c_sph_pp_i[1] = -1 * (np.arctan((np.sin(phi) * np.cos(theta)) / np.cos(phi))) * (180/np.pi)
    c_sph_pp_i[0] = (np.arctan((np.sin(phi) * np.sin(theta)) / np.cos(phi))) * (180/np.pi)
    
    return c_sph_pp_i                                     
    
bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print("Reading Data of Gyroscope and Accelerometer")




while(True):
                 
    c_out = get_angles()    
    
    print("Phi_x = ", (c_out[0]), "Phi_y = ", (c_out[1]))
    sleep(1)


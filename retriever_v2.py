#!/usr/bin/env python3

"""
This program run a colour sorting algorithm, which also retrieve one specific coloured cube on demand.
It must be run on the robot.
"""

# Import
from utils.brick import TouchSensor, EV3ColorSensor, configure_ports, reset_brick, Motor
from time import sleep
from utils.sound import *

# Program parameters
DELAY_SEC = 0.01 #seconds of delay between measurements
CALIBRATION_ADJUSTMENT = 10 # number of degrees to rotate after detecting block during calibration 
CALIBRATION_DELAY = 0.2 # seconds of delay between measurements of color sensor during calibration 
MOTOR_DPS =  30 # speed of the wheel/platform motor in degrees per second


print("Program start. \nWaiting for sensors to turn on...")


# Random tone
tone1 = Sound(duration=0.25, volume=90, pitch=1, mod_f="C3", mod_k=1)

# List setup
color_list = []
position_list = []

# Port configuration
push_motor = Motor("A")
platform_motor = Motor("B")

TOUCH_SENSOR, COLOR_SENSOR = configure_ports(PORT_1=TouchSensor, PORT_3=EV3ColorSensor)
COLOR_SENSOR_REQUEST = configure_ports(PORT_4=EV3ColorSensor)
print("Done waiting.")

# Motor limits
platform_motor.set_limits(power=15,dps=MOTOR_DPS)
push_motor.set_limits(dps = 360)

#temporary reset encoder
platform_motor.reset_encoder()


def calibrate_wheel():
    "Calibrate wheel at the beggining of the program"
    print("Calibrating wheel...")
    while True:
        color = COLOR_SENSOR.get_color_name()
        #print(color) DEBUG
        # if color is a known cube, stop calibrating
        if color == "Red" or color == "Blue" or color == "Yellow":
            # additional adjustment to center cube
            platform_motor.set_position_relative(CALIBRATION_ADJUSTMENT)
            sleep(CALIBRATION_ADJUSTMENT/MOTOR_DPS)
            platform_motor.set_power(0) # stop motor
            break
        platform_motor.set_position_relative(5)
        sleep(CALIBRATION_DELAY)
        
            

# Sort the colours in a list, with their indexes defined.
def color_sorting():
    try:
        sleep(1)
        print("Ready to collect first sample")
        # Loop is set up to not stop till break or BaseException
        while True:
            color_name = COLOR_SENSOR.get_color_name()
            sleep(2) # pause between measurements
            platform_motor.set_position_relative(60)    
            if(color_name != "Unknown" or color_name != "Black"):
                color_list.append(color_name)
                if len(color_list) == 6: # completed list
                    break
            # If the color_data is None, this means that something wrong has occurred with the data collection
            if color_name is not None:
                print(f"Detected {color_name}")
            print("Ready to collect next sample")
            sleep(60/MOTOR_DPS) # delay for motor
        for i in range(len(color_list)):
            print(color_list[i])

    except BaseException: #capture all exceptions including KeyboardInterrupt
        pass
    finally:
        print("Pre-sorting finished")
    
        
def color_name_check():
    "Function that gets a color from the request area and returns the index, if found, of that same color"
    "in the color list"
    sleep(1)
    while True:
        if TOUCH_SENSOR.is_pressed():
            print("------------")
            # get color name from request area
            color_name = COLOR_SENSOR_REQUEST.get_color_name()
            if color_name in color_list:
                #print("342") DEBUG
                print(f"{color_name} cube requested.")
                # find first index corresponding to the same color as detected
                for i in range(len(color_list)):
                    if color_name == color_list[i]:
                        color_list[i] = None
                        #print("-------") DEBUG
                        #print(color_name) DEBUG
                        return i
            else:
                print("Incompatible color has been detected.")
                print(color_name)
                return 50
        sleep(0.3) # controls the polling rate for touch sensor
            
def increment_motor(i):
    "Function takes in an index i and moves the wheel motor to the correct index/position, and pushes block off"
    "the platform"
    rotation = ((i+1)*60)%360
    #print(rotation) DEBUG
    platform_motor.set_position_relative(rotation)
    sleep(rotation/MOTOR_DPS)
    push_motor_up()
    
            
def push_motor_up():
    "Function that activates the motor that pushes the block off the edge of the platform"
    #print("push_motor")  DEBUG
    push_motor.set_position_relative(180) 
    sleep(1)
    push_motor.reset_encoder()

 

if __name__ == "__main__":
    calibrate_wheel()
    platform_motor.set_position_relative(15)
    color_sorting()
    #tone1 = Sound(duration=0.25, volume=90, pitch=1, mod_f="C3", mod_k=1)
    #tone1.play()
    color_name_index = color_name_check()
    # if (color_name_index == 50):
    # print("_one play")
    # tone1.play()
    increment_motor(color_name_index)    
    reset_brick()
    
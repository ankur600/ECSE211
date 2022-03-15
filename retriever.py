#!/usr/bin/env python3

"""
This program run a colour sorting algorithm, which also retrieve one specific coloured cube on demand.
It must be run on the robot.
"""

# Import
from utils.brick import TouchSensor, EV3ColorSensor, configure_ports, reset_brick, Motor
from time import sleep
from utils.sound import *


DELAY_SEC = 0.01 #seconds of delay between measurements

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
platform_motor.set_limits(power=15,dps=30)
push_motor.set_limits(dps = 360)

#temporary reset encoder
platform_motor.reset_encoder()


def calibrate_wheel():
    #Calibrate wheel at the beggining of the program
    print("Calibrating wheel...")
    while True:
        color = COLOR_SENSOR.get_color_name()
        print(color)
        if color == "Red" or color == "Blue" or color == "Yellow":
            platform_motor.set_position_relative(10)
            sleep(10/30)
            platform_motor.set_power(0)
            break
        platform_motor.set_position_relative(5)
        sleep(5/15)
        
            

# Sort the colours in a list, with their indexes defined.
def color_sorting():
    try:
        sleep(1)
        print("Ready to collect first sample")

        # Loop is set up to not stop till break or BaseException
        while True:
            # if TOUCH_SENSOR is pressed, collect RGB data and write it
            #if TOUCH_SENSOR.is_pressed():
            
                # get_rgb returns an array with three values, the R G B intensity values
            color_name = COLOR_SENSOR.get_color_name()
            sleep(2)
            platform_motor.set_position_relative(60)    
            if(color_name != "Unknown" or color_name != "Black"):
                color_list.append(color_name)
                if len(color_list) == 6:
                    break
            # If the color_data is None, this means that something wrong has occurred with the data collection
            if color_name is not None:
                print(color_name)
            print("Ready to collect next sample")
            
            # Sleep for 0.3 seconds, so it doesnt collect data constantly when the button is pressed
            sleep(2)
        for i in range(len(color_list)):
            print(color_list[i])

    except BaseException: #capture all exceptions including KeyboardInterrupt
        pass
    finally:
        # program termination: message, closing output file, exit program
        print("Done collecting COLOR samples")
    
        
def color_name_check():
    print("dsf lol ok idk what that means")
    sleep(1)
    j=50
    while True:
        if TOUCH_SENSOR.is_pressed():
            print("------------")
            color_name = COLOR_SENSOR_REQUEST.get_color_name()
            if color_name in color_list:
                print("342")
                for i in range(len(color_list)):
                    if color_name == color_list[i]:
                        color_list[i] = None
                        print("-------")
                        print(color_name)
                        return i
            else:
                print("we are in 50 loop")
                print(color_name)
                return 50
        sleep(0.3)
            
def increment_motor(i):
    rotation = ((i+1)*60)%360
    print(rotation)
    platform_motor.set_position_relative(rotation)
    sleep(rotation/30)
    push_motor_up()
    
            
def push_motor_up():
    print("push_motor")    
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
  #      print("_one play")
  #      tone1.play()
    increment_motor(color_name_index)    
    reset_brick()
    
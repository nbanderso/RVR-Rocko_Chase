import smbus
import os
import sys
import time
import io
from datetime import datetime, timedelta
import statistics

#Third Party Modules
import pi_servo_hat       # Pan/Tilt mast controller
from picamera import PiCamera
import qwiic

tf_width = 299 #Width required for Tensorflow
tf_height = 299 #Height required for Tensorflow
tf_bw = True #Whether Tensflow wants black and white
servo = pi_servo_hat.PiServoHat()
#ToF = qwiic.QwiicVL53L1X()


def take_picture(outFile):
	with picamera() as camera:
		camera.vflip = True
		camera.hflip = True
		camera.contrast = 15
		camera.sharpness = 35
		camera.saturation = 20
		camera.shutter_speed = 0 #auto
		camera.color_effects = (128,128) #sets camera to black and white
		camera.PiResolution(width=tf_width, Height=tf_height)
		camera.capture(outFile, format="jpeg")

def take_picture_hd(outFile):
	with picamera() as camera:
		camera.vflip = True
		camera.hflip = True
		# camera.iso = 400
		camera.contrast = 15
		camera.sharpness = 35
		camera.saturation = 35
		#time.sleep(2)
		#camera.shutter_speed = camera.exposure_speed
		camera.shutter_speed = 0 #auto
		#camera.exposure_mode = 'off'
		camera.capture(outFile, format="png")

def convert_pic_to_tf(inFile, outFile, outWidth, outHeight, black_and_white=True):
	pass


def ToF_to_range():
    ToF.StartRanging()
    time.sleep(.005)
    valuelist = []
    valuelist.append(ToF.GetDistance())
    value_median = statistics.median(valueList)
    return(value_median)
'''
def read_ToF():
    curVal = chan.value
    curVolt = chan.voltage
    return (curVal, curVolt)
'''
#sets camera servos to center
def center_camera():
	servo.move_servo_position(1,0,180)
	servo.move_servo_position(0,0,180)

#sets camera servos to level and left
def left_camera():
    servo.move_servo_position(1,0,180)
    servo.move_servo_position(0,-90,180)
    
#sets camera servoes to level and right
def right_camera():
    servo.move_servo_position(1,0,180)
    servo.move_servo_position(0,90,180)
    
#sets camera servos to up and center
def up_camera():
    servo.move_servo_position(1,90,180)
    servo.move_servo_position(0,0,180)

def main():
	center_camera()
	PicCount = 1 #keeps track of picture count
	for Look_left():
	    left_camera()
	    picFile = "rocko%0.3d.png" % (PicCount)
	    time.sleep(1)
	    take_picture(PicFile)
	    rRange = ToF_to_range()
	    print("Picture %s, range %0.3f, azimuth %d" %(PicFile, rRange, Look_Left))
	    PicCount += 1
    for Look_right():
        right_camera()
        picFile = "rocko%0.3d.png" % (PicCount)
        time.sleep(1)
        take_picture(PicFile)
        rRange = ToF_to_range()
        print("Picture %s, range %0.3f, azimuth %d" % (PicFile, rRange, Look_right))
        PicCount += 1
    center_camera()
    
if __name__ == '__main__':
    main()

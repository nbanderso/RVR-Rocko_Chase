import smbus
import os
import sys
import time
import io
from datetime import datetime, timedelta
import statistics

#Third Party Modules
import pi_servo_hat       # Pan/Tilt mast controller
import picamera


tf_width = 299 #Width required for Tensorflow
tf_height = 299 #Height required for Tensorflow
tf_bw = True #Whether Tensflow wants black and white
camera = PiCamera()
servo = pi_servo_hat.PiServoHat()

'''
take_picture() captures a single black and white frame in the dimensions required for TF
arguments: outFile - defines where to store the captured image
'''
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
'''
take_poicture() captures a single high-resolution image from the pi camera.
Note: this image will need to be downgrated to 299x299 and converted to black and white for TF
arguments: outFile - defines where to store the image 
'''
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

'''
convert_pic_to_tf process pic to TF requirements.
arguments:	inFile - name and path of input file
			outFile - name and path of outfile
			outWidth - width of output image (pixels)
			outHeight - height of output image (pixels)
			black_and_white - boolean indicating change to black and white
'''
def convert_pic_to_tf(inFile, outFile, outWidth, outHeight, black_and_white=True):
	pass

'''
point_camera() uses the servos to point the camera in a particular pan and tilt.
input 1 = up/down
input 0 = left/right
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
	    PicCount += 1
    for Look_right():
        right_camera()
        picFile = "rocko%0.3d.png" % (PicCount)
        time.sleep(1)
        take_picture(PicFile)
        PicCount += 1
    center_camera()

from picamera import PiCamera	
from time import sleep		

camera = PiCamera()

camera.start_preview()
camera.start_recording('/home/pi/shooting_5.h264')
sleep(3)
camera.stop_recording()
camera.stop_preview()

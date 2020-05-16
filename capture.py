'''
    This code will only take a picture
    and save as /home/pi/Pic1/Image.png
'''
from picamera import PiCamera
camera = PiCamera()
camera.capture('/home/pi/SmartHome/Pic1/Image.png')

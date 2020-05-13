#import RPi.GPIO as GPIO
import time
import requests
import os
#import Adafruit_DHT
import microgear.client as microgear
import logging
'''
sensor = Adafruit_DHT.DHT22
button = 16
DHT_Sensor = 14
Green_LED = 38
Blue_LED = 40
Red_LED = 36

LED_State = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Blue_LED ,GPIO.OUT)
GPIO.setup(Green_LED ,GPIO.OUT)
GPIO.setup(Red_LED ,GPIO.OUT)
'''
appid = 'SmartHomeTUP'
gearkey = ' ' #ขออนุญาตเว้นไว้
gearsecret =  ' ' #ขออนุญาตเว้นไว้

#Connect to Netpie
microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)
    #LED_State(message)
def disconnect():
    logging.info("disconnected")

microgear.setalias("RaspiTUP")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/Led")
microgear.connect()

'''
def LED_State(message):
	print(message)
	if message == "b'ON'":
		GPIO.output(Red_LED,1)
		GPIO.output(Green_LED,1)
		GPIO.output(Blue_LED,1)
		LED_State = 1
		microgear.chat("LED-Status",LED_State)
	elif message == "b'OFF'":
		GPIO.output(Red_LED,0)
		GPIO.output(Green_LED,0)
		GPIO.output(Blue_LED,0)
		LED_State = 0
		microgear.chat("LED-Status",LED_State)
	elif message == "b'RED'":
                GPIO.output(Red_LED,1)
                GPIO.output(Green_LED,0)
                GPIO.output(Blue_LED,0)
	elif message == "b'GREEN'":
                GPIO.output(Red_LED,0)
                GPIO.output(Green_LED,1)
                GPIO.output(Blue_LED,0)
	elif message == "b'BLUE'":
                GPIO.output(Red_LED,0)
                GPIO.output(Green_LED,0)
                GPIO.output(Blue_LED,1)
'''

def main1():
	while True:
        #DHT22 Sensor Reading
		#humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_Sensor)
		#print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
		#microgear.publish("/outdoor/temp",int(temperature))
		#microgear.publish("/outdoor/hud",int(humidity))

	#Button Reading
		#button_state = GPIO.input(button)
		if button_state == False:
			print('Button Pressed...')
			
                	#Run Capture File
			os.system('python capture.py')
			
			#Send Image to Line
			file = {
				'message': (None, "Someone has press the button"),
				'imageFile': open('/home/pi/Pic1/Image.png', 'r+b')
				}
			url = 'https://notify-api.line.me/api/notify'
			token = 'f2tilnNiJDmTacnp4Xa7njNCZmppUckraZR071Aiw4Z'
			headers = {'Authorization': 'Bearer ' + token}
			res = requests.post(url, headers=headers, files=file)
			print(res.text)
			os.remove('/home/pi/Pic1/Image.png')
			time.sleep(1)

		#Starting Face_Recognition
			os.system('python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle')
			time.sleep(0.2)

try :
	main1()
#except KeyboardInterrupt :
	#GPIO.cleanup()

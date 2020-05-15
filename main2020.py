import RPi.GPIO as GPIO # pip install RPi.GPIO
import time
import requests
import os
import Adafruit_DHT # sudo pip3 install Adafruit_DHT
#import microgear.client as microgear
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
#import logging
import json

myData = { "temperature" : 0, "humidity" : 0, "led_status" : 'false', "led_color" : None}

# Set up RPI GPIO pin
sensor = Adafruit_DHT.DHT22
button = 16
DHT_Sensor = 14
Green_LED = 38
Blue_LED = 40
Red_LED = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Blue_LED ,GPIO.OUT)
GPIO.setup(Green_LED ,GPIO.OUT)
GPIO.setup(Red_LED ,GPIO.OUT)    

def led_color_setState(key):
	if key == 'red':
		GPIO.output(Red_LED,1)
		GPIO.output(Green_LED,0)
		GPIO.output(Blue_LED,0)
	elif key == 'green':
		GPIO.output(Red_LED,0)
		GPIO.output(Green_LED,1)
		GPIO.output(Blue_LED,0)
	elif key == 'blue':
		GPIO.output(Red_LED,0)
		GPIO.output(Green_LED,0)
		GPIO.output(Blue_LED,1)

def led_status_setState(key):
	if key == 'true':
		GPIO.output(Red_LED,1)
		GPIO.output(Green_LED,1)
		GPIO.output(Blue_LED,1)
	elif key == 'false':
		GPIO.output(Red_LED,0)
		GPIO.output(Green_LED,0)
		GPIO.output(Blue_LED,0)

def funcToDo(key,value):
	if key == "led_status":
		led_status_setState(value)
	elif key == "led_color" and myData['led_status'] == 'true':
		led_color_setState(value)


# Initialize Netpie information
NETPIE_HOST = "broker.netpie.io"
CLIENT_ID = " " # YOUR CLIENT ID
DEVICE_TOKEN = " " # YOUR TOKEN

# Function to react with NETPIE
def on_connect(client, userdata, flags, rc):
    print("Result from connect : {}".format(mqtt.connack_string(rc)))
    client.subscribe("@shadow/data/updated")

def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribe successful")

def on_message(client, userdata, msg):
	data = str(msg.payload).split(",")
	data_split = data[1].split("{")[1].split(":")
	key = data_split[0].split('"')[1]
	value = data_split[1].split('}')[0]
	if value[0] == '"':
	    value = value.split('"')[1]
	myData[key] = value
	
	print(key,value)
	funcToDo(key,value)

#Connecting to NETPIE
client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(DEVICE_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect(NETPIE_HOST, 1883)
client.loop_start()

try :
	while True:
    	#DHT22 Sensor Reading
		humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_Sensor)
		myData['humidity'] = humidity
		myData['temperature'] = temperature
		
		#send myData (in JSON from) to NETPIE2020 shadow
		client.publish("@shadow/data/update",json.dumps({"data": myData}), 1)

		#print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
		
		#Button Reading
		button_state = GPIO.input(button)
		if button_state == False:
			print('Button Pressed...')

            #Run Capture.py file to capture user face
			os.system('python capture.py')
			
			#Send Image to Line notify
			file = {
				'message': (None, "Someone has press the button"),
				'imageFile': open('/home/pi/Pic1/Image.png', 'r+b')
				}
			url = 'https://notify-api.line.me/api/notify'
			line_token = ' ' # YOUR LINE NOTIFY TOKEN
			headers = {'Authorization': 'Bearer ' + line_token}
			res = requests.post(url, headers=headers, files=file)
			print(res.text)
			os.remove('/home/pi/Pic1/Image.png')
			time.sleep(1)

			#Run pi_face_recognition.py to use face recognition
			os.system('python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle')
			time.sleep(0.2)

except KeyboardInterrupt:
	print('Disconnecting successful')
	GPIO.cleanup()
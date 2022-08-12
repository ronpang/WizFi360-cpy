# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Note, you must create a feed called temp-wizfi360 in your AdafruitIO account, or adjust variable Feed to correspond. 
# Your secrets file must contain your aio_username and aio_key
# based on https://github.com/ronpang/WizFi360-cpy/new/main/examples/http
# added led flash, dht
# 

import time
import board
import busio
import adafruit_dht
from digitalio import DigitalInOut
from digitalio import Direction
dht = adafruit_dht.DHT22(board.GP1) #set up DHT22/AM2303 on GP1/Pin 2, gnd Pin 40,  3v Pin 42
dht = adafruit_dht.DHT22(board.GP1) #set up DHT22/AM2303 on GP1/Pin 2, gnd Pin 40,  3v Pin 42

led = DigitalInOut(board.LED) 		# set up the Pico Led Pin 
led.direction = Direction.OUTPUT 	# set to Output


# ESP32 AT
from adafruit_espatcontrol import (
    adafruit_espatcontrol,
    adafruit_espatcontrol_wifimanager,
)


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False

# Pins setup with WizFi360 through UART connection
RX = board.GP5 #TX pin for WizFi360-EVB-PICO
TX = board.GP4 #RX pin for WizFi360-EVB-PICO
resetpin = DigitalInOut(board.GP20) #Reset pin for WizFi360-EVB-PICO
rtspin = False #RTS pin
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048) #Serial settings
status_light = False #only if board has neopixel 
 
print("ESP AT commands")
# For Boards that do not have an rtspin like WizFi360-EVB-PICO set rtspin to False.
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light) #Class that handles HTTPs and MQTT (more information from lib)

counter = 0

while True:
    try:
        led.value = True
        temperature = dht.temperature #get temperature
        #humidity = dht.humidity #get temperature
        print("Posting data...", end="") 
        data = temperature #counter result = input data
        #data = humidity #counter result = input data
        feed = "temp-wizfi360" # Adafruit IO feed, the name on adafruit io needs to be lowercase, - only special char 
        payload = {"value": data} # Json format
        # HTTP Post method to Adafruit IO
        response = wifi.post(
            "https://io.adafruit.com/api/v2/" #address to adafruit io
            + secrets["aio_username"] #input adafruit io name for "secret"
            + "/feeds/"
            + feed #feed = "test"
            + "/data",
            json=payload, # counter 
            headers={"X-AIO-KEY": secrets["aio_key"]}, #input adafruit io key from "secret"
        )
        print(response.json()) #send data and print the data that you sent
        response.close() #close the connection
        counter = counter + 2
        print("OK")
        print(dht.temperature) #print to serial to see if the senor is working
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        continue
    response = None
    led.value = True 	#Turn led on
    time.sleep(10)
    led.value = False 	#Turn led off
    time.sleep(5)

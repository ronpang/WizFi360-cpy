# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Note, you must create a feed called "test" in your AdafruitIO account.
# Your secrets file must contain your aio_username and aio_key

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction

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
status_light = None

print("ESP AT commands")
# For Boards that do not have an rtspin like WizFi360-EVB-PICO set rtspin to False.
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light,attempts=5) #Class that handles HTTPs and MQTT (more information from lib)

counter = 0

while True:
    wifi.IO_Con("test","test","MQTT") #connect to adafruit io - publish topic name = "test", subscribe topic name = "test", protcol = MQTT
    wifi.MQTT_pub(str(counter)) #publish data to "test"
    data = wifi.MQTT_sub() #collect subscribed channel data from "test"
    print (data) #print out the result
    wifi.MQTT_disconnect() #disconnect with adafruit io
    counter += 1   
    time.sleep(15)

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


RX = board.GP5
TX = board.GP4
resetpin = DigitalInOut(board.GP20)
rtspin = False
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
status_light = None


print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
esp.hard_reset()
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light,attempts=5)


counter = 0
result = None #variable for cleaning data
#set the topics 
wifi.topic_set("test","feed")
#select which topic that you wanted to publish
wifi.IO_topics("test")
#Connect to adafruitio (please remember to set the above settings before connect to adafruit io)
wifi.IO_Con("MQTT")
while True:
    #Collect information from subscribe channel (test)
    data = wifi.MQTT_sub()
    print (data)
    # find the data and the topic name from WizFi360 to further use.
    sub,result = wifi.clean_data(data,"test",result)
    print (sub, result)
    #publish to related channel (test)
    wifi.MQTT_pub(str(counter))    
    
    counter += 1
    time.sleep(0.5)
    if counter > 5:
        wifi.MQTT_disconnect() #disconnect with adafruit io
        counter = 0
        time.sleep(15)
        wifi.IO_Con("MQTT") #reconnect with adafruit io

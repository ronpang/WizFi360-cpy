# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Note, you must create a feed called "test" in your AdafruitIO account.
# Note 2, you must create a group called "tesing" in your Adafruit account that has "result" and "counter" feeds
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
wifi.topic_set("test","feed","testing","group")
#select which topic that you wanted to publish
wifi.IO_topics("test")
#Connect to adafruitio (please remember to set the above settings before connect to adafruit io)
wifi.IO_Con("MQTT")
while True:
  
    #Collect information from subscribe channel (test)
    data = wifi.MQTT_sub()
    print (data)
    # Collect data from each subscribe topic
    if counter < 6: #Collect from feed -> "test"
        sub,result = wifi.clean_data(data,"test",result)        
    elif counter >= 6 and counter < 11: #Collect from group -> "result" from "testing" group 
        sub,result = wifi.clean_data(data,"testing.result",result)
    elif counter >= 11 and counter < 16: #Collect from group -> "counter" from "testing" group 
        sub,result = wifi.clean_data(data,"testing.counter",result)
    print (sub, result)
    
    counter += 1
    #publish to related channel (test, testing.result, testing.counter)
    if counter <= 5: #Publish feed -> "test"
        pub_data  = counter
    elif counter > 5 and counter <= 10: #Publish to group -> "testing" 's feed "result"
        pub_data = wifi.IO_json('testing.result',str(counter))        
    elif counter > 10 and counter <= 15: #Publish to group -> "testing" 's feed "counter"
        pub_data = wifi.IO_json('testing.counter',str(counter))
    wifi.MQTT_pub(str(pub_data))
    
    # Change the topic from feed to group
    if counter is 5:
        wifi.IO_topics("testing")
        
    # Disconnecting with adafruit io
    elif counter is 16:
        wifi.MQTT_disconnect() #disconnect with adafruit io
        wifi.IO_topics("test")
        counter = 0
        time.sleep(15)
        wifi.IO_Con("MQTT") #reconnect with adafruit io
        
    time.sleep(1)

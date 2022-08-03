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
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light)

counter = 0

while True:
    try:
        print("Posting data...", end="") 
        data = counter #counter result = input data
        feed = "test" # Adafruit IO feed, the name on adafruit io needs to be "test"
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
        counter = counter + 1
        print("OK")
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        continue
    response = None
    time.sleep(15)

# MQTT example
This is a exmaple using WIZnet's WizFi360 MQTT commands to communicate adafruit IO.

## Getting start for Adafruit IO
For applying a adafruit account and how to use adafruit accounts, please refer to [Get start adafruit IO][link-get start]

## 🤖 Basic Setup
### Step 1: How to install circuit Python into WizFi360-EVB-PICO (same method as adding to Raspberry Pi Pico)
🟥Youtube: [Linux install method][link-linux install]

🟥Youtube: [Window install method][link-window install]

### Step 2: Modified your secret.py and put the file inside the Pico flash
It is used for saving your AP information and Adafruit IO information to allow WizFi360 to connect.
```python
secrets = {
    "ssid": "my access point", # Your AP's or router's name
    "password": "my password", # The password for your AP/router
    "timezone": -5,  # this is offset from UTC
    "github_token": "abcdefghij0123456789",
    "aio_username": "myusername", #adafruit IO username
    "aio_key": "abcdefghij0123456789", #adafruit IO 
}
```
### Step 3: Add the libraries to your lib section
It is required to add libraries to the folder lib to allow the codes could run.
![link-lib_image]

### Step 4: Put the example codes to flash
Draging the examples codes to the flash inside the pico board, it should run the software easily.

### Step 5: Setting the GPIO PINS
It is required to modify the GPIO PIN settings to allow the RP2040 coould communicate with WizFi360
```python
RX = board.GP5 #TXD1 pin for WizFi360
TX = board.GP4 #RXD1 pin for WizFi360
resetpin = DigitalInOut(board.GP20) 
rtspin = False
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
```

## 🔰MQTT conncection setup
1. Required files: [aio.py][link-aio], [Secret.py][link-secret]
2. Required commands:
```python
# Connect to adafruit io - it used the secret from secret.py
# Pubish topic: test , Subscribe topic: test , Mode: MQTT / MQTTS
wifi.IO_Con("test","test","MQTT") 
# Pubish data to the adafruit IO's Subscribe topic - test
# data -> the data that you wanted to publish
wifi.MQTT_pub(str(data)) #publish data
# Collect data from the subscribed channel - test
# data -> saved the data from the subscribed channel
data = wifi.MQTT_sub() #collect subscribed channel data
# Disconnect with adafruit io 
wifi.MQTT_disconnect()
```
## ☑️Results
### Thonny (in debug mode)
The result of the MQTT communicated with adafruit IO.

Since it is in debug mode to the connecting details, it shows the secret information for connecting to the adafruit IO. 

The results has been covered in different colors.

🔵Blue: Adafruit IO username

🔴Red: Adafruit IO password / key

![link-thonny_img]

### Adafruit IO 
The results from Adafruit IO

🔵Blue: Adafruit IO username

🔴Red: Results

![link-adadfruit_img]


[link-aio]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/MQTT/aio.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-thonny_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20MQTT.PNG
[link-adadfruit_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/adafruit%20io%20recevied%20result%20(updated)-%20wizfi360%20-%20MQTT.PNG
[link-get start]: https://github.com/ronpang/RP2040-HAT-CircuitPython/blob/master/examples/Adafruit_IO/Getting%20Start%20Adafruit%20IO.md

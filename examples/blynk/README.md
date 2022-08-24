# WizFi360-EVB-PICO (Blynk)
This is a exmaple ussd WizFi360-EVB-PICO in Circuitpython to communicate with Blynk

This example based on the python coding made from Blynk. (For the communication part, it shifted to the main code.)

For more information about Blynk's coding, please go to this [LINK][link-blynk].

## Getting start for Blynk
Blynk provided a good instruction on how to create a account and quickstart setup, please follow [Blynk getting started][link-get start].

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

## 🔰Blynk conncection setup
1. Required files: [TCP Blynk.py][link-aio], [Secret.py][link-secret], [Blynk_lib.py][link-blynk_lib] (Modified - No communication section)
2. Required commands:
For Blynk Setups, it is required to have the following information. (All the information will be showed on the "device info" section)
```python
BLYNK_TEMPLATE_ID =  "TEMPLATE_ID" 
BLYNK_DEVICE_NAME = "DEVICE_NAME"
BLYNK_AUTH_TOKEN = "AUTH_TOKEN"
```
For communicating with blynk Based on Blynk's example codings. ([Write Virtual pin][link-write] , [Read Virtual pin][link-read])
```python
esp.socket_connect("TCP",Dest_IP,Dest_PORT) #TCP connection. If SSL, please change "TCP" to "SSL"
blynk = Blynk(BLYNK_AUTH_TOKEN) #Open the class and connect to Blynk
counter = 0 # Counter for posting information to Blynk

# Register virtual pin handler
@blynk.on("V5") #collect data from Blynk (Virtual Pin V5)
def v5_write_handler(value):
    print('Current slider value: {}'.format(value[0])) 

while True:
    blynk.run()
    print("Adding counter: "+ str(counter))
    blynk.virtual_write(4, str(counter)) #post counter data to virtual pin 4
    time.sleep(1)
    counter +=1
```

## ☑️Results in Youtube Video
[![Watch the video](https://img.youtube.com/vi/sE3b4VML8AM/maxresdefault.jpg)](https://youtu.be/sE3b4VML8AM)


[link-aio]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/blynk/TCP%20blynk.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-blynk_lib]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/blynk/BlynkLib%20(modfied).py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-thonny_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20MQTT.PNG
[link-adadfruit_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/adafruit%20io%20recevied%20result%20(updated)-%20wizfi360%20-%20MQTT.PNG
[link-get start]: https://docs.blynk.io/en/getting-started/what-do-i-need-to-blynk
[link-blynk]: https://github.com/blynkkk/lib-python
[link-write]: https://github.com/blynkkk/lib-python/blob/master/examples/01_write_virtual_pin.py
[link-read]: https://github.com/blynkkk/lib-python/blob/master/examples/02_read_virtual_pin.py

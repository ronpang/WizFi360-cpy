# MQTT example
This is a exmaple using WIZnet's WizFi360 MQTT commands to communicate adafruit IO.

## Getting start for Adafruit IO
For applying an Adafruit account and how to use adafruit accounts, please refer to [Get start adafruit IO][link-get start]

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
### Before the loop
```python
#set the topics 
wifi.topic_set("test","feed")
#select which topic that you wanted to publish
wifi.IO_topics("test")
#Connect to adafruitio (please remember to set the above settings before connect to adafruit io)
wifi.IO_Con("MQTT")
```
### Inside the loop
```python
while True:
    #Collect information from subscribe channel (test)
    data = wifi.MQTT_sub()
    print (data)
    # Split realted information to usable data
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
```
## ☑️Results
### Thonny (in debug mode)
The result of the MQTT communicated with adafruit IO.

![link-thonny_img]

### Adafruit IO 
The results from Adafruit IO

![link-adadfruit_img]


[link-aio]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/MQTT/aio.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-thonny_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20MQTT%20(5-10-2022).PNG
[link-adadfruit_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20MQTT%20-adafruit%20(5-10-2022).PNG
[link-get start]: https://github.com/ronpang/RP2040-HAT-CircuitPython/blob/master/examples/Adafruit_IO/Getting%20Start%20Adafruit%20IO.md

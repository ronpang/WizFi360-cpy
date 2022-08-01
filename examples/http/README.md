# HTTP example
This is a example code for HTTP to connect with adafruit io.

The code is totally the same as ESP AT control. 

If it is using SSL to post the information , it takes a longer response.

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
1. Required files: [aio.py][link-aio_http], [Secret.py][link-secret]
2. Required commands:
```python
# Using counter's value to send to adafruit io
data = counter
# HTTP feed - Topic on adafruit IO -> test
feed = "test"
#send the data in Json format
payload = {"value": data}
# The whole HTTP Post format that send to adafruit IO
response = wifi.post(
"https://io.adafruit.com/api/v2/" #Domain name for HTTP
+ secrets["aio_username"] #username for adafruit IO
+ "/feeds/" 
+ feed  # Feed topic: test
+ "/data",
json=payload, #load the counter information
headers={"X-AIO-KEY": secrets["aio_key"]}, #password for adafruit io
)
# Send the result and print the result
print(response.json()) 
# Turn of the HTTPs connection 
response.close() 
# Adding counter value
counter = counter + 1 
```
## ☑️Results
### Thonny 
The following are the results used HTTP post to post information to the adafruiit IO

![link-thonny]

### Adafruit IO 
The result from adafruit io.

![link-adafruitio]

[link-readme]: https://github.com/ronpang/WizFi360-cpy
[link-aio_http]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/http/aio_http.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-thonny]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20HTTP.PNG
[link-adafruitio]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/adafruit%20io%20recevied%20result%20-%20wizfi360%20-%20http.PNG

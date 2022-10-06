# WizFi360-EVB-Pico in Circuitpython (WizFi360 + RP2040)
These code is based on Adafruit's circuitpython ESP AT control to modified. 

WizFi360 Firmware version: 1.1.1.9

If you are interested on the codes and commands, please refer to the links below.

1.[ESP AT control - circuitpython][link-ESP_cpy]

2.[WizFi360 AT commands][link-AT commands]

3.[WizFi360 Vs ESP8266][link-AT comparison]

By using WIZnet's WizFi360-EVB-PICO, it required to use AT commands to control WizFi360 to communicate to the world


## :lotus_position_man: Upadtes

### MQTT:

1. Allow to change MQTT Publish topic after connected to adafruit IO
2. Accept JSON method
3. WizFi360 could accept Maximum 3 Subscribe topics

### Library:
1. Added Firmware upgrade for WizFi360
2. Added Read_UART - Directly collect UART message from WizFi360 without any modification (in byte format)

## 📚Required Software
### Bundles:
1. [Circuit Python 7.0 or above][link-circuit python] (it required to use 1 MB from the flash) 
2. [Adafruit circuit python bundle][link-adafruit] - Use the latest version from adafruit bundle page [ESP AT control or download from this github]

### Required Libraries from adafruit bundle:
1. adafruit_espatcontrol library or [this library][link-library]
2. adafruit_request

### Required codes to run example codes
1. [Secret.py][link-secret] -> Please modified the information to allow WizFi360 to connect your personal AP and adafruit IO.
2. Example codes 

### Programming and debug software 
1. [Thonny][link-Thonny]
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

##  📓Examples:
1. [TCP Client][link-tcp client]
2. [Adafruit io (MQTT)][link-Adafruit_io_mqtt]
3. [Adafruit io (HTTP)][link-Adafrui_io_http] - Used the same coding method as ESP AT control
4. [Ping][link-ping]  - Used the same coding method as ESP AT control
5. [Blynk][link-blynk]
6. [Adafruit io (MQTT- Multiple topics)][link-multi]

[link-library]: https://github.com/ronpang/WizFi360-cpy/tree/main/lib/adafruit_espatcontrol
[link-Thonny]: https://thonny.org/
[link-ESP_cpy]: https://github.com/adafruit/Adafruit_CircuitPython_ESP_ATcontrol
[link-AT commands]: https://docs.wiznet.io/img/products/wizfi360/wizfi360ds/wizfi360_atset_v1118_e.pdf
[link-AT comparison]: https://docs.wiznet.io/img/products/wizfi360/wizfi360ds/wizfi360_atcp_v102.pdf
[link-circuit python]: https://circuitpython.org/board/raspberry_pi_pico/
[link-adafruit]: https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20211208
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-tcp client]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/TCP%20client_loopback.py
[link-Adafruit_io_mqtt]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/MQTT/aio.py
[link-Adafrui_io_http]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/http/aio_http.py
[link-ping]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/ping.py
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-blynk]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/blynk/TCP%20blynk.py
[link-multi]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/MQTT/aio_change_to_group.py

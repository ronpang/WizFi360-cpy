# Firmware Upgrade

It is a example code to allow WizFi360-EVB-PICO user to upgrade WizFi360's Firmware.

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

## 🔰Firmware Upgrade
1. Required files: [firmware upgrade.py][link-fw], [Secret.py][link-secret]
2. Required commands:
```python
esp.firmware_upgrade() #firmware upgrade function - no output
esp.get_version() #check firmware version 
```
## ☑️Results
### Thonny 
The following are the results is in debug mode

![link-thonny]


[link-readme]: https://github.com/ronpang/WizFi360-cpy
[link-fw]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Firmware%20upgrade/firmware%20upgrade.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-thonny]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20firmware%20upgrade.PNG


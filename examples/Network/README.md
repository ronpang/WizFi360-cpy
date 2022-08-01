# Network Examples
This section includes codings as follow:
1. [TCP client](#TCP) : Communicate with a TCP server through
2. [Ping](#Ping): Pinging the AP to test the connection is work

### Extra Software tools: 

[Hercules][link-Hercules] - Create a TCP server to communicate with the PICO 

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

<a name="TCP"></a>
## 🔰Tcp conncection setup
1. Required files: [TCP Client.py][link-tcp], [Secret.py][link-secret]
2. Required commands:
```python
#1.Connect to a PC - IP address: 10.0.1.75, Port:5000
esp.socket_connect("TCP","10.0.1.75",5000) 
#2.Send data, data -> it the data wanted to send out.
esp.socket_send(str(data).encode())
#3 Receive function to collect data
esp.socket_receive(1)
#4 Disconnect with the server
esp.socket_disconnect()
```

## ☑️TCP results
### Thonny (in debug mode)
It is required to use debug mode to show the progress of the TCP communication

The following image shows the one of the TCP connection (From connect -> send data -> receive data  -> disconnect)

![link-tcp_thonny]

### Hercules
The Hercules software will create a TCP server to allow PICO to connect.

It receive counting data from the module and sent "disconnect" ( 10 bytes of data) to WizFi360

![link-tcp_hercules]

<a name="Ping"></a>
## 💻Ping
1. Required files: [Ping.py][link-ping], [Secret.py][link-secret]
2. Required commands:
```python
#Print out the pinging result
print(esp.ping("8.8.8.8"))
```

## ☑️Ping Result
The following result shows the Pico has ping 4 times with the AP

The result is showing in debug mode.

![link-ping_thonny]


[link-tcp]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/TCP%20client.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-ping]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/ping.py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-tcp_thonny]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20(updated)%20-%20tcp.PNG
[link-Hercules]: https://www.hw-group.com/software/hercules-setup-utility
[link-tcp_hercules]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/Hercules%20result%20-%20wizfi360%20-%20tcp.PNG
[link-ping_thonny]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20Ping.PNG

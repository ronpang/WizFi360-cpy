import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
from adafruit_espatcontrol import adafruit_espatcontrol


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

print("ESP AT commands")
# For Boards that do not have an rtspin like WizFi360-EVB-PICO set rtspin to False.
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
print("Resetting ESP module")
esp.hard_reset()

esp.at_response("at")

first_pass = True
while True:
    try:
        if first_pass:
            # Comment out the next 3 lines if you get a No OK response to AT+CWLAP
            print("Scanning for AP's")
            for ap in esp.scan_APs():
                print(ap)
            print("Checking connection...")
            # secrets dictionary must contain 'ssid' and 'password' at a minimum
            print("Connecting...")
            esp.connect(secrets)
            print("Connected to AT software version ", esp.version)
            print("IP address ", esp.local_ip)
            first_pass = False
        print("Pinging 8.8.8.8...", end="")
        print(esp.ping("8.8.8.8")) #Print the ping result
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

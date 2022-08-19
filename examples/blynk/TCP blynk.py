import time
import board
import busio

from digitalio import DigitalInOut
from digitalio import Direction
from adafruit_espatcontrol import adafruit_espatcontrol

import struct
import BlynkLib # Same library as the python version
#Input the related information after you have a blynk account
BLYNK_TEMPLATE_ID =  "TEMPLATE_ID" 
BLYNK_DEVICE_NAME = "DEVICE_NAME"
BLYNK_AUTH_TOKEN = "AUTH_TOKEN"

#Since BlynkLib has included the socket section for connection, it is needed to move to this section for connection and communication.
class Blynk(BlynkLib.BlynkProtocol): #same as the library
    def __init__(self, auth, **kwargs):
        self.insecure = kwargs.pop('insecure', True)
        self.server = kwargs.pop('server', 'blynk.cloud')
        self.port = kwargs.pop('port', 80 if self.insecure else 443)
        BlynkLib.BlynkProtocol.__init__(self, auth, **kwargs) 
        #self.on('redirect', self.redirect)
    
    def _write(self, data): #function to send data to blynk
        #print('<', data)
        esp.socket_send(data)
        # TODO: handle disconnect
    
    def run(self): #run funcation and check data for collection.
        data = b''
        try:
            data = esp.socket_receive()
            #print('>', data)
        except KeyboardInterrupt:
            raise
        #except socket.timeout:
            # No data received, call process to send ping messages when needed
            #pass
        except: # TODO: handle disconnect
            return
        self.process(data)
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False
#LED = board.GP25

RX = board.GP5
TX = board.GP4
resetpin = DigitalInOut(board.GP20)
rtspin = False
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
#edit host and port to match server
Dest_IP = "128.199.144.129" #bkynk.cloud
Dest_PORT= 80 #TCP Port -> If SSL, please use 443

print("ESP AT commands")
# For Boards that do not have an rtspin like challenger_rp2040_wifi set rtspin to False.
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
print("Resetting ESP module")
esp.hard_reset()

esp.at_response("at")
counter = 1
print (counter)
print("Checking connection")

while not esp.is_connected:
  try:
    # Some ESP do not return OK on AP Scan.
    # See https://github.com/adafruit/Adafruit_CircuitPython_ESP_ATcontrol/issues/48
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
    
  except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
    print("Failed to get data, retrying\n", e)
    print("Resetting ESP module")
    esp.hard_reset()
    continue


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

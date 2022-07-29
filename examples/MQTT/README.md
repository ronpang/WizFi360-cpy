# MQTT example
This is a exmaple using WIZnet's WizFi360 MQTT commands to communicate adafruit IO.

## 🔰MQTT conncection setup
1. Basic setup - please refer to [WizFi360 Basic Setup][link-readme]
2. Required files: [aio.py][link-aio], [Secret.py][link-secret]
3. Required commands:
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


[link-readme]: https://github.com/ronpang/WizFi360-cpy
[link-aio]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/MQTT/aio.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py

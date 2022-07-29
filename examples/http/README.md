# HTTP example
This is a example code for HTTP to connect with adafruit io.

## 🔰MQTT conncection setup
1. Basic setup - please refer to [WizFi360 Basic Setup][link-readme]
2. Required files: [aio.py][link-aio_http], [Secret.py][link-secret]
3. Required commands:
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


[link-readme]: https://github.com/ronpang/WizFi360-cpy
[link-aio_http]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/http/aio_http.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py

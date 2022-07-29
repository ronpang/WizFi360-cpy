# Network Examples
This section includes codings as follow:
1. TCP client: Communicate with a TCP server through
2. Ping: Pinging the AP to test the connection is work

## 🔰Tcp conncection setup
1. Basic setup - please refer to [WizFi360 Basic Setup][link-readme]
2. Required files: [TCP Client.py][link-tcp], [Secret.py][link-secret]
3. Required commands:
```python
#1.Connect to a PC - IP address: 10.0.1.75, Port:5000
esp.socket_connect("TCP","10.0.1.75",5000) 
#2.Send data, str: data -> it the data wanted to send out.
esp.socket_send(str(data).encode())
#3 Receive function to collect data
esp.socket_receive(1)
#4 Disconnect with the server
esp.socket_disconnect()
```
## 💻Ping
1. Basic setup - please refer to [WizFi360 Basic Setup][link-readme]
2. Required files: [Ping.py][link-ping], [Secret.py][link-secret]
3. Required commands:
```python
#Print out the pinging result
print(esp.ping("8.8.8.8"))
```


[link-readme]: https://github.com/ronpang/WizFi360-cpy
[link-tcp]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/TCP%20client.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
[link-ping]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/ping.py

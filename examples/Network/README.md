# Network Examples
This section includes codings as follow:
1. TCP client: Communicate with a TCP server through
2. Ping: Pinging the AP to test the connection is work

# Tcp conncection setup
1. Basic setup - please refer to [WizFi360 Basic Setup][link-readme]
2. Required files: [TCP Client.py][link-tcp], [Secret.py][link-secret]
3. Required commands:
```python
#1.Connect to a PC - IP address: 10.0.1.75, Port:5000
esp.socket_connect("TCP","10.0.1.75",5000) 
#2.Send data
esp.socket_send(str(counter).encode())
#3 Receive function to collect data
esp.socket_receive(1)
#4 Disconnect with the server
esp.socket_disconnect()
```


[link-readme]: https://github.com/ronpang/WizFi360-cpy
[link-tcp]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/Network/TCP%20client.py
[link-secret]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/secrets.py
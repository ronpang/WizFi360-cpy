# SPDX-FileCopyrightText: 2019 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_espatcontrol_wifimanager`
================================================================================

WiFi Manager for making ESP32 AT Control as WiFi much easier

* Author(s): Melissa LeBlanc-Williams, ladyada, Jerry Needell
"""

# pylint: disable=no-name-in-module

import adafruit_requests as requests
import time
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket

try:
    from typing import Dict, Any, Optional, Union, Tuple
    from circuitpython_typing.led import FillBasedLED
    from adafruit_espatcontrol.adafruit_espatcontrol import ESP_ATcontrol
except ImportError:
    pass


class ESPAT_WiFiManager:
    """
    A class to help manage the Wifi connection
    """

    def __init__(
        self,
        esp: ESP_ATcontrol,
        secrets: Dict[str, Union[str, int]],
        status_pixel: Optional[FillBasedLED] = None,
        attempts: int = 2,
    ):
        """
        :param ESP_SPIcontrol esp: The ESP object we are using
        :param dict secrets: The WiFi and Adafruit IO secrets dict (See examples)
        :param status_pixel: (Optional) The pixel device - A NeoPixel or DotStar (default=None)
        :type status_pixel: NeoPixel or DotStar
        :param int attempts: (Optional) Failed attempts before resetting the ESP32 (default=2)
        """
        # Read the settings
        self._esp = esp
        self.debug = False
        self.secrets = secrets
        self.attempts = attempts
        requests.set_socket(socket, esp)
        self.statuspix = status_pixel
        self.pixel_status(0)

    def reset(self) -> None:
        """
        Perform a hard reset on the ESP
        """
        if self.debug:
            print("Resetting ESP")
        self._esp.hard_reset()

    def connect(self) -> None:
        """
        Attempt to connect to WiFi using the current settings
        """
        failure_count = 0
        while not self._esp.is_connected:
            try:
                if self.debug:
                    print("Connecting to AP...")
                self.pixel_status((100, 0, 0))
                self._esp.connect(self.secrets)
                failure_count = 0
                self.pixel_status((0, 100, 0))
            except (ValueError, RuntimeError) as error:
                print("Failed to connect, retrying\n", error)
                failure_count += 1
                if failure_count >= self.attempts:
                    failure_count = 0
                    self.reset()
                continue

    def IO_set(self) -> None:
        """
        Collect information from secrets
        
        """
        cmd = (
            'AT+MQTTSET="'
            + self.secrets["aio_username"]
            + '","'
            + self.secrets["aio_key"]
            + '","'
            + '",60' #keep alive 60s
        )
        self._esp.at_response(cmd, timeout=10, retries=3)
    
    def IO_topics(self, Pub_topic: str, Sub_topic: str) -> None:
        """
        Set MQTT topics for sub and pub
        :param str Pub_topic: Publish channel topic name
        :param str Sub_topic: Subscribe channel topic name
        """
        cmd = (
            'AT+MQTTTOPIC="'
            + self.secrets["aio_username"] + '/feeds/'+ Pub_topic
            + '","'
            + self.secrets["aio_username"] + '/feeds/'+ Sub_topic
            + '"'
        )
        self._esp.at_response(cmd, timeout=10, retries=3)
    
    def IO_Con(self,
        Pub_topic: str,
        Sub_topic: str,
        Mode: str
        ) -> None:
        """
        Connnect to a MQTT server
        :param str Pub_topic: Publish channel topic name (for IO_topics)
        :param str Sub_topic: Subscribe channel topic name (for IO_topics)
        :param str mode: MQTT mode or MQTTs mode (MQTT in SSL)
        """
        self.IO_set()
        self.IO_topics(Pub_topic,Sub_topic)
        if Mode == "MQTT":
            cmd_mode = "0"
            port = "1883"
        elif Mode == "MSSL":
            cmd_mode = "1"
            port = "8883"
        else:
            raise RuntimeError("Connection type must be MQTT or MQTT SSL")
        cmd = (
            'AT+MQTTCON='
            + cmd_mode
            + ',"'
            + "io.adafruit.com"
            + '",'
            + port
        )
        self._esp.at_response(cmd, timeout=25, retries=3)
    
    def MQTT_disconnect(self) -> None:
        """
        Disconnect with MQTT server
        
        """
        cmd = "AT+MQTTDIS"
        self._esp.at_response(cmd, timeout=10, retries=3)
        
    def MQTT_pub(self, data: str) -> None:
        """
        Publish the data to MQTT server
        :param str data: the data that you need to send to the MQTT server
        """
        cmd = (
            'AT+MQTTPUB="'
            + data
            + '"'
            )
        self._esp.at_response(cmd, timeout=10, retries=3)
        
    def MQTT_sub (self, timeout: int = 5) -> None:
        """
        Collect data from MQTT server
        :param int timeout: Retry times for collecting subscribe data
        """
        stamp = time.monotonic()
        result = b''
        while (time.monotonic() - stamp) < timeout:
            temp = self._esp._uart.read(1)
            if temp != None:
                result += temp
        return result
    
    def get(self, url: str, **kw: Any) -> requests.Response:
        """
        Pass the Get request to requests and update Status NeoPixel

        :param str url: The URL to retrieve data from
        :param dict data: (Optional) Form data to submit
        :param dict json: (Optional) JSON data to submit. (Data must be None)
        :param dict header: (Optional) Header data to include
        :param bool stream: (Optional) Whether to stream the Response
        :return: The response from the request
        :rtype: Response
        """
        if not self._esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.get(url, **kw)
        self.pixel_status(0)
        return return_val

    def post(self, url: str, **kw: Any) -> requests.Response:
        """
        Pass the Post request to requests and update Status NeoPixel

        :param str url: The URL to post data to
        :param dict data: (Optional) Form data to submit
        :param dict json: (Optional) JSON data to submit. (Data must be None)
        :param dict header: (Optional) Header data to include
        :param bool stream: (Optional) Whether to stream the Response
        :return: The response from the request
        :rtype: Response
        """
        if not self._esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.post(url, **kw)
        return return_val

    def put(self, url: str, **kw: Any) -> requests.Response:
        """
        Pass the put request to requests and update Status NeoPixel

        :param str url: The URL to PUT data to
        :param dict data: (Optional) Form data to submit
        :param dict json: (Optional) JSON data to submit. (Data must be None)
        :param dict header: (Optional) Header data to include
        :param bool stream: (Optional) Whether to stream the Response
        :return: The response from the request
        :rtype: Response
        """
        if not self._esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.put(url, **kw)
        self.pixel_status(0)
        return return_val

    def patch(self, url: str, **kw: Any) -> requests.Response:
        """
        Pass the patch request to requests and update Status NeoPixel

        :param str url: The URL to PUT data to
        :param dict data: (Optional) Form data to submit
        :param dict json: (Optional) JSON data to submit. (Data must be None)
        :param dict header: (Optional) Header data to include
        :param bool stream: (Optional) Whether to stream the Response
        :return: The response from the request
        :rtype: Response
        """
        if not self._esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.patch(url, **kw)
        self.pixel_status(0)
        return return_val

    def delete(self, url: str, **kw: Any) -> requests.Response:
        """
        Pass the delete request to requests and update Status NeoPixel

        :param str url: The URL to PUT data to
        :param dict data: (Optional) Form data to submit
        :param dict json: (Optional) JSON data to submit. (Data must be None)
        :param dict header: (Optional) Header data to include
        :param bool stream: (Optional) Whether to stream the Response
        :return: The response from the request
        :rtype: Response
        """
        if not self._esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.delete(url, **kw)
        self.pixel_status(0)
        return return_val

    def ping(self, host: str, ttl: int = 250) -> Union[int, None]:
        """
        Pass the Ping request to the ESP32, update Status NeoPixel, return response time

        :param str host: The hostname or IP address to ping
        :param int ttl: (Optional) The Time To Live in milliseconds for the packet (default=250)
        :return: The response time in milliseconds
        :rtype: int
        """
        if not self._esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        response_time = self._esp.ping(host, ttl=ttl)
        self.pixel_status(0)
        return response_time

    def pixel_status(self, value: Union[int, Tuple[int, int, int]]) -> None:
        """
        Change Status NeoPixel if it was defined

        :param value: The value to set the Board's Status NeoPixel to
        :type value: int or 3-value tuple
        """
        if self.statuspix:
            self.statuspix.fill(value)

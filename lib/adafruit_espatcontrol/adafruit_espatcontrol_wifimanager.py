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
        
    def topic_set (self,
                   topic1: str,
                   t1type: str,
                   topic2: str = None,
                   t2type: str = None,
                   topic3: str = None,
                   t3type: str = None,
                   ) -> None:
        """
        Define all the topic types for MQTT setup for adafruitio
        The topics will be fixed and it cannot add or substract during the connection with adafruitio
        :param str topic1: First topic Name (Must included)
        :param str topic2: Second topic Name
        :param str topic3: Third topic Name
        :param str t1type: First topic type (Must included)
        :param str t2type: Second topic type
        :param str t3type: Third topic type
        """
        self.topic1 = topic1
        self.topic2 = topic2
        self.topic3 = topic3
        self.type1 = t1type
        self.type2 = t2type
        self.type3 = t3type   
    
    def IO_topics (self, pub: str) -> None:
        """
        MQTT topic setup for connection.
        Set MQTT topics for subcribe and publish
        it will select the publish topic from pub
        :param str pub: Publish topic
        """
        if self.topic1 is pub:
            pub = self.topic1
            pub_t = self.type1
        elif self.topic2 is pub:
            pub = self.topic2
            pub_t = self.type2
        elif self.topic3 is pub: 
            pub = self.topic3
            pub_t = self.type3
        
        cmd = (
             'AT+MQTTTOPIC="'
             + self.secrets["aio_username"]
             )
        if pub_t is "feed":
            cmd = cmd + ('/feeds/' + pub
                             + '","' + self.secrets["aio_username"] + '/feeds/'+ pub
                             + '"'
                             )
        elif pub_t is "group":
            cmd = cmd + ('/groups/' + pub + '/json'
                             + '","' + self.secrets["aio_username"] + '/groups/'+ pub + '/json'
                             + '"'
                             )
        else:
            raise RuntimeError("Publish type must be feed or group")
        
        if self.topic1 is not pub:
            if self.type1 is "feed":
                cmd = cmd + (',"' +self.secrets["aio_username"] + '/feeds/'+ self.topic1
                             + '"'
                            )
            elif self.type1 is "group":
                cmd = cmd + (',"' +self.secrets["aio_username"] + '/groups/'+ self.topic1 + '/json'
                             + '"'
                            )
            else:
                raise RuntimeError("Topic" + self.topic1 + "Type must be feed or group")
        
        if self.topic2 is not pub: 
            if self.type2 is "feed":
                cmd = cmd + (',"' +self.secrets["aio_username"] + '/feeds/'+ self.topic2
                             + '"'
                            )
            elif self.type2 is "group":
                cmd = cmd + (',"' +self.secrets["aio_username"] + '/groups/'+ self.topic2 + '/json'
                             + '"'
                            )   
            elif self.type2 is None:
                self._esp.at_response(cmd, timeout=10, retries=3)
                return
            else:
                raise RuntimeError("Topic" + self.topic2 + "Type must be feed or group")
            
        if self.topic3 is not pub:
            if self.type3 is "feed":
                cmd = cmd + (',"' + self.secrets["aio_username"] + '/feeds/'+ self.topic3
                             + '"'
                            )
            elif self.type3 is "group":
                cmd = cmd + (',"' +self.secrets["aio_username"] + '/groups/'+ self.topic3 + '/json'
                             + '"'
                            )
            elif self.type3 is None:
                self._esp.at_response(cmd, timeout=10, retries=3)
                return
            else:
                raise RuntimeError("Topic" + self.topic3 + "Type must be feed or group")
        
        self._esp.at_response(cmd, timeout=10, retries=3)
                
    def IO_Con(self, Mode: str) -> None:
        """
        Connnect to a MQTT server (at least one Publish and one Subscribe channel)
        Please set the topics before using this function
        :param str mode: MQTT mode or MQTTS mode (MQTT in SSL)
        """
        self.IO_set()
        if Mode == "MQTT":
            cmd_mode = "0"
            port = "1883"
        elif Mode == "MQTTS":
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
        self._esp.at_response(cmd, timeout=10, retries=3)
    
    def MQTT_disconnect(self) -> None:
        """
        Disconnect with MQTT server
        
        """
        cmd = "AT+MQTTDIS"
        self._esp.at_response(cmd, timeout=10, retries=3)
        
    def MQTT_pub(self, data: str) -> None:
        """
        Publish the data to MQTT server
        
        """
        cmd = (
            'AT+MQTTPUB="'
            + data
            + '"'
            )
        self._esp.at_response(cmd, timeout=10, retries=3)
        
    def IO_json(self,
                topic1 :str,
                data1: str,
                topic2 :str = None,
                data2: str = None,
                topic3 :str = None,
                data3: str = None
                ) -> None:
        """
        Make the data in json format (max 3 topics)
        param str topic1: first topic name
        param str topic2: second topic name
        param str topic3: third topic name
        param str data1: first topic data
        param str data2: second topic data
        param str data3: third topic data
        """
        result = ('{"feeds": {"' #TODO - the logic is wrong, it needs to set the situaton for all kinds of topics 
                + topic1 + '": "'
                + data1  
                )
        if topic2 is not None:
            result = result + ( '","'
                    + topic2 + '": "'
                    + data2 
                    )
        if topic3 is not None:
            result = result + ('","'
                    + topic3
                    +'": "'
                    + data3
                    )
        
        result = result + ('"},"location": {"lat": 0.0,"lon": 0.0,"ele": 0.0}}')

        return result
    def MQTT_sub (self, timeout: int = 1) -> None:
        """
        Collect data from MQTT server
        
        """
        stamp = time.monotonic()
        result = b''
        while (time.monotonic() - stamp) < timeout:
            temp = self._esp._uart.read(1)
            if temp != None:
                result += temp
        return result
    
    def clean_data(self,data, sub_title, fresult):
        """
        Collect the data from MQTT return message
        a) Ability to determine is it a group topic or feed
        b) It could collect data from Json or normal feed reutrn message
        c) If the return message has seperate, it could wait until they have receive the whole message and collect the correct information
        :param str data: Data collected from MQTT_sub
        :param str sub_title: Subcribe topic that you wanted to collect. (MQTT or Group is okay) - > Group needs to include the internal topic (example: group.test)
        :param str fresult: Return result (Receive the whole message from MQTT) or Uncomplete message (wait for combine to a complete message) 
        """
        if sub_title.find(".") >= 0:
            group = sub_title.split(".") #checking the input is a group or a feed value - if group, split
        else:
            group = None #it is a feed
        if str(data).find("b''") is -1: #check the data is it in byte
            if str(data).rfind("\\r\\n") is len(str(data))-5: #check is it end of the input
                # Combine and find the data
                if group and fresult is not None and str(fresult).find(sub_title) >= 0:
                    data = fresult + data #for combining to search feed
                
                result = data.splitlines() #remove all the next line 
                if group is None: #if it is a feed input
                    sub_loc = str(result).find(sub_title) #check is it inlcuded in the data
            
                    if  sub_loc >= 0: #if it is, 
                        if str(result).find("/feeds/", sub_loc - 7) >= 0: #check is it inside a feed
                            # Collect the Sub
                            info = str(result).partition("/feeds/" + sub_title)
                            S_info = info[1].partition(sub_title)
                            Sub = S_info[1]
                            # Collect the Data
                            D_Tinfo = info[2].split(" -> ")
                            D_Finfo = D_Tinfo[1].split("'")
                            fresult = D_Finfo[0]
                        else: Sub, fresult = None , None #Can't find the topic of your feed (other Topic in group used the same name)
                
                    else: Sub, fresult = None , None #Can't find the topic
        
                else: # if it is a group
                    sub_loc = str(result).find(group[0]) #check is it included in the data
                    if  sub_loc >= 0: #if it is,
                        if str(result).find('/groups/', sub_loc - 8) >= 0: #check is it inside a group feed
                            # Collect the Sub name
                            info = str(result).partition("/groups/" + group[0])
                            S_Tinfo = info[2].partition('"' + group[1] + '"')
                            S_Finfo = S_Tinfo[1].split('"')
                            Sub = S_Finfo[1]
                            # Collect the Data
                            D_Finfo = S_Tinfo[2].split('"')
                            fresult = D_Finfo[1]
                        else: Sub, fresult = None , None #Can't find the topic of your group (other Topic in feed used the same name)
                    else: Sub, fresult = None , None #Can't find the topic
            else: #if it is not the end of the line
                Sub = None
                if fresult is None: #first time to add
                    fresult = data
                else: #2nd time and afterwards
                    fresult = fresult + data
        else:
            Sub, fresult = None , None

        return Sub, fresult
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

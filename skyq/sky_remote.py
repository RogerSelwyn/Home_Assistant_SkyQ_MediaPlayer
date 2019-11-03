import time
import math
import socket
import requests
import json
import xml
import xmltodict
from http import HTTPStatus

SKY_STATE_NO_MEDIA_PRESENT = 'NO_MEDIA_PRESENT'
SKY_STATE_PLAYING = 'PLAYING'
SKY_STATE_PAUSED = 'PAUSED_PLAYBACK'
SKY_STATE_OFF = 'OFF'

# SOAP/UPnP Constants
SKY_PLAY_URN = 'urn:nds-com:serviceId:SkyPlay'
SOAP_ACTION = '"urn:schemas-nds-com:service:SkyPlay:2#{0}"'
SOAP_CONTROL_BASE_URL = 'http://{0}:49153{1}'
SOAP_DESCRIPTION_BASE_URL = 'http://{0}:49153/description{1}.xml'
SOAP_PAYLOAD = """<s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/' s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'>
	<s:Body>
		<u:{0} xmlns:u="urn:schemas-nds-com:service:SkyPlay:2">
			<InstanceID>0</InstanceID>
		</u:{0}>
	</s:Body>
</s:Envelope>"""
SOAP_RESPONSE = 'u:{0}Response'
SOAP_USER_AGENT = 'SKYPLUS_skyplus'
UPNP_GET_MEDIA_INFO = 'GetMediaInfo'
UPNP_GET_TRANSPORT_INFO = 'GetTransportInfo'

# REST Constants
REST_BASE_URL = 'http://{0}:{1}/as/{2}'
REST_PATH_INFO = 'system/information'
REST_PATH_APPS = 'apps/status'
REST_CHANNEL_LIST = 'services'
REST_RECORDING_DETAILS = 'pvr/details/{0}'# SOAP/UPnP Constants

# Sky specific constants
CURRENT_URI = 'CurrentURI'
CURRENT_TRANSPORT_STATE = 'CurrentTransportState'
IMAGE_URL_BASE = 'http://images.metadata.sky.com/pd-image/{0}/16-9/1788'
PVR = 'pvr'
SKY_STATE_NO_MEDIA_PRESENT = 'NO_MEDIA_PRESENT'
SKY_STATE_PLAYING = 'PLAYING'
SKY_STATE_PAUSED = 'PAUSED_PLAYBACK'
XSI = 'xsi'


class SkyRemote:
    commands={"power": 0, "select": 1, "backup": 2, "dismiss": 2, "channelup": 6, "channeldown": 7, "interactive": 8, "sidebar": 8, "help": 9, "services": 10, "search": 10, "tvguide": 11, "home": 11, "i": 14, "text": 15,  "up": 16, "down": 17, "left": 18, "right": 19, "red": 32, "green": 33, "yellow": 34, "blue": 35, "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, "play": 64, "pause": 65, "stop": 66, "record": 67, "fastforward": 69, "rewind": 71, "boxoffice": 240, "sky": 241}
    connectTimeout = 1000
    TIMEOUT = 3

    REST_BASE_URL = 'http://{0}:{1}/as/{2}'
    REST_PATH_INFO = 'system/information'

    def __init__(self, host, port=49160, jsonport=9006):
        self._host=host
        self._port=port
        self._jsonport = jsonport
        self._soapControlURl = self._getSoapControlURL(0)
        if (self._soapControlURl is None):
            self._soapControlURl = self._getSoapControlURL(1)

    def http_json(self, path) -> str:
        try:
            response = requests.get(self.REST_BASE_URL.format(self._host, self._jsonport, path), timeout=self.TIMEOUT)
            return json.loads(response.content)
        except Exception as err:
            return {}
    

    def _getSoapControlURL(self, descriptionIndex):
        try:
            descriptionUrl = SOAP_DESCRIPTION_BASE_URL.format(self._host, descriptionIndex)
            print(descriptionUrl)
            headers = {'User-Agent': SOAP_USER_AGENT}
            resp = requests.get(descriptionUrl, headers=headers, timeout=self.TIMEOUT)
            if resp.status_code == HTTPStatus.OK:
                description = xmltodict.parse(resp.text)
                services = description['root']['device']['serviceList']['service']
                playService = next(s for s in services if s['serviceId'] == SKY_PLAY_URN)
                return SOAP_CONTROL_BASE_URL.format(self._host, playService['controlURL'])
            return None
        except:
            print ("soap error")
            return None
		    
    def _callSkySOAPService(self, method):
        try:
            payload = SOAP_PAYLOAD.format(method)
            headers = {'Content-Type': 'text/xml; charset="utf-8"', 'SOAPACTION': SOAP_ACTION.format(method)}
            resp = requests.post(self._soapControlURl, headers=headers, data=payload, verify=False, timeout=self.TIMEOUT)
            if resp.status_code == HTTPStatus.OK:
                xml = resp.text
                return xmltodict.parse(xml)['s:Envelope']['s:Body'][SOAP_RESPONSE.format(method)]
            else:
                return None
        except requests.exceptions.RequestException as err:
                self._connfail = CONNFAILCOUNT
                return None


    def powerStatus(self) -> str:
        output = self.http_json(self.REST_PATH_INFO)
        if ('activeStandby' in output and output['activeStandby'] is False):
            return 'On'
        else:
            return 'Off'

    def getCurrentState(self):
        if(self.powerStatus() == 'Off'):
           return 'Off'
        response = self._callSkySOAPService(UPNP_GET_TRANSPORT_INFO)
        if (response is not None):
            state = response[CURRENT_TRANSPORT_STATE]
            if state == SKY_STATE_PLAYING:
                return SKY_STATE_PLAYING
            elif state == SKY_STATE_PAUSED:
                return SKY_STATE_PAUSED
        return SKY_STATE_OFF
        
        
    
    def press(self, sequence):
        if isinstance(sequence, list):
            for item in sequence:
                if item not in self.commands:
                    print('Invalid command: {}'.format(item))
                    break
                self.sendCommand(self.commands[item.casefold()])
                time.sleep(0.5)
        else:
            if sequence not in self.commands:
                print('Invalid command: {}'.format(sequence))
            else:
                self.sendCommand(self.commands[sequence])    

    def sendCommand(self, code):
        commandBytes = bytearray([4,1,0,0,0,0, int(math.floor(224 + (code/16))), code % 16])

        try:
            client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print('Failed to create socket. Error code: %s , Error message : %s' % (str(msg[0]), msg[1]))
            return

        try:
            client.connect((self._host, self._port))
        except:
            print("Failed to connect to client")
            return

        l=12
        timeout=time.time()+self.connectTimeout

        while 1:
            data=client.recv(1024)
            data=data

            if len(data)<24:
                client.sendall(data[0:l])
                l=1
            else:
                client.sendall(commandBytes)
                commandBytes[1]=0
                client.sendall(commandBytes)
                client.close()
                break

            if time.time() > timeout:
                print("timeout error")
                break
            

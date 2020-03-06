import time
import math
import socket
import requests
import json
import xml
import xmltodict
import pytz
from http import HTTPStatus
from custom_components.skyq.skyq.ws4py.client.threadedclient import WebSocketClient
from datetime import datetime, timedelta


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

# WebSocket Constants
WS_BASE_URL = 'ws://{0}:9006/as/{1}'
WS_CURRENT_APPS = 'apps/status'

# REST Constants
REST_PATH_APPS = 'apps/status'
REST_CHANNEL_LIST = 'services'
REST_RECORDING_DETAILS = 'pvr/details/{0}'

# Generic Constants
DEFAULT_ENCODING = 'utf-8'
RESPONSE_OK = 200

# Sky specific constants
CURRENT_URI = 'CurrentURI'
CURRENT_TRANSPORT_STATE = 'CurrentTransportState'
IMAGE_URL_BASE = 'https://images.metadata.sky.com/pd-image/{0}/16-9/1788'
PVR = 'pvr'
XSI = 'xsi'

xmlTvUrlBase = 'http://www.xmltv.co.uk'
xmlTvUrl = xmlTvUrlBase + '/feed/6743'

class SkyRemote:
    commands={"power": 0, "select": 1, "backup": 2, "dismiss": 2, "channelup": 6, "channeldown": 7, "interactive": 8, "sidebar": 8, "help": 9, "services": 10, "search": 10, "tvguide": 11, "home": 11, "i": 14, "text": 15,  "up": 16, "down": 17, "left": 18, "right": 19, "red": 32, "green": 33, "yellow": 34, "blue": 35, "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, "play": 64, "pause": 65, "stop": 66, "record": 67, "fastforward": 69, "rewind": 71, "boxoffice": 240, "sky": 241}
    connectTimeout = 1000
    TIMEOUT = 2

    REST_BASE_URL = 'http://{0}:{1}/as/{2}'
    REST_PATH_INFO = 'system/information'

    SKY_STATE_NO_MEDIA_PRESENT = 'NO_MEDIA_PRESENT'
    SKY_STATE_PLAYING = 'PLAYING'
    SKY_STATE_PAUSED = 'PAUSED_PLAYBACK'
    SKY_STATE_OFF = 'OFF'

    # Application Constants
    APP_EPG = 'com.bskyb.epgui'
    APP_YOUTUBE = 'YouTube'
    APP_YOUTUBE_TITLE = 'YouTube'
    APP_VEVO = 'com.bskyb.vevo'
    APP_VEVO_TITLE = 'Vevo'
    APP_STATUS_VISIBLE = 'VISIBLE'

    def __init__(self, host, port=49160, jsonport=9006):
        self._host=host
        self._port=port
        self._jsonport = jsonport
        response = self._getSoapControlURL(1)
        self._soapControlURl = response['url']
        if (self._soapControlURl is None and response['status'] == 'Not Found'):
            self._soapControlURl = self._getSoapControlURL(0)['url']
        self.lastEpgUpdate = None
        self._xmlTvUrl = xmlTvUrl

    def http_json(self, path, headers=None) -> str:
        try:
            response = requests.get(self.REST_BASE_URL.format(self._host, self._jsonport, path), timeout=self.TIMEOUT, headers=headers)
            return json.loads(response.content)
        except Exception as err:
            return {}
    
    def _getSoapControlURL(self, descriptionIndex):
        try:
            descriptionUrl = SOAP_DESCRIPTION_BASE_URL.format(self._host, descriptionIndex)
            headers = {'User-Agent': SOAP_USER_AGENT}
            resp = requests.get(descriptionUrl, headers=headers, timeout=self.TIMEOUT)
            if resp.status_code == HTTPStatus.OK:
                description = xmltodict.parse(resp.text)
                services = description['root']['device']['serviceList']['service']
                if (type(services) != list):
                    services = [services]
                playService = None
                for s in services:
                    if s['serviceId'] == SKY_PLAY_URN:
                        playService = s
                if playService == None:
                    return {'url': None, 'status': 'Not Found'}
                return {'url':SOAP_CONTROL_BASE_URL.format(self._host, playService['controlURL']), 'status': 'OK'}
            return {'url': None, 'status': 'Not Found'}
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return {'url': None, 'status': 'Error'}
        except Exception as err:
            print(f'Other error occurred: {err}')
            return {'url': None, 'status': 'Error'}
            
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
                # self._connfail = CONNFAILCOUNT
                return None

    def _callSkyWebSocket(self, method):
        try:
            client = SkyWebSocket(WS_BASE_URL.format(self._host, method))
            client.connect()
            timeout = datetime.now() + timedelta(0, 5)
            while client.data is None and datetime.now() < timeout:
                pass
            client.close()
            if client.data is not None:
                return json.loads(client.data.decode(DEFAULT_ENCODING), encoding=DEFAULT_ENCODING)
            else:
                return None
        except Exception as err:
            print(f'Error occurred: {err}')
            return None

    def getActiveApplication(self):
        try:
            apps = self._callSkyWebSocket(WS_CURRENT_APPS)
            return next(a for a in apps['apps'] if a['status'] == self.APP_STATUS_VISIBLE)['appId']
        except Exception:
            return self.APP_EPG


    def powerStatus(self) -> str:
        if self._soapControlURl is None:
            return 'Powered Off'
        output = self.http_json(self.REST_PATH_INFO)
        if ('activeStandby' in output and output['activeStandby'] is False):
            return 'On'
        else:
            return 'Off'

    def _getEpgData(self):
        if self.lastEpgUpdate is None or self.lastEpgUpdate < (datetime.now() - timedelta(hours = 12)):
            resp = requests.get(self._xmlTvUrl)
            if resp.status_code == RESPONSE_OK:
                self.epgData = xmltodict.parse(resp.text)
                self.lastEpgUpdate = datetime.now()

    def _getCurrentLiveTVProgramme(self, channel):
        try:
            result = { 'channel': channel, 'imageUrl': None, 'title': None, 'season': None, 'episode': None}
            title = None
            season = None
            episode = None
            imageUrl = None
            self._getEpgData()
            queryChannel = channel
            if queryChannel.endswith(" HD"):
                queryChannel = queryChannel[:-3]
            if queryChannel == 'BBC Two':
                queryChannel = 'BBC Two Eng'
            channelNode = next(c for c in self.epgData['tv']['channel'] if c['display-name'].startswith(queryChannel))
            channelId = channelNode['@id']
            if 'icon' in channelNode:
                imageUrl = xmlTvUrlBase + channelNode['icon']['@src']
                result.update({'imageUrl': imageUrl})
            now = pytz.utc.localize(datetime.now())
            programme = next(p for p in self.epgData['tv']['programme'] if p["@channel"] == channelId and datetime.strptime(p["@start"], "%Y%m%d%H%M%S %z").astimezone(pytz.utc) < now and datetime.strptime(p["@stop"], "%Y%m%d%H%M%S %z").astimezone(pytz.utc) > now)
            title = programme['title']['#text']
            result.update({'title': title})
            if 'episode-num' not in programme:
                episodeNum = programme['episode-num']['#text']
                if episodeNum[0:1] == 's':
                    season = int(episodeNum[1:3])
                    episode = int(episodeNum[5:7])
                else:
                    episode = int(episodeNum[1:3])
            result.update({'season': season})
            result.update({'episode': episode})
            return result
        except Exception as err:
            return result
        
    def getCurrentMedia(self):
        result = { 'channel': None, 'imageUrl': None, 'title': None, 'season': None, 'episode': None}

        response = self._callSkySOAPService(UPNP_GET_MEDIA_INFO)
        if (response is not None):
            currentURI = response[CURRENT_URI]
            if (currentURI is not None):
                if (XSI in currentURI):
                    # Live content
                    sid = int(currentURI[6:], 16)
                    channels = self.http_json(REST_CHANNEL_LIST)
                    channelNode = next(s for s in channels['services'] if s['sid'] == str(sid))
                    result.update({'imageUrl': None})
                    channel = channelNode['t']
                    programme = self._getCurrentLiveTVProgramme(channel)
                    result.update(programme)
                elif (PVR in currentURI):
                    # Recorded content
                    pvrId = "P"+currentURI[11:]
                    recording = self.http_json(REST_RECORDING_DETAILS.format(pvrId))
                    result.update({'channel': recording['details']['cn']})
                    result.update({'title': recording['details']['t']})
                    #if (title.startswith('New: ')):
                    #    result.udpate({'title': title[5:]})
                    if ('seasonnumber' in recording['details'] and 'episodenumber' in recording['details']):
                        result.update({'season':  recording['details']['seasonnumber']})
                        result.update({'episode': recording['details']['episodenumber'] })
                    if ('programmeuuid' in recording['details']):
                        programmeuuid = recording['details']['programmeuuid']
                        imageUrl = IMAGE_URL_BASE.format(str(programmeuuid))
                        if ('osid' in recording['details']):
                            osid = recording['details']['osid']
                            imageUrl += ("?sid=" + str(osid))
                        result.update({'imageUrl': imageUrl})
        return result


    def getCurrentState(self):
        if(self.powerStatus() == 'Off'):
           return 'Off'
        response = self._callSkySOAPService(UPNP_GET_TRANSPORT_INFO)
        if (response is not None):
            state = response[CURRENT_TRANSPORT_STATE]
            if state == self.SKY_STATE_PLAYING:
                return self.SKY_STATE_PLAYING
            elif state == self.SKY_STATE_PAUSED:
                return self.SKY_STATE_PAUSED
        return self.SKY_STATE_OFF
        
        
    
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
            
class SkyWebSocket(WebSocketClient):
    def __init__(self, url):
        super(SkyWebSocket, self).__init__(url)
        self.data = None
    def received_message(self, message):
        self.data = message.data
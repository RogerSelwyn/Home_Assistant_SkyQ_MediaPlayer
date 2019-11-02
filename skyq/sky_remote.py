import time
import math
import socket
import requests
import json

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

    def http_json(self, path) -> str:
        try:
            response = requests.get(self.REST_BASE_URL.format(self._host, self._jsonport, path), timeout=self.TIMEOUT)
            return json.loads(response.content)
        except Exception as err:
            return {}

    def powerStatus(self) -> str:
        output = self.http_json(self.REST_PATH_INFO)
        if ('activeStandby' in output and output['activeStandby'] is False):
            return 'On'
        else:
            return 'Off'
    
    
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
            

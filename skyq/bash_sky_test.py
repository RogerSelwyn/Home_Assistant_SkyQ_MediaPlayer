#!/usr/bin/env python3
import sky_remote
import requests
import sys

# Run ./bash_sky.py <sky_box_ip>
# example: ./bash_sky_test.py 192.168.0.9
# Note: you may need to modify top line change python3 to python, depending on OS/setup. this is works for me on my mac
logo_url = ''
if len(sys.argv) == 3:
    logo_url = sys.argv[2]

sky = sky_remote.SkyRemote(sys.argv[1], logo_url)
print("----------- Power status")
print(sky.powerStatus())
print("----------- Current Media")
print(str(sky.getCurrentMedia()))
print("----------- Active Application")
print(str(sky.getActiveApplication()))

#print("----------- Testing Description 0")
#print(sky._getSoapControlURL(0))
#print("----------- Testing Description 1")
#print(sky._getSoapControlURL(1))
#print("----------- Testing Description 2")
#print(sky._getSoapControlURL(2))

#print("----------- Transport Info")
#print(sky._callSkySOAPService('GetTransportInfo'))

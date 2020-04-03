#!/usr/bin/env python
import sky_remote
import requests
import sys

# Run ./bash_sky.py <sky_box_ip>
# example: ./bash_sky_test.py 192.168.0.9
# Note: you may need to modify top line change python3 to python, depending on OS/setup. this is works for me on my mac
if len(sys.argv) == 3:
    get_live_tv = True
    if sys.argv[2] == "False":
        get_live_tv = False
    sky = sky_remote.SkyRemote(sys.argv[1], get_live_tv=get_live_tv, country="UK")
else:
    sky = sky_remote.SkyRemote(sys.argv[1], get_live_tv=True, country="UK")

print("----------- Power status")
print(sky.powerStatus())
print("----------- Current Media")
print(str(sky.getCurrentMedia()))
print("----------- Active Application")
print(str(sky.getActiveApplication()))

# print("----------- Testing Description 0")
# print(sky._getSoapControlURL(0))
# print("----------- Testing Description 1")
# print(sky._getSoapControlURL(1))
# print("----------- Testing Description 2")
# print(sky._getSoapControlURL(2))

# print("----------- Transport Info")
# print(sky._callSkySOAPService('GetTransportInfo'))

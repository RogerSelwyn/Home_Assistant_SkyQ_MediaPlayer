import logging
import math
import requests
import json
import socket
import time


from custom_components.skyq.skyq.sky_remote import SkyRemote
from custom_components.skyq.util.config_gen import SwitchMaker

import voluptuous as vol

from homeassistant import util
from homeassistant.components.media_player import MediaPlayerDevice, PLATFORM_SCHEMA
from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_SELECT_SOURCE,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PLAYING,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.script import Script

_LOGGER = logging.getLogger(__name__)

CONF_SOURCES = "sources"
CONF_ROOM = "room"
CONF_DIR = "config_directory"
CONF_GEN_SWITCH = "generate_switches_for_channels"

DEFAULT_NAME = "SkyQ Box"

SUPPORT_SKYQ = (
    SUPPORT_TURN_OFF
    | SUPPORT_PAUSE
    | SUPPORT_TURN_ON
    | SUPPORT_PLAY
    | SUPPORT_NEXT_TRACK
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_SELECT_SOURCE
)



#CUSTOMIZE_SCHEMA = vol.Schema(
#    {vol.Optional(CONF_SOURCES): vol.All(cv.string, [cv.string, cv.string])}
#)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SOURCES, default={}): {cv.string: cv.string},
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_ROOM): cv.string,
        vol.Required(CONF_DIR): cv.string,
        vol.Optional(CONF_GEN_SWITCH, default=False): cv.string,

    }
)
POWER = 0
SELECT = 1
BACKUP = 2
DISMISS = 2
CHANNELUP = 6
CHANNELDOWN = 7
INTERACTIVE = 8
SIDEBAR = 8
HELP = 9
SERVICES = 10
SEARCH = 10
TVGUIDE = 11
HOME = 11
INFO = 14
TEXT = 15 
UP = 16
DOWN = 17
LEFT = 18
RIGHT = 19
RED = 32
GREEN = 33
YELLOW = 34
BLUE = 35
ZERO = 48
ONE = 49
TWO = 50
THREE = 51
FOUR = 52
FIVE = 53
SIX = 54
SEVEN = 55
EIGHT = 56
NINE = 57
PLAY = 64
PAUSE = 65
STOP = 66
RECORD = 67
FASTFORWARD = 69
REWIND = 71
BOXOFFICE = 240
SKY = 241
LOGGER = logging.getLogger(__name__)
REMOTE_PORT = 49160

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SkyQ platform."""
    player = SkyQDevice(
        hass,
        config.get(CONF_NAME),
        config.get(CONF_HOST),
        config.get(CONF_SOURCES),
        config.get(CONF_ROOM),
        config.get(CONF_GEN_SWITCH),
        config.get(CONF_DIR),
        )
    add_entities([player])




class SkyQDevice(MediaPlayerDevice):
    """Representation of a SkyQ Box"""
    def __init__(self,hass,name,host,sources,room,generate_switches_for_channels,config_directory):
        self.hass = hass
        self._name = name
        self._host = host
        self._client = SkyRemote(host)
        self._playing = True
        self._current_source = None
        self._current_source_id = None
        self._state = STATE_OFF
        self._power = STATE_OFF
        self._source_names = sources or {}
        LOGGER.warning(generate_switches_for_channels)
        if (generate_switches_for_channels is 'True'):
            swMaker = SwitchMaker(name, room, config_directory)
            for ch in [*self._source_names.keys()]:
                swMaker.addChannel(ch)
            swMaker.closeFile()      
        
        

    @property
    def supported_features(self):
        return SUPPORT_SKYQ  
    
    @property
    def name(self):
        return self._name
    
    @property
    def state(self):
        return self._state
    
    @property
    def source_list(self):
        return [*self._source_names.keys()]

    def update(self):
    #LOGGER.warning(self._client.powerStatus())
        if (self._client.powerStatus() is 'On'):
            if(self._power is not STATE_PLAYING):
                self._state = STATE_PLAYING
                self._power = STATE_PLAYING
                self._playing = True

        else:
            self._power = STATE_OFF
            self._state = STATE_OFF
            self._playing = False
        

    def turn_off(self):
        self._client.press('power')
        return None

    def turn_on(self):
        self._client.press(['home', 'dismiss'])
        return None

    def media_play(self):
        self._client.press('play')
        self._state = STATE_PLAYING
        self._playing = True
        return None

    def media_pause(self):
        self._client.press('pause')
        self._state = STATE_PAUSED
        self._playing = False
        return None
    
    def media_next_track(self):
        self._client.press('fastforward')

    def media_previous_track(self):
        self._client.press('rewind')
        
    def select_source(self, source):
        self._client.press(self._source_names.get(source).split(','))

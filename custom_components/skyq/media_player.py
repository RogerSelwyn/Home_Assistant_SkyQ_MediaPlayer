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
    SUPPORT_STOP,
    SUPPORT_SEEK,
    MEDIA_TYPE_TVSHOW,
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

SKY_STATE_NO_MEDIA_PRESENT = "NO_MEDIA_PRESENT"
SKY_STATE_PLAYING = "PLAYING"
SKY_STATE_PAUSED = "PAUSED_PLAYBACK"
SKY_STATE_OFF = "OFF"

_LOGGER = logging.getLogger(__name__)

CONF_SOURCES = "sources"
CONF_ROOM = "room"
CONF_DIR = "config_directory"
CONF_GEN_SWITCH = "generate_switches_for_channels"
CONF_OUTPUT_PROGRAMME_IMAGE = "output_programme_image"
CONF_GET_LIVETV = "get_live_tv"
CONF_LIVE_TV = "live_tv"
CONF_COUNTRY = "country"

DEFAULT_NAME = "SkyQ Box"

SUPPORT_SKYQ = (
    SUPPORT_TURN_OFF
    | SUPPORT_PAUSE
    | SUPPORT_TURN_ON
    | SUPPORT_PLAY
    | SUPPORT_NEXT_TRACK
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_SELECT_SOURCE
    | SUPPORT_STOP
    | SUPPORT_SEEK
)

FEATURE_BASIC = 1
FEATURE_IMAGE = 2


ENABLED_FEATURES = FEATURE_BASIC | FEATURE_IMAGE

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SOURCES, default={}): {cv.string: cv.string},
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ROOM, default="Default Room"): cv.string,
        vol.Optional(CONF_DIR, default="/config/"): cv.string,
        vol.Optional(CONF_GEN_SWITCH, default=False): cv.boolean,
        vol.Optional(CONF_OUTPUT_PROGRAMME_IMAGE, default=True): cv.boolean,
        vol.Optional(CONF_GET_LIVETV, default=True): cv.boolean,
        vol.Optional(CONF_LIVE_TV, default=True): cv.boolean,
        vol.Optional(CONF_COUNTRY, default="UK"): cv.string,
    }
)

RESPONSE_OK = 200

SKYQ_ICONS = {
    "app": "mdi:application",
    "live": "mdi:satellite-variant",
    "pvr": "mdi:movie-open",
}


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
        config.get(CONF_OUTPUT_PROGRAMME_IMAGE),
        config.get(CONF_GET_LIVETV),
        config.get(CONF_LIVE_TV),
        config.get(CONF_COUNTRY),
    )
    add_entities([player])


class SkyQDevice(MediaPlayerDevice):
    """Representation of a SkyQ Box"""

    def __init__(
        self,
        hass,
        name,
        host,
        sources,
        room,
        generate_switches_for_channels,
        config_directory,
        output_programme_image,
        get_live_tv,
        live_tv,
        country,
    ):
        self.hass = hass
        self._name = name
        self._host = host
        self._live_tv = live_tv
        if not get_live_tv:
            self._live_tv = get_live_tv
        self._country = country
        self._client = SkyRemote(host, country=self._country)
        self._current_source = None
        self._current_source_id = None
        self._state = STATE_OFF
        self._power = STATE_OFF
        self._enabled_features = ENABLED_FEATURES
        self._title = None
        self.channel = None
        self.episode = None
        self.imageUrl = None
        self.season = None
        self._skyq_type = None
        self._skyq_icon = None

        if not (output_programme_image):
            self._enabled_features = FEATURE_BASIC

        self._source_names = sources or {}

        # _LOGGER.warning(generate_switches_for_channels)
        if generate_switches_for_channels:
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
    def should_poll(self):
        # Device should be polled.
        return True

    @property
    def state(self):
        """Get the device state. An exception means OFF state."""
        return self._state

    @property
    def source_list(self):
        return [*self._source_names.keys()]

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return self.imageUrl

    @property
    def media_channel(self):
        """Channel currently playing"""
        return self.channel

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        return MEDIA_TYPE_TVSHOW

    @property
    def media_series_title(self):
        """Return the title of the series of current playing media."""
        # return self._title if self.isTvShow else None
        return self._title if self.channel is not None else None

    @property
    def media_title(self):
        """Title of current playing media."""
        # return self._title if not self.isTvShow else self.channel
        return self.channel if self.channel is not None else self._title

    @property
    def media_season(self):
        """Season of current playing media (TV Show only)."""
        return self.season

    @property
    def media_episode(self):
        """Episode of current playing media (TV Show only)."""
        return self.episode

    @property
    def icon(self):
        """Entity icon."""
        return self._skyq_icon

    @property
    def device_state_attributes(self):
        """Return entity specific state attributes."""
        attributes = {}
        attributes["skyq_media_type"] = self._skyq_type
        return attributes

    def update(self):
        """Get the latest data and update device state."""

        self._skyq_icon = None

        self._updateState()

        self._skyq_type = self._power

        if self._power != STATE_OFF:
            self._updateCurrentProgramme()

    def _updateState(self):
        if self._client.powerStatus() == "On":
            if self._power is not STATE_PLAYING:
                self._state = STATE_PLAYING
                self._power = STATE_PLAYING
            # this checks is flakey during channel changes, so only used for pause checks if we know its on
            if self._client.getCurrentState() == SkyRemote.SKY_STATE_PAUSED:
                self._state = STATE_PAUSED
            else:
                self._state = STATE_PLAYING
        else:
            self._power = STATE_OFF
            self._state = STATE_OFF

    def _updateCurrentProgramme(self):
        self.channel = None
        self.episode = None
        self.imageUrl = None
        self.isTvShow = False
        self.season = None
        self._title = None

        app = self._client.getActiveApplication()
        # _LOGGER.warning('Active APP: ' + str(activeApp))
        if app["activeApp"] == SkyRemote.APP_EPG:
            currentMedia = self._client.getCurrentMedia()
            self.channel = currentMedia.get("channel")
            self.isTvShow = False
            if currentMedia["live"]:
                self._skyq_type = "live"
                if self._live_tv:
                    currentProgramme = self._client.getCurrentLiveTVProgramme(
                        currentMedia["sid"]
                    )
                    self.episode = currentProgramme.get("episode")
                    self.season = currentProgramme.get("season")
                    self._title = currentProgramme.get("title")
                    if self._enabled_features & FEATURE_IMAGE:
                        self.imageUrl = currentProgramme.get("imageUrl")
            else:
                self._skyq_type = "pvr"
                self.episode = currentMedia.get("episode")
                self.season = currentMedia.get("season")
                self._title = currentMedia.get("title")
                if self._enabled_features & FEATURE_IMAGE:
                    self.imageUrl = currentMedia.get("imageUrl")

        else:
            self._skyq_type = "app"
            # self._state = STATE_PLAYING
            self._title = app["appTitle"]

        self._skyq_icon = SKYQ_ICONS[self._skyq_type]

        if self._enabled_features & FEATURE_IMAGE and self.imageUrl is None:
            try:
                resp = requests.head(self.hass.config.api.base_url + app["appImageURL"])
                if resp.status_code == RESPONSE_OK:
                    self.imageUrl = app["appImageURL"]
            except Exception as err:
                _LOGGER.exception(f"X0010M - Image file check failed: {err}")

    def turn_off(self):
        if self._client.powerStatus() == "On":
            self._client.press("power")

    def turn_on(self):
        if self._client.powerStatus() == "Off":
            self._client.press(["home", "dismiss"])

    def media_play(self):
        self._client.press("play")
        self._state = STATE_PLAYING

    def media_pause(self):
        self._client.press("pause")
        self._state = STATE_PAUSED

    def media_next_track(self):
        self._client.press("fastforward")

    def media_previous_track(self):
        self._client.press("rewind")

    def select_source(self, source):
        self._client.press(self._source_names.get(source).split(","))

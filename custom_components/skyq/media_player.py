import logging
import requests


from pyskyqremote.skyq_remote import SkyQRemote
from custom_components.skyq.util.config_gen import SwitchMaker

import voluptuous as vol

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

_LOGGER = logging.getLogger(__name__)

CONF_SOURCES = "sources"
CONF_ROOM = "room"
CONF_DIR = "config_directory"
CONF_GEN_SWITCH = "generate_switches_for_channels"
CONF_OUTPUT_PROGRAMME_IMAGE = "output_programme_image"
CONF_LIVE_TV = "live_tv"
CONF_COUNTRY = "country"

DEFAULT_NAME = "SkyQ Box"
DEVICE_CLASS = "tv"

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
        vol.Optional(CONF_LIVE_TV, default=True): cv.boolean,
        vol.Optional(CONF_COUNTRY, default="UK"): cv.string,
    }
)

RESPONSE_OK = 200

SKYQ_ICONS = {
    "app": "mdi:application",
    "live": "mdi:satellite-variant",
    "off": "mdi:television",
    "pvr": "mdi:movie-open",
}
APP_TITLES = {
    "com.bskyb.vevo": "Vevo",
    "com.spotify.spotify.tvv2": "Spotify",
    "com.roku": "Roku",
    "com.bskyb.epgui": "EPG",
}
APP_IMAGE_URL_BASE = "/local/community/skyq/{0}.png"


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
        live_tv,
        country,
    ):
        self.hass = hass
        self._name = name
        self._host = host
        self._live_tv = live_tv
        self._country = country.casefold()
        self._remote = SkyQRemote(self._host, country=self._country)
        self._state = STATE_OFF
        self._enabled_features = ENABLED_FEATURES
        self._title = None
        self.channel = None
        self.episode = None
        self.imageUrl = None
        self.season = None
        self._skyq_type = None
        self._skyq_icon = SKYQ_ICONS[STATE_OFF]
        self._lastAppTitle = None
        self._appImageUrl = None

        if not (output_programme_image):
            self._enabled_features = FEATURE_BASIC

        self._source_names = sources or {}

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
        return self.imageUrl if self._enabled_features & FEATURE_IMAGE else None

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
        return self._title if self.channel is not None else None

    @property
    def media_title(self):
        """Title of current playing media."""
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
    def device_class(self):
        """Entity class."""
        return DEVICE_CLASS

    @property
    def device_state_attributes(self):
        """Return entity specific state attributes."""
        attributes = {}
        attributes["skyq_media_type"] = self._skyq_type
        return attributes

    def update(self):
        """Get the latest data and update device state."""
        self.channel = None
        self.episode = None
        self.imageUrl = None
        self.season = None
        self._title = None

        self._updateState()

        if self._state != STATE_OFF:
            self._updateCurrentProgramme()

        self._skyq_icon = SKYQ_ICONS[self._skyq_type]

    def turn_off(self):
        if self._remote.powerStatus() == self._remote.SKY_STATE_ON:
            self._remote.press("power")

    def turn_on(self):
        if self._remote.powerStatus() == self._remote.SKY_STATE_OFF:
            self._remote.press(["home", "dismiss"])

    def media_play(self):
        self._remote.press("play")
        self._state = STATE_PLAYING

    def media_pause(self):
        self._remote.press("pause")
        self._state = STATE_PAUSED

    def media_next_track(self):
        self._remote.press("fastforward")

    def media_previous_track(self):
        self._remote.press("rewind")

    def select_source(self, source):
        self._remote.press(self._source_names.get(source).split(","))

    def _updateState(self):
        if self._remote.powerStatus() == self._remote.SKY_STATE_ON:
            self._state = STATE_PLAYING
            # this checks is flakey during channel changes, so only used for pause checks if we know its on
            if self._remote.getCurrentState() == SkyQRemote.SKY_STATE_PAUSED:
                self._state = STATE_PAUSED
            else:
                self._state = STATE_PLAYING
        else:
            self._skyq_type = STATE_OFF
            self._state = STATE_OFF

    def _updateCurrentProgramme(self):

        app = self._remote.getActiveApplication()
        appTitle = app
        if appTitle.casefold() in APP_TITLES:
            appTitle = APP_TITLES[appTitle.casefold()]

        if app == SkyQRemote.APP_EPG:
            currentMedia = self._remote.getCurrentMedia()
            self.channel = currentMedia["channel"]
            self.imageUrl = currentMedia["imageUrl"]
            if currentMedia["live"]:
                self._skyq_type = "live"
                if self._live_tv:
                    currentProgramme = self._remote.getCurrentLiveTVProgramme(
                        currentMedia["sid"]
                    )
                    self.episode = currentProgramme["episode"]
                    self.season = currentProgramme["season"]
                    self._title = currentProgramme["title"]
                    if currentProgramme["imageUrl"]:
                        self.imageUrl = currentProgramme["imageUrl"]
            else:
                self._skyq_type = "pvr"
                self.episode = currentMedia["episode"]
                self.season = currentMedia["season"]
                self._title = currentMedia["title"]
                self.imageUrl = currentMedia["imageUrl"]

        else:
            self._skyq_type = "app"
            self._title = appTitle

        if not self.imageUrl:
            appImageUrl = self._getAppImageUrl(appTitle)
            if appImageUrl:
                self.imageUrl = self._getAppImageUrl(appTitle)

    def _getAppImageUrl(self, appTitle):
        if appTitle == self._lastAppTitle:
            return self._appImageUrl

        self._lastAppTitle = appTitle
        self._appImageUrl = None

        appImageUrl = APP_IMAGE_URL_BASE.format(appTitle.casefold())

        try:
            resp = requests.head(self.hass.config.api.base_url + appImageUrl)
            if resp.status_code == RESPONSE_OK:
                self._appImageUrl = appImageUrl

            return self._appImageUrl
        except (requests.exceptions.ConnectionError) as err:
            _LOGGER.info(f"I0010M - Image file check failed: {appImageUrl} : {err}")
            return self._appImageUrl
        except Exception as err:
            _LOGGER.exception(
                f"X0010M - Image file check failed: {appImageUrl} : {err}"
            )
            return self._appImageUrl

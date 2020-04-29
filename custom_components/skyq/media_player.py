"""The skyq platform allows you to control a SkyQ set top box."""
import logging
import requests
import voluptuous as vol

from homeassistant.components.media_player import MediaPlayerDevice, PLATFORM_SCHEMA
from homeassistant.components.media_player.const import MEDIA_TYPE_TVSHOW
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    STATE_OFF,
    STATE_UNKNOWN,
    STATE_PAUSED,
    STATE_PLAYING,
)
import homeassistant.helpers.config_validation as cv

from pyskyqremote.skyq_remote import SkyQRemote
from custom_components.skyq.util.config_gen import SwitchMaker
from pyskyqremote.const import (
    SKY_STATE_PAUSED,
    SKY_STATE_STANDBY,
    SKY_STATE_ON,
    APP_EPG,
)
from .const import (
    SUPPORT_SKYQ,
    CONF_SOURCES,
    CONF_ROOM,
    CONF_DIR,
    CONF_GEN_SWITCH,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_LIVE_TV,
    CONF_COUNTRY,
    CONF_TEST_CHANNEL,
    DEVICE_CLASS,
    FEATURE_BASIC,
    FEATURE_IMAGE,
    FEATURE_LIVE_TV,
    FEATURE_SWITCHES,
    SKYQ_ICONS,
    APP_TITLES,
    APP_IMAGE_URL_BASE,
    RESPONSE_OK,
)

_LOGGER = logging.getLogger(__name__)

ENABLED_FEATURES = FEATURE_BASIC | FEATURE_IMAGE | FEATURE_LIVE_TV | FEATURE_SWITCHES

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SOURCES, default={}): {cv.string: cv.string},
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ROOM, default="Default Room"): cv.string,
        vol.Optional(CONF_DIR, default="(deprecated)"): cv.string,
        vol.Optional(CONF_GEN_SWITCH, default=False): cv.boolean,
        vol.Optional(CONF_OUTPUT_PROGRAMME_IMAGE, default=True): cv.boolean,
        vol.Optional(CONF_LIVE_TV, default=True): cv.boolean,
        vol.Optional(CONF_COUNTRY, default="(default)"): cv.string,
        vol.Optional(CONF_TEST_CHANNEL, default="(test)"): cv.string,
    }
)


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
        config.get(CONF_TEST_CHANNEL),
    )
    add_entities([player])


class SkyQDevice(MediaPlayerDevice):
    """Representation of a SkyQ Box."""

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
        test_channel,
    ):
        """Initialise the SkyQRemote."""
        self._hass = hass
        self._name = name
        self._host = host
        self._state = STATE_OFF
        self._enabled_features = ENABLED_FEATURES
        self._title = None
        self._channel = None
        self._episode = None
        self._imageUrl = None
        self._season = None
        self._skyq_type = STATE_OFF
        self._lastAppTitle = None
        self._appImageUrl = None

        if country == "(default)":
            country = None
        self._overrideCountry = country

        self._test_channel = None
        if test_channel != "(test)":
            self._test_channel = test_channel

        self._remote = SkyQRemote(self._host, self._overrideCountry, self._test_channel)

        if not (output_programme_image):
            self._enabled_features ^= FEATURE_IMAGE

        if not (live_tv):
            self._enabled_features ^= FEATURE_LIVE_TV

        if not (generate_switches_for_channels):
            self._enabled_features ^= FEATURE_SWITCHES

        if config_directory != "(deprecated)":
            _LOGGER.warning(
                f"Use of 'config_directory' is deprecated since it is no longer required. You set it to {config_directory}."
            )
        if self._overrideCountry:
            if self._overrideCountry.casefold() == "it":
                self._overrideCountry = "ITA"
                _LOGGER.warning(
                    f"Please change country 'it' to 'ITA' in you configuration."
                )
            if self._overrideCountry.casefold() == "uk":
                self._overrideCountry = "GBR"
                _LOGGER.warning(
                    f"Please change country 'uk' to 'GBR' in you configuration."
                )

        self._source_names = sources or {}

        if self._enabled_features & FEATURE_SWITCHES:
            SwitchMaker(hass, name, room, [*self._source_names.keys()])

    @property
    def supported_features(self):
        """Get the supported features."""
        return SUPPORT_SKYQ

    @property
    def name(self):
        """Get the name of the devices."""
        return self._name

    @property
    def should_poll(self):
        """Device should be polled."""
        return True

    @property
    def state(self):
        """Get the device state. An exception means OFF state."""
        return self._state

    @property
    def source_list(self):
        """Get the list of sources for the device."""
        return [*self._source_names.keys()]

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return self._imageUrl if self._enabled_features & FEATURE_IMAGE else None

    @property
    def media_channel(self):
        """Channel currently playing."""
        return self._channel

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        return MEDIA_TYPE_TVSHOW if self.state != STATE_UNKNOWN else None

    @property
    def media_series_title(self):
        """Get the title of the series of current playing media."""
        return self._title if self._channel is not None else None

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._channel if self._channel is not None else self._title

    @property
    def media_season(self):
        """Season of current playing media (TV Show only)."""
        return self._season

    @property
    def media_episode(self):
        """Episode of current playing media (TV Show only)."""
        return self._episode

    @property
    def icon(self):
        """Entity icon."""
        return SKYQ_ICONS[self._skyq_type]

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
        self._channel = None
        self._episode = None
        self._imageUrl = None
        self._season = None
        self._title = None

        self._updateState()

        if self._state != STATE_UNKNOWN and self._state != STATE_OFF:
            self._updateCurrentProgramme()

    def turn_off(self):
        """Turn SkyQ box off."""
        if self._remote.powerStatus() == SKY_STATE_ON:
            self._remote.press("power")

    def turn_on(self):
        """Turn SkyQ box on."""
        if self._remote.powerStatus() == SKY_STATE_STANDBY:
            self._remote.press(["home", "dismiss"])

    def media_play(self):
        """Play the current media item."""
        self._remote.press("play")
        self._state = STATE_PLAYING

    def media_pause(self):
        """Pause teh current media item."""
        self._remote.press("pause")
        self._state = STATE_PAUSED

    def media_next_track(self):
        """Fast forward the current media item."""
        self._remote.press("fastforward")

    def media_previous_track(self):
        """Rewind the current media item."""
        self._remote.press("rewind")

    def select_source(self, source):
        """Select the specified source."""
        self._remote.press(self._source_names.get(source).split(","))

    def _updateState(self):
        powerState = self._remote.powerStatus()
        if powerState == SKY_STATE_ON:
            self._state = STATE_PLAYING
            # this checks is flakey during channel changes, so only used for pause checks if we know its on
            if self._remote.getCurrentState() == SKY_STATE_PAUSED:
                self._state = STATE_PAUSED
            else:
                self._state = STATE_PLAYING
        elif powerState == SKY_STATE_STANDBY:
            self._skyq_type = STATE_OFF
            self._state = STATE_OFF
        else:
            self._skyq_type = STATE_UNKNOWN
            self._state = STATE_OFF

    def _updateCurrentProgramme(self):

        app = self._remote.getActiveApplication()
        appTitle = app
        if appTitle.casefold() in APP_TITLES:
            appTitle = APP_TITLES[appTitle.casefold()]

        if app == APP_EPG:
            currentMedia = self._remote.getCurrentMedia()
            if currentMedia.live:
                self._channel = currentMedia.channel
                self._imageUrl = currentMedia.imageUrl
                self._skyq_type = "live"
                if self._enabled_features & FEATURE_LIVE_TV:
                    currentProgramme = self._remote.getCurrentLiveTVProgramme(
                        currentMedia.sid
                    )
                    if currentProgramme:
                        self._episode = currentProgramme.episode
                        self._season = currentProgramme.season
                        self._title = currentProgramme.title
                        if currentProgramme.imageUrl:
                            self._imageUrl = currentProgramme.imageUrl
            else:
                recording = self._remote.getRecording(currentMedia.pvrId)
                self._skyq_type = "pvr"
                self._channel = recording.channel
                self._episode = recording.episode
                self._season = recording.season
                self._title = recording.title
                self._imageUrl = recording.imageUrl

        else:
            self._skyq_type = "app"
            self._title = appTitle

        if not self._imageUrl:
            appImageUrl = self._getAppImageUrl(appTitle)
            if appImageUrl:
                self._imageUrl = self._getAppImageUrl(appTitle)

    def _getAppImageUrl(self, appTitle):
        if appTitle == self._lastAppTitle:
            return self._appImageUrl

        self._lastAppTitle = appTitle
        self._appImageUrl = None

        appImageUrl = APP_IMAGE_URL_BASE.format(appTitle.casefold())

        try:
            resp = requests.head(self._hass.config.api.base_url + appImageUrl)
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

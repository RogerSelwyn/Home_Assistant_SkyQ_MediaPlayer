"""The skyq platform allows you to control a SkyQ set top box."""
import logging
import voluptuous as vol
import asyncio
import aiohttp
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# from homeassistant.exceptions import PlatformNotReady

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    HTTP_OK,
    STATE_OFF,
    STATE_UNKNOWN,
    STATE_PAUSED,
    STATE_PLAYING,
)

try:
    from homeassistant.helpers.network import get_url
except ImportError:
    pass

from homeassistant.components.media_player import PLATFORM_SCHEMA
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_TVSHOW,
    MEDIA_TYPE_APP,
)

try:
    from homeassistant.components.media_player import MediaPlayerEntity
except ImportError:
    from homeassistant.components.media_player import (
        MediaPlayerDevice as MediaPlayerEntity,
    )


from pyskyqremote.skyq_remote import SkyQRemote
from custom_components.skyq.util.config_gen import SwitchMaker
from pyskyqremote.const import (
    APP_EPG,
    SKY_STATE_ON,
    SKY_STATE_OFF,
    SKY_STATE_PAUSED,
    SKY_STATE_STANDBY,
)
from .const import (
    APP_TITLES,
    APP_IMAGE_URL_BASE,
    CONF_SOURCES,
    CONF_CHANNEL_SOURCES,
    CONF_ROOM,
    CONF_DIR,
    CONF_GEN_SWITCH,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_LIVE_TV,
    CONF_COUNTRY,
    CONF_TEST_CHANNEL,
    CONST_DEFAULT_ROOM,
    CONST_SKYQ_MEDIA_TYPE,
    DEVICE_CLASS,
    DOMAIN,
    SKYQREMOTE,
    FEATURE_BASIC,
    FEATURE_IMAGE,
    FEATURE_LIVE_TV,
    FEATURE_SWITCHES,
    SKYQ_APP,
    SKYQ_LIVE,
    SKYQ_PVR,
    SKYQ_ICONS,
    SUPPORT_SKYQ,
    TIMEOUT,
)

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)

ENABLED_FEATURES = FEATURE_BASIC | FEATURE_IMAGE | FEATURE_LIVE_TV | FEATURE_SWITCHES

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SOURCES, default={}): {cv.string: cv.string},
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ROOM, default=CONST_DEFAULT_ROOM): cv.string,
        vol.Optional(CONF_DIR): cv.string,
        vol.Optional(CONF_GEN_SWITCH, default=False): cv.boolean,
        vol.Optional(CONF_OUTPUT_PROGRAMME_IMAGE, default=True): cv.boolean,
        vol.Optional(CONF_LIVE_TV, default=True): cv.boolean,
        vol.Optional(CONF_COUNTRY): cv.string,
        vol.Optional(CONF_TEST_CHANNEL): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the SkyQ platform."""
    host = config.get(CONF_HOST)
    remote = await hass.async_add_executor_job(SkyQRemote, host)

    config_directory = config.get(CONF_DIR)
    if config_directory:
        _LOGGER.warning(
            f"Use of 'config_directory' is deprecated since it is no longer required. You set it to {config_directory}."
        )

    unique_id = None
    name = config.get(CONF_NAME)

    await _async_setup_platform_entry(
        hass, config, async_add_entities, remote, unique_id, name,
    )


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up a SKY Q entity."""
    remote = hass.data[DOMAIN][config_entry.entry_id][SKYQREMOTE]

    unique_id = config_entry.unique_id
    name = config_entry.data[CONF_NAME]

    await _async_setup_platform_entry(
        hass, config_entry.options, async_add_entities, remote, unique_id, name,
    )


async def _async_setup_platform_entry(
    hass, config_item, async_add_entities, remote, unique_id, name
):
    player = SkyQDevice(
        hass,
        remote,
        unique_id,
        name,
        config_item.get(CONF_TEST_CHANNEL),
        config_item.get(CONF_COUNTRY),
        config_item.get(CONF_SOURCES, {}),
        config_item.get(CONF_ROOM, CONST_DEFAULT_ROOM),
        config_item.get(CONF_GEN_SWITCH, False),
        config_item.get(CONF_OUTPUT_PROGRAMME_IMAGE, True),
        config_item.get(CONF_LIVE_TV, True),
        config_item.get(CONF_CHANNEL_SOURCES, {}),
    )
    async_add_entities([player], True)


class SkyQDevice(MediaPlayerEntity):
    """Representation of a SkyQ Box."""

    def __init__(
        self,
        hass,
        remote,
        unique_id,
        name,
        test_channel,
        overrideCountry,
        sources,
        room,
        generate_switches_for_channels,
        output_programme_image,
        live_tv,
        channel_sources,
    ):
        """Initialise the SkyQRemote."""
        self._name = name
        self._state = STATE_OFF
        self._enabled_features = ENABLED_FEATURES
        self._test_channel = test_channel
        self._overrideCountry = overrideCountry
        self._title = None
        self._channel = None
        self._episode = None
        self._imageUrl = None
        self._imageRemotelyAccessible = False
        self._season = None
        self._skyq_type = STATE_OFF
        self._lastAppTitle = None
        self._appImageUrl = None
        self._remote = remote
        self._available = True
        self._startupSetup = True
        self._unique_id = unique_id
        self._deviceInfo = None
        self._firstError = True
        self._channel_list = None

        if not (output_programme_image):
            self._enabled_features ^= FEATURE_IMAGE

        if not (live_tv):
            self._enabled_features ^= FEATURE_LIVE_TV

        if not (generate_switches_for_channels):
            self._enabled_features ^= FEATURE_SWITCHES

        self._source_names = sources or []
        self._channel_sources = channel_sources or []
        self._source_list = []
        if len(self._source_names) > 0:
            self._source_list = [*self._source_names.keys()]
        self._source_list += self._channel_sources

        if self._enabled_features & FEATURE_SWITCHES:
            SwitchMaker(hass, name, room, [*self._source_names.keys()])

        if not self._remote.deviceSetup:
            self._available = False
            self._startupSetup = False
            _LOGGER.warning(f"W0010M - Device is not available: {self.name}")

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
        return self._source_list

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return self._imageUrl if self._enabled_features & FEATURE_IMAGE else None

    @property
    def media_image_remotely_accessible(self):
        """Is the media image available outside home network."""
        return self._imageRemotelyAccessible

    @property
    def media_channel(self):
        """Channel currently playing."""
        return self._channel

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        if self.state == STATE_UNKNOWN:
            return None
        if self._skyq_type == SKYQ_APP:
            return MEDIA_TYPE_APP

        return MEDIA_TYPE_TVSHOW

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
    def available(self):
        """Entity availability."""
        return self._available

    @property
    def device_info(self):
        """Entity device information."""
        device_info = None
        if self._deviceInfo:
            device_info = {
                "identifiers": {(DOMAIN, self._deviceInfo.serialNumber)},
                "name": self.name,
                "manufacturer": self._deviceInfo.manufacturer,
                "model": self._deviceInfo.hardwareModel,
                "sw_version": f"{self._deviceInfo.ASVersion}:{self._deviceInfo.versionNumber}",
            }
        return device_info

    @property
    def unique_id(self):
        """Entity unique id."""
        return self._unique_id

    @property
    def device_state_attributes(self):
        """Return entity specific state attributes."""
        attributes = {}
        attributes[CONST_SKYQ_MEDIA_TYPE] = self._skyq_type
        return attributes

    async def async_update(self):
        """Get the latest data and update device state."""
        self._channel = None
        self._episode = None
        self._imageUrl = None
        self._season = None
        self._title = None

        if not self._deviceInfo:
            await self._async_getDeviceInfo()

        if self._deviceInfo:
            await self._async_updateState()

        if self._state != STATE_UNKNOWN and self._state != STATE_OFF:
            await self._async_updateCurrentProgramme()

    async def async_turn_off(self):
        """Turn SkyQ box off."""
        powerStatus = await self.hass.async_add_executor_job(self._remote.powerStatus)
        if powerStatus == SKY_STATE_ON:
            await self.hass.async_add_executor_job(self._remote.press, "power")

    async def async_turn_on(self):
        """Turn SkyQ box on."""
        powerStatus = await self.hass.async_add_executor_job(self._remote.powerStatus)
        if powerStatus == SKY_STATE_STANDBY:
            await self.hass.async_add_executor_job(
                self._remote.press, ["home", "dismiss"]
            )

    async def async_media_play(self):
        """Play the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "play")
        self._state = STATE_PLAYING

    async def async_media_pause(self):
        """Pause the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "pause")
        self._state = STATE_PAUSED

    async def async_media_next_track(self):
        """Fast forward the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "fastforward")

    async def async_media_previous_track(self):
        """Rewind the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "rewind")

    async def async_select_source(self, source):
        """Select the specified source."""
        command = None
        if source in self._source_names:
            command = self._source_names.get(source).split(",")
        else:
            channel = next(c for c in self._channel_list if c.channelname == source)
            if channel:
                command = list(channel.channelno)
        if command:
            await self.hass.async_add_executor_job(self._remote.press, command)

    async def async_play_media(self, media_id, media_type):
        """Perform a media action."""
        if media_type.casefold() == DOMAIN:
            await self.hass.async_add_executor_job(
                self._remote.press, media_id.casefold()
            )

    async def _async_updateState(self):
        powerState = await self.hass.async_add_executor_job(self._remote.powerStatus)
        self._setPowerStatus(powerState)
        if powerState == SKY_STATE_ON:
            self._state = STATE_PLAYING
            # this checks is flakey during channel changes, so only used for pause checks if we know its on
            currentState = await self.hass.async_add_executor_job(
                self._remote.getCurrentState
            )
            if currentState == SKY_STATE_PAUSED:
                self._state = STATE_PAUSED
            else:
                self._state = STATE_PLAYING
        elif powerState == SKY_STATE_STANDBY:
            self._skyq_type = STATE_OFF
            self._state = STATE_OFF
        else:
            self._skyq_type = STATE_UNKNOWN
            self._state = STATE_OFF

    async def _async_updateCurrentProgramme(self):

        app = await self.hass.async_add_executor_job(self._remote.getActiveApplication)
        appTitle = app
        if appTitle.casefold() in APP_TITLES:
            appTitle = APP_TITLES[appTitle.casefold()]

        if app == APP_EPG:
            await self._async_getCurrentMedia()
        else:
            self._skyq_type = SKYQ_APP
            self._title = appTitle

        self._imageRemotelyAccessible = True
        if not self._imageUrl:
            appImageUrl = await self._async_getAppImageUrl(appTitle)
            if appImageUrl:
                self._imageUrl = appImageUrl
                self._imageRemotelyAccessible = False

    async def _async_getCurrentMedia(self):
        try:
            currentMedia = await self.hass.async_add_executor_job(
                self._remote.getCurrentMedia
            )

            if currentMedia.live and currentMedia.sid:
                self._channel = currentMedia.channel
                self._imageUrl = currentMedia.imageUrl
                self._skyq_type = SKYQ_LIVE
                if self._enabled_features & FEATURE_LIVE_TV:
                    currentProgramme = await self.hass.async_add_executor_job(
                        self._remote.getCurrentLiveTVProgramme, currentMedia.sid
                    )
                    if currentProgramme:
                        self._episode = currentProgramme.episode
                        self._season = currentProgramme.season
                        self._title = currentProgramme.title
                        if currentProgramme.imageUrl:
                            self._imageUrl = currentProgramme.imageUrl
            elif currentMedia.pvrId:
                recording = await self.hass.async_add_executor_job(
                    self._remote.getRecording, currentMedia.pvrId
                )
                self._skyq_type = SKYQ_PVR
                if recording:
                    self._channel = recording.channel
                    self._episode = recording.episode
                    self._season = recording.season
                    self._title = recording.title
                    self._imageUrl = recording.imageUrl

        except Exception as err:
            _LOGGER.exception(
                f"X0010M - Current Media retrieval failed: {currentMedia} : {err}"
            )

    async def _async_getAppImageUrl(self, appTitle):
        """Check app image is present."""
        if appTitle == self._lastAppTitle:
            return self._appImageUrl

        self._appImageUrl = None

        appImageUrl = APP_IMAGE_URL_BASE.format(appTitle.casefold())

        websession = async_get_clientsession(self.hass)
        try:
            base_url = get_url(self.hass)
        except NameError:
            base_url = self.hass.config.api.base_url
        request_url = base_url + appImageUrl

        try:
            async with getattr(websession, "head")(
                request_url, timeout=TIMEOUT,
            ) as response:
                if response.status == HTTP_OK:
                    self._appImageUrl = appImageUrl

                self._lastAppTitle = appTitle

                return self._appImageUrl
        except aiohttp.client_exceptions.ClientConnectorError as err:
            # This error when server is starting up and app running
            if self._firstError:
                self._firstError = False
            else:
                _LOGGER.exception(
                    f"X0020M - Image file check failed: {request_url} : {err}"
                )
                self._lastAppTitle = appTitle
            return self._appImageUrl
        except asyncio.TimeoutError as err:
            _LOGGER.info(f"I0030M - Image file check timed out: {request_url} : {err}")
            self._lastAppTitle = appTitle
            return self._appImageUrl
        except (aiohttp.ClientError, Exception) as err:
            _LOGGER.exception(
                f"X0030M - Image file check failed: {request_url} : {err}"
            )
            self._lastAppTitle = appTitle
            return self._appImageUrl

    async def _async_getDeviceInfo(self):
        await self.hass.async_add_executor_job(
            self._remote.setOverrides, self._overrideCountry, self._test_channel
        )
        self._deviceInfo = await self.hass.async_add_executor_job(
            self._remote.getDeviceInformation
        )
        if self._deviceInfo:
            self._setUniqueId()

            if not self._channel_list and len(self._channel_sources) > 0:
                channelData = await self.hass.async_add_executor_job(
                    self._remote.getChannelList
                )
                self._channel_list = channelData.channels

    def _setUniqueId(self):
        if not self._unique_id:
            self._unique_id = self._deviceInfo.epgCountryCode + "".join(
                e for e in self._deviceInfo.serialNumber.casefold() if e.isalnum()
            )

    def _setPowerStatus(self, powerStatus):
        if powerStatus == SKY_STATE_OFF and self._available:
            self._available = False
            _LOGGER.info(f"I0010M - Device is not available: {self.name}")

        if powerStatus != SKY_STATE_OFF and not self._available:
            self._available = True
            if self._startupSetup:
                _LOGGER.info(f"I0020M - Device is now available: {self.name}")
            else:
                self._startupSetup = True
                _LOGGER.warning(f"W0020M - Device is now available: {self.name}")

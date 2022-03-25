"""The skyq platform allows you to control a SkyQ set top box."""
import logging
from datetime import datetime, timedelta
from pathlib import Path

from homeassistant.components.media_player import (
    DEVICE_CLASS_RECEIVER,
    DEVICE_CLASS_TV,
    MediaPlayerEntity,
)
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_APP,
    MEDIA_TYPE_TVSHOW,
    SUPPORT_BROWSE_MEDIA,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_SET,
    SUPPORT_VOLUME_STEP,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_HOST,
    CONF_NAME,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PLAYING,
    STATE_UNKNOWN,
)
from pyskyqremote.const import (
    APP_EPG,
    COMMANDS,
    SKY_STATE_OFF,
    SKY_STATE_ON,
    SKY_STATE_PAUSED,
    SKY_STATE_STANDBY,
)
from pyskyqremote.skyq_remote import SkyQRemote

from .classes.config import Config
from .classes.mediabrowser import MediaBrowser
from .classes.switchmaker import SwitchMaker
from .classes.volumeentity import VolumeEntity
from .const import (
    APP_IMAGE_URL_BASE,
    CONF_EPG_CACHE_LEN,
    CONST_DEFAULT_EPGCACHELEN,
    CONST_SKYQ_CHANNELNO,
    CONST_SKYQ_MEDIA_TYPE,
    DOMAIN,
    DOMAINBROWSER,
    ERROR_TIMEOUT,
    FEATURE_BASE,
    FEATURE_GET_LIVE_RECORD,
    FEATURE_IMAGE,
    FEATURE_LIVE_TV,
    FEATURE_SWITCHES,
    FEATURE_TV_DEVICE_CLASS,
    REMOTE_BUTTONS,
    SKYQ_APP,
    SKYQ_ICONS,
    SKYQ_LIVE,
    SKYQ_LIVEREC,
    SKYQ_PVR,
    SKYQREMOTE,
)
from .const_homekit import (
    ATTR_KEY_NAME,
    EVENT_HOMEKIT_TV_REMOTE_KEY_PRESSED,
    KEY_FAST_FORWARD,
    KEY_REWIND,
)
from .entity import SkyQEntity
from .utils import AppImageUrl, get_command

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Set up the SkyQ platform."""
    host = config.get(CONF_HOST)
    epg_cache_len = config.get(CONF_EPG_CACHE_LEN, CONST_DEFAULT_EPGCACHELEN)
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)

    unique_id = None
    name = config.get(CONF_NAME)

    await _async_setup_platform_entry(
        config,
        async_add_entities,
        remote,
        unique_id,
        name,
        host,
        hass,
    )


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up a SKY Q entity."""
    remote = hass.data[DOMAIN][config_entry.entry_id][SKYQREMOTE]

    unique_id = config_entry.unique_id
    name = config_entry.data[CONF_NAME]
    host = config_entry.data[CONF_HOST]

    await _async_setup_platform_entry(
        config_entry.options,
        async_add_entities,
        remote,
        unique_id,
        name,
        host,
        hass,
    )


async def _async_setup_platform_entry(
    config_item, async_add_entities, remote, unique_id, name, host, hass
):

    config = Config(unique_id, name, host, config_item)

    player = SkyQDevice(
        hass,
        remote,
        config,
    )

    should_cache = False
    files_path = Path(__file__).parent / "static"
    hass.http.register_static_path(APP_IMAGE_URL_BASE, str(files_path), should_cache)

    async_add_entities([player], False)

    async def _async_homekit_event(_event):
        if player.entity_id != _event.data[ATTR_ENTITY_ID]:
            return

        keyname = _event.data[ATTR_KEY_NAME]
        # _LOGGER.debug(f"D0030 - Homekit event - {player.entity_id} - {keyname}")
        if keyname in REMOTE_BUTTONS:
            await player.async_play_media(REMOTE_BUTTONS[keyname], DOMAIN)
        elif keyname == KEY_REWIND:
            # Lovelace previous_track buttons do rewind
            await player.async_media_previous_track()
        elif keyname == KEY_FAST_FORWARD:
            # Lovelace next_track buttons do fast forward
            await player.async_media_next_track()
        else:
            _LOGGER.warning(
                "W0010 - Invalid Homekit event - %s - %s", player.entity_id, keyname
            )

    hass.bus.async_listen(EVENT_HOMEKIT_TV_REMOTE_KEY_PRESSED, _async_homekit_event)


class SkyQDevice(SkyQEntity, MediaPlayerEntity):
    """Representation of a SkyQ Box."""

    def __init__(
        self,
        hass,
        remote,
        config,
    ):
        """Initialise the SkyQRemote."""
        super().__init__(remote, config)
        if config.volume_entity:
            self._volume_entity = VolumeEntity(
                hass, config.volume_entity, self._config.name
            )
        else:
            self._volume_entity = None
        self._app_image_url = AppImageUrl()
        self._media_browser = MediaBrowser(remote, config, self._app_image_url)
        self._state = STATE_OFF
        self._skyq_type = STATE_OFF
        self._skyq_channelno = None
        self._title = None
        self._channel = None
        self._episode = None
        self._image_url = None
        self._image_remotely_accessible = False
        self._season = None
        self._available = None
        self._error_time = None
        self._startup_setup = True
        self._channel_list = None
        self._use_internal = True
        self._switches_generated = False

        if not self._remote.device_setup:
            self._available = False
            self._startup_setup = False
            _LOGGER.warning("W0020 - Device is not available: %s", self.name)

        self._supported_features = FEATURE_BASE

    @property
    def device_info(self):
        """Entity device information."""
        return self.skyq_device_info

    @property
    def supported_features(self):
        """Get the supported features."""
        if self._config.volume_entity:
            self._supported_features = self._supported_features | SUPPORT_VOLUME_MUTE
            self._supported_features = self._supported_features | SUPPORT_VOLUME_STEP
            if (
                self._volume_entity.supported_features
                and self._volume_entity.supported_features & SUPPORT_VOLUME_SET
            ):
                self._supported_features = self._supported_features | SUPPORT_VOLUME_SET
        if len(self._config.source_list) > 0 and self.state not in (
            STATE_OFF,
            STATE_UNKNOWN,
        ):
            return self._supported_features | SUPPORT_BROWSE_MEDIA

        return self._supported_features

    @property
    def name(self):
        """Get the name of the devices."""
        return self._config.name

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
        if not self.source or self.source in self._config.source_list:
            return self._config.source_list
        sources = self._config.source_list.copy()
        sources.insert(0, self.source)
        return sources

    @property
    def source(self):
        """Title of current playing media."""
        if self._skyq_type == SKYQ_PVR:
            return SKYQ_PVR.upper()

        return self._channel if self._channel is not None else None

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return (
            self._image_url if self._config.enabled_features & FEATURE_IMAGE else None
        )

    @property
    def media_image_remotely_accessible(self):
        """Is the media image available outside home network."""
        return self._image_remotely_accessible

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
        return (
            DEVICE_CLASS_TV
            if self._config.enabled_features & FEATURE_TV_DEVICE_CLASS
            else DEVICE_CLASS_RECEIVER
        )

    @property
    def available(self):
        """Entity availability."""
        return self._available

    @property
    def unique_id(self):
        """Entity unique id."""
        return self._unique_id

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        attributes = {CONST_SKYQ_MEDIA_TYPE: self._skyq_type}
        if self._skyq_channelno:
            attributes[CONST_SKYQ_CHANNELNO] = self._skyq_channelno
        return attributes

    @property
    def volume_level(self):
        """Volume level of entity specified in config."""
        return self._volume_entity.volume_level if self._volume_entity else None

    @property
    def is_volume_muted(self):
        """Boolean if volume is muted."""
        return self._volume_entity.is_volume_muted if self._volume_entity else None

    async def async_update(self):
        """Get the latest data and update device state."""
        self._channel = None
        self._skyq_channelno = None
        self._episode = None
        self._image_url = None
        self._season = None
        self._title = None

        if not self._device_info:
            await self._async_get_mp_device_info()

        if self._device_info:
            await self._async_update_state()

        if self._state not in [STATE_UNKNOWN, STATE_OFF]:
            await self._async_update_current_programme()

        if self._volume_entity:
            await self._volume_entity.async_update_volume_state(self.hass)

        if not self._switches_generated and self.entity_id:
            self._switches_generated = True
            if self._config.enabled_features & FEATURE_SWITCHES:
                SwitchMaker(
                    self.hass.config.config_dir,
                    self.entity_id,
                    self._config.room,
                    self._config.source_list,
                )

    async def async_turn_off(self):
        """Turn SkyQ box off."""
        power_status = await self.hass.async_add_executor_job(self._remote.power_status)
        if power_status == SKY_STATE_ON:
            await self.hass.async_add_executor_job(self._remote.press, "power")
            await self.async_update()

    async def async_turn_on(self):
        """Turn SkyQ box on."""
        power_status = await self.hass.async_add_executor_job(self._remote.power_status)
        if power_status == SKY_STATE_STANDBY:
            await self.hass.async_add_executor_job(
                self._remote.press, ["home", "dismiss"]
            )
            await self.async_update()

    async def async_media_play(self):
        """Play the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "play")
        self._state = STATE_PLAYING
        self.async_write_ha_state()

    async def async_media_pause(self):
        """Pause the current media item."""
        app = await self.hass.async_add_executor_job(
            self._remote.get_active_application
        )
        if app.appId == APP_EPG:
            await self.hass.async_add_executor_job(self._remote.press, "pause")
        else:
            await self.hass.async_add_executor_job(self._remote.press, "play")

        self._state = STATE_PAUSED
        self.async_write_ha_state()

    async def async_media_next_track(self):
        """Fast forward the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "fastforward")
        await self.async_update()

    async def async_media_previous_track(self):
        """Rewind the current media item."""
        await self.hass.async_add_executor_job(self._remote.press, "rewind")
        await self.async_update()

    async def async_select_source(self, source):
        """Select the specified source."""
        if command := get_command(
            self._config.custom_sources, self._channel_list, source
        ):
            await self.hass.async_add_executor_job(self._remote.press, command)
            await self.async_update()

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Perform a media action."""
        if media_type.casefold() == DOMAIN:
            command = media_id.casefold()
            if command not in COMMANDS:
                command = command.split(",")
            await self.hass.async_add_executor_job(self._remote.press, command)
            await self.async_update()
        if media_type.casefold() == DOMAINBROWSER:
            await self.async_select_source(media_id)

    async def async_mute_volume(self, mute):
        """Mute the volume."""
        if self._volume_entity.supported_features & SUPPORT_VOLUME_MUTE:
            await self._volume_entity.async_mute_volume(self.hass, mute)
        else:
            await self.async_set_volume_level(0)

    async def async_set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        await self._volume_entity.async_set_volume_level(self.hass, volume)

    async def async_volume_up(self):
        """Turn volume up for media player."""
        if self._volume_entity.supported_features & SUPPORT_VOLUME_STEP:
            await self._volume_entity.async_volume_up(self.hass)
        elif self.volume_level:
            await self.async_set_volume_level(self.volume_level + 0.02)

    async def async_volume_down(self):
        """Turn volume down for media player."""
        if self._volume_entity.supported_features & SUPPORT_VOLUME_STEP:
            await self._volume_entity.async_volume_down(self.hass)
        elif self.volume_level:
            await self.async_set_volume_level(self.volume_level - 0.02)

    async def async_browse_media(self, media_content_type=None, media_content_id=None):
        """Implement the websocket media browsing helper."""
        return await self._media_browser.async_browse_media(
            self.hass, self._channel_list, media_content_type, media_content_id
        )

    async def _async_update_state(self):
        power_state = await self.hass.async_add_executor_job(self._remote.power_status)
        self._set_power_status(power_state)
        if power_state == SKY_STATE_STANDBY:
            self._skyq_type = STATE_OFF
            self._state = STATE_OFF
            return
        if power_state != SKY_STATE_ON:
            self._skyq_type = STATE_UNKNOWN
            self._state = STATE_OFF
            return

        current_state = await self.hass.async_add_executor_job(
            self._remote.get_current_state
        )

        if current_state == SKY_STATE_PAUSED:
            self._state = STATE_PAUSED
        else:
            self._state = STATE_PLAYING

    async def _async_update_current_programme(self):

        app = await self.hass.async_add_executor_job(
            self._remote.get_active_application
        )
        app_title = app.title

        if app.appId == APP_EPG:
            await self._async_get_current_media()
        else:
            self._skyq_type = SKYQ_APP
            self._title = app_title

        self._image_remotely_accessible = True
        if not self._image_url:
            self._app_image(app_title)

    def _app_image(self, app_title):
        if app_image_url := self._app_image_url.get_app_image_url(app_title):
            self._image_url = app_image_url
            self._image_remotely_accessible = False

    async def _async_get_current_media(self):
        current_media = None
        try:
            current_media = await self.hass.async_add_executor_job(
                self._remote.get_current_media
            )

            if not current_media:
                # Extra warnings can be produced unneccesarily if SkyQ box is powering up/down
                # _LOGGER.warning(f"W0030 - Current Media retrieval failed  - {self._config.host}")
                return None

            if current_media.live and current_media.sid:
                await self._async_get_live_media(current_media)

            elif current_media.pvrid:
                await self._async_get_recording(current_media)

        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.exception(
                "X0010 - Current Media retrieval failed: %s : %s", current_media, err
            )

    async def _async_get_live_media(self, current_media):
        self._channel = current_media.channel
        self._skyq_channelno = current_media.channelno
        self._image_url = current_media.image_url
        self._skyq_type = SKYQ_LIVE
        if not self._config.enabled_features & FEATURE_LIVE_TV:
            return

        current_programme = await self.hass.async_add_executor_job(
            self._remote.get_current_live_tv_programme, current_media.sid
        )
        if not current_programme:
            return

        self._episode = current_programme.episode
        self._season = current_programme.season
        self._title = current_programme.title
        if current_programme.image_url:
            self._image_url = current_programme.image_url

        if not self._config.enabled_features & FEATURE_GET_LIVE_RECORD:
            return

        recordings = await self.hass.async_add_executor_job(
            self._remote.get_recordings, "RECORDING"
        )
        for recording in recordings.programmes:
            if current_programme.programmeuuid == recording.programmeuuid:
                self._skyq_type = SKYQ_LIVEREC

    async def _async_get_recording(self, current_media):
        recording = await self.hass.async_add_executor_job(
            self._remote.get_recording, current_media.pvrid
        )
        self._skyq_type = SKYQ_PVR
        if recording:
            self._channel = recording.channelname
            self._skyq_channelno = None
            self._episode = recording.episode
            self._season = recording.season
            self._title = recording.title
            self._image_url = recording.image_url

    async def _async_get_mp_device_info(self):
        await self.hass.async_add_executor_job(
            self._remote.set_overrides,
            self._config.override_country,
            self._config.test_channel,
        )
        await self._async_get_device_info(self.hass)
        if (
            self._device_info
            and not self._channel_list
            and len(self._config.channel_sources) > 0
        ):
            channel_data = await self.hass.async_add_executor_job(
                self._remote.get_channel_list
            )
            self._channel_list = channel_data.channels

    def _set_power_status(self, power_status):

        if power_status == SKY_STATE_OFF:
            self._power_status_off_handling()
        else:
            self._power_status_on_handling()

    def _power_status_off_handling(self):
        error_time_target = (
            self._error_time + timedelta(seconds=ERROR_TIMEOUT)
            if self._error_time
            else 0
        )
        if not self._error_time or datetime.now() < error_time_target:
            if not self._error_time:
                self._error_time = datetime.now()
            _LOGGER.debug(
                "D0010 - Device is not available - %s Seconds: %s",
                self._error_time_so_far(),
                self.name,
            )
        elif datetime.now() >= error_time_target and self._available:
            self._available = False
            _LOGGER.warning("W0040 - Device is not available: %s", self.name)

    def _power_status_on_handling(self):
        if not self._available:
            self._available = True
            if self._startup_setup:
                _LOGGER.debug("D0040 - Device is now available: %s", self.name)
            else:
                self._startup_setup = True
                _LOGGER.warning("W0050 - Device is now available: %s", self.name)
        elif self._error_time:
            _LOGGER.debug(
                "D0020 - Device is now available - %s Seconds: %s",
                self._error_time_so_far(),
                self.name,
            )
        self._error_time = None

    def _error_time_so_far(self):
        return (datetime.now() - self._error_time).seconds if self._error_time else 0

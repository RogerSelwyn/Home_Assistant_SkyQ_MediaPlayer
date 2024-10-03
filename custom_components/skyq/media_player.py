"""The skyq platform allows you to control a SkyQ set top box."""

import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.const import ATTR_ENTITY_ID, CONF_HOST, CONF_NAME
from homeassistant.exceptions import PlatformNotReady
from pyskyqremote.const import (
    APP_EPG,
    COMMANDS,
    DEFAULT_TRANSPORT_STATE,
    SKY_STATE_OFF,
    SKY_STATE_ON,
    SKY_STATE_PAUSED,
    SKY_STATE_STANDBY,
    SKY_STATE_UNSUPPORTED,
    UNSUPPORTED_DEVICES,
)
from pyskyqremote.skyq_remote import SkyQRemote

from .classes.config import Config
from .classes.mediabrowser import MediaBrowser
from .classes.mpentity import MPEntityAttributes
from .classes.power import SkyQPower
from .classes.switchmaker import SwitchMaker
from .classes.volumeentity import VolumeEntity
from .const import (
    APP_IMAGE_URL_BASE,
    CONF_COUNTRY,
    CONF_EPG_CACHE_LEN,
    CONF_TEST_CHANNEL,
    CONST_DEFAULT_EPGCACHELEN,
    CONST_SKYQ_CHANNELNO,
    CONST_SKYQ_MEDIA_TYPE,
    CONST_SKYQ_TRANSPORT_STATUS,
    DOMAIN,
    DOMAINBROWSER,
    FEATURE_GET_LIVE_RECORD,
    FEATURE_IMAGE,
    FEATURE_LIVE_TV,
    FEATURE_SWITCHES,
    FEATURE_TV_DEVICE_CLASS,
    REMOTE_BUTTONS,
    SKY_STATE_TEMP_ERROR_CHECK,
    SKYQ_APP,
    SKYQ_ICONS,
    SKYQ_LIVE,
    SKYQ_LIVEREC,
    SKYQ_OFF,
    SKYQ_PVR,
    SKYQ_UNKNOWN,
    SKYQREMOTE,
)
from .const_homekit import (
    ATTR_KEY_NAME,
    EVENT_HOMEKIT_TV_REMOTE_KEY_PRESSED,
    KEY_FAST_FORWARD,
    KEY_REWIND,
)
from .entity import SkyQEntity
from .utils import (
    AppImageUrl,
    async_get_channel_data,
    async_get_device_info,
    get_command,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):  # pylint: disable=unused-argument
    """Set up the SkyQ platform."""
    host = config.get(CONF_HOST)
    epg_cache_len = config.get(CONF_EPG_CACHE_LEN, CONST_DEFAULT_EPGCACHELEN)
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)
    if not remote.device_setup:
        raise PlatformNotReady(f"W0010 - Device is not available: {host}")

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
    await hass.async_add_executor_job(
        remote.set_overrides,
        config_item.get(CONF_COUNTRY),
        config_item.get(CONF_TEST_CHANNEL),
    )
    device_info, gateway_device_info, unique_id = await async_get_device_info(
        hass, remote, unique_id
    )
    config = Config(
        unique_id,
        name,
        host,
        device_info,
        config_item,
        gateway_device_info=gateway_device_info,
    )

    player = SkyQDevice(
        hass,
        remote,
        config,
    )

    should_cache = True
    files_path = Path(__file__).parent / "static"
    # hass.http.register_static_path(APP_IMAGE_URL_BASE, str(files_path), should_cache)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                APP_IMAGE_URL_BASE, str(files_path), cache_headers=should_cache
            )
        ]
    )

    async_add_entities([player], False)

    async def _async_homekit_event(_event):
        if player.entity_id != _event.data[ATTR_ENTITY_ID]:
            return

        keyname = _event.data[ATTR_KEY_NAME]
        # _LOGGER.debug(f"D0030 - Homekit event - {player.entity_id} - {keyname}")
        if keyname in REMOTE_BUTTONS:
            await player.async_play_media(DOMAIN, REMOTE_BUTTONS[keyname])
        elif keyname == KEY_REWIND:
            # Lovelace previous_track buttons do rewind
            await player.async_media_previous_track()
        elif keyname == KEY_FAST_FORWARD:
            # Lovelace next_track buttons do fast forward
            await player.async_media_next_track()
        else:
            _LOGGER.warning(
                "W0020 - Invalid Homekit event - %s - %s", player.entity_id, keyname
            )

    hass.bus.async_listen(EVENT_HOMEKIT_TV_REMOTE_KEY_PRESSED, _async_homekit_event)


class SkyQDevice(SkyQEntity, MediaPlayerEntity):
    """Representation of a SkyQ Box."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass,
        remote,
        config,
    ):
        """Initialise the SkyQRemote."""
        super().__init__(hass, remote, config)
        if config.volume_entity:
            self._volume_entity = VolumeEntity(
                hass, config.volume_entity, self._config.name
            )
        else:
            self._volume_entity = None
        self._app_image_url = AppImageUrl()
        self._media_browser = MediaBrowser(remote, config, self._app_image_url)
        self._state = MediaPlayerState.OFF
        self._entity_attr = MPEntityAttributes()
        self._power_state = SkyQPower(hass, self._remote, self._config)
        self._channel_list = None
        self._use_internal = True
        self._switches_generated = False
        self._old_state = None

    @property
    def device_info(self):
        """Entity device information."""
        return self.skyq_device_info

    @property
    def supported_features(self):
        """Get the supported features."""
        if self._config.volume_entity:
            self._entity_attr.add_supported_feature(
                MediaPlayerEntityFeature.VOLUME_MUTE
            )
            self._entity_attr.add_supported_feature(
                MediaPlayerEntityFeature.VOLUME_STEP
            )
            if (
                self._volume_entity.supported_features
                and self._volume_entity.supported_features
                & MediaPlayerEntityFeature.VOLUME_SET
            ):
                self._entity_attr.add_supported_feature(
                    MediaPlayerEntityFeature.VOLUME_SET
                )
        if len(self._config.source_list) > 0 and self.state != MediaPlayerState.OFF:
            return (
                self._entity_attr.supported_features
                | MediaPlayerEntityFeature.BROWSE_MEDIA
            )

        return self._entity_attr.supported_features

    @property
    def name(self):
        """Get the name of the devices."""
        return None

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
        if self._entity_attr.skyq_media_type == SKYQ_PVR:
            return SKYQ_PVR.upper()

        return (
            self._entity_attr.channel if self._entity_attr.channel is not None else None
        )

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return (
            self._entity_attr.image_url
            if self._config.enabled_features & FEATURE_IMAGE
            else None
        )

    @property
    def media_image_remotely_accessible(self):
        """Is the media image available outside home network."""
        return self._entity_attr.image_remotely_accessible

    @property
    def media_channel(self):
        """Channel currently playing."""
        return self._entity_attr.channel

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        if self._entity_attr.skyq_media_type == SKYQ_APP:
            return MediaType.APP

        return MediaType.TVSHOW

    @property
    def media_series_title(self):
        """Get the title of the series of current playing media."""
        return (
            self._entity_attr.title if self._entity_attr.channel is not None else None
        )

    @property
    def media_title(self):
        """Title of current playing media."""
        return (
            self._entity_attr.channel
            if self._entity_attr.channel is not None
            else self._entity_attr.title
        )

    @property
    def media_season(self):
        """Season of current playing media (TV Show only)."""
        return self._entity_attr.season

    @property
    def media_episode(self):
        """Episode of current playing media (TV Show only)."""
        return self._entity_attr.episode

    @property
    def icon(self):
        """Entity icon."""
        return SKYQ_ICONS[self._entity_attr.skyq_media_type]

    @property
    def device_class(self):
        """Entity class."""
        return (
            MediaPlayerDeviceClass.TV
            if self._config.enabled_features & FEATURE_TV_DEVICE_CLASS
            else MediaPlayerDeviceClass.RECEIVER
        )

    @property
    def available(self):
        """Entity availability."""
        return self._power_state.available

    @property
    def unique_id(self):
        """Entity unique id."""
        return self._unique_id

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        attributes = {
            CONST_SKYQ_MEDIA_TYPE: self._entity_attr.skyq_media_type,
            CONST_SKYQ_TRANSPORT_STATUS: self._entity_attr.skyq_transport_status,
        }
        if self._entity_attr.skyq_channelno:
            attributes[CONST_SKYQ_CHANNELNO] = self._entity_attr.skyq_channelno
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
        # _LOGGER.debug("D0010 - Update started - %s", self.name)
        self._entity_attr.reset()

        if not self._config.device_info:
            await self._async_get_device_info(self.hass)

        if not self._channel_list:
            self._channel_list = await self._async_get_channel_list()

        if self._config.device_info:
            error_state = await self._async_update_state()
        if error_state:
            return

        if self._old_state != self._state:
            _LOGGER.debug("D0010 - State changed to '%s' - %s", self._state, self.name)
            self._old_state = self._state

        if self._state != MediaPlayerState.OFF:
            await self._async_update_current_programme()

        if self._volume_entity:
            await self._volume_entity.async_update_volume_state(self.hass)

        if not self._switches_generated and self.entity_id:
            self._switches_generated = True
            if self._config.enabled_features & FEATURE_SWITCHES:
                switchmaker = SwitchMaker(
                    self.hass.config.config_dir,
                    self.entity_id,
                    self._config.room,
                    self._config.source_list,
                )
                await self.hass.async_add_executor_job(switchmaker.create_file)

    async def async_turn_off(self):
        """Turn SkyQ box off."""
        power_status = await self.hass.async_add_executor_job(self._remote.power_status)
        if power_status == SKY_STATE_ON:
            await self._press_button("power")
            await self.async_update()

    async def async_turn_on(self):
        """Turn SkyQ box on."""
        power_status = await self.hass.async_add_executor_job(self._remote.power_status)
        if power_status == SKY_STATE_STANDBY:
            await self._press_button(["home", "dismiss"])
            await self.async_update()

    async def async_media_play(self):
        """Play the current media item."""
        await self._press_button("play")
        self._state = MediaPlayerState.PLAYING
        self.async_write_ha_state()

    async def async_media_pause(self):
        """Pause the current media item."""
        app = await self.hass.async_add_executor_job(
            self._remote.get_active_application
        )
        if app.appId == APP_EPG:
            await self._press_button("pause")
        else:
            await self._press_button("play")

        self._state = MediaPlayerState.PAUSED
        self.async_write_ha_state()

    async def async_media_next_track(self):
        """Fast forward the current media item."""
        await self._press_button("fastforward")
        await self.async_update()

    async def async_media_previous_track(self):
        """Rewind the current media item."""
        await self._press_button("rewind")
        await self.async_update()

    async def async_select_source(self, source):
        """Select the specified source."""
        if command := get_command(
            self._config.custom_sources,
            self._channel_list,
            source,
            self._config.enabled_features,
        ):
            await self._press_button(command)
            await self.async_update()

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Perform a media action."""
        if media_type.casefold() == DOMAIN:
            command = media_id.casefold()
            if command not in COMMANDS:
                command = command.split(",")
            await self._press_button(command)
            await self.async_update()
        if media_type.casefold() == DOMAINBROWSER:
            await self.async_select_source(media_id)

    async def async_mute_volume(self, mute):
        """Mute the volume."""
        if (
            self._volume_entity.supported_features
            & MediaPlayerEntityFeature.VOLUME_MUTE
        ):
            await self._volume_entity.async_mute_volume(self.hass, mute)
        else:
            await self.async_set_volume_level(0)

    async def async_set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        await self._volume_entity.async_set_volume_level(self.hass, volume)

    async def async_volume_up(self):
        """Turn volume up for media player."""
        if (
            self._volume_entity.supported_features
            & MediaPlayerEntityFeature.VOLUME_STEP
        ):
            await self._volume_entity.async_volume_up(self.hass)
        elif self.volume_level:
            await self.async_set_volume_level(self.volume_level + 0.02)

    async def async_volume_down(self):
        """Turn volume down for media player."""
        if (
            self._volume_entity.supported_features
            & MediaPlayerEntityFeature.VOLUME_STEP
        ):
            await self._volume_entity.async_volume_down(self.hass)
        elif self.volume_level:
            await self.async_set_volume_level(self.volume_level - 0.02)

    async def async_browse_media(self, media_content_type=None, media_content_id=None):
        """Implement the websocket media browsing helper."""
        return await self._media_browser.async_browse_media(
            self.hass, self._channel_list, media_content_type, media_content_id
        )

    async def _press_button(self, command):
        if self._remote.device_type in UNSUPPORTED_DEVICES:
            _LOGGER.warning(
                "W0050 - Button press - %s - is not supported for %s",
                command,
                self.name,
            )
            return

        await self.hass.async_add_executor_job(self._remote.press, command)

    async def _async_update_state(self):
        power_state = await self._power_state.async_get_power_status()
        if power_state == SKY_STATE_STANDBY:
            self._entity_attr.skyq_media_type = SKYQ_OFF
            self._state = MediaPlayerState.OFF
            self._entity_attr.skyq_transport_status = DEFAULT_TRANSPORT_STATE
            return False
        if power_state == SKY_STATE_TEMP_ERROR_CHECK:
            return True
        if power_state != SKY_STATE_ON:
            self._entity_attr.skyq_media_type = SKYQ_UNKNOWN
            self._state = MediaPlayerState.OFF
            self._entity_attr.skyq_transport_status = None
            return False

        response = await self.hass.async_add_executor_job(
            self._remote.get_current_state
        )
        current_state = response.state
        self._entity_attr.skyq_transport_status = response.CurrentTransportStatus

        if current_state == SKY_STATE_PAUSED:
            self._state = MediaPlayerState.PAUSED
        elif current_state == SKY_STATE_UNSUPPORTED:
            self._state = SKY_STATE_UNSUPPORTED
        elif current_state == SKY_STATE_OFF:
            self._state = MediaPlayerState.OFF
        else:
            self._state = MediaPlayerState.PLAYING

        return False

    async def _async_update_current_programme(self):
        app = await self.hass.async_add_executor_job(
            self._remote.get_active_application
        )
        app_title = app.title

        if app.appId == APP_EPG:
            if self._remote.device_type not in UNSUPPORTED_DEVICES:
                await self._async_get_current_media()
            else:
                self._entity_attr.skyq_media_type = SKYQ_LIVE
                self._entity_attr.title = SKY_STATE_UNSUPPORTED.capitalize()
        else:
            self._entity_attr.skyq_media_type = SKYQ_APP
            self._entity_attr.title = app_title

        self._entity_attr.image_remotely_accessible = True
        if not self._entity_attr.image_url:
            self._app_image(app_title)

    def _app_image(self, app_title):
        if app_image_url := self._app_image_url.get_app_image_url(app_title):
            self._entity_attr.image_url = app_image_url
            self._entity_attr.image_remotely_accessible = False

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
        self._entity_attr.store_current_media(current_media)
        self._entity_attr.skyq_media_type = SKYQ_LIVE
        if not self._config.enabled_features & FEATURE_LIVE_TV:
            return

        current_programme = await self.hass.async_add_executor_job(
            self._remote.get_current_live_tv_programme, current_media.sid
        )
        if not current_programme:
            return

        self._entity_attr.store_current_programme(current_programme)
        if not self._config.enabled_features & FEATURE_GET_LIVE_RECORD:
            return

        recordings = await self.hass.async_add_executor_job(
            self._remote.get_recordings, "RECORDING"
        )
        for recording in recordings.recordings:
            if current_programme.programmeuuid == recording.programmeuuid:
                self._entity_attr.skyq_media_typee = SKYQ_LIVEREC

    async def _async_get_recording(self, current_media):
        recording = await self.hass.async_add_executor_job(
            self._remote.get_recording, current_media.pvrid
        )
        self._entity_attr.skyq_media_type = SKYQ_PVR
        if recording:
            self._entity_attr.store_recording(recording)

    async def _async_get_channel_list(self):
        if (
            self._config.device_info
            and not self._channel_list
            and len(self._config.channel_sources) > 0
        ):
            channel_data = await async_get_channel_data(self.hass, self._remote)
            return channel_data.channels
        return None

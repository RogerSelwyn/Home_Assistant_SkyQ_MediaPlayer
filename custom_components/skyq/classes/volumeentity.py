"""Volume entity class for Sky Q."""

import logging

from homeassistant.components.media_player.const import (
    ATTR_MEDIA_VOLUME_LEVEL,
    ATTR_MEDIA_VOLUME_MUTED,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    SERVICE_VOLUME_DOWN,
    SERVICE_VOLUME_MUTE,
    SERVICE_VOLUME_SET,
    SERVICE_VOLUME_UP,
)
from homeassistant.helpers.service import async_call_from_config

_LOGGER = logging.getLogger(__name__)


class VolumeEntity:
    """Class representing the volume entity."""

    def __init__(self, hass, volume_entity, mpname):
        """Initialise the volume entity class."""
        self._volume_level = None
        self._mpname = mpname
        self._is_volume_muted = None
        self._entity_name = volume_entity
        self._entity_name_error = False
        self._supported_features = None
        self._startup_error = True
        self._startup = True
        if self._entity_name:
            if state_obj := hass.states.get(self._entity_name):
                self._supported_features = state_obj.attributes.get(
                    ATTR_SUPPORTED_FEATURES
                )

    async def async_update_volume_state(self, hass):
        """Get the volume entity state."""
        if not self._entity_name:
            return

        try:
            if state_obj := hass.states.get(self._entity_name):
                self._volume_level = state_obj.attributes.get(ATTR_MEDIA_VOLUME_LEVEL)
                self._is_volume_muted = state_obj.attributes.get(
                    ATTR_MEDIA_VOLUME_MUTED
                )
                self._supported_features = state_obj.attributes.get(
                    ATTR_SUPPORTED_FEATURES
                )
                if self._entity_name_error:
                    _LOGGER.info(
                        "I0010 - Volume entity now exists: %s - %s",
                        self._mpname,
                        self._entity_name,
                    )
                    self._entity_name_error = False
                    self._startup_error = False
                    self._startup = False
                elif self._startup:
                    _LOGGER.debug(
                        "D0010 - Volume entity connected: %s - %s",
                        self._mpname,
                        self._entity_name,
                    )
                    self._startup = False
            elif not self._entity_name_error:
                if not self._startup_error:
                    _LOGGER.warning(
                        "W0010 - Volume entity does not exist: %s - %s",
                        self._mpname,
                        self._entity_name,
                    )
                    self._entity_name_error = True
                else:
                    _LOGGER.debug(
                        "D0020 - Volume entity does not exist: %s - %s",
                        self._mpname,
                        self._entity_name,
                    )
                    self._startup_error = False
            return
        except (TypeError, ValueError):
            return None

    async def async_mute_volume(self, hass, mute):
        """Mute the volume."""
        data = {ATTR_ENTITY_ID: self._entity_name, ATTR_MEDIA_VOLUME_MUTED: mute}
        await self._async_call_service(hass, SERVICE_VOLUME_MUTE, data)
        return

    async def async_set_volume_level(self, hass, volume):
        """Set volume level, range 0..1."""
        data = {ATTR_ENTITY_ID: self._entity_name, ATTR_MEDIA_VOLUME_LEVEL: volume}
        await self._async_call_service(hass, SERVICE_VOLUME_SET, data)
        return

    async def async_volume_up(self, hass):
        """Turn volume up for media player."""
        data = {ATTR_ENTITY_ID: self._entity_name}
        await self._async_call_service(hass, SERVICE_VOLUME_UP, data)

    async def async_volume_down(self, hass):
        """Turn volume down for media player."""
        data = {ATTR_ENTITY_ID: self._entity_name}
        await self._async_call_service(hass, SERVICE_VOLUME_DOWN, data)

    async def _async_call_service(self, hass, service_name, variable_data=None):
        service_data = {
            "action": f"media_player.{service_name}",
            "data": variable_data,
        }

        await async_call_from_config(
            hass,
            service_data,
            blocking=True,
            validate_config=False,
        )
        return

    @property
    def supported_features(self):
        """Provide supported features of the volume entity."""
        return self._supported_features

    @property
    def volume_level(self):
        """Provide volume level of the volume entity."""
        return self._volume_level

    @property
    def is_volume_muted(self):
        """Provide mute status of the volume entity."""
        return self._is_volume_muted

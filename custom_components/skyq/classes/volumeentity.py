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


class Volume_Entity:
    """Class representing the volume entity."""

    def __init__(self, volume_entity):
        """Initialise the volume entity class."""
        self.volume_level = None
        self.is_volume_muted = None
        self.supported_features = None
        self._entity_name = volume_entity
        self._entity_name_error = False

    async def async_update_volume_state(self, hass, mpname):
        """Get the volume entity state."""
        if not self._entity_name:
            return

        try:
            state_obj = hass.states.get(self._entity_name)
            if state_obj:
                self.volume_level = state_obj.attributes.get(ATTR_MEDIA_VOLUME_LEVEL)
                self.is_volume_muted = state_obj.attributes.get(ATTR_MEDIA_VOLUME_MUTED)
                self.supported_features = state_obj.attributes.get(
                    ATTR_SUPPORTED_FEATURES
                )
                if self._entity_name_error:
                    _LOGGER.info(
                        f"I0010V - Volume entity now exists: {mpname} - {self._entity_name}"
                    )
                    self._entity_name_error = False
            else:
                if not self._entity_name_error:
                    _LOGGER.warning(
                        f"W0010V - Volume entity does not exist: {mpname} - {self._entity_name}"
                    )
                    self._entity_name_error = True
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
        service_data = {}
        service_data["service"] = "media_player." + service_name
        service_data["data"] = variable_data
        await async_call_from_config(
            hass,
            service_data,
            blocking=True,
            validate_config=False,
        )
        return

"""Entity representing a Sky Device."""
import os

from homeassistant.const import (
    ATTR_CONFIGURATION_URL,
    ATTR_HW_VERSION,
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_NAME,
    ATTR_SW_VERSION,
)
from homeassistant.helpers import device_registry as dr

from .const import CONST_STATEFILE, DOMAIN
from .utils import async_get_device_info


class SkyQEntity:
    """Representation of a SkyQ Device."""

    def __init__(self, hass, remote, config):
        """Initialise the SkyQEntity."""
        self._hass = hass
        self._remote = remote
        self._config = config
        self._unique_id = config.unique_id
        self._statefile = os.path.join(hass.config.config_dir, CONST_STATEFILE)

    @property
    def skyq_device_info(self):
        """Entity device information."""
        device_info = None
        if self._config.device_info:
            device_info = {
                ATTR_IDENTIFIERS: {(DOMAIN, self._config.device_info.serialNumber)},
                ATTR_NAME: self._config.name,
                ATTR_MANUFACTURER: self._config.device_info.manufacturer,
                ATTR_MODEL: f"{self._config.device_info.hardwareModel} "
                + f"({self._config.device_info.hardwareName})",
                ATTR_HW_VERSION: f"{self._config.device_info.versionNumber}",
                ATTR_SW_VERSION: f"{self._config.device_info.modelNumber}",
                ATTR_CONFIGURATION_URL: f"http://{self._config.host}:9006/as/system/information",
            }
            if self._config.gateway_device_info:
                gateway_identifier = (
                    DOMAIN,
                    self._config.gateway_device_info.serialNumber,
                )
                if gateway_identifier not in device_info[ATTR_IDENTIFIERS]:
                    self._set_via_device(device_info, gateway_identifier)
        return device_info

    def _set_via_device(self, device_info, gateway_identifier):
        """Link to a registered gateway without using deprecated registry APIs."""
        if "via_device_id" not in dr.DeviceInfo.__annotations__:
            # Compatibility with older supported Home Assistant versions.
            device_info["via_device"] = gateway_identifier
            return

        registry = dr.async_get(self._hass)
        gateways = [
            device
            for device in registry.async_get_devices(identifiers={gateway_identifier})
            if (entry := self._hass.config_entries.async_get_entry(device.config_entry_id))
            and entry.domain == DOMAIN
        ]
        # The main box has its own config entry. Do not guess if it is missing
        # or if more than one SkyQ config entry registers the same identifier.
        if len(gateways) == 1:
            device_info["via_device_id"] = gateways[0].id

    async def _async_get_device_info(self, hass):
        """Query the device for device info."""
        (
            self._config.device_info,
            self._config.gateway_device_info,
            self._unique_id,
        ) = await async_get_device_info(hass, self._remote, self._unique_id)

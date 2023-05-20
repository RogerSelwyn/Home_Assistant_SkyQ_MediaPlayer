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
    ATTR_VIA_DEVICE,
)

from .const import CONST_STATEFILE, DOMAIN
from .utils import async_get_device_info


class SkyQEntity:
    """Representation of a SkyQ Device."""

    def __init__(self, hass, remote, config):
        """Initialise the SkyQEntity."""
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
                device_info[ATTR_VIA_DEVICE] = (
                    DOMAIN,
                    self._config.gateway_device_info.serialNumber,
                )
        return device_info

    async def _async_get_device_info(self, hass):
        """Query the device for device info."""
        (
            self._config.device_info,
            self._config.gateway_device_info,
            self._unique_id,
        ) = await async_get_device_info(hass, self._remote, self._unique_id)

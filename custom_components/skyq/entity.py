"""Entity representing a Sky Device."""

from .const import DOMAIN


class SkyQEntity:
    """Representation of a SkyQ Device."""

    def __init__(self, remote, config):
        """Initialise the SkyQEntity."""
        self._remote = remote
        self._config = config
        self._unique_id = config.unique_id

    @property
    def skyq_device_info(self):
        """Entity device information."""
        return (
            {
                "identifiers": {(DOMAIN, self._config.device_info.serialNumber)},
                "name": self._config.name,
                "manufacturer": self._config.device_info.manufacturer,
                "model": f"{self._config.device_info.hardwareModel} "
                + f"({self._config.device_info.hardwareName})",
                "hw_version": f"{self._config.device_info.versionNumber}",
                "sw_version": f"{self._config.device_info.modelNumber}",
                "configuration_url": f"http://{self._config.host}:9006/as/system/information",
            }
            if self._config.device_info
            else None
        )

    async def _async_get_device_info(self, hass):
        """Query the device for device info."""
        self._config.device_info = await hass.async_add_executor_job(
            self._remote.get_device_information
        )
        if self._config.device_info and not self._unique_id:
            self._unique_id = self._config.device_info.used_country_code + "".join(
                e
                for e in self._config.device_info.serialNumber.casefold()
                if e.isalnum()
            )

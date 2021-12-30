"""Entity representing a Sky Device."""

from .const import DOMAIN


class SkyQEntity:
    """Representation of a SkyQ Device."""

    def __init__(self, remote, config):
        """Initialise the SkyQEntity."""
        self._remote = remote
        self._config = config
        self._unique_id = config.unique_id
        self._deviceInfo = None

    @property
    def skyq_device_info(self):
        """Entity device information."""
        return (
            {
                "identifiers": {(DOMAIN, self._deviceInfo.serialNumber)},
                "name": self._config.name,
                "manufacturer": self._deviceInfo.manufacturer,
                "model": self._deviceInfo.hardwareModel,
                "sw_version": f"{self._deviceInfo.ASVersion}:{self._deviceInfo.versionNumber}",
            }
            if self._deviceInfo
            else None
        )

    async def _async_get_device_info(self):
        """Query the device for device info."""
        if self._deviceInfo:
            return
        self._deviceInfo = await self.hass.async_add_executor_job(self._remote.getDeviceInformation)
        if self._deviceInfo:
            if not self._unique_id:
                self._unique_id = self._deviceInfo.epgCountryCode + "".join(
                    e for e in self._deviceInfo.serialNumber.casefold() if e.isalnum()
                )

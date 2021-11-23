"""Entity representing a Sky Device."""

from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class SkyQEntity(Entity):
    """Representation of a SkyQ Device."""

    @property
    def device_info(self):
        """Entity device information."""
        return (
            {
                "identifiers": {(DOMAIN, self._deviceInfo.serialNumber)},
                "name": self.name,
                "manufacturer": self._deviceInfo.manufacturer,
                "model": self._deviceInfo.hardwareModel,
                "sw_version": f"{self._deviceInfo.ASVersion}:{self._deviceInfo.versionNumber}",
            }
            if self._deviceInfo
            else None
        )

"""Entity representation for storage usage."""
import logging
from datetime import timedelta

from custom_components.skyq.entity import SkyQEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, DATA_GIGABYTES, ENTITY_CATEGORY_DIAGNOSTIC

from .classes.config import Config
from .const import (
    CONST_SKYQ_STORAGE_MAX,
    CONST_SKYQ_STORAGE_PERCENT,
    CONST_SKYQ_STORAGE_USED,
    DOMAIN,
    SKYQ_ICONS,
    SKYQREMOTE,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Sonos from a config entry."""
    config = Config(config_entry.unique_id, config_entry.data[CONF_NAME], config_entry.options)
    remote = hass.data[DOMAIN][config_entry.entry_id][SKYQREMOTE]

    usedsensor = SkyQUsedStorage(remote, config)

    async_add_entities([usedsensor], True)


class SkyQUsedStorage(SkyQEntity, SensorEntity):
    """Used Storage Entity for SkyQ Device."""

    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    def __init__(self, remote, config):
        """Initialize the used storage sensor."""
        super().__init__(remote, config)
        self._quotaInfo = None
        self._available = True

    @property
    def device_info(self):
        """Entity device information."""
        return self.skyq_device_info

    @property
    def unit_of_measurement(self):
        """Provide the unit of measurement."""
        return DATA_GIGABYTES

    @property
    def name(self):
        """Get the name of the devices."""
        return f"{self._config.name} Used Storage"

    @property
    def unique_id(self):
        """Get the unique id of the devices."""
        return f"{self._unique_id}_used" if self._unique_id else None

    @property
    def icon(self):
        """Entity icon."""
        return SKYQ_ICONS[CONST_SKYQ_STORAGE_USED]

    @property
    def available(self):
        """Entity availability."""
        return self._available

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return "{:.1f}".format(round(self._quotaInfo.quotaUsed / 1024, 1))

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return {
            CONST_SKYQ_STORAGE_MAX: "{:.1f}".format(round(self._quotaInfo.quotaMax / 1024, 1)),
            CONST_SKYQ_STORAGE_PERCENT: "{:.1f}".format(
                round((self._quotaInfo.quotaUsed / self._quotaInfo.quotaMax) * 100, 1)
            ),
        }

    async def async_update(self):
        """Get the latest data and update device state."""
        await self._async_get_device_info(self.hass)

        resp = await self.hass.async_add_executor_job(self._remote.getQuota)
        if not resp:
            self._powerStatus_off_handling()
            return

        self._powerStatus_on_handling()
        self._quotaInfo = resp

    def _powerStatus_off_handling(self):
        if self._available:
            self._available = False
            _LOGGER.warning(f"W0010S - Device is not available: {self.name}")

    def _powerStatus_on_handling(self):
        if not self._available:
            self._available = True
            _LOGGER.info(f"I0020M - Device is now available: {self.name}")

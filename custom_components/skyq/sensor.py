"""Entity representation for storage usage."""
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    DATA_GIGABYTES,
    ENTITY_CATEGORY_DIAGNOSTIC,
)

from .classes.config import Config
from .const import (
    CONST_SKYQ_STORAGE_MAX,
    CONST_SKYQ_STORAGE_PERCENT,
    CONST_SKYQ_STORAGE_USED,
    DOMAIN,
    SKYQ_ICONS,
    SKYQREMOTE,
)
from .entity import SkyQEntity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Sonos from a config entry."""
    config = Config(
        config_entry.unique_id,
        config_entry.data[CONF_NAME],
        config_entry.data[CONF_HOST],
        config_entry.options,
    )
    remote = hass.data[DOMAIN][config_entry.entry_id][SKYQREMOTE]

    usedsensor = SkyQUsedStorage(remote, config)

    async_add_entities([usedsensor], True)


class SkyQUsedStorage(SkyQEntity, SensorEntity):
    """Used Storage Entity for SkyQ Device."""

    _attr_entity_category = ENTITY_CATEGORY_DIAGNOSTIC

    def __init__(self, remote, config):
        """Initialize the used storage sensor."""
        super().__init__(remote, config)
        self._quota_info = None
        self._available = True

    @property
    def device_info(self):
        """Entity device information."""
        return self.skyq_device_info

    @property
    def unit_of_measurement(self):  # pylint: disable=overridden-final-method
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
        return f"{round(self._quota_info.quota_used / 1024, 1)}"

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        maxs = round(self._quota_info.quota_max / 1024, 1)
        percent = round(
            (self._quota_info.quota_used / self._quota_info.quota_max) * 100, 1
        )
        return {
            CONST_SKYQ_STORAGE_MAX: f"{maxs}",
            CONST_SKYQ_STORAGE_PERCENT: f"{percent}",
        }

    async def async_update(self):
        """Get the latest data and update device state."""
        await self._async_get_device_info(self.hass)

        resp = await self.hass.async_add_executor_job(self._remote.get_quota)
        if not resp:
            self._power_status_off_handling()
            return

        self._power_status_on_handling()
        self._quota_info = resp

    def _power_status_off_handling(self):
        if self._available:
            self._available = False
            _LOGGER.warning("W0010S - Device is not available: %s", self.name)

    def _power_status_on_handling(self):
        if not self._available:
            self._available = True
            _LOGGER.info("I0020M - Device is now available: %s", self.name)

"""Entity representation for storage usage."""

import json
import logging
from datetime import datetime, timedelta, timezone
from operator import attrgetter
from types import SimpleNamespace

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_HOST, CONF_NAME, DATA_GIGABYTES
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util import Throttle

from .classes.config import Config
from .const import (
    CONST_DATE_FORMAT,
    CONST_NONE,
    CONST_SCHEDULED,
    CONST_SCHEDULED_OFF,
    CONST_SKYQ_RECORDING_END,
    CONST_SKYQ_RECORDING_START,
    CONST_SKYQ_RECORDING_TITLE,
    CONST_SKYQ_SCHEDULED,
    CONST_SKYQ_SCHEDULED_END,
    CONST_SKYQ_SCHEDULED_START,
    CONST_SKYQ_SCHEDULED_TITLE,
    CONST_SKYQ_STORAGE_MAX,
    CONST_SKYQ_STORAGE_PERCENT,
    CONST_SKYQ_STORAGE_USED,
    DOMAIN,
    FEATURE_GET_LIVE_RECORD,
    SKYQ_ICONS,
    SKYQREMOTE,
    STORAGE_SENSOR_SCHEDULE,
    STORAGE_SENSOR_STORAGE,
)
from .entity import SkyQEntity
from .utils import read_state, write_state

_LOGGER = logging.getLogger(__name__)

_SCAN_INTERVAL_STORAGE = timedelta(minutes=5)
_SCAN_INTERVAL_SCHEDULE = timedelta(minutes=1)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Sky Q from a config entry."""
    remote = hass.data[DOMAIN][config_entry.entry_id][SKYQREMOTE]
    device_info = await hass.async_add_executor_job(remote.get_device_information)
    config = Config(
        config_entry.unique_id,
        config_entry.data[CONF_NAME],
        config_entry.data[CONF_HOST],
        device_info,
        config_entry.options,
    )

    sensors = [SkyQUsedStorage(hass, remote, config)]
    if config.enabled_features & FEATURE_GET_LIVE_RECORD:
        sensors.append(SkyQSchedule(hass, remote, config))

    async_add_entities(sensors, False)


class SkyQUsedStorage(SkyQEntity, SensorEntity):
    """Used Storage Entity for SkyQ Device."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, hass, remote, config):
        """Initialize the used storage sensor."""
        super().__init__(hass, remote, config)
        self._available = None
        self._config = config
        attributes = read_state(
            self._statefile, STORAGE_SENSOR_STORAGE, self._config.host
        )

        self._quota_info = None
        if attributes:
            self._quota_info = json.loads(
                json.dumps(attributes), object_hook=lambda d: SimpleNamespace(**d)
            )
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

    @Throttle(_SCAN_INTERVAL_STORAGE)
    async def async_update(self):
        """Get the latest data and update device state."""
        resp = await self.hass.async_add_executor_job(self._remote.get_quota)
        if not resp:
            self._power_status_off_handling()
            return

        self._power_status_on_handling()
        self._quota_info = resp
        write_state(
            self._statefile,
            STORAGE_SENSOR_STORAGE,
            self._config.host,
            self._quota_info.__dict__,
        )

    def _power_status_off_handling(self):
        self._utc_now = datetime.now(tz=timezone.utc)
        if self._available:
            self._available = False
            if self._quiet_period():
                _LOGGER.info(
                    "I0020 - Device is not available overnight, ECO/reboot?: %s",
                    self.name,
                )
            else:
                _LOGGER.warning("W0010 - Device is not available: %s", self.name)

    def _power_status_on_handling(self):
        if not self._available:
            self._available = True
            _LOGGER.info("I0010 - Device is now available: %s", self.name)


class SkyQSchedule(SkyQEntity, SensorEntity):
    """Schedule information for SkyQ Device."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, hass, remote, config):
        """Initialize the used storage sensor."""
        super().__init__(hass, remote, config)
        self._available = None
        self._scheduled_programme = None
        self._config = config

        attributes = read_state(
            self._statefile, STORAGE_SENSOR_SCHEDULE, self._config.host
        )
        self._schedule_attributes = None
        if attributes:
            self._schedule_attributes = attributes
            self._available = True

    @property
    def device_info(self):
        """Entity device information."""
        return self.skyq_device_info

    @property
    def name(self):
        """Get the name of the devices."""
        return f"{self._config.name} Schedule"

    @property
    def unique_id(self):
        """Get the unique id of the devices."""
        return f"{self._unique_id}_schedule" if self._unique_id else None

    @property
    def icon(self):
        """Entity icon."""
        return SKYQ_ICONS[CONST_SKYQ_SCHEDULED]

    @property
    def available(self):
        """Entity availability."""
        return self._available

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._scheduled_programme

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._schedule_attributes

    @Throttle(_SCAN_INTERVAL_SCHEDULE)
    async def async_update(self):
        """Get the latest data and update device state."""
        recordings = await self.hass.async_add_executor_job(self._remote.get_recordings)

        if not recordings:
            self._scheduled_programme = CONST_SCHEDULED_OFF
            return
        self._available = True

        self._next_scheduled_programme(recordings)
        self._recordings_data(recordings)

        write_state(
            self._statefile,
            STORAGE_SENSOR_SCHEDULE,
            self._config.host,
            self._schedule_attributes,
        )

    def _next_scheduled_programme(self, recordings):
        recordings_scheduled = _filter_recordings(recordings, "SCHEDULED")
        self._scheduled_programme = CONST_NONE
        if len(recordings_scheduled) > 0:
            self._scheduled_programme = CONST_SCHEDULED

        for recording in recordings_scheduled:
            self._schedule_attributes = {
                CONST_SKYQ_SCHEDULED_START: recording.starttime.strftime(
                    CONST_DATE_FORMAT
                ),
                CONST_SKYQ_SCHEDULED_END: recording.endtime.strftime(CONST_DATE_FORMAT),
                CONST_SKYQ_SCHEDULED_TITLE: recording.title,
            }
            break

    def _recordings_data(self, recordings):
        recordings_recording = _filter_recordings(recordings, "RECORDING")
        if len(recordings_recording) > 0:
            schedule_data = [
                {
                    CONST_SKYQ_RECORDING_START: recording.starttime.strftime(
                        CONST_DATE_FORMAT
                    ),
                    CONST_SKYQ_RECORDING_END: recording.endtime.strftime(
                        CONST_DATE_FORMAT
                    ),
                    CONST_SKYQ_RECORDING_TITLE: recording.title,
                }
                for recording in recordings_recording
            ]

            self._schedule_attributes.update({"recordings": schedule_data})


def _filter_recordings(recordings, status):
    recordings_filtered = {
        recording for recording in recordings.programmes if recording.status == status
    }

    return sorted(recordings_filtered, key=attrgetter("starttime"))

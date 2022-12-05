"""Entity representation for storage usage."""

import json
import logging
from datetime import timedelta
from operator import attrgetter
from types import SimpleNamespace

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    DATA_GIGABYTES,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util import Throttle

from .classes.config import Config
from .const import (
    CONST_BOX_STATE,
    CONST_DATE_FORMAT,
    CONST_SKYQ_RECORDING_END,
    CONST_SKYQ_RECORDING_START,
    CONST_SKYQ_RECORDING_TITLE,
    CONST_SKYQ_RECORDINGS,
    CONST_SKYQ_SCHEDULED,
    CONST_SKYQ_SCHEDULED_END,
    CONST_SKYQ_SCHEDULED_START,
    CONST_SKYQ_SCHEDULED_TITLE,
    CONST_SKYQ_STORAGE_MAX,
    CONST_SKYQ_STORAGE_PERCENT,
    CONST_SKYQ_STORAGE_USED,
    DOMAIN,
    SKYQ_ICONS,
    SKYQREMOTE,
    STATE_NONE,
    STATE_RECORDING,
    STATE_SCHEDULED,
    STORAGE_SENSOR_SCHEDULE,
    STORAGE_SENSOR_STORAGE,
)
from .entity import SkyQEntity
from .utils import read_state, write_state

_LOGGER = logging.getLogger(__name__)

_SCAN_INTERVAL_STORAGE = timedelta(minutes=5)
_SCAN_INTERVAL_SCHEDULE = timedelta(minutes=5)


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
    sensors.append(SkyQSchedule(hass, remote, config))

    async_add_entities(sensors, False)


class SkyQUsedStorage(SkyQEntity, SensorEntity):
    """Used Storage Entity for SkyQ Device."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False
    _attr_native_unit_of_measurement = DATA_GIGABYTES

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
            self._available = False
            return

        self._available = True
        self._quota_info = resp
        write_state(
            self._statefile,
            STORAGE_SENSOR_STORAGE,
            self._config.host,
            self._quota_info.__dict__,
        )


class SkyQSchedule(SkyQEntity, SensorEntity):
    """Schedule information for SkyQ Device."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hass, remote, config):
        """Initialize the used storage sensor."""
        super().__init__(hass, remote, config)
        self._available = None
        self._state = None
        self._config = config
        self._box_state = None
        self._recordings_scheduled = []

        attributes = read_state(
            self._statefile, STORAGE_SENSOR_SCHEDULE, self._config.host
        )
        self._schedule_attributes = None
        if attributes:
            self._schedule_attributes = attributes
            self._available = True
            if CONST_SKYQ_RECORDINGS in attributes:
                self._state = STATE_RECORDING
            elif CONST_SKYQ_SCHEDULED_START in attributes:
                self._state = STATE_SCHEDULED
            else:
                self._state = STATE_NONE

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
        return self._state

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._schedule_attributes

    @Throttle(_SCAN_INTERVAL_SCHEDULE)
    async def async_update(self):
        """Get the latest data and update device state."""
        recordings = await self.hass.async_add_executor_job(self._remote.get_recordings)

        if not recordings:
            self._state = (
                STATE_SCHEDULED if len(self._recordings_scheduled) > 0 else STATE_NONE
            )
            self._box_state = STATE_OFF
            return

        self._available = True
        self._box_state = STATE_ON

        self._schedule_attributes = {CONST_BOX_STATE: self._box_state}
        self._next_scheduled_programme(recordings)
        self._recordings_data(recordings)

        write_state(
            self._statefile,
            STORAGE_SENSOR_SCHEDULE,
            self._config.host,
            self._schedule_attributes,
        )

    def _next_scheduled_programme(self, recordings):
        self._recordings_scheduled = _filter_recordings(recordings, "SCHEDULED")
        self._state = STATE_NONE
        if len(self._recordings_scheduled) > 0:
            self._state = STATE_SCHEDULED

        for recording in self._recordings_scheduled:
            self._schedule_attributes |= {
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
            self._state = STATE_RECORDING
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

            self._schedule_attributes |= {CONST_SKYQ_RECORDINGS: schedule_data}


def _filter_recordings(recordings, status):
    recordings_filtered = {
        recording for recording in recordings.recordings if recording.status == status
    }

    return sorted(recordings_filtered, key=attrgetter("starttime"))

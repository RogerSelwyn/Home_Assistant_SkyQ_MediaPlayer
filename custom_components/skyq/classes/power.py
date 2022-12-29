"""Class to handle the power state of the Sky Q box."""

import logging
from datetime import datetime, timedelta, timezone

import pytz

from pyskyqremote.const import DEVICE_MULTIROOMSTB, SKY_STATE_OFF

from ..const import (
    ECO_WAKEREASON,
    ERROR_TIMEOUT,
    QUIET_END,
    QUIET_START,
    REBOOT_MAIN_TIMEOUT,
    REBOOT_MINI_TIMEOUT,
    SKY_STATE_TEMP_ERROR_CHECK,
)

_LOGGER = logging.getLogger(__name__)


class SkyQPower:  # pylint: disable=too-few-public-methods
    """Sky Q Power class."""

    def __init__(self, hass, remote, config):
        """Intialise the power status."""
        self.available = None
        self._quiet_time_error = False
        self._reboot_check = True
        self._hass = hass
        self._remote = remote
        self._config = config
        self._error_time = None
        self._startup_setup = False
        self._utc_now = None
        self._power_state = None

    async def async_get_power_status(self):
        """Get the power status."""
        power_state = await self._hass.async_add_executor_job(self._remote.power_status)
        self._set_power_status(power_state)
        return self._power_state

    def _set_power_status(self, power_state):
        self._utc_now = datetime.now(tz=timezone.utc)
        if power_state == SKY_STATE_OFF:
            self._power_status_off_handling()
        else:
            self._power_state = power_state
            self._power_status_on_handling()

    def _power_status_off_handling(self):
        if not self._error_time:
            self._error_time = self._utc_now
        error_time_target, reboot_time_target = self._target_times()
        self._error_time_debug(error_time_target)

        if self._utc_now > error_time_target:
            self._power_state = SKY_STATE_OFF
        else:
            self._power_state = SKY_STATE_TEMP_ERROR_CHECK

        if not self._quiet_period():
            self._power_off_standard_hours(error_time_target)
            return

        if self._config.device_info.wakeReason == ECO_WAKEREASON or (
            self._config.gateway_device_info
            and self._config.gateway_device_info.wakeReason == ECO_WAKEREASON
        ):
            self._power_off_eco(error_time_target)
            return

        self._power_off_other(error_time_target, reboot_time_target)

    def _power_off_standard_hours(self, error_time_target):
        if (
            self.available or self._quiet_time_error
        ) and self._utc_now > error_time_target:
            self.available = False
            self._quiet_time_error = False
            self._reboot_check = False
            _LOGGER.warning("W0010 - Device is not available: %s", self._config.name)

    def _power_off_eco(self, error_time_target):
        if (
            error_time_target != 0
            and self._utc_now > error_time_target
            and self.available
        ):
            self._quiet_time_error_log(
                "I0030 - Device is not available. ECO sleep?: %s"
            )

    def _power_off_other(self, error_time_target, reboot_time_target):
        if (
            error_time_target != 0
            and self._utc_now > error_time_target
            and self.available
        ):
            self._quiet_time_error_log(
                "I0040 - Device is not available. Nightly reboot?: %s"
            )
            return

        if (
            reboot_time_target != 0
            and self._utc_now > reboot_time_target
            and self._reboot_check
        ):
            self._reboot_check = False
            _LOGGER.warning("W0020 - Device is not available: %s", self._config.name)
            return

    def _quiet_time_error_log(self, error_message):
        self.available = False
        self._quiet_time_error = True
        _LOGGER.info(error_message, self._config.name)

    def _power_status_on_handling(self):
        self._quiet_time_error = False
        self._reboot_check = True
        if not self.available:
            self.available = True
            if self._startup_setup:
                _LOGGER.info("I0010 - Device is now available: %s", self._config.name)
            else:
                self._startup_setup = True
                _LOGGER.info(
                    "I0020 - Device is now available after startup: %s",
                    self._config.name,
                )
        elif self._error_time:
            _LOGGER.debug(
                "D0020 - Device is now available - %s Seconds: %s",
                self._error_time_so_far(),
                self._config.name,
            )
        self._error_time = None

    def _error_time_so_far(self):
        return (self._utc_now - self._error_time).seconds if self._error_time else 0

    def _skyq_time(self):
        if self._utc_now > datetime.fromtimestamp(
            self._config.device_info.futureTransitionUtc, tz=timezone.utc
        ):
            offset = self._config.device_info.futureLocalTimeOffset
        else:
            offset = self._config.device_info.presentLocalTimeOffset
        return self._utc_now + timedelta(seconds=offset)

    def _quiet_period(self):
        skyq_timenow = self._skyq_time()
        utctz = pytz.timezone("UTC")
        quiet_start = utctz.localize(datetime.combine(skyq_timenow.date(), QUIET_START))
        quiet_end = utctz.localize(datetime.combine(skyq_timenow.date(), QUIET_END))

        return skyq_timenow >= quiet_start and skyq_timenow <= quiet_end

    def _target_times(self):
        error_time_target = (
            self._error_time + timedelta(seconds=ERROR_TIMEOUT)
            if self._error_time
            else 0
        )
        reboot_timeout = (
            REBOOT_MINI_TIMEOUT
            if self._config.device_info.deviceType == DEVICE_MULTIROOMSTB
            else REBOOT_MAIN_TIMEOUT
        )

        reboot_time_target = (
            self._error_time + timedelta(seconds=reboot_timeout)
            if self._error_time
            else 0
        )
        return error_time_target, reboot_time_target

    def _error_time_debug(self, time_target):
        if self._utc_now < time_target:
            _LOGGER.debug(
                "D0010 - Device is not available - %s Seconds: %s",
                self._error_time_so_far(),
                self._config.name,
            )
            return

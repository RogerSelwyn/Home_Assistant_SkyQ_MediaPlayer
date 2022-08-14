"""Class to handle the power state of the Sky Q box."""
import logging
from datetime import datetime, timedelta

from pyskyqremote.const import SKY_STATE_OFF

from ..const import (
    ECO_WAKEREASON,
    ERROR_TIMEOUT,
    QUIET_END,
    QUIET_START,
    REBOOT_TIMEOUT,
    RESET_WAKEREASON,
)

_LOGGER = logging.getLogger(__name__)


class SkyQPower:
    """Sky Q Power class."""

    def __init__(self, hass, remote, config):
        """Intialise the power status."""
        self.available = None
        self.quiet_time = False
        self._hass = hass
        self._remote = remote
        self._config = config
        self._error_time = None
        self._reboot_check = False
        self._startup_setup = False

    async def async_get_power_status(self):
        """Get the power status."""
        power_state = await self._hass.async_add_executor_job(self._remote.power_status)
        self._set_power_status(power_state)
        return power_state

    def _set_power_status(self, power_status):
        if power_status == SKY_STATE_OFF:
            self._power_status_off_handling()
        else:
            self._power_status_on_handling()

    def _power_status_off_handling(self):
        utc_now = datetime.utcnow()
        skyq_timenow = self._skyq_time(utc_now)

        quiet_start = datetime.combine(utc_now.date(), QUIET_START)
        quiet_end = datetime.combine(utc_now.date(), QUIET_END)
        error_time_target = (
            self._error_time + timedelta(seconds=ERROR_TIMEOUT)
            if self._error_time
            else 0
        )
        reboot_time_target = (
            self._error_time + timedelta(seconds=REBOOT_TIMEOUT)
            if self._error_time
            else 0
        )
        if not self._error_time or utc_now < error_time_target:
            if not self._error_time:
                self._error_time = utc_now
            _LOGGER.debug(
                "D0010 - Device is not available - %s Seconds: %s",
                self._error_time_so_far(),
                self._config.name,
            )
        elif utc_now >= error_time_target:
            quiet_time_end = False
            reboot_time_end = False
            if not self.available and self.quiet_time and skyq_timenow > quiet_end:
                quiet_time_end = True
            if (
                not self.available
                and self.quiet_time
                and utc_now > reboot_time_target
                and self._config.device_info.wakeReason == RESET_WAKEREASON
            ):
                reboot_time_end = True
            if skyq_timenow >= quiet_start and skyq_timenow <= quiet_end:
                self.quiet_time = True
            else:
                self.quiet_time = False
            if (
                self.available
                or quiet_time_end
                or (self._reboot_check and reboot_time_end)
            ):
                self.available = False
                if (
                    self.quiet_time
                    and self._config.device_info.wakeReason == ECO_WAKEREASON
                ):
                    _LOGGER.info(
                        "I0030 - Device is not available. ECO sleep?: %s",
                        self._config.name,
                    )
                elif (
                    self.quiet_time
                    and utc_now < reboot_time_target
                    and not self._reboot_check
                ):
                    self._reboot_check = True
                    _LOGGER.info(
                        "I0040 - Device is not available. Nightly reboot?: %s",
                        self._config.name,
                    )
                else:
                    self._reboot_check = False
                    _LOGGER.warning(
                        "W0010 - Device is not available: %s", self._config.name
                    )

    def _power_status_on_handling(self):
        self._reboot_check = False
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
        return (datetime.now() - self._error_time).seconds if self._error_time else 0

    def _skyq_time(self, utc_now):
        if utc_now > datetime.fromtimestamp(
            self._config.device_info.futureTransitionUtc
        ):
            offset = self._config.device_info.futureLocalTimeOffset
        else:
            offset = self._config.device_info.presentLocalTimeOffset
        return utc_now + timedelta(seconds=offset)

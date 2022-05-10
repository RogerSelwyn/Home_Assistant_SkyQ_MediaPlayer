"""Class to handle the power state of the Sky Q box."""
import logging
from datetime import datetime, timedelta

from pyskyqremote.const import SKY_STATE_OFF

from ..const import ERROR_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class SkyQPower:
    """Sky Q Power class."""

    def __init__(self, hass, remote, config):
        """Intialise the power status."""
        self.available = None
        self._hass = hass
        self._remote = remote
        self._name = config.name
        self._error_time = None
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
        error_time_target = (
            self._error_time + timedelta(seconds=ERROR_TIMEOUT)
            if self._error_time
            else 0
        )
        if not self._error_time or datetime.now() < error_time_target:
            if not self._error_time:
                self._error_time = datetime.now()
            _LOGGER.debug(
                "D0010 - Device is not available - %s Seconds: %s",
                self._error_time_so_far(),
                self._name,
            )
        elif datetime.now() >= error_time_target and self.available:
            self.available = False
            _LOGGER.warning("W0010 - Device is not available: %s", self._name)

    def _power_status_on_handling(self):
        if not self.available:
            self.available = True
            if self._startup_setup:
                _LOGGER.info("I0010 - Device is now available: %s", self._name)
            else:
                self._startup_setup = True
                _LOGGER.info(
                    "I0020 - Device is now available after startup: %s", self._name
                )
        elif self._error_time:
            _LOGGER.debug(
                "D0020 - Device is now available - %s Seconds: %s",
                self._error_time_so_far(),
                self._name,
            )
        self._error_time = None

    def _error_time_so_far(self):
        return (datetime.now() - self._error_time).seconds if self._error_time else 0

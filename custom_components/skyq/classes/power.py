"""Class to handle the power state of the Sky Q box."""
import logging
from datetime import datetime, timedelta

from pyskyqremote.const import SKY_STATE_OFF

from ..const import ERROR_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class SkyQPower:
    """Sky Q Power class."""

    def __init__(self, name):
        """Intialise the power status."""
        self.available = None
        self.name = name
        self._error_time = None
        self._startup_setup = False

    def set_power_status(self, power_status):
        """Manage the power status."""
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
                self.name,
            )
        elif datetime.now() >= error_time_target and self.available:
            self.available = False
            _LOGGER.warning("W0010 - Device is not available: %s", self.name)

    def _power_status_on_handling(self):
        if not self.available:
            self.available = True
            if self._startup_setup:
                _LOGGER.info("I0010 - Device is now available: %s", self.name)
            else:
                self._startup_setup = True
                _LOGGER.info(
                    "I0020 - Device is now available after startup: %s", self.name
                )
        elif self._error_time:
            _LOGGER.debug(
                "D0020 - Device is now available - %s Seconds: %s",
                self._error_time_so_far(),
                self.name,
            )
        self._error_time = None

    def _error_time_so_far(self):
        return (datetime.now() - self._error_time).seconds if self._error_time else 0

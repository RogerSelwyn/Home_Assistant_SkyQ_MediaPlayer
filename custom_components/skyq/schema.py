"""Schema for Sk Q Integration."""

import voluptuous as vol
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
)
from homeassistant.components.media_player import PLATFORM_SCHEMA

from .const import (
    CONF_SOURCES,
    CONF_ROOM,
    CONF_DIR,
    CONF_GEN_SWITCH,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_LIVE_TV,
    CONF_COUNTRY,
    CONF_TEST_CHANNEL,
    CONST_DEFAULT_ROOM,
)

SCAN_INTERVAL = timedelta(seconds=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_SOURCES, default={}): {cv.string: cv.string},
        vol.Optional(CONF_ROOM, default=CONST_DEFAULT_ROOM): cv.string,
        vol.Optional(CONF_DIR): cv.string,
        vol.Optional(CONF_GEN_SWITCH, default=False): cv.boolean,
        vol.Optional(CONF_OUTPUT_PROGRAMME_IMAGE, default=True): cv.boolean,
        vol.Optional(CONF_LIVE_TV, default=True): cv.boolean,
        vol.Optional(CONF_COUNTRY): cv.string,
        vol.Optional(CONF_TEST_CHANNEL): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,
    }
)

DATA_SCHEMA = {
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_NAME, default="Sky Q"): str,
}

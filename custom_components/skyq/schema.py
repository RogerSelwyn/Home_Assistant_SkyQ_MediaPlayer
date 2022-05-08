"""Schema for Sky Q Integration."""

from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.media_player import PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL

from .const import (CONF_ADVANCED_OPTIONS, CONF_COUNTRY, CONF_EPG_CACHE_LEN,
                    CONF_GEN_SWITCH, CONF_GET_LIVE_RECORD, CONF_LIVE_TV,
                    CONF_OUTPUT_PROGRAMME_IMAGE, CONF_ROOM, CONF_SOURCES,
                    CONF_TEST_CHANNEL, CONF_TV_DEVICE_CLASS,
                    CONF_VOLUME_ENTITY, CONST_DEFAULT_EPGCACHELEN,
                    CONST_DEFAULT_ROOM)

SCAN_INTERVAL = timedelta(seconds=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ROOM, default=CONST_DEFAULT_ROOM): cv.string,
        vol.Optional(CONF_GEN_SWITCH, default=False): cv.boolean,
        vol.Optional(CONF_OUTPUT_PROGRAMME_IMAGE, default=True): cv.boolean,
        vol.Optional(CONF_LIVE_TV, default=True): cv.boolean,
        vol.Optional(CONF_GET_LIVE_RECORD, default=False): cv.boolean,
        vol.Optional(CONF_TEST_CHANNEL): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_VOLUME_ENTITY): cv.string,
        vol.Optional(CONF_ADVANCED_OPTIONS, default=False): cv.boolean,

        vol.Optional(CONF_TV_DEVICE_CLASS, default=True): cv.boolean,
        vol.Optional(CONF_COUNTRY): cv.string,
        vol.Optional(
            CONF_EPG_CACHE_LEN, default=CONST_DEFAULT_EPGCACHELEN
        ): cv.positive_int,
        vol.Optional(CONF_SOURCES, default={}): {cv.string: cv.string},
    }
)

DATA_SCHEMA = {
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_NAME, default="Sky Q"): str,
}

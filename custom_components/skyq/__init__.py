"""Initialise."""
import asyncio
import logging

from homeassistant.const import CONF_HOST
from homeassistant.exceptions import ConfigEntryNotReady
from pyskyqremote.skyq_remote import SkyQRemote

from .const import (
    CONF_EPG_CACHE_LEN,
    CONST_DEFAULT_EPGCACHELEN,
    DOMAIN,
    SKYQREMOTE,
    UNDO_UPDATE_LISTENER,
)

_LOGGER = logging.getLogger(__name__)

ENTITY_SENSOR = "sensor"
ENTITY_MEDIA_PLAYER = "media_player"
PLATFORMS = [ENTITY_MEDIA_PLAYER, ENTITY_SENSOR]


async def async_setup(hass, config):  # pylint: disable=unused-argument
    """Set up the integration."""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up a config entry."""

    host = config_entry.data[CONF_HOST]
    _LOGGER.debug("Startup - host: %s", host)
    epg_cache_len = CONST_DEFAULT_EPGCACHELEN
    if CONF_EPG_CACHE_LEN in config_entry.options:
        epg_cache_len = config_entry.options[CONF_EPG_CACHE_LEN]

    undo_listener = config_entry.add_update_listener(update_listener)

    hass.data.setdefault(DOMAIN, {})
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)
    if not remote.device_setup:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = {
        SKYQREMOTE: remote,
        UNDO_UPDATE_LISTENER: undo_listener,
    }

    for component in PLATFORMS:
        if remote.gateway or component == ENTITY_MEDIA_PLAYER:
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, component)
            )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    host = config_entry.data[CONF_HOST]
    epg_cache_len = CONST_DEFAULT_EPGCACHELEN
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)
    process_platforms = [
        component
        for component in PLATFORMS
        if remote.gateway or component == ENTITY_MEDIA_PLAYER
    ]

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, component)
                for component in process_platforms
            ]
        )
    )

    hass.data[DOMAIN][config_entry.entry_id][UNDO_UPDATE_LISTENER]()

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass, config_entry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

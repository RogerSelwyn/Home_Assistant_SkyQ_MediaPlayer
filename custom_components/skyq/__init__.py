"""Initialise."""
import asyncio

from homeassistant.const import CONF_HOST
from homeassistant.exceptions import ConfigEntryNotReady
from pyskyqremote.skyq_remote import SkyQRemote

from .const import CONF_EPG_CACHE_LEN, CONST_DEFAULT_EPGCACHELEN, DOMAIN, SKYQREMOTE, UNDO_UPDATE_LISTENER

entity_sensor = "sensor"
entity_media_player = "media_player"
PLATFORMS = [entity_media_player, entity_sensor]


async def async_setup(hass, config):
    """Set up the integration."""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up a config entry."""
    host = config_entry.data[CONF_HOST]
    epg_cache_len = CONST_DEFAULT_EPGCACHELEN
    if CONF_EPG_CACHE_LEN in config_entry.options:
        epg_cache_len = config_entry.options[CONF_EPG_CACHE_LEN]

    undo_listener = config_entry.add_update_listener(update_listener)

    hass.data.setdefault(DOMAIN, {})
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)
    if not remote.deviceSetup:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = {
        SKYQREMOTE: remote,
        UNDO_UPDATE_LISTENER: undo_listener,
    }

    for component in PLATFORMS:
        if remote.gateway or component == entity_media_player:
            hass.async_create_task(hass.config_entries.async_forward_entry_setup(config_entry, component))

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(config_entry, component) for component in PLATFORMS]
        )
    )

    hass.data[DOMAIN][config_entry.entry_id][UNDO_UPDATE_LISTENER]()

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass, config_entry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

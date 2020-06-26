"""Initialise."""
import asyncio

from pyskyqremote.skyq_remote import SkyQRemote

from homeassistant.const import CONF_HOST

from .const import DOMAIN, SKYQREMOTE, UNDO_UPDATE_LISTENER

PLATFORMS = ["media_player"]


async def async_setup(hass, config):
    """Set up the integration."""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up a config entry."""
    host = config_entry.data[CONF_HOST]

    undo_listener = config_entry.add_update_listener(update_listener)

    hass.data.setdefault(DOMAIN, {})
    remote = await hass.async_add_executor_job(SkyQRemote, host)
    hass.data[DOMAIN][config_entry.entry_id] = {
        SKYQREMOTE: remote,
        UNDO_UPDATE_LISTENER: undo_listener,
    }

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, component)
        )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, component)
                for component in PLATFORMS
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

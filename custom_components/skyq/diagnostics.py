"""Diagnostics support for skyq."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    remote = hass.data[DOMAIN][config_entry.entry_id]["skyqremote"]
    device_info = await hass.async_add_executor_job(remote.get_device_information)
    return {
        'config_entry_data': dict(config_entry.data),
        'config_entry_options': dict(config_entry.options),
        'device_information': vars(device_info),
    }

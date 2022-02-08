"""Diagnostics support for skyq."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    diag: dict[str, Any] = {}

    diag["config_entry_data"] = dict(config_entry.data)
    diag["config_entry_options"] = dict(config_entry.options)

    remote = hass.data[DOMAIN][config_entry.entry_id]["skyqremote"]
    device_info = await hass.async_add_executor_job(remote.getDeviceInformation)
    diag["device_information"] = vars(device_info)

    return diag

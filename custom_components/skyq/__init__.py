"""Initialise."""

import json
import logging
import os

from homeassistant.const import CONF_HOST, CONF_NAME, Platform
from homeassistant.exceptions import ConfigEntryNotReady
from pyskyqremote.const import DEVICE_GATEWAYSTB, UNSUPPORTED_DEVICES
from pyskyqremote.skyq_remote import SkyQRemote

from .const import (
    CONF_ADVANCED_OPTIONS,
    CONF_COUNTRY,
    CONF_EPG_CACHE_LEN,
    CONF_SOURCES,
    CONF_TV_DEVICE_CLASS,
    CONST_DEFAULT_EPGCACHELEN,
    CONST_STATEFILE,
    DOMAIN,
    SKYQREMOTE,
    STORAGE_ENCODING,
    UNDO_UPDATE_LISTENER,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.MEDIA_PLAYER, Platform.SENSOR]


async def async_setup(hass, config):  # pylint: disable=unused-argument
    """Set up the integration."""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up a config entry."""
    _LOGGER.debug(
        "D0010 - Load %s, %s", config_entry.data[CONF_HOST], config_entry.unique_id
    )
    host = config_entry.data[CONF_HOST]
    name = config_entry.data[CONF_NAME]
    epg_cache_len = CONST_DEFAULT_EPGCACHELEN
    if CONF_EPG_CACHE_LEN in config_entry.options:
        epg_cache_len = config_entry.options[CONF_EPG_CACHE_LEN]

    undo_listener = config_entry.add_update_listener(update_listener)

    hass.data.setdefault(DOMAIN, {})
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)
    if not remote.device_setup:
        raise ConfigEntryNotReady(f"W0010 - Device is not available: {host}")

    if remote.device_type in UNSUPPORTED_DEVICES:
        _LOGGER.warning(
            "W0020 - Device type - %s - is not supported - %s",
            remote.device_type,
            name,
        )

    await hass.async_add_executor_job(_check_for_storage_contents, hass)

    hass.data[DOMAIN][config_entry.entry_id] = {
        SKYQREMOTE: remote,
        UNDO_UPDATE_LISTENER: undo_listener,
    }

    for component in PLATFORMS:
        if (
            remote.device_type == DEVICE_GATEWAYSTB
            or component == Platform.MEDIA_PLAYER
        ):
            await hass.config_entries.async_forward_entry_setups(
                config_entry, [component]
            )

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    _LOGGER.debug(
        "D0020 - Unload %s, %s", config_entry.data[CONF_HOST], config_entry.unique_id
    )
    host = config_entry.data[CONF_HOST]
    epg_cache_len = CONST_DEFAULT_EPGCACHELEN
    remote = await hass.async_add_executor_job(SkyQRemote, host, epg_cache_len)
    process_platforms = [
        component
        for component in PLATFORMS
        if remote.device_type == DEVICE_GATEWAYSTB or component == Platform.MEDIA_PLAYER
    ]

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, process_platforms
    )

    hass.data[DOMAIN][config_entry.entry_id][UNDO_UPDATE_LISTENER]()

    if unload_ok:
        _LOGGER.debug(
            "D0030 - Unload OK %s, %s",
            config_entry.data[CONF_HOST],
            config_entry.unique_id,
        )
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass, config_entry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_migrate_entry(hass, config_entry):
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, merge-dict-assign
    """Migrate old entry."""
    _LOGGER.debug(
        "D0040 - Migrating %s from version %s", config_entry.title, config_entry.version
    )

    if config_entry.version == 1:
        new_options = {**config_entry.options}
        if (
            not config_entry.options.get(CONF_TV_DEVICE_CLASS, True)
            or config_entry.options.get(CONF_COUNTRY)
            or config_entry.options.get(CONF_EPG_CACHE_LEN, CONST_DEFAULT_EPGCACHELEN)
            != CONST_DEFAULT_EPGCACHELEN
            or config_entry.options.get(CONF_SOURCES)
        ):
            new_options[CONF_ADVANCED_OPTIONS] = True
        else:
            new_options[CONF_ADVANCED_OPTIONS] = False
        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, options=new_options)

    _LOGGER.info(
        "Migration of %s to version %s successful",
        config_entry.title,
        config_entry.version,
    )

    return True


def _check_for_storage_contents(hass):
    """Check if storage is current standard and not corrupt."""
    statefile = os.path.join(hass.config.config_dir, CONST_STATEFILE)
    if os.path.isfile(statefile):
        try:
            with open(statefile, "r", encoding=STORAGE_ENCODING) as infile:
                file_content = json.load(infile)

            for sensor in file_content:
                if Platform.SENSOR not in sensor:
                    os.remove(statefile)
                    break
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            os.remove(statefile)

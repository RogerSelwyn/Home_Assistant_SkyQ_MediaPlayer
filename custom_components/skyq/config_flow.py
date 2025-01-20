"""Configuration flow for the skyq platform."""

import contextlib
import json
import logging
from operator import attrgetter
from typing import Any
from urllib.parse import urlparse

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow, FlowResult
from homeassistant.helpers.service_info import ssdp
from pyskyqremote.const import KNOWN_COUNTRIES, UNSUPPORTED_DEVICES
from pyskyqremote.skyq_remote import SkyQRemote

from .const import (
    CHANNEL_DISPLAY,
    CHANNEL_SOURCES_DISPLAY,
    CONF_ADD_BACKUP,
    CONF_ADVANCED_OPTIONS,
    CONF_CHANNEL_SOURCES,
    CONF_COUNTRY,
    CONF_EPG_CACHE_LEN,
    CONF_GEN_SWITCH,
    CONF_GET_LIVE_RECORD,
    CONF_LIVE_TV,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_ROOM,
    CONF_SOURCES,
    CONF_TV_DEVICE_CLASS,
    CONF_VOLUME_ENTITY,
    CONST_DEFAULT,
    CONST_DEFAULT_EPGCACHELEN,
    DEFAULT_ENTITY_NAME,
    DEFAULT_MINI,
    DOMAIN,
    LIST_EPGCACHELEN,
    MR_DEVICE,
    SKYQREMOTE,
)
from .schema import DATA_SCHEMA
from .utils import async_get_channel_data, convert_sources_json, host_valid

SORT_CHANNELS = False

_LOGGER = logging.getLogger(__name__)


class SkyqConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initiliase the configuration flow."""

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Sky Q options callback."""
        return SkyQOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input:
            if host_valid(user_input[CONF_HOST]):
                host = user_input[CONF_HOST]
                name = user_input[CONF_NAME]

                try:
                    await self._async_setuniqueid(host)
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(title=name, data=user_input)
            else:
                errors[CONF_HOST] = "invalid_host"

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(DATA_SCHEMA), errors=errors
        )

    async def _async_setuniqueid(self, host):
        self._async_abort_entries_match({CONF_HOST: host})
        remote = await self.hass.async_add_executor_job(SkyQRemote, host)
        if not remote.device_setup:
            raise CannotConnect()

        if remote.device_type in UNSUPPORTED_DEVICES:
            _LOGGER.warning(
                "W0010 - Device type - %s - is not supported", remote.device_type
            )

        device_info = await self.hass.async_add_executor_job(
            remote.get_device_information
        )

        await self.async_set_unique_id(
            device_info.countryCode
            + "".join(e for e in device_info.serialNumber.casefold() if e.isalnum())
        )
        self._abort_if_unique_id_configured()

    async def async_step_ssdp(self, discovery_info: ssdp.SsdpServiceInfo) -> FlowResult:
        """Handle a discovered device."""
        host = str(urlparse(discovery_info.ssdp_location).hostname)
        _LOGGER.debug("D0020 - Discovered device: %s", host)
        try:
            await self._async_setuniqueid(host)
            name = discovery_info.ssdp_server

            context = self.context
            context[CONF_HOST] = host
            context[CONF_NAME] = name
            return await self.async_step_confirm()
        except CannotConnect:
            _LOGGER.warning("W0020 - Failed to connect - Skipping Device: %s", host)

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user-confirmation of discovered node."""
        context = self.context
        errors = {}
        name = context[CONF_NAME]
        host = context[CONF_HOST]
        devicetype = None
        try:
            devicetype = name.split("/")[0]
        finally:
            title = DEFAULT_ENTITY_NAME
            if devicetype == MR_DEVICE:
                title = f"{title} {DEFAULT_MINI}"

        placeholders = {
            CONF_NAME: name,
            CONF_HOST: host,
        }
        context["title_placeholders"] = placeholders
        if user_input is not None:
            try:
                await self._async_setuniqueid(host)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            else:
                user_input = {CONF_HOST: host, CONF_NAME: title}
                return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="confirm",
            description_placeholders=placeholders,
            errors=errors,
        )


class SkyQOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options for Sky Q."""

    def __init__(self, config_entry):
        """Initialize Sky Q options flow."""
        _LOGGER.debug(
            "D0010 - Config options flow initiated for: %s, %s, %s",
            config_entry.title,
            config_entry.data[CONF_HOST],
            config_entry.unique_id,
        )
        self._name = config_entry.title
        self._config_entry = config_entry
        self._remote = None
        self._channel_sources = config_entry.options.get(CONF_CHANNEL_SOURCES, [])
        self._country_list = None
        self._channel_sources_display = []

        self._sources = config_entry.options.get(CONF_SOURCES)
        """If old format sources list, need to convert. Changed in 2.6.10"""
        if isinstance(self._sources, list):
            self._sources = convert_sources_json(sources_list=self._sources)

        self._room = config_entry.options.get(CONF_ROOM)
        self._volume_entity = config_entry.options.get(CONF_VOLUME_ENTITY)
        self._gen_switch = config_entry.options.get(CONF_GEN_SWITCH, False)
        self._live_tv = config_entry.options.get(CONF_LIVE_TV, True)
        self._get_live_record = config_entry.options.get(CONF_GET_LIVE_RECORD, False)
        self._country = config_entry.options.get(CONF_COUNTRY, CONST_DEFAULT)
        self._output_programme_image = config_entry.options.get(
            CONF_OUTPUT_PROGRAMME_IMAGE, True
        )
        self._tv_device_class = config_entry.options.get(CONF_TV_DEVICE_CLASS, True)
        self._epg_cache_len = config_entry.options.get(
            CONF_EPG_CACHE_LEN, CONST_DEFAULT_EPGCACHELEN
        )
        self._add_backup = config_entry.options.get(CONF_ADD_BACKUP, False)
        self._advanced_options = config_entry.options.get(CONF_ADVANCED_OPTIONS, False)
        self._channel_display = []
        self._channel_list = []
        self._user_input = None

    async def async_step_init(
        self,
        user_input=None,  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Set up the option flow."""
        if self._config_entry.entry_id not in self.hass.data[DOMAIN]:
            errmsg = (
                "E0010 - Sky Q box has not been available "
                f"since last Home Assistant restart: {self._config_entry.title}"
            )
            _LOGGER.error(errmsg)
            raise AbortFlow(errmsg)

        self._remote = self.hass.data[DOMAIN][self._config_entry.entry_id][SKYQREMOTE]

        country_alphas = {
            KNOWN_COUNTRIES[country]
            for country in KNOWN_COUNTRIES  # pylint: disable=consider-using-dict-items
        }
        country_names = list(country_alphas)

        self._country_list = [CONST_DEFAULT] + sorted(country_names)

        if self._remote.device_setup:
            channel_data = await async_get_channel_data(self.hass, self._remote)
            if not channel_data:
                errmsg = f"E0020 - Sky Q box is unavailable: {self._config_entry.title}"
                _LOGGER.error(errmsg)
                raise AbortFlow(errmsg)

            self._channel_list = channel_data.channels

            for channel in self._channel_list:
                self._channel_display.append(
                    CHANNEL_DISPLAY.format(channel.channelno, channel.channelname)
                )

            self._channel_sources_display = []
            for channel in self._channel_sources:
                with contextlib.suppress(StopIteration):
                    channel_data = next(
                        c for c in self._channel_list if c.channelname == channel
                    )
                    self._channel_sources_display.append(
                        CHANNEL_DISPLAY.format(
                            channel_data.channelno, channel_data.channelname
                        )
                    )
            return await self.async_step_user()

        return await self.async_step_retry()

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input:
            self._user_input = self._store_user_input(user_input)
            if self._advanced_options:
                return await self.async_step_advanced()

            advanced_input = self._fake_advanced_input()
            user_input = {**self._user_input, **advanced_input}
            return self.async_create_entry(title="", data=user_input)

        schema = self._create_options_schema()
        return self.async_show_form(
            step_id="user",
            description_placeholders={CONF_NAME: self._name},
            data_schema=vol.Schema(schema),
            errors=errors,
        )

    async def async_step_advanced(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input:
            try:
                advanced_input = self._store_advanced_input(user_input)
                user_input = {**self._user_input, **advanced_input}
                return self.async_create_entry(title="", data=user_input)
            except json.decoder.JSONDecodeError:
                errors["base"] = "invalid_sources"
            except InvalidCommand:
                errors["base"] = "invalid_command"

        schema = self._create_advanced_options_schema()
        return self.async_show_form(
            step_id="advanced",
            description_placeholders={CONF_NAME: self._name},
            data_schema=vol.Schema(schema),
            errors=errors,
        )

    def _store_user_input(self, user_input):
        self._channel_sources_display = user_input[CHANNEL_SOURCES_DISPLAY]
        user_input.pop(CHANNEL_SOURCES_DISPLAY)
        if len(self._channel_sources_display) > 0:
            channelitems = []
            for channel in self._channel_sources_display:
                channel_data = next(
                    c
                    for c in self._channel_list
                    if channel == CHANNEL_DISPLAY.format(c.channelno, c.channelname)
                )
                channelitems.append(channel_data)

            channel_sources = []
            if SORT_CHANNELS:
                channelnosorted = sorted(channelitems, key=attrgetter("channelno"))
                channelsorted = sorted(
                    channelnosorted, key=attrgetter("channeltype"), reverse=True
                )
                channel_sources.extend(
                    sorted_channel.channelname for sorted_channel in channelsorted
                )

            else:
                channel_sources.extend(
                    sorted_channel.channelname for sorted_channel in channelitems
                )

            user_input[CONF_CHANNEL_SOURCES] = channel_sources

        self._gen_switch = user_input.get(CONF_GEN_SWITCH)
        self._live_tv = user_input.get(CONF_LIVE_TV)
        self._get_live_record = user_input.get(CONF_GET_LIVE_RECORD)
        self._output_programme_image = user_input.get(CONF_OUTPUT_PROGRAMME_IMAGE)
        self._room = user_input.get(CONF_ROOM)
        self._volume_entity = user_input.get(CONF_VOLUME_ENTITY)
        self._advanced_options = user_input.get(CONF_ADVANCED_OPTIONS)

        return user_input

    def _store_advanced_input(self, user_input):
        self._tv_device_class = user_input.get(CONF_TV_DEVICE_CLASS)
        self._country = user_input.get(CONF_COUNTRY)
        if self._country == CONST_DEFAULT:
            user_input.pop(CONF_COUNTRY)
        else:
            user_input[CONF_COUNTRY] = self._country
        self._epg_cache_len = user_input.get(CONF_EPG_CACHE_LEN)

        self._sources = user_input.get(CONF_SOURCES)
        if self._sources:
            sources_list = convert_sources_json(sources_json=self._sources)
            for source in sources_list:
                _validate_commands(source)
        self._add_backup = user_input.get(CONF_ADD_BACKUP)
        return user_input

    def _fake_advanced_input(self):
        advanced_input = {CONF_TV_DEVICE_CLASS: self._tv_device_class}
        if self._country != CONST_DEFAULT:
            advanced_input[CONF_COUNTRY] = self._country
        advanced_input[CONF_EPG_CACHE_LEN] = self._epg_cache_len
        if self._sources:
            advanced_input[CONF_SOURCES] = self._sources
        advanced_input[CONF_ADD_BACKUP] = self._add_backup
        return advanced_input

    async def async_step_retry(self, user_input=None):  # pylint: disable=unused-argument
        """Handle a failed connection."""
        errors = {"base": "cannot_connect"}

        return self.async_show_form(
            step_id="retry",
            data_schema=vol.Schema({}),
            errors=errors,
        )

    def _create_options_schema(self):
        return {
            vol.Optional(
                CHANNEL_SOURCES_DISPLAY, default=self._channel_sources_display
            ): cv.multi_select(self._channel_display),
            vol.Optional(
                CONF_OUTPUT_PROGRAMME_IMAGE,
                default=self._output_programme_image,
            ): bool,
            vol.Optional(CONF_LIVE_TV, default=self._live_tv): bool,
            vol.Optional(CONF_GET_LIVE_RECORD, default=self._get_live_record): bool,
            vol.Optional(CONF_GEN_SWITCH, default=self._gen_switch): bool,
            vol.Optional(CONF_ROOM, description={"suggested_value": self._room}): str,
            vol.Optional(
                CONF_VOLUME_ENTITY,
                description={"suggested_value": self._volume_entity},
            ): str,
            vol.Optional(CONF_ADVANCED_OPTIONS, default=self._advanced_options): bool,
        }

    def _create_advanced_options_schema(self):
        return {
            vol.Optional(CONF_TV_DEVICE_CLASS, default=self._tv_device_class): bool,
            vol.Optional(CONF_COUNTRY, default=self._country): vol.In(
                self._country_list
            ),
            vol.Optional(CONF_EPG_CACHE_LEN, default=self._epg_cache_len): vol.In(
                LIST_EPGCACHELEN
            ),
            vol.Optional(
                CONF_SOURCES, description={"suggested_value": self._sources}
            ): str,
            vol.Optional(CONF_ADD_BACKUP, default=self._add_backup): bool,
        }


def _validate_commands(source):
    commands = source[1].split(",")
    for command in commands:
        if command not in SkyQRemote.commands:
            raise InvalidCommand()


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidCommand(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

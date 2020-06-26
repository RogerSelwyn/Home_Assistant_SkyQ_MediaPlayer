"""Configuration flow for the skyq platform."""
import ipaddress
import json
import logging
import re
from operator import attrgetter

import pycountry
import voluptuous as vol
from pyskyqremote.const import KNOWN_COUNTRIES
from pyskyqremote.skyq_remote import SkyQRemote

import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import callback

from .const import (
    CHANNEL_DISPLAY,
    CHANNEL_SOURCES_DISPLAY,
    CONF_CHANNEL_SOURCES,
    CONF_COUNTRY,
    CONF_GEN_SWITCH,
    CONF_LIVE_TV,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_ROOM,
    CONF_SOURCES,
    CONST_DEFAULT,
    DOMAIN,
    SKYQREMOTE,
)
from .schema import DATA_SCHEMA
from .utils import convert_sources_JSON

SORT_CHANNELS = False

_LOGGER = logging.getLogger(__name__)


def host_valid(host):
    """Return True if hostname or IP address is valid."""
    try:
        if ipaddress.ip_address(host).version == (4 or 6):
            return True
    except ValueError:
        disallowed = re.compile(r"[^a-zA-Z\d\-]")
        return all(x and not disallowed.search(x) for x in host.split("."))


class SkyqConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    VERSION = 1
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
                    await self._async_setUniqueID(host)
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(title=name, data=user_input)

            errors[CONF_HOST] = "invalid_host"

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(DATA_SCHEMA), errors=errors
        )

    async def _async_setUniqueID(self, host):
        remote = await self.hass.async_add_executor_job(SkyQRemote, host)
        if not remote.deviceSetup:
            raise CannotConnect()
        deviceInfo = await self.hass.async_add_executor_job(remote.getDeviceInformation)
        await self.async_set_unique_id(
            deviceInfo.countryCode
            + "".join(e for e in deviceInfo.serialNumber.casefold() if e.isalnum())
        )
        self._abort_if_unique_id_configured()


class SkyQOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options for Sky Q."""

    def __init__(self, config_entry):
        """Initialize Sky Q options flow."""
        self._name = config_entry.title
        self._config_entry = config_entry
        self._remote = None
        self._channel_sources = config_entry.options.get(CONF_CHANNEL_SOURCES, [])

        self._sources = convert_sources_JSON(
            sources_list=config_entry.options.get(CONF_SOURCES)
        )

        self._room = config_entry.options.get(CONF_ROOM)
        self._gen_switch = config_entry.options.get(CONF_GEN_SWITCH, False)
        self._live_tv = config_entry.options.get(CONF_LIVE_TV, True)
        self._country = config_entry.options.get(CONF_COUNTRY, CONST_DEFAULT)
        if self._country != CONST_DEFAULT:
            self._country = self._convertCountry(alpha_3=self._country)
        self._output_programme_image = config_entry.options.get(
            CONF_OUTPUT_PROGRAMME_IMAGE, True
        )
        self._channelDisplay = []
        self._channel_list = []

    async def async_step_init(self, user_input=None):
        """Set up the option flow."""
        self._remote = self.hass.data[DOMAIN][self._config_entry.entry_id][SKYQREMOTE]

        s = set(KNOWN_COUNTRIES[country] for country in KNOWN_COUNTRIES)
        countryNames = []
        for alpha3 in s:
            countryName = self._convertCountry(alpha_3=alpha3)
            countryNames.append(countryName)

        self._country_list = [CONST_DEFAULT] + sorted(countryNames)

        if self._remote.deviceSetup:
            channelData = await self.hass.async_add_executor_job(
                self._remote.getChannelList
            )
            self._channel_list = channelData.channels

            for channel in self._channel_list:
                self._channelDisplay.append(
                    CHANNEL_DISPLAY.format(channel.channelno, channel.channelname)
                )

            self._channel_sources_display = []
            for channel in self._channel_sources:
                channelData = next(
                    c for c in self._channel_list if c.channelname == channel
                )
                self._channel_sources_display.append(
                    CHANNEL_DISPLAY.format(
                        channelData.channelno, channelData.channelname
                    )
                )

            return await self.async_step_user()

        return await self.async_step_retry()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input:
            self._channel_sources_display = user_input[CHANNEL_SOURCES_DISPLAY]
            user_input.pop(CHANNEL_SOURCES_DISPLAY)
            if len(self._channel_sources_display) > 0:

                channelitems = []
                for channel in self._channel_sources_display:
                    channelData = next(
                        c
                        for c in self._channel_list
                        if channel == CHANNEL_DISPLAY.format(c.channelno, c.channelname)
                    )
                    channelitems.append(channelData)

                if SORT_CHANNELS:
                    channelnosorted = sorted(channelitems, key=attrgetter("channelno"))
                    channelsorted = sorted(
                        channelnosorted, key=attrgetter("channeltype"), reverse=True
                    )
                    channel_sources = []
                    for c in channelsorted:
                        channel_sources.append(c.channelname)
                else:
                    channel_sources = []
                    for c in channelitems:
                        channel_sources.append(c.channelname)

                user_input[CONF_CHANNEL_SOURCES] = channel_sources

            self._gen_switch = user_input.get(CONF_GEN_SWITCH)
            self._live_tv = user_input.get(CONF_LIVE_TV)
            self._output_programme_image = user_input.get(CONF_OUTPUT_PROGRAMME_IMAGE)
            self._room = user_input.get(CONF_ROOM)
            self._country = user_input.get(CONF_COUNTRY)
            if self._country == CONST_DEFAULT:
                user_input.pop(CONF_COUNTRY)
            else:
                user_input[CONF_COUNTRY] = self._convertCountry(name=self._country)

            try:
                self._sources = user_input.get(CONF_SOURCES)
                if self._sources:
                    user_input[CONF_SOURCES] = convert_sources_JSON(
                        sources_json=self._sources
                    )
                    for source in user_input[CONF_SOURCES]:
                        self._validate_commands(source)

                return self.async_create_entry(title="", data=user_input)
            except json.decoder.JSONDecodeError:
                errors["base"] = "invalid_sources"
            except InvalidCommand:
                errors["base"] = "invalid_command"

        return self.async_show_form(
            step_id="user",
            description_placeholders={CONF_NAME: self._name},
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CHANNEL_SOURCES_DISPLAY, default=self._channel_sources_display
                    ): cv.multi_select(self._channelDisplay),
                    vol.Optional(
                        CONF_OUTPUT_PROGRAMME_IMAGE,
                        default=self._output_programme_image,
                    ): bool,
                    vol.Optional(CONF_LIVE_TV, default=self._live_tv): bool,
                    vol.Optional(CONF_GEN_SWITCH, default=self._gen_switch): bool,
                    vol.Optional(
                        CONF_ROOM, description={"suggested_value": self._room}
                    ): str,
                    vol.Optional(CONF_COUNTRY, default=self._country): vol.In(
                        self._country_list
                    ),
                    vol.Optional(
                        CONF_SOURCES, description={"suggested_value": self._sources}
                    ): str,
                }
            ),
            errors=errors,
        )

    async def async_step_retry(self, user_input=None):
        """Handle a failed connection."""
        errors = {}

        errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="retry", data_schema=vol.Schema({}), errors=errors,
        )

    def _convertCountry(self, alpha_3=None, name=None):
        if name:
            return pycountry.countries.get(name=name).alpha_3
        if alpha_3:
            return pycountry.countries.get(alpha_3=alpha_3).name

    def _validate_commands(self, source):
        commands = source[1].split(",")
        for command in commands:
            if command not in SkyQRemote.commands:
                raise InvalidCommand()


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidCommand(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

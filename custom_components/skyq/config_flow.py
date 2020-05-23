"""Configuration flow for the skyq platform."""
import ipaddress
import logging
import re
import json
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
)
from .const import (
    CONF_CHANNEL_SOURCES,
    CONF_ROOM,
    CONF_GEN_SWITCH,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_LIVE_TV,
    CONF_COUNTRY,
    CONF_SOURCES,
    DOMAIN,
    SKYQREMOTE,
)
from pyskyqremote.skyq_remote import SkyQRemote


DATA_SCHEMA = {
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_NAME, default="Sky Q"): str,
}

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
        self._config_entry = config_entry
        self._remote = None
        self._channel_sources = config_entry.options.get(CONF_CHANNEL_SOURCES)
        sources = config_entry.options.get(CONF_SOURCES, {})
        self._sources = None
        if len(sources) > 0:
            self._sources = json.dumps(sources)
        self._room = config_entry.options.get(CONF_ROOM)
        self._gen_switch = config_entry.options.get(CONF_GEN_SWITCH, False)
        self._live_tv = config_entry.options.get(CONF_LIVE_TV, True)
        self._country = config_entry.options.get(CONF_COUNTRY)
        self._output_programme_image = config_entry.options.get(
            CONF_OUTPUT_PROGRAMME_IMAGE, True
        )
        self._channelList = []

    async def async_step_init(self, user_input=None):
        """Set up the option flow."""
        self._remote = self.hass.data[DOMAIN][self._config_entry.entry_id][SKYQREMOTE]

        if self._remote.deviceSetup:
            channelData = await self.hass.async_add_executor_job(
                self._remote.getChannelList
            )

            for channel in channelData.channels:
                self._channelList.append(channel.channelname)

            return await self.async_step_user()
        else:
            return await self.async_step_retry()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input:
            self._channel_sources = user_input[CONF_CHANNEL_SOURCES]
            if CONF_SOURCES in user_input:
                self._sources = user_input[CONF_SOURCES]
            if CONF_ROOM in user_input:
                self._room = user_input[CONF_ROOM]
            self._gen_switch = user_input[CONF_GEN_SWITCH]
            self._live_tv = user_input[CONF_LIVE_TV]
            if CONF_COUNTRY in user_input:
                self._country = user_input[CONF_COUNTRY]
            self._output_programme_image = user_input[CONF_OUTPUT_PROGRAMME_IMAGE]

            try:
                user_input[CONF_SOURCES] = json.loads(self._sources)
                return self.async_create_entry(title="", data=user_input)
            except Exception:
                errors["base"] = "invalid_sources"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_CHANNEL_SOURCES, default=self._channel_sources
                    ): cv.multi_select(self._channelList),
                    vol.Optional(
                        CONF_OUTPUT_PROGRAMME_IMAGE,
                        default=self._output_programme_image,
                    ): bool,
                    vol.Optional(CONF_LIVE_TV, default=self._live_tv): bool,
                    vol.Optional(CONF_GEN_SWITCH, default=self._gen_switch): bool,
                    vol.Optional(
                        CONF_ROOM, description={"suggested_value": self._room}
                    ): str,
                    vol.Optional(
                        CONF_COUNTRY, description={"suggested_value": self._country}
                    ): str,
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


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class AbortFlow(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

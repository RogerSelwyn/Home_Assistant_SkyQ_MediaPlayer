"""Utilities for the skyq platform."""
import asyncio
import collections
import json
import logging

import aiohttp
from homeassistant.const import HTTP_OK
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.network import get_url

from .const import APP_IMAGE_URL_BASE, TIMEOUT

_LOGGER = logging.getLogger(__name__)


def convert_sources_JSON(sources_list=None, sources_json=None):
    """Convert sources to JSON format."""
    if sources_list:
        sources_dict = convert_sources(sources_list=sources_list)

        return json.dumps(sources_dict)

    if sources_json:
        sources_dict = json.loads(sources_json)

        return convert_sources(sources_dict=sources_dict)

    return None


def convert_sources(sources_list=None, sources_dict=None):
    """Convert sources to JSON format."""
    if sources_list:
        sources_dict = collections.OrderedDict()
        for s in sources_list:
            sources_dict[s[0]] = s[1]

        return sources_dict

    if sources_dict:
        sources_list = []
        for k, v in sources_dict.items():
            sources_list.append([k, v])

        return sources_list

    return None


def get_command(custom_sources, channel_list, source):
    """Select the specified source."""
    if source in custom_sources:
        return custom_sources.get(source).split(",")

    try:
        channel = next(c for c in channel_list if c.channelname == source)
        return list(channel.channelno)
    except (TypeError, StopIteration):
        return source


class App_Image_Url:
    """Class to manage the app image url."""

    def __init__(self):
        """Initialise the app image url class."""
        self._appImageUrl = None
        self._use_internal = True
        self._lastAppTitle = None
        self._firstError = True

    async def async_getAppImageUrl(self, hass, appTitle):
        """Check app image is present."""
        if appTitle == self._lastAppTitle:
            return self._appImageUrl

        self._appImageUrl = None

        appImageUrl = APP_IMAGE_URL_BASE.format(appTitle.casefold())

        websession = async_get_clientsession(hass)
        base_url = get_url(hass)
        request_url = base_url + appImageUrl
        certok = False

        if self._use_internal:
            certok = await self._async_check_for_image(
                websession, appTitle, appImageUrl, request_url
            )
        if not self._use_internal or not certok:
            self._use_internal = False
            base_url = get_url(hass, allow_internal=False)
            request_url = base_url + appImageUrl
            certok = await self._async_check_for_image(
                websession, appTitle, request_url, request_url
            )

        return self._appImageUrl

    async def _async_check_for_image(
        self, websession, appTitle, appImageUrl, request_url
    ):
        certok = True
        try:
            response = await websession.head(request_url, timeout=TIMEOUT)
            async with response:
                if response.status == HTTP_OK:
                    self._appImageUrl = appImageUrl

                self._lastAppTitle = appTitle

        except (aiohttp.client_exceptions.ClientConnectorCertificateError) as err:
            _LOGGER.info(
                f"I0040M - Image file check certificate error, routing externally: {request_url} : {err}"
            )
            certok = False
        except (
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.ClientError,
        ) as err:
            # This error when server is starting up and app running
            if self._firstError:
                self._firstError = False
            else:
                _LOGGER.exception(
                    f"X0020M - Image file check failed: {request_url} : {err}"
                )
                self._lastAppTitle = appTitle
        except asyncio.TimeoutError as err:
            _LOGGER.info(f"I0030M - Image file check timed out: {request_url} : {err}")
            self._lastAppTitle = appTitle

        return certok

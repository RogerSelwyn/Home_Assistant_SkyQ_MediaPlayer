"""Utilities for the skyq platform."""

import collections
import ipaddress
import json
import logging
import os
import re
from operator import attrgetter
from time import sleep

from homeassistant.const import Platform
from homeassistant.util import dt as dt_util
from pyskyqremote.skyq_remote import SkyQRemote

from .const import (
    APP_IMAGE_URL_BASE,
    FEATURE_ADD_BACKUP,
    STORAGE_ATTRIBUTES,
    STORAGE_ENCODING,
    STORAGE_HOST,
    STORAGE_HOSTS,
    STORAGE_LAST_UPDATED,
)

CHAR_REPLACE = {" ": "", "+": "plus", "_": "", ".": ""}

_LOGGER = logging.getLogger(__name__)


def convert_sources_json(sources_list=None, sources_json=None):
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
        for source in sources_list:
            sources_dict[source[0]] = source[1]

        return sources_dict

    if sources_dict:
        sources_list = []
        sources_list.extend([k, val] for k, val in sources_dict.items())
        return sources_list

    return None


def get_command(custom_sources, channel_list, source, enabled_features):
    """Select the specified source."""
    if source in custom_sources:
        return custom_sources.get(source).split(",")

    try:
        channel = next(c for c in channel_list if c.channelname == source)
        base_channel = list(channel.channelno)
        if enabled_features & FEATURE_ADD_BACKUP:
            base_channel.insert(0, "backup")
        return base_channel
    except (TypeError, StopIteration):
        return source


class AppImageUrl:
    """Class to manage the app image url."""

    def __init__(self):
        """Initialise the app image url class."""
        self._app_image_url = None
        self._use_internal = True
        self._last_app_title = None
        self._first_error = True

    def get_app_image_url(self, app_title):
        """Check app image is present."""
        if app_title == self._last_app_title:
            return self._app_image_url
        self._last_app_title = app_title

        self._app_image_url = None

        for searcher, replacer in CHAR_REPLACE.items():
            app_title = app_title.replace(searcher, replacer)

        app_image_url = f"{APP_IMAGE_URL_BASE}/{app_title.casefold()}.png"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_path = f"{dir_path}/static/{app_title.casefold()}.png"
        if os.path.isfile(image_path):
            self._app_image_url = app_image_url

        return self._app_image_url


async def async_get_channel_data(hass, remote):
    """Retrieve and process the channel data."""
    channel_data = await hass.async_add_executor_job(remote.get_channel_list)
    for index1, channel1 in enumerate(channel_data.channels):
        for index2, channel2 in enumerate(channel_data.channels):
            if index2 == index1:
                break
            if channel2.channelname == channel1.channelname:
                channel1.channelname = f"{channel1.channelname} ({channel1.channelno})"
                break
    return channel_data


def read_state(statefile, sensor_type, config_host):
    """Read state from storage."""
    if os.path.isfile(statefile):
        with open(statefile, "r", encoding=STORAGE_ENCODING) as infile:
            file_content = json.load(infile)

        for sensor in file_content:
            if sensor[Platform.SENSOR] == sensor_type:
                for host in sensor[STORAGE_HOSTS]:
                    if host[STORAGE_HOST] == config_host:
                        return host[STORAGE_ATTRIBUTES]

    return None


def write_state(statefile, sensor_type, config_host, new_attributes):
    """Write state to storage."""
    _LOGGER.info("Statefile update for: %s - %s", sensor_type, config_host)
    for _ in range(4):
        if _do_statefile_update(statefile, sensor_type, config_host, new_attributes):
            return
        sleep(0.2)
    _LOGGER.warning("Error reading statefile for: %s - %s", sensor_type, config_host)


def _do_statefile_update(statefile, sensor_type, config_host, new_attributes):
    file_content = []
    old_sensor = None

    if os.path.isfile(statefile):
        with open(statefile, "r", encoding=STORAGE_ENCODING) as infile:
            try:
                old_file_content = json.load(infile)
                for sensor in old_file_content:
                    if sensor[Platform.SENSOR] != sensor_type:
                        file_content.append(sensor)
                    else:
                        old_sensor = sensor
            except json.JSONDecodeError:
                return False

    sensor_hosts = []
    if old_sensor:
        sensor_hosts.extend(
            host
            for host in old_sensor[STORAGE_HOSTS]
            if host[STORAGE_HOST] != config_host
        )

    host_content = {
        STORAGE_HOST: config_host,
        STORAGE_ATTRIBUTES: new_attributes,
        STORAGE_LAST_UPDATED: dt_util.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    sensor_hosts.append(host_content)
    sensor_content = {
        Platform.SENSOR: sensor_type,
        STORAGE_HOSTS: sensor_hosts,
    }
    file_content.append(sensor_content)

    with open(statefile, "w", encoding=STORAGE_ENCODING) as outfile:
        json.dump(file_content, outfile, ensure_ascii=False, indent=4)
    return True


async def async_get_device_info(hass, remote, unique_id):
    """Get device information from the box."""
    device_info = await hass.async_add_executor_job(remote.get_device_information)
    gateway_device_info = None
    if device_info:
        if not unique_id:
            unique_id = device_info.used_country_code + "".join(
                e for e in device_info.serialNumber.casefold() if e.isalnum()
            )
        if host_valid(device_info.gatewayIPAddress):
            gatewayremote = await hass.async_add_executor_job(
                SkyQRemote, device_info.gatewayIPAddress
            )
            gateway_device_info = await hass.async_add_executor_job(
                gatewayremote.get_device_information
            )

    return device_info, gateway_device_info, unique_id


def host_valid(host):
    """Return True if hostname or IP address is valid."""
    try:
        return ipaddress.ip_address(host).version == (4 or 6)
    except ValueError:
        disallowed = re.compile(r"[^a-zA-Z\d\-]")
        return all(x and not disallowed.search(x) for x in host.split("."))


def none_aware_attrgetter(attr):
    """Handle sorting with None value."""
    getter = attrgetter(attr)

    def key_func(item):
        value = getter(item)
        return (value is not None, value)

    return key_func

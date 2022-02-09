"""Utilities for the skyq platform."""
import collections
import json
import logging
import os

from .const import APP_IMAGE_URL_BASE

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


def get_command(custom_sources, channel_list, source):
    """Select the specified source."""
    if source in custom_sources:
        return custom_sources.get(source).split(",")

    try:
        channel = next(c for c in channel_list if c.channelname == source)
        return list(channel.channelno)
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

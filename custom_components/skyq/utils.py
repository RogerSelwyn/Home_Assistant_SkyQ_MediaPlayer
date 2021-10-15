"""Utilities for the skyq platform."""
import collections
import json
import logging
import os

from .const import APP_IMAGE_URL_BASE

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

    def getAppImageUrl(self, appTitle):
        """Check app image is present."""
        if appTitle == self._lastAppTitle:
            return self._appImageUrl

        self._appImageUrl = None

        appImageUrl = f"{APP_IMAGE_URL_BASE}/{appTitle.casefold()}.png"
        dirPath = os.path.dirname(os.path.realpath(__file__))
        imagePath = f"{dirPath}/static/{appTitle.casefold()}.png"
        if os.path.isfile(imagePath):
            self._appImageUrl = appImageUrl

        return self._appImageUrl

"""Media Browser class for Sky Q."""
import asyncio
from datetime import datetime

from homeassistant.components.media_player import BrowseMedia
from homeassistant.components.media_player.const import (
    MEDIA_CLASS_DIRECTORY,
    MEDIA_CLASS_TV_SHOW,
)
from homeassistant.components.media_player.errors import BrowseError
from pyskyqremote.classes.programme import Programme

from ..const import DOMAINBROWSER
from ..utils import get_command


class Media_Browser:
    """Class representing the media browser."""

    def __init__(self, remote, config, appImageUrl):
        """Initialise the volume entity class."""
        self._remote = remote
        self._config = config
        self._appImageUrl = appImageUrl

    async def async_browse_media(self, hass, channel_list, media_content_type=None, media_content_id=None):
        """Implement the websocket media browsing helper."""
        if media_content_id not in (None, "root", "channels"):
            raise BrowseError(f"Media not found: {media_content_type} / {media_content_id}")

        channellist = await self._async_prepareChannels(hass, channel_list)
        channels = [
            BrowseMedia(
                title=channel["title"],
                media_class=MEDIA_CLASS_TV_SHOW,
                media_content_id=channel["channelName"],
                media_content_type=DOMAINBROWSER,
                can_play=True,
                can_expand=False,
                thumbnail=channel["thumbnail"],
            )
            for channel in channellist
        ]

        return BrowseMedia(
            title=self._config.name,
            media_content_id="root",
            media_content_type="library",
            media_class=MEDIA_CLASS_DIRECTORY,
            can_play=False,
            can_expand=True,
            children=channels,
        )

    async def _async_prepareChannels(self, hass, channel_list):
        self._channels = []
        channels = await asyncio.gather(
            *[self._async_get_channelInfo(hass, channel_list, source) for source in self._config.source_list]
        )
        return channels

    async def _async_get_channelInfo(self, hass, channel_list, source):
        command = get_command(self._config.custom_sources, channel_list, source)
        if command[0] == "backup":
            command.remove("backup")
        channelno = "".join(command)
        channelInfo = await hass.async_add_executor_job(self._remote.getChannelInfo, channelno)
        if not channelInfo:
            channelInfo = {
                "channelName": source,
                "thumbnail": await self._appImageUrl.async_getAppImageUrl(hass, source),
                "title": source,
            }
        else:
            queryDate = datetime.utcnow()
            programme = await hass.async_add_executor_job(
                self._remote.getProgrammeFromEpg,
                channelInfo.channelsid,
                queryDate,
                queryDate,
            )
            if not isinstance(programme, Programme):
                channelInfo = {
                    "channelName": source,
                    "thumbnail": await self._appImageUrl.async_getAppImageUrl(hass, source),
                    "title": source,
                }
            else:
                imageUrl = programme.imageUrl or channelInfo.channelimageurl
                channelInfo = {
                    "channelName": source,
                    "thumbnail": imageUrl,
                    "title": f"{source} - {programme.title}",
                }

        return channelInfo

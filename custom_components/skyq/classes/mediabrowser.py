"""Media Browser class for Sky Q."""

from homeassistant.components.media_player import BrowseMedia, MediaClass
from homeassistant.components.media_player.errors import BrowseError
from homeassistant.util import dt

from pyskyqremote.classes.programme import Programme

from ..const import DOMAINBROWSER
from ..utils import get_command


class MediaBrowser:
    """Class representing the media browser."""

    def __init__(self, remote, config, app_image_url):
        """Initialise the volume entity class."""
        self._remote = remote
        self._config = config
        self._app_image_url = app_image_url

    async def async_browse_media(
        self, hass, channel_list, media_content_type=None, media_content_id=None
    ):
        """Implement the websocket media browsing helper."""
        if media_content_id not in (None, "root", "channels"):
            raise BrowseError(
                f"Media not found: {media_content_type} / {media_content_id}"
            )

        channellist = await self._async_prepare_channels(hass, channel_list)
        channels = [
            BrowseMedia(
                title=channel["title"],
                media_class=MediaClass.TV_SHOW,
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
            media_class=MediaClass.DIRECTORY,
            can_play=False,
            can_expand=True,
            children=channels,
        )

    async def _async_prepare_channels(self, hass, channel_list):
        channels = []
        for source in self._config.source_list:
            channel = await self._async_get_channel_info(hass, channel_list, source)
            channels.append(channel)

        # channels = await asyncio.gather(
        #     *[
        #         self._async_get_channelInfo(hass, channel_list, source)
        #         for source in self._config.source_list
        #     ]
        # )
        return channels

    async def _async_get_channel_info(self, hass, channel_list, source):
        command = get_command(
            self._config.custom_sources,
            channel_list,
            source,
            self._config.enabled_features,
        )
        if command[0] == "backup":
            command.remove("backup")
        channelno = "".join(command)
        channel_info = await hass.async_add_executor_job(
            self._remote.get_channel_info, channelno
        )
        if not channel_info:
            channel_info = {
                "channelName": source,
                "thumbnail": self._app_image_url.get_app_image_url(source),
                "title": source,
            }
        else:
            query_date = dt.utcnow()
            programme = await hass.async_add_executor_job(
                self._remote.get_programme_from_epg,
                channel_info.channelsid,
                query_date,
                query_date,
            )
            if not isinstance(programme, Programme):
                channel_info = {
                    "channelName": source,
                    "thumbnail": self._app_image_url.get_app_image_url(source),
                    "title": source,
                }
            else:
                image_url = programme.image_url or channel_info.channelimageurl
                channel_info = {
                    "channelName": source,
                    "thumbnail": image_url,
                    "title": f"{source} - {programme.title}",
                }

        return channel_info

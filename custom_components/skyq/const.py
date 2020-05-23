"""Constants for SkyQ."""

from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_STOP,
    SUPPORT_SEEK,
    SUPPORT_PLAY_MEDIA,
)
from homeassistant.const import (
    STATE_OFF,
    STATE_UNKNOWN,
)

DOMAIN = "skyq"
SKYQREMOTE = "skyqremote"
UNDO_UPDATE_LISTENER = "undo_update_listener"

SUPPORT_SKYQ = (
    SUPPORT_TURN_OFF
    | SUPPORT_PAUSE
    | SUPPORT_TURN_ON
    | SUPPORT_PLAY
    | SUPPORT_NEXT_TRACK
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_SELECT_SOURCE
    | SUPPORT_STOP
    | SUPPORT_SEEK
    | SUPPORT_PLAY_MEDIA
)

CONF_SOURCES = "sources"
CONF_CHANNEL_SOURCES = "channel_sources"
CONF_ROOM = "room"
CONF_DIR = "config_directory"
CONF_GEN_SWITCH = "generate_switches_for_channels"
CONF_OUTPUT_PROGRAMME_IMAGE = "output_programme_image"
CONF_LIVE_TV = "live_tv"
CONF_COUNTRY = "country"
CONF_TEST_CHANNEL = "test_channel"

CONST_DEFAULT_ROOM = "Default Room"
CONST_DEPRECATED = "(deprecated)"
CONST_DEFAULT = "(default)"
CONST_TEST = "(test)"
CONST_SKYQ_MEDIA_TYPE = "skyq_media_type"

DEVICE_CLASS = "tv"

FEATURE_BASIC = 1
FEATURE_IMAGE = 2
FEATURE_LIVE_TV = 4
FEATURE_SWITCHES = 8

TIMEOUT = 2

SKYQ_APP = "app"
SKYQ_LIVE = "live"
SKYQ_PVR = "pvr"
SKYQ_ICONS = {
    "app": "mdi:application",
    "live": "mdi:satellite-variant",
    STATE_OFF: "mdi:television",
    "pvr": "mdi:movie-open",
    STATE_UNKNOWN: "mdi:alert-circle-outline",
}
APP_TITLES = {
    "com.bskyb.vevo": "Vevo",
    "com.spotify.spotify.tvv2": "Spotify",
    "com.roku": "Roku",
    "com.bskyb.epgui": "EPG",
}
APP_IMAGE_URL_BASE = "/local/community/skyq/{0}.png"

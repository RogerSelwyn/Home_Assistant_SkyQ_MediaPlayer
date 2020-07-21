"""Constants for SkyQ."""

from homeassistant.const import STATE_OFF, STATE_UNKNOWN

DOMAIN = "skyq"
SKYQREMOTE = "skyqremote"
UNDO_UPDATE_LISTENER = "undo_update_listener"

CONF_SOURCES = "sources"
CONF_CHANNEL_SOURCES = "channel_sources"
CONF_ROOM = "room"
CONF_DIR = "config_directory"
CONF_GEN_SWITCH = "generate_switches_for_channels"
CONF_OUTPUT_PROGRAMME_IMAGE = "output_programme_image"
CONF_LIVE_TV = "live_tv"
CONF_COUNTRY = "country"
CONF_TEST_CHANNEL = "test_channel"
CONF_VOLUME_ENTITY = "volume_entity"
CHANNEL_SOURCES_DISPLAY = "channel_sources_display"
CHANNEL_DISPLAY = "{0} - {1}"

CONST_DEFAULT_ROOM = "Default Room"
CONST_SKYQ_MEDIA_TYPE = "skyq_media_type"
CONST_DEFAULT = "Default"

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

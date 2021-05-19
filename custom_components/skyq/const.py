"""Constants for SkyQ."""

from homeassistant.const import STATE_OFF, STATE_UNKNOWN

DOMAIN = "skyq"
DOMAINBROWSER = "skyq_browser"
SKYQREMOTE = "skyqremote"
UNDO_UPDATE_LISTENER = "undo_update_listener"

CONF_SOURCES = "sources"
CONF_CHANNEL_SOURCES = "channel_sources"
CONF_ROOM = "room"
CONF_EPG_CACHE_LEN = "epg_cache_len"
CONF_GEN_SWITCH = "generate_switches_for_channels"
CONF_OUTPUT_PROGRAMME_IMAGE = "output_programme_image"
CONF_LIVE_TV = "live_tv"
CONF_COUNTRY = "country"
CONF_TEST_CHANNEL = "test_channel"
CONF_VOLUME_ENTITY = "volume_entity"
CONF_GET_LIVE_RECORD = "get_live_record"
CHANNEL_SOURCES_DISPLAY = "channel_sources_display"
CHANNEL_DISPLAY = "{0} - {1}"

CONST_DEFAULT_ROOM = "Default Room"
CONST_ALIAS_FILENAME = "skyqswitchalias.yaml"
CONST_SKYQ_CHANNELNO = "skyq_channelno"
CONST_SKYQ_MEDIA_TYPE = "skyq_media_type"
CONST_DEFAULT = "Default"
CONST_DEFAULT_EPGCACHELEN = 20
LIST_EPGCACHELEN = [10, 20, 30, 50, 999]

DEVICE_CLASS = "receiver"

FEATURE_BASIC = 1
FEATURE_IMAGE = 2
FEATURE_LIVE_TV = 4
FEATURE_SWITCHES = 8
FEATURE_GET_LIVE_RECORD = 16

TIMEOUT = 2
ERROR_TIMEOUT = 10

SKYQ_APP = "app"
SKYQ_LIVE = "live"
SKYQ_LIVEREC = "liverecord"
SKYQ_PVR = "pvr"
SKYQ_ICONS = {
    SKYQ_APP: "mdi:application",
    SKYQ_LIVE: "mdi:satellite-variant",
    SKYQ_LIVEREC: "mdi:record-rec",
    STATE_OFF: "mdi:television",
    SKYQ_PVR: "mdi:movie-open",
    STATE_UNKNOWN: "mdi:alert-circle-outline",
}
APP_TITLES = {
    "com.bskyb.epgui": "EPG",
    "com.bskyb.news": "SkyNews",
    "com.bskyb.vevo": "Vevo",
    "com.roku": "Roku",
    "com.skyita.dazn": "DAZN",
    "com.spotify.spotify.tvv2": "Spotify",
    "fiit.tv": "Fiit",
    "mediasetplay": "MediasetPlay",
    "play.works": "PlayWorks",
    "prime.video": "PrimeVideo",
}
APP_IMAGE_URL_BASE = "/api/" + DOMAIN + "/static"

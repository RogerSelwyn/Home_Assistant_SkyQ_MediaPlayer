"""Constants for SkyQ."""

from datetime import datetime, timedelta

from homeassistant.components.media_player import MediaPlayerEntityFeature

from .const_homekit import (
    KEY_ARROW_DOWN,
    KEY_ARROW_LEFT,
    KEY_ARROW_RIGHT,
    KEY_ARROW_UP,
    KEY_BACK,
    KEY_INFORMATION,
    KEY_NEXT_TRACK,
    KEY_PREVIOUS_TRACK,
    KEY_SELECT,
)

DEFAULT_ENTITY_NAME = "Sky Q"
DEFAULT_MINI = "Mini"
DOMAIN = "skyq"
DOMAINBROWSER = "skyq_browser"
MR_DEVICE = "MR-Device"
SKYQREMOTE = "skyqremote"
UNDO_UPDATE_LISTENER = "undo_update_listener"
SCAN_INTERVAL = timedelta(seconds=10)
SCAN_INTERVAL_STORAGE = timedelta(minutes=5)
SCAN_INTERVAL_SCHEDULE = timedelta(minutes=5)


CONF_ADVANCED_OPTIONS = "advanced_options"
CONF_ADD_BACKUP = "add_backup"
CONF_TV_DEVICE_CLASS = "tv_device_class"
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

CONST_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
CONST_DEFAULT_ROOM = "Default Room"
CONST_ALIAS_FILENAME = "skyqswitchalias.yaml"
CONST_BOX_STATE = "skyq_box_state"
CONST_SKYQ_CHANNELNO = "skyq_channelno"
CONST_SKYQ_MEDIA_TYPE = "skyq_media_type"
CONST_SKYQ_RECORDINGS = "skyq_recordings"
CONST_SKYQ_RECORDING_START = "skyq_recording_start"
CONST_SKYQ_RECORDING_END = "skyq_recording_end"
CONST_SKYQ_RECORDING_TITLE = "skyq_recording_title"
CONST_SKYQ_STORAGE_MAX = "skyq_storage_max"
CONST_SKYQ_STORAGE_PERCENT = "skyq_storage_percent"
CONST_SKYQ_STORAGE_USED = "skyq_storage_used"
CONST_SKYQ_SCHEDULED = "skyq_scheduled"
CONST_SKYQ_SCHEDULED_START = "skyq_scheduled_start"
CONST_SKYQ_SCHEDULED_END = "skyq_scheduled_end"
CONST_SKYQ_SCHEDULED_TITLE = "skyq_scheduled_title"
CONST_SKYQ_TRANSPORT_STATUS = "skyq_transport_status"
CONST_STATEFILE = ".storage/skyq.restore_state"
CONST_DEFAULT = "Default"
CONST_DEFAULT_EPGCACHELEN = 20
LIST_EPGCACHELEN = [10, 20, 30, 50, 999]

FEATURE_BASIC = 1
FEATURE_IMAGE = 2
FEATURE_LIVE_TV = 4
FEATURE_SWITCHES = 8
FEATURE_GET_LIVE_RECORD = 16
FEATURE_TV_DEVICE_CLASS = 32
FEATURE_ADD_BACKUP = 64

FEATURE_BASE = (
    MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.PLAY
    # | MediaPlayerEntityFeature.STOP
    | MediaPlayerEntityFeature.NEXT_TRACK
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.SELECT_SOURCE
    # | MediaPlayerEntityFeature.SEEK
    | MediaPlayerEntityFeature.PLAY_MEDIA
)

TIMEOUT = 2
ERROR_TIMEOUT = 10
REBOOT_MAIN_TIMEOUT = 180
REBOOT_MINI_TIMEOUT = 360
QUIET_START = datetime.strptime("0045", "%H%M").time()
QUIET_END = datetime.strptime("0600", "%H%M").time()
ECO_WAKEREASON = "ECO"

SKYQ_APP = "app"
SKYQ_LIVE = "live"
SKYQ_LIVEREC = "liverecord"
SKYQ_OFF = "off"
SKYQ_PVR = "pvr"
SKYQ_UNKNOWN = "unknown"

APP_IMAGE_URL_BASE = f"/api/{DOMAIN}/static"

BUTTON_PRESS_CHANNELUP = "channelup"
BUTTON_PRESS_CHANNELDOWN = "channeldown"
BUTTON_PRESS_SELECT = "select"
BUTTON_PRESS_DISMISS = "dismiss"
BUTTON_PRESS_I = "i"
BUTTON_PRESS_TVGUIDE = "tvguide"
BUTTON_PRESS_UP = "up"
BUTTON_PRESS_DOWN = "down"
BUTTON_PRESS_LEFT = "left"
BUTTON_PRESS_RIGHT = "right"

REMOTE_BUTTONS = {
    KEY_ARROW_RIGHT: BUTTON_PRESS_RIGHT,
    KEY_ARROW_LEFT: BUTTON_PRESS_LEFT,
    KEY_ARROW_UP: BUTTON_PRESS_UP,
    KEY_ARROW_DOWN: BUTTON_PRESS_DOWN,
    KEY_SELECT: BUTTON_PRESS_SELECT,
    KEY_BACK: BUTTON_PRESS_DISMISS,
    KEY_INFORMATION: BUTTON_PRESS_TVGUIDE,
    KEY_PREVIOUS_TRACK: BUTTON_PRESS_CHANNELDOWN,
    KEY_NEXT_TRACK: BUTTON_PRESS_CHANNELUP,
}

STORAGE_ATTRIBUTES = "attributes"
STORAGE_LAST_UPDATED = "last_updated"
STORAGE_ENCODING = "UTF8"
STORAGE_HOST = "host"
STORAGE_HOSTS = "hosts"
STORAGE_SENSOR_STORAGE = "storage"
STORAGE_SENSOR_SCHEDULE = "schedule"

STATE_NONE = "none"
STATE_RECORDING = "recording"
STATE_SCHEDULED = "scheduled"
SKY_STATE_TEMP_ERROR_CHECK = "error_check"

SKYQ_ICONS = {
    SKYQ_APP: "mdi:application-outline",
    SKYQ_LIVE: "mdi:satellite-variant",
    SKYQ_LIVEREC: "mdi:record-rec",
    SKYQ_OFF: "mdi:television",
    SKYQ_PVR: "mdi:movie-open",
    SKYQ_UNKNOWN: "mdi:alert-circle-outline",
    CONST_SKYQ_STORAGE_USED: "mdi:database",
    STATE_SCHEDULED: "mdi:clock-outline",
    STATE_RECORDING: "mdi:record-rec",
    STATE_NONE: "mdi:clock-remove-outline",
}

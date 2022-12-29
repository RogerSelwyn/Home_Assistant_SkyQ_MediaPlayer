"""Config class definition for the skyq platform."""
from dataclasses import InitVar, dataclass, field

from ..const import (
    CONF_CHANNEL_SOURCES,
    CONF_COUNTRY,
    CONF_GEN_SWITCH,
    CONF_GET_LIVE_RECORD,
    CONF_LIVE_TV,
    CONF_OUTPUT_PROGRAMME_IMAGE,
    CONF_ROOM,
    CONF_SOURCES,
    CONF_TEST_CHANNEL,
    CONF_TV_DEVICE_CLASS,
    CONF_VOLUME_ENTITY,
    CONST_DEFAULT_ROOM,
    FEATURE_BASIC,
    FEATURE_GET_LIVE_RECORD,
    FEATURE_IMAGE,
    FEATURE_LIVE_TV,
    FEATURE_SWITCHES,
    FEATURE_TV_DEVICE_CLASS,
)
from ..utils import convert_sources, convert_sources_json

ENABLED_FEATURES = (
    FEATURE_BASIC
    | FEATURE_IMAGE
    | FEATURE_LIVE_TV
    | FEATURE_SWITCHES
    | FEATURE_GET_LIVE_RECORD
    | FEATURE_TV_DEVICE_CLASS
)


@dataclass
class Config:
    """Sky Q configuration information."""

    unique_id: str = field(init=True, repr=True, compare=True)
    name: str = field(init=True, repr=True, compare=True)
    host: str = field(init=True, repr=True, compare=True)
    device_info: object
    config_item: InitVar[object]
    room: str = None
    volume_entity: str = None
    test_channel: str = None
    override_country: str = None
    enabled_features: int = None
    source_list = None
    gateway_device_info: object = None

    def __post_init__(
        self,
        config_item,
    ):
        """Set up the config with all attributes."""
        self.room = config_item.get(CONF_ROOM, CONST_DEFAULT_ROOM)
        self.volume_entity = config_item.get(CONF_VOLUME_ENTITY, None)
        self.test_channel = config_item.get(CONF_TEST_CHANNEL)
        self.override_country = config_item.get(CONF_COUNTRY)
        self.custom_sources = config_item.get(CONF_SOURCES)
        self.channel_sources = config_item.get(CONF_CHANNEL_SOURCES, [])
        generate_switches_for_channels = config_item.get(CONF_GEN_SWITCH, False)
        output_programme_image = config_item.get(CONF_OUTPUT_PROGRAMME_IMAGE, True)
        tv_device_class = config_item.get(CONF_TV_DEVICE_CLASS, True)
        live_tv = config_item.get(CONF_LIVE_TV, True)
        get_live_record = config_item.get(CONF_GET_LIVE_RECORD, False)

        self.enabled_features = ENABLED_FEATURES
        self.source_list = []

        if not output_programme_image:
            self.enabled_features ^= FEATURE_IMAGE

        if not tv_device_class:
            self.enabled_features ^= FEATURE_TV_DEVICE_CLASS

        if not live_tv:
            self.enabled_features ^= FEATURE_LIVE_TV

        if not get_live_record:
            self.enabled_features ^= FEATURE_GET_LIVE_RECORD

        if not generate_switches_for_channels:
            self.enabled_features ^= FEATURE_SWITCHES

        if isinstance(self.custom_sources, str):
            cs_list = convert_sources_json(sources_json=self.custom_sources)
            self.custom_sources = convert_sources(sources_list=cs_list)
        elif isinstance(
            self.custom_sources, list
        ):  # If old format sources list, need to convert. Changed in 2.6.10
            self.custom_sources = convert_sources(sources_list=self.custom_sources)
        elif not self.custom_sources:
            self.custom_sources = []

        if self.custom_sources and len(self.custom_sources) > 0:
            self.source_list = [*self.custom_sources.keys()]
        self.source_list += self.channel_sources

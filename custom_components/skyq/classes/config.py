"""Config class definition for the skyq platform."""
from dataclasses import InitVar, dataclass, field

from ..const import (
    FEATURE_BASIC,
    FEATURE_GET_LIVE_RECORD,
    FEATURE_IMAGE,
    FEATURE_LIVE_TV,
    FEATURE_SWITCHES,
    FEATURE_TV_DEVICE_CLASS,
)
from ..utils import convert_sources

enabled_features = (
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
    room: str = field(init=True, repr=True, compare=True)
    volume_entity: str = field(init=True, repr=True, compare=True)
    test_channel: str = field(init=True, repr=True, compare=True)
    overrideCountry: str = field(init=True, repr=True, compare=True)
    custom_sources: field(init=True, repr=False, compare=True)
    channel_sources: list = field(init=True, repr=True, compare=True)
    generate_switches_for_channels: InitVar[bool]
    output_programme_image: InitVar[bool]
    otv_device_class: InitVar[bool]
    live_tv: InitVar[bool]
    get_live_record: InitVar[bool]
    enabled_features: int = None
    source_list = None

    def __post_init__(
        self,
        generate_switches_for_channels,
        output_programme_image,
        tv_device_class,
        live_tv,
        get_live_record,
    ):
        """Set up the config."""
        self.enabled_features = enabled_features
        self.source_list = []

        if not (output_programme_image):
            self.enabled_features ^= FEATURE_IMAGE

        if not (tv_device_class):
            self.enabled_features ^= FEATURE_TV_DEVICE_CLASS

        if not (live_tv):
            self.enabled_features ^= FEATURE_LIVE_TV

        if not (get_live_record):
            self.enabled_features ^= FEATURE_GET_LIVE_RECORD

        if not (generate_switches_for_channels):
            self.enabled_features ^= FEATURE_SWITCHES

        if isinstance(self.custom_sources, list):
            self.custom_sources = convert_sources(sources_list=self.custom_sources)
        elif not self.custom_sources:
            self.custom_sources = []

        if self.custom_sources and len(self.custom_sources) > 0:
            self.source_list = [*self.custom_sources.keys()]
        self.source_list += self.channel_sources

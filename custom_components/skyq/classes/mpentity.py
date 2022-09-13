"""Class to hold the core media_player entity attributes."""

from ..const import FEATURE_BASE, SKYQ_OFF


class MPEntityAttributes:
    """Media player entity attribute class."""

    def __init__(self):
        """Media player entity attribute setup."""
        self.channel = None
        self.episode = None
        self.image_url = None
        self.season = None
        self.title = None
        self.skyq_channelno = None
        self.supported_features = FEATURE_BASE

        self._image_remotely_accessible = False

        self.skyq_media_type = SKYQ_OFF
        self.skyq_transport_status = None

    def reset(self):
        """Reset the core attributes."""
        self.channel = None
        self.episode = None
        self.image_url = None
        self.season = None
        self.title = None
        self.skyq_channelno = None

    def store_current_media(self, current_media):
        """Store attributes from current_media."""
        self.channel = current_media.channel
        self.skyq_channelno = current_media.channelno
        self.image_url = current_media.image_url

    def store_recording(self, recording):
        """Store attributes from recording."""
        self.channel = recording.channelname
        self.skyq_channelno = None
        self.episode = recording.episode
        self.season = recording.season
        self.title = recording.title
        self.image_url = recording.image_url

    def store_current_programme(self, current_programme):
        """Store attributes from current_programme."""
        self.episode = current_programme.episode
        self.season = current_programme.season
        self.title = current_programme.title
        if current_programme.image_url:
            self.image_url = current_programme.image_url

    def add_supported_feature(self, feature):
        """Add feature to supported feature enumerator."""
        self.supported_features = self.supported_features | feature

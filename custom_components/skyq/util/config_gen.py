"""
A utility function to generate yaml config for SkyQ media players.

To support easy usage with other home assistant integrations, e.g. google home
"""


class SwitchMaker:
    """The Switchmaker Class."""

    def __init__(self, config_dir, name, room, channels):
        """Initialise the Switcmaker."""
        self._name = name
        self._room = room
        self._root = config_dir

        if self._root[-1] != "/":
            self._root += "/"
        self._f = open(
            self._root + "skyq" + self._room.replace(" ", "") + ".yaml", "w+"
        )
        self._addSwitch("pause", "pause", "media_pause")
        self._addSwitch("play", "play", "media_play")
        self._addSwitch("ff", "fastforward", "media_next_track")
        self._addSwitch("rw", "rewind", "media_previous_track")

        dedup_channels = list(dict.fromkeys(channels))
        for ch in dedup_channels:
            self._addSwitch(ch, ch, "select_source", True)

        self._f.close()

    def _addSwitch(self, switch, friendly_name, service, source=False):
        """Add switch to switches."""
        switch_name = (
            "skyq_"
            + switch.replace(" ", "").lower()
            + self._room.replace(" ", "").lower()
        )
        entity_id = "media_player." + self._name.replace(" ", "_").lower()
        source_name = ""
        if source:
            source_name = "          source: '" + switch + "'\n"

        self._f.write(
            "    "
            + switch_name
            + ":\n"
            + "      value_template: '{{\"off\"}}'\n"
            + "      friendly_name: '"
            + friendly_name
            + " in the "
            + self._room
            + "'\n"
            + "      turn_on:\n"
            + "        service: media_player."
            + service
            + "\n"
            + "        data:\n"
            + "          entity_id: "
            + entity_id
            + "\n"
            + source_name
            + "      turn_off:\n"
            + "        service: script.placeholder\n"
        )

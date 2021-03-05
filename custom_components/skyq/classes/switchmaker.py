"""
A utility function to generate yaml config for SkyQ media players.

To support easy usage with other home assistant integrations, e.g. google home
"""
import os.path as _path

import yaml

from ..const import CONST_ALIAS_FILENAME


class Switch_Maker:
    """The Switchmaker Class."""

    def __init__(self, config_dir, entity_id, room, channels):
        """Initialise the Switchmaker."""
        self._entity_id = entity_id
        self._room = room
        self._root = config_dir
        self._alias = {}

        if self._root[-1] != "/":
            self._root += "/"
        self._f = open(
            self._root + "skyq" + self._room.replace(" ", "") + ".yaml", "w+"
        )

        if _path.isfile(self._root + CONST_ALIAS_FILENAME):
            aliasfile = open(self._root + CONST_ALIAS_FILENAME, "r")
            self._alias = yaml.full_load(aliasfile)
            aliasfile.close()

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
        source_switch = switch.replace("'", "''")
        if len(self._alias) > 0:
            friendly_name = self._findAlias(friendly_name)
        else:
            friendly_name = friendly_name.replace("'", "")
        switch_name = (
            "skyq_"
            + switch.replace(" ", "")
            .replace("'", "")
            .replace("+", "_")
            .replace(".", "")
            .replace("!", "")
            .replace(":", "_")
            .replace("/", "_")
            .lower()
            + self._room.replace(" ", "").lower()
        )
        source_name = ""
        if source:
            source_name = "          source: '" + source_switch + "'\n"

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
            + self._entity_id
            + "\n"
            + source_name
            + "      turn_off:\n"
            + "        service: script.placeholder\n"
        )

    def _findAlias(self, friendly_name):
        try:
            alias = self._alias[friendly_name]
        except KeyError:
            alias = friendly_name
        return alias

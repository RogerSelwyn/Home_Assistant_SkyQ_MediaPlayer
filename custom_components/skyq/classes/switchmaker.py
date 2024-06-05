"""
A utility function to generate yaml config for SkyQ media players.

To support easy usage with other home assistant integrations, e.g. google home
"""

import logging
import os.path as _path

import yaml

from ..const import CONST_ALIAS_FILENAME

SWITCH_REPLACE = {
    " ": "",
    "'": "",
    "+": "_",
    ".": "",
    "!": "",
    ":": "_",
    "/": "_",
    "&": "_",
    "-": "_",
    "(": "_",
    ")": "_",
}


_LOGGER = logging.getLogger(__name__)


class SwitchMaker:
    """The Switchmaker Class."""

    def __init__(self, config_dir, entity_id, room, channels):
        """Initialise the Switchmaker."""
        self._entity_id = entity_id
        self._room = room
        self._root = config_dir
        self._alias = {}
        self._channels = channels

        if self._root[-1] != "/":
            self._root += "/"

        self._f = None

    def create_file(self):
        """Create the switch file."""
        self._f = open(
            f"{self._root}skyq{self._room.replace(' ', '')}.yaml",
            "w+",
            encoding="utf-8",
        )

        if _path.isfile(self._root + CONST_ALIAS_FILENAME):
            with open(
                self._root + CONST_ALIAS_FILENAME, "r", encoding="utf-8"
            ) as aliasfile:
                self._alias = yaml.full_load(aliasfile)
            if not self._alias:
                _LOGGER.info("I0010 - skyqswitchalias.yaml is empty, it can be deleted")

        self._add_switch("pause", "pause", "media_pause")
        self._add_switch("play", "play", "media_play")
        self._add_switch("ff", "fastforward", "media_next_track")
        self._add_switch("rw", "rewind", "media_previous_track")

        dedup_channels = list(dict.fromkeys(self._channels))
        for channel in dedup_channels:
            self._add_switch(channel, channel, "select_source", True)

        self._f.close()

    def _add_switch(self, switch, friendly_name, service, source=False):
        """Add switch to switches."""
        source_switch = str(switch).replace("'", "''")
        if self._alias and len(self._alias) > 0:
            friendly_name = self._find_alias(friendly_name).replace("'", "")
        else:
            friendly_name = friendly_name.replace("'", "")

        for searcher, replacer in SWITCH_REPLACE.items():
            switch = switch.replace(searcher, replacer)
        switch = switch.lower()
        source_name = "            source: '" + source_switch + "'\n" if source else ""

        self._write_switch(switch, friendly_name, service, source_name)

    def _write_switch(self, switch, friendly_name, service, source_name):
        room_name = switch + self._room.replace(" ", "").lower()
        self._f.write("    " + "skyq_" + room_name + ":\n")
        self._f.write("      value_template: '{{\"off\"}}'\n")
        self._f.write(
            "      friendly_name: '" + friendly_name + " in the " + self._room + "'\n"
        )
        self._f.write("      turn_on:\n")
        self._f.write(f"        - service: media_player.{service}\n")
        self._f.write("          data:\n")
        self._f.write(f"            entity_id: {self._entity_id}\n")
        self._f.write(source_name)
        self._f.write("        - delay:\n")
        self._f.write("            seconds: 10\n")
        self._f.write("      turn_off:\n")
        self._f.write("        stop:\n")

    def _find_alias(self, friendly_name):
        try:
            alias = self._alias[friendly_name]
        except KeyError:
            alias = friendly_name
        return alias

"""
A utility function to generate yaml config for SkyQ media players.

To support easy usage with other home assistant integrations, e.g. google home
"""
import logging
import os.path as _path

import yaml

from ..const import CONST_ALIAS_FILENAME

SWITCH_REPLACE = {" ": "", "'": "", "+": "_", ".": "", "!": "", ":": "_", "/": "_", "&": "_", "-": "_"}


_LOGGER = logging.getLogger(__name__)


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
        self._f = open(self._root + "skyq" + self._room.replace(" ", "") + ".yaml", "w+")

        if _path.isfile(self._root + CONST_ALIAS_FILENAME):
            with open(self._root + CONST_ALIAS_FILENAME, "r") as aliasfile:
                self._alias = yaml.full_load(aliasfile)
            if self._alias:
                _LOGGER.info("I0010S - skyqswitchalias.yaml is empty, it can be deleted")

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
        if self._alias and len(self._alias) > 0:
            friendly_name = self._findAlias(friendly_name)
        else:
            friendly_name = friendly_name.replace("'", "")

        for searcher, replacer in SWITCH_REPLACE.items():
            switch = switch.replace(searcher, replacer)
        switch = switch.lower()
        source_name = "          source: '" + source_switch + "'\n" if source else ""

        self._write_switch(switch, friendly_name, service, source_name)

    def _write_switch(self, switch, friendly_name, service, source_name):
        room_name = switch + self._room.replace(" ", "").lower()
        self._f.write("    " + "skyq_" + room_name + ":\n")
        self._f.write("      value_template: '{{\"off\"}}'\n")
        self._f.write("      friendly_name: '" + friendly_name + " in the " + self._room + "'\n")
        self._f.write("      turn_on:\n")
        self._f.write("        service: media_player." + service + "\n")
        self._f.write("        data:\n")
        self._f.write("          entity_id: " + self._entity_id + "\n")
        self._f.write(source_name)
        self._f.write("      turn_off:\n")
        self._f.write("        service: script.placeholder\n")

    def _findAlias(self, friendly_name):
        try:
            alias = self._alias[friendly_name]
        except KeyError:
            alias = friendly_name
        return alias

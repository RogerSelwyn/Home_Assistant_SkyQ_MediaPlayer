"""
A utility function to generate YAML config for SkyQ media players.

Generates modern Template integration YAML intended for use with:
  template: !include_dir_merge_list templates/

This version:
- Writes generated YAML files into <config_root>/templates/
- Reads skyqswitchalias.yaml from <config_root>/
- Uses modern template switch syntax
"""

import logging
import os
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
    """The SwitchMaker Class."""

    def __init__(self, config_dir, entity_id, room, channels):
        """Initialise the SwitchMaker."""
        self._entity_id = entity_id
        self._room = room
        self._channels = channels
        self._alias = {}

        # Resolve Home Assistant config root safely
        self._config_root = self._resolve_config_root(config_dir)

        # Always write into <config_root>/templates/
        self._templates_dir = _path.join(self._config_root, "templates")
        os.makedirs(self._templates_dir, exist_ok=True)

        self._f = None
        self._first_switch_written = False

    @staticmethod
    def _resolve_config_root(config_dir: str) -> str:
        """Return the HA config directory (handles being passed a file path)."""
        if not config_dir:
            return os.getcwd()

        p = _path.abspath(config_dir)

        # If it's a file (or looks like one), use parent directory
        if _path.isfile(p) or p.lower().endswith((".yaml", ".yml")):
            p = _path.dirname(p)

        # If they passed .../templates, treat its parent as config root
        if _path.basename(p).lower() == "templates":
            p = _path.dirname(p)

        return p

    def create_file(self):
        """Create the switch file."""
        out_path = _path.join(
            self._templates_dir,
            f"skyq{self._room.replace(' ', '')}.yaml",
        )

        self._f = open(out_path, "w+", encoding="utf-8")

        # Load optional alias map from config root
        alias_path = _path.join(self._config_root, CONST_ALIAS_FILENAME)
        if _path.isfile(alias_path):
            with open(alias_path, "r", encoding="utf-8") as aliasfile:
                self._alias = yaml.full_load(aliasfile) or {}
            if not self._alias:
                _LOGGER.info("I0010 - skyqswitchalias.yaml is empty")

        # Transport controls
        self._add_switch("pause", "pause", "media_pause")
        self._add_switch("play", "play", "media_play")
        self._add_switch("ff", "fastforward", "media_next_track")
        self._add_switch("rw", "rewind", "media_previous_track")

        # Channel / source switches
        for channel in dict.fromkeys(self._channels):
            self._add_switch(channel, channel, "select_source", source=True)

        self._f.close()

    def _add_switch(self, switch, friendly_name, service, source=False):
        """Add switch to switches."""
        source_switch = str(switch).replace("'", "''")

        if self._alias:
            friendly_name = self._alias.get(friendly_name, friendly_name)

        friendly_name = friendly_name.replace("'", "")

        for searcher, replacer in SWITCH_REPLACE.items():
            switch = switch.replace(searcher, replacer)

        switch = switch.lower()

        self._write_switch(
            switch,
            friendly_name,
            service,
            source_switch if source else None,
        )

    def _open_block_if_needed(self):
        """Start a single template list-item block that contains a switch list."""
        if self._first_switch_written:
            return

        self._f.write("- switch:\n")
        self._first_switch_written = True

    def _write_switch(self, switch, friendly_name, service, source_name):
        """Write a modern template switch entry."""
        self._open_block_if_needed()

        room_suffix = self._room.replace(" ", "").lower()
        room_name = f"{switch}{room_suffix}"
        default_entity_id = f"switch.skyq_{room_name}"
        display_name = f"{friendly_name} in the {self._room}"

        self._f.write(f"    - default_entity_id: {default_entity_id}\n")
        self._f.write(f"      name: \"{display_name}\"\n")
        self._f.write("      state: \"{{ 'off' }}\"\n")

        self._f.write("      turn_on:\n")
        self._f.write(f"        - action: media_player.{service}\n")
        self._f.write("          target:\n")
        self._f.write(f"            entity_id: {self._entity_id}\n")

        if source_name is not None:
            self._f.write("          data:\n")
            self._f.write(f"            source: '{source_name}'\n")

        self._f.write("        - delay: \"00:00:10\"\n")
        self._f.write("      turn_off:\n")
        self._f.write("        - stop: \"\"\n")

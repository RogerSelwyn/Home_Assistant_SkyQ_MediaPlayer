"""Utilities for the skyq platform."""
import collections
import json


def convert_sources_JSON(sources_list=None, sources_json=None):
    """Convert sources to JSON format."""
    if sources_list:
        sources_dict = convert_sources(sources_list=sources_list)

        return json.dumps(sources_dict)

    if sources_json:
        sources_dict = json.loads(sources_json)

        return convert_sources(sources_dict=sources_dict)

    return None


def convert_sources(sources_list=None, sources_dict=None):
    """Convert sources to JSON format."""
    if sources_list:
        sources_dict = collections.OrderedDict()
        for s in sources_list:
            sources_dict[s[0]] = s[1]

        return sources_dict

    if sources_dict:
        sources_list = []
        for k, v in sources_dict.items():
            sources_list.append([k, v])

        return sources_list

    return None

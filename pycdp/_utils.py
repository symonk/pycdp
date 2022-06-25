import json
import pathlib

from ._types import ProtocolMappingAlias, SwappableAlias


def protocol_file_to_mapping(path: pathlib.Path) -> ProtocolMappingAlias:
    """Load the protocol json file and return the json parsed mapping object."""
    with open(path, "rb") as file:
        return json.load(file)


def js_protocol_data() -> ProtocolMappingAlias:
    js_json_path = pathlib.Path(__file__).parents[1].joinpath("devtools-protocol", "json", "js_protocol.json")
    return protocol_file_to_mapping(js_json_path)


def browser_protocol_data() -> ProtocolMappingAlias:
    browser_json_path = pathlib.Path(__file__).parents[1].joinpath("devtools-protocol", "json", "browser_protocol.json")
    return protocol_file_to_mapping(browser_json_path)


def clone_map_with_defaults(
    mapping: ProtocolMappingAlias, swap_if_missing: SwappableAlias
) -> ProtocolMappingAlias:
    """Given a mapping, Update keys with missing values."""
    new = dict(**mapping)
    for key, missing in swap_if_missing:
        new.setdefault(key, missing)
    return new


def name_to_snake_case(name: str):
    """Given a string, convert it to snake case."""
    if not name:
        return name
    new = [name[0].lower()]
    for char in name[1:]:
        if char.isupper():
            new.append("_")
            new.append(char.lower())
        else:
            new.append(char)
    return "".join(new)

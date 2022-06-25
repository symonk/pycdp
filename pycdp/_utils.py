import json
import pathlib

from ._types import ProtocolMappingAlias


def protocol_file_to_mapping(name: str) -> ProtocolMappingAlias:
    """Load the protocol json file and return the json parsed mapping object."""
    base_path = pathlib.Path(__file__).parents[1].joinpath("devtools-protocol", "json")
    with open(base_path.joinpath(name), "rb") as file:
        return json.load(file)


def js_protocol_data() -> ProtocolMappingAlias:
    """Parse and return the javascript protocol json content."""
    return protocol_file_to_mapping("js_protocol.json")


def browser_protocol_data() -> ProtocolMappingAlias:
    """Parse and return the browser protocol json content."""
    return protocol_file_to_mapping("browser_protocol.json")


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

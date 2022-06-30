import json
import pathlib
import re

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
    """Given a string; convert it to camel case.
    Taken from https://stackoverflow.com/a/1176023
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

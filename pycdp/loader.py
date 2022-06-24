import typing
import json
import pathlib
from dataclasses import dataclass


def protocol_file_to_mapping(path: pathlib.Path) -> typing.Dict[str, typing.Any]:
    """Load the protocol json file and return the json parsed mapping object."""
    with open(path) as file:
        return json.load(file)



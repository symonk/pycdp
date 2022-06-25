import json
import pathlib
import typing
from .types import JavascriptProtocolAlias
from .schemas import JavascriptProtocolSchema


def protocol_file_to_mapping(path: pathlib.Path) -> JavascriptProtocolAlias:
    """Load the protocol json file and return the json parsed mapping object."""
    with open(path) as file:
        return json.load(file)


def validate_response(protocol_json: JavascriptProtocolAlias) -> bool:
    """ Validates that (post loading) of the protocol json file, pycdp can build it's
    python objects from the response and there are no issues with the schemas.

    :param protocol_json: A mapping of json data, built from `protocol_file_to_mapping`.
    """
    JavascriptProtocolSchema().validate(protocol_json)

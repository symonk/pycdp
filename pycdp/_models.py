from __future__ import annotations

import typing
from dataclasses import dataclass

from ._protocols import Transformable
from ._types import SwappableAlias
from ._utils import clone_map_with_defaults


@dataclass
class TypeProperty:
    name: str
    description: str
    type: str


@dataclass
class Parameter:
    ...


@dataclass
class Event:
    name: str
    description: str
    parameters: typing.List[Parameter]


@dataclass
class Returns:
    ...


@dataclass
class Command:
    name: str
    description: str
    returns: typing.List[Returns]


@dataclass
class Type(Transformable):
    id: str
    description: typing.Optional[str]
    experimental: bool
    type: str
    properties: typing.Optional[typing.List[TypeProperty]]
    enum: typing.Optional[typing.List[str]]

    @classmethod
    def from_json(cls, mapping) -> Type:
        swappable: SwappableAlias = (("properties", []), ("experimental", False), ("description", None), ("enum", []))
        mapping = clone_map_with_defaults(mapping, swappable)
        return cls(**mapping)


@dataclass
class Domain(Transformable):
    """An encapsulation of a devtools protocol domain.  A domain is built from
    some basic metadata, types, commands and events."""

    domain: str
    description: typing.Optional[str]
    experimental: bool
    dependencies: typing.List[str]
    types: typing.List[Type]
    commands: typing.List[Command]
    events: typing.List[Event]

    @classmethod
    def from_json(cls, mapping) -> Domain:
        # Todo: This is naive and only a place holder for now!
        swappable: SwappableAlias = (
            ("dependencies", []),
            ("types", []),
            ("commands", []),
            ("events", []),
            ("experimental", False),
        )
        mapping = clone_map_with_defaults(mapping, swappable)
        mapping["types"] = [Type.from_json(t) for t in mapping["types"]]
        return cls(**mapping)

    def to_json(self) -> ...:  # type: ignore
        ...

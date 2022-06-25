from __future__ import annotations

import typing
from dataclasses import dataclass

from ._protocols import Transformable
from ._types import SwappableAlias
from ._utils import name_to_snake_case
from ._utils import clone_map_with_defaults


@dataclass
class TypeProperty(Transformable):
    name: str
    description: str
    type: str


@dataclass
class Parameter(Transformable):
    name: str
    description: typing.Optional[str]
    ref: typing.Optional[str]
    optional: bool
    type: typing.Optional[str]


@dataclass
class Event(Transformable):
    name: str
    description: typing.Optional[str]
    experimental: bool
    parameters: typing.Optional[typing.List[Parameter]]

    @classmethod
    def from_json(cls, mapping) -> ...:
        swaps = (("parameters", []), ("description", None), ("experimental", False))
        mapping = clone_map_with_defaults(mapping, swaps)
        return cls(**mapping)


@dataclass
class Property(Transformable):
    ...


@dataclass
class Returns(Transformable):
    name: str
    description: str
    type: typing.Optional[str]
    ref: str


@dataclass
class Command(Transformable):
    name: str
    description: typing.Optional[str]
    parameters: typing.Optional[Parameter]
    experimental: bool
    redirect: typing.Optional[str]
    returns: typing.Optional[typing.List[Returns]]

    @classmethod
    def from_json(cls, mapping) -> ...:  # type: ignore
        swappable = (("description", None), ("parameters", []), ("experimental", False), ("redirect", None))
        mapping["returns"] = []  # hack for now.
        mapping = clone_map_with_defaults(mapping, swappable)
        mapping["parameters"] = [Parameter.from_json(p) for p in mapping["parameters"]]
        return cls(**mapping)

    def to_json(self) -> ...: # type: ignore
        ...


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
            ("description", None),
            ("types", []),
            ("commands", []),
            ("events", []),
            ("experimental", False),
        )
        mapping = clone_map_with_defaults(mapping, swappable)
        mapping["types"] = [Type.from_json(t) for t in mapping["types"]]
        mapping["commands"] = [Command.from_json(comm) for comm in mapping["commands"] if "deprecated" not in comm]
        mapping["events"] = [Event.from_json(ev) for ev in mapping["events"]]
        return cls(**mapping)

    def to_json(self) -> ...:  # type: ignore
        ...

    @property
    def mod_name(self) -> str:
        """The python module name in snake case."""
        return f"{name_to_snake_case(self.domain)}.py"

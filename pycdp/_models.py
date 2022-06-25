from __future__ import annotations

import enum
import typing
from dataclasses import dataclass

from ._mixins import GeneratesModuleMixin
from ._protocols import Transformable
from ._types import SwappableAlias
from ._utils import clone_map_with_defaults


# Todo: Do we care about avoid deprecated? should we just compile everything possible?
# Todo: The whole generating code concept; I assume we can just store literal text and write it to files
    #Todo: is there a better / existing lib for that kind of thing?
# Todo: Fix CI.

"""
Devtools Protocol stipulates the following types:
    :: string
    :: integer
    :: boolean
    :: array
    :: number
    :: object
    :: any
"""


class AvailableTypes(enum.Enum):
    # store a callable to convert data to the appropriate type.
    string = str
    integer = int
    number = float
    object = dict
    array = list
    boolean = bool
    # any?


@dataclass
class DevtoolsTypeProperty(Transformable):
    name: str
    description: str
    ref: typing.Optional[str]
    type: typing.Optional[str]
    items: typing.Optional[typing.Dict]

    @classmethod
    def from_dict(cls, mapping) -> DevtoolsTypeProperty:
        return cls(**mapping)


@dataclass
class DevtoolsParameter(Transformable):
    name: str
    description: typing.Optional[str]
    ref: typing.Optional[str]
    optional: bool
    type: typing.Optional[str]


@dataclass
class DevtoolsEvent(Transformable):
    name: str
    description: typing.Optional[str]
    experimental: bool
    parameters: typing.Optional[typing.List[DevtoolsParameter]]

    @classmethod
    def from_dict(cls, mapping) -> ...:
        swaps = (("parameters", []), ("description", None), ("experimental", False))
        mapping = clone_map_with_defaults(mapping, swaps)
        return cls(**mapping)


@dataclass
class DevtoolsItems(Transformable):
    type: str
    ref: str

    @classmethod
    def from_dict(cls, mapping) -> ...:
        ...


@dataclass
class DevtoolsProperty(Transformable, GeneratesModuleMixin):
    name: str
    description: str
    type: typing.Optional[str]
    ref: typing.Optional[str]
    enum: typing.List[str]
    items: typing.Optional[DevtoolsItems]
    optional: bool
    experimental: bool


@dataclass
class DevtoolsReturns(Transformable):
    name: str
    description: str
    type: typing.Optional[str]
    ref: str


@dataclass
class DevtoolsCommand(Transformable):
    name: str
    description: typing.Optional[str]
    parameters: typing.Optional[DevtoolsParameter]
    experimental: bool
    redirect: typing.Optional[str]
    returns: typing.Optional[typing.List[DevtoolsReturns]]

    @classmethod
    def from_dict(cls, mapping) -> ...:  # type: ignore
        swappable = (("description", None), ("parameters", []), ("experimental", False), ("redirect", None))
        mapping["returns"] = []  # hack for now.
        mapping = clone_map_with_defaults(mapping, swappable)
        mapping["parameters"] = [DevtoolsParameter.from_dict(p) for p in mapping["parameters"]]
        return cls(**mapping)

    def to_dict(self) -> ...: # type: ignore
        ...


@dataclass
class DevtoolsItems:
    ...


@dataclass
class DevtoolsType(Transformable):
    id: str
    description: typing.Optional[str]
    type: str
    items: typing.Optional[DevtoolsItems]
    properties: typing.List[DevtoolsProperty]
    enum: typing.List[str]

    @classmethod
    def from_dict(cls, mapping) -> DevtoolsType:
        swappable: SwappableAlias = (("properties", []), ("experimental", False), ("description", None), ("enum", []))
        mapping = clone_map_with_defaults(mapping, swappable)
        return cls(**mapping)


@dataclass
class DevtoolsDomain(Transformable, GeneratesModuleMixin):
    """Encapsulation of a devtools domain."""
    domain: str
    description: typing.Optional[str]
    experimental: bool
    dependencies: typing.List[str]
    types: typing.List[DevtoolsType]
    commands: typing.List[DevtoolsCommand]
    events: typing.List[DevtoolsEvent]

    @classmethod
    def from_dict(cls, mapping) -> DevtoolsDomain:
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
        mapping["types"] = [DevtoolsType.from_dict(t) for t in mapping["types"]]
        mapping["commands"] = [DevtoolsCommand.from_dict(comm) for comm in mapping["commands"] if "deprecated" not in comm]
        mapping["events"] = [DevtoolsEvent.from_dict(ev) for ev in mapping["events"]]
        return cls(**mapping)

    def to_dict(self) -> ...:  # type: ignore
        ...

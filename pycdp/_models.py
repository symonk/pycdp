from __future__ import annotations

import enum
import typing
from dataclasses import dataclass

from ._mixins import GeneratesModuleMixin
from ._types import ProtocolMappingAlias

# Todo: Do we care about avoid deprecated? should we just compile everything possible?
# Todo: The whole generating code concept; I assume we can just store literal text and write it to files
# Todo: Fix CI.


class MimicPrimitives(enum.Enum):
    """Encapsulation of devtools types and their corresponding python types.
    These are the primitive types, tho python doesn't really have any primitive
    types as everything is an object.  For more complex cases we use an object
    and that gets converted into a subsequent dataclass.
    """

    string = "str"
    integer = "int"
    number = "float"
    object = "dict"
    array = "list"
    boolean = "bool"
    # Todo: Handle any?


@dataclass
class TypeProperty:
    name: str
    description: str
    ref: typing.Optional[str]
    type: typing.Optional[str]
    items: typing.Optional[typing.Dict[str, typing.Any]]


@dataclass
class Parameter:
    name: str
    description: typing.Optional[str]
    ref: typing.Optional[str]
    optional: bool
    type: typing.Optional[str]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Parameter:
        return cls(
            name=data["name"],
            description=data.get("description", None),
            ref=data.get("ref", None),
            optional=data.get("optional", False),
            type=data.get("type", None),
        )


@dataclass
class Event:
    """The encapsulation of a CDP domain Event."""

    name: str
    description: typing.Optional[str]
    experimental: bool
    parameters: typing.List[Parameter]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Event:
        return cls(
            name=data["name"],
            description=data.get("description", None),
            experimental=data.get("experimental", False),
            parameters=[Parameter.deserialize(parameter) for parameter in data.get("parameters", [])],
        )


@dataclass
class Items:
    type: str
    ref: str


@dataclass
class ObjectProperty(GeneratesModuleMixin):
    name: str
    description: str
    type: typing.Optional[str]
    ref: typing.Optional[str]
    enum: typing.List[str]
    items: typing.Optional[Items]
    optional: bool
    experimental: bool

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> ObjectProperty:
        raise NotImplementedError


@dataclass
class CommandProperty(ObjectProperty):
    """A Command Argument."""


@dataclass
class Returns:
    """Encapsulation of the return value from a devtools Command."""

    name: str
    description: str
    type: typing.Optional[str]
    ref: str


@dataclass
class Command:
    """Encapsulation of a domain command."""

    name: str
    description: typing.Optional[str]
    parameters: typing.Optional[Parameter]
    experimental: bool
    redirect: typing.Optional[str]
    returns: typing.List[Returns]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Command:  # type: ignore
        return cls(
            name=data["name"],
            description=data.get("description", None),
            parameters=data.get("parameters", []),
            experimental=data.get("experimental", False),
            redirect=data.get("redirect", None),
            returns=data.get("returns", []),
        )


@dataclass
class Type:
    id: str
    description: typing.Optional[str]
    type: str
    properties: typing.List[ObjectProperty]
    enum: typing.List[str]
    items: typing.Optional[Items]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Type:
        return cls(
            id=data["id"],
            description=data.get("description", None),
            type=data["type"],
            properties=[ObjectProperty.deserialize(prop) for prop in data.get("properties", [])],
            enum=data.get("enum", []),
            items=data.get("items", None),
        )


@dataclass
class Domain(GeneratesModuleMixin):
    """Encapsulation of a devtools domain."""

    domain: str
    description: typing.Optional[str]
    experimental: bool
    dependencies: typing.List[str]
    types: typing.List[Type]
    commands: typing.List[Command]
    events: typing.List[Event]

    @classmethod
    def from_dict(cls, data: ProtocolMappingAlias) -> Domain:
        return cls(
            domain=data["domain"],
            description=data.get("description", None),
            experimental=data.get("experimental", False),
            dependencies=data.get("dependencies", []),
            types=[Type.deserialize(_type) for _type in data.get("types", [])],
            commands=[Command.deserialize(command) for command in data.get("commands", [])],
            events=[Event.deserialize(event) for event in data.get("events", [])],
        )

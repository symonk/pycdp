"""
The following is on-going documentation as I research and wrap my head around the devtools protocol
APIs, they are quite complex and take a bit of deciphering to fully understand how it pieces together.
They may be completely incorrect, this is 'notes' from studying the browser_protocl.json and js_protocol.json
files.

-----

Model explanations.
    Domain is the highest level and the entire CDP is based around an array of Domain objects
    -- Each domain has the following (potential) keys:
        -- domain | description | experimental | dependencies | types | commands | events |
    -- Each command has the following (potential keys):
        -- deprecated | description | experimental | name | parameters | redirect | returns
    -- Each event has the following (potential) keys:
        -- deprecated | description | experimental | name | parameters
    -- Each type has the following (potential) keys:
        -- deprecated | description | enum | experimental | id | items | properties | type

Types composition:
    # What is a domain?
    Domain:
        domain: str  # The domain name
        description: typing.Optional[str]  # The optional domain description
        experimental: bool  # If the api is marked experimental
        deprecated: bool  # If the domain is marked deprecated
        dependencies: typing.List[str]  # List of strings of other domain dependencies
        commands: typing.List[Command]  # List of command object instances
        events: typing.List[Event]  # List of event object instances
        types: typing.List[Type]  # List of types

    # What is a command?
    Command:
        name: str  # The command name
        description: typing.Optional[str]  # The optional command description
        experimental: bool  # If the command is marked experimental
        deprecated: bool  # If the command is marked deprecated (The entire domain may not be)
        parameters: typing.List[Parameter]  # A list of command arguments (primitives or objects)
        redirect: typing.Optional[str]  # Another domain name for the redirect? (still not sure here...)
        returns: typing.Optional[Parameter]  # A list of returned data from the command (primitives or objects)

    # Notes: Command parameter and returns appear to be largely the same thing

    -----

    # What is a Parameter?
        -- Todo

    # What is an event?
    Event:
        deprecated: bool  # Whether the event has been deprecated.
        description: typing.Optional[str]  # An optional string of the event description.
        experimental: bool  # Whether the event is considered experimental and may change.
        name: str  # The name of the event
        parameters: typing.List[Parameter]  # A list of event parameters.

    # What is a Type?
    Type:
        ...

"""

from __future__ import annotations

import enum
import typing
from dataclasses import dataclass

from ._mixins import GeneratesModuleMixin
from ._types import ProtocolMappingAlias


class Primitive(enum.Enum):
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
    """An argument type to a command.  This may also be returned by the response from a commands
    actions, tho I need to understand how that fits in together."""

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
    """Encapsulation of a domain omitted event.

    :param name: The name of the event
    :param description: The optional description of the event
    :param experimental: Whether the event is considered experimental and may change.
    :param deprecated: Whether the event has been deprecated or not.
    :param parameters: A list of parameters for the event.
    """

    name: str
    description: typing.Optional[str]
    experimental: bool
    deprecated: bool
    parameters: typing.List[Parameter]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Event:
        return cls(
            name=data["name"],
            description=data.get("description", None),
            experimental=data.get("experimental", False),
            deprecated=data.get("deprecated", False),
            parameters=[Parameter.deserialize(parameter) for parameter in data.get("parameters", [])],
        )


@dataclass
class Items:
    """Encapsulation of the types that are recurring inside properties of array types.

    :param type: Optional string representing the type of the value if primitive.
    :param ref: Optional string representing the type of the value if object.
    """

    type: typing.Optional[str]
    ref: typing.Optional[str]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Items:
        return cls(type=data.get("type", None), ref=data.get("ref", None))


@dataclass
class ObjectProperty(GeneratesModuleMixin):
    """A Property for non primitives types; object types are composed of these.

    :param name: The name of the property (attribute name).
    :param description: The optional description of the property.
    :param deprecated: If the property has been marked as deprecated.
    :param experimental: If the property has been marked experimental.
    :param enum: Allowed literal values for the property.
    :param optional: Whether the property is optional to a command etc.
    :param type: An optional string indicating the type of property, primitive of object etc.
    :param items: Recurring property array items, only appears if property type is an array.

    """

    name: str
    description: typing.Optional[str]
    deprecated: bool
    experimental: bool
    enum: typing.List[str]
    optional: bool
    type: typing.Optional[str]
    items: typing.Optional[Items]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> ObjectProperty:
        return cls(
            name=data["name"],
            description=data.get("description", None),
            deprecated=data.get("deprecated", False),
            experimental=data.get("experimental", False),
            enum=data.get("enum", []),
            optional=data.get("optional", False),
            type=data.get("type", None),
            items=Items.deserialize(data["items"]) if "items" in data else None,
        )


@dataclass
class ReturnParameter(Parameter):
    """Encapsulation of the return parameters for a command."""


@dataclass
class Command:
    """Encapsulation of a command for a given domain.  Commands accept arbitrary parameter types
    and return those same modelled types in the form of a `Parameter`.

    :param name: The name of the command.
    :param description: The (Optional) description of the command.
    :param parameters: The arguments to be dispatched with the command.
    :param experimental: Whether the command has been marked experimental by the chrome team and may change.
    :param redirect: A module to be used for a redirect?  # Todo: Update this I don't fully understand what it is.
    :param returns: A list of parameters that can be returned for the command response.
    """

    name: str
    description: typing.Optional[str]
    parameters: typing.List[Parameter]
    experimental: bool
    redirect: typing.Optional[str]
    returns: typing.List[Parameter]

    @classmethod
    def deserialize(cls, data: ProtocolMappingAlias) -> Command:
        return cls(
            name=data["name"],
            description=data.get("description", None),
            parameters=[Parameter.deserialize(parameter) for parameter in data.get("parameters", [])],
            experimental=data.get("experimental", False),
            redirect=data.get("redirect", None),
            returns=[ReturnParameter.deserialize(parameter) for parameter in data.get("returns", [])],
        )


@dataclass
class Type:
    """Encapsulation of the types associated with a devtools Domain

    :param id: The ID of the type
    :param description: An optional description of the type
    :param type: The type of the type (primitive or object)
    :param properties: A list of Object properties if the type is `object`.
    :param enum: The literal values if the type is a `string`.
    :param items: The recurring array items if type is an `array` of items.
    """

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
    def deserialize(cls, data: ProtocolMappingAlias) -> Domain:
        return cls(
            domain=data["domain"],
            description=data.get("description", None),
            experimental=data.get("experimental", False),
            dependencies=data.get("dependencies", []),
            types=[Type.deserialize(_type) for _type in data.get("types", [])],
            commands=[Command.deserialize(command) for command in data.get("commands", [])],
            events=[Event.deserialize(event) for event in data.get("events", [])],
        )

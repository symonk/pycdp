from marshmallow import Schema, fields


class BaseSchema(Schema):
    """A base schema with improved error handling."""


class Version(Schema):
    major = fields.String(required=True)
    minor = fields.String(required=True)


class Type(BaseSchema):
    identity = fields.String(data_key="id")
    description = fields.String()
    type = fields.String()


class Types(BaseSchema):
    types = fields.List(fields.Nested(Type))


class Parameter(BaseSchema):
    name = fields.String()
    description = fields.String()
    optional = fields.Boolean()
    ref = fields.String(data_key="$ref")


class Parameters(BaseSchema):
    parameters = fields.List(fields.Nested(Parameter))


class Returns(BaseSchema):
    name = fields.String()
    description = fields.String()
    type_ = fields.String(data_key="type")
    items = fields.Dict(fields.String(), fields.String())


class Command(BaseSchema):
    name = fields.String()
    description = fields.String()
    experimental = fields.Boolean()
    parameters = fields.List(fields.Nested(Parameter))
    returns = fields.List(fields.Nested(Returns))


class Commands(BaseSchema):
    commands = fields.List(fields.Nested(Command))


class Event(BaseSchema):
    name = fields.String()
    description = fields.String()
    experimental = fields.Boolean()
    parameters = fields.List(fields.Nested(Parameter))


class EventParameter(BaseSchema):
    name = fields.String()
    description = fields.String()
    ref = fields.String(data_key="$ref")
    type_ = fields.String()


class Events(BaseSchema):
    events = fields.List(fields.Nested(Event))


class Domain(BaseSchema):
    domain = fields.String()
    experimental = fields.Boolean()
    dependencies = fields.List(fields.String())
    types = fields.Nested(Types)
    commands = fields.Nested(Commands)


class Domains(BaseSchema):
    domains = fields.List(fields.Nested(Domain))


class JavascriptProtocol(BaseSchema):
    version = fields.Nested(Version)
    domains = fields.Nested(Domains)

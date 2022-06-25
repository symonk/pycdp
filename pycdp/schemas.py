from marshmallow import Schema, fields


class BaseSchema(Schema):
    """A base schema with improved error handling."""


class VersionSchema(BaseSchema):
    major = fields.String(required=True)
    minor = fields.String(required=True)


class TypeSchema(BaseSchema):
    identity = fields.String(data_key="id")
    description = fields.String()
    type = fields.String()


class TypesSchema(BaseSchema):
    types = fields.List(fields.Nested(TypeSchema))


class ParameterSchema(BaseSchema):
    name = fields.String()
    description = fields.String()
    optional = fields.Boolean()
    ref = fields.String(data_key="$ref")


class ParametersSchema(BaseSchema):
    parameters = fields.List(fields.Nested(ParameterSchema))


class ReturnsSchema(BaseSchema):
    name = fields.String()
    description = fields.String()
    type_ = fields.String(data_key="type")
    items = fields.Dict(fields.String(), fields.String())


class CommandSchema(BaseSchema):
    name = fields.String()
    description = fields.String()
    experimental = fields.Boolean()
    parameters = fields.List(fields.Nested(ParameterSchema))
    returns = fields.List(fields.Nested(ReturnsSchema))


class CommandsSchema(BaseSchema):
    commands = fields.List(fields.Nested(CommandSchema))


class EventSchema(BaseSchema):
    name = fields.String()
    description = fields.String()
    experimental = fields.Boolean()
    parameters = fields.List(fields.Nested(ParameterSchema))


class EventParamSchema(BaseSchema):
    name = fields.String()
    description = fields.String()
    ref = fields.String(data_key="$ref")
    type_ = fields.String()


class EventsSchema(BaseSchema):
    events = fields.List(fields.Nested(EventSchema))


class DomainSchema(BaseSchema):
    domain = fields.String()
    experimental = fields.Boolean()
    dependencies = fields.List(fields.String())
    types = fields.Nested(TypesSchema)
    commands = fields.Nested(CommandsSchema)


class DomainsSchema(BaseSchema):
    domains = fields.List(fields.Nested(DomainSchema))


class JavascriptProtocolSchema(BaseSchema):
    version = fields.Nested(VersionSchema)
    domains = fields.Nested(DomainsSchema)

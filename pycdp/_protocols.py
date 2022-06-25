import typing
from typing import Protocol

from ._types import ProtocolMappingAlias

T = typing.TypeVar("T")


class JsonSerializable(Protocol):
    """A protocol for (de)serialisation of pythonic objects."""

    @classmethod
    def deserialize(cls: typing.Type[T], data: ProtocolMappingAlias) -> T:  # type: ignore
        ...

    def serialize(self: T) -> ProtocolMappingAlias:  # type: ignore
        ...


class TransformsToCode(Protocol):
    """A protocol for generating python modules from in memory objects."""

    def generate(self) -> str:  # type: ignore
        ...

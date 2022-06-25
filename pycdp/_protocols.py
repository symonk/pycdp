from typing import Protocol


class Transformable(Protocol):
    """A protocol for (de)serialisation of pythonic objects."""

    @classmethod
    def from_json(cls, mapping) -> ...:  # type: ignore
        ...

    def to_json(self) -> ...:  # type: ignore
        ...


class Generatable(Protocol):
    """A protocol for generating python modules from in memory objects."""

    def generate(self) -> ...:  # type: ignore
        ...

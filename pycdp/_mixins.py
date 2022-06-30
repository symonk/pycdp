from pycdp._utils import name_to_snake_case


class GeneratesModuleMixin:
    """Allows various models to convert their class names to snake case"""

    def mod_name(self, attr: str) -> str:
        """The python module name in snake case."""
        attribute: str = getattr(self, attr, None)
        if attribute is None:
            raise AttributeError(f"Cannot determine module name from: {self}")
        return f"{name_to_snake_case(attribute)}.py"

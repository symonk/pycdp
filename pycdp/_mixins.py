from pycdp._utils import name_to_snake_case


class GeneratesModuleMixin:
    """ Allows various models to convert their class names to snake case"""

    def mod_name(self, attr: str) -> str:
        """The python module name in snake case."""
        return f"{name_to_snake_case(self.__dict__[attr])}.py"

from pycdp._utils import name_to_snake_case


def test_snake_case(asserto):
    asserto(name_to_snake_case("Schema")).is_equal_to("schema")
    asserto(name_to_snake_case("SomeCamelName")).is_equal_to("some_camel_name")
    asserto(name_to_snake_case("")).is_equal_to("")
    asserto(name_to_snake_case("nothing")).is_equal_to("nothing")
    asserto(name_to_snake_case("ABC")).is_equal_to("a_b_c")

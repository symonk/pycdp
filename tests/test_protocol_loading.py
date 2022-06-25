from pycdp._utils import js_protocol_data


def test_can_load_protocol(protocol_path) -> None:
    js_protocol_data()  # no exception is sufficient.

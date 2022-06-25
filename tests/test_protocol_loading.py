from pycdp._utils import protocol_file_to_mapping


def test_can_load_protocol(asserto, protocol_path) -> None:
    asserto(protocol_file_to_mapping(protocol_path)).is_equal_to({})

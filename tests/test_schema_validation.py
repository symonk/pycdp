from pycdp.loader import protocol_file_to_mapping
from pycdp.loader import validate_response


def test_javascript_json_can_be_validated(asserto, protocol_path):
    json_data = protocol_file_to_mapping(protocol_path)
    asserto(validate_response(json_data)).is_true()

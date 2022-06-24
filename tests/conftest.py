import pathlib

import pytest
from asserto import Asserto


@pytest.fixture
def asserto():
    return Asserto


@pytest.fixture
def protocol_path() -> pathlib.Path:
    return pathlib.Path(__file__).parents[1].joinpath("devtools-protocol").joinpath("json").joinpath("js_protocol.json")

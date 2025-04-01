import os
import shutil
from os.path import join

import pytest

from tests import OUTPUTS_PATH


@pytest.fixture(scope="function", name="outputs_path")
def fixture_temporary_outputs_path():
    temp_outputs_path = join(OUTPUTS_PATH, "temp")
    os.mkdir(temp_outputs_path)
    yield temp_outputs_path
    shutil.rmtree(temp_outputs_path)

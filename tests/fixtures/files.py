from pathlib import Path

import pytest
from werkzeug.datastructures import FileStorage


@pytest.fixture(scope="function")
def make_FileStorage(request):
    filename = request.param
    file_path = (
        Path(__file__).parent / f"../fixtures/example_data/example_images/{filename}"
    )
    with open(file_path, "rb") as f:
        yield FileStorage(f)

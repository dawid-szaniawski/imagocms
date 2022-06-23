from pathlib import Path

import pytest
from werkzeug.datastructures import FileStorage


@pytest.fixture(scope="function")
def make_FileStorage(request) -> FileStorage:
    filename = request.param
    file_path = (
        Path(__file__).parent / f"../fixtures/example_data/example_images/{filename}"
    )
    with open(file_path, "rb") as f:
        yield FileStorage(f)


@pytest.fixture(scope="function")
def temp_path() -> Path:
    return Path(__file__).parent / "../fixtures/tmp/"

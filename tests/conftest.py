from pathlib import Path

from pytest import fixture
from responses import RequestsMock


@fixture
def bytes_generator():
    def prepare_bytes(filename: str) -> bytes:
        file_path = (
            Path(__file__) / f"../fixtures/example_data/example_images/{filename}"
        )
        with open(file_path, "rb") as f:
            return f.read()

    yield prepare_bytes


@fixture
def mocked_responses() -> RequestsMock:
    with RequestsMock() as response:
        yield response

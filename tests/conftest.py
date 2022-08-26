from pathlib import Path

from pytest import fixture


@fixture
def bytes_generator():
    def prepare_bytes(filename: str) -> bytes:
        file_path = (
                Path(__file__)
                / f"../fixtures/example_data/example_images/{filename}"
        )
        with open(file_path, "rb") as f:
            return f.read()
    return prepare_bytes

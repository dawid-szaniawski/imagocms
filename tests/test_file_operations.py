import io
from pathlib import Path
from typing import IO
from requests import get

from utilities import file_operations

import pytest


@pytest.fixture(scope="function")
def prepare_bytesio_and_filename(request) -> IO[bytes]:
    """Takes the name of a file and looks for that file in a folder with sample data.
    Then creates a file-like object and pass it back.

    Args:
        request: filename

    Returns:
        BytesIO: file-like object.
    """
    filename = request.param
    file_path = Path(__file__) / f"../fixtures/example_data/example_images/{filename}"
    with open(file_path, "rb") as f:
        yield io.BytesIO(f.read()), filename


@pytest.fixture(scope="function")
def prepare_request_object(request):
    return get(request.param)


class TestIsValidImage:
    allowed_extensions = {"JPEG", "PNG", "GIF"}
    correct_files = ("correct01.jpeg", "correct02.png")
    not_a_valid_image = ("incorrect01.jpg",)
    wrong_extension_in_name = ("incorrect02.pdf",)
    different_extensions = ("incorrect03.jpg",)
    wrong_extension_in_bytes = ("incorrect04.jpg",)
    to_much_extensions = ("incorrect05.sql.jpg",)

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", correct_files, indirect=True
    )
    def test_return_true_if_image_is_valid(self, prepare_bytesio_and_filename):
        bytesio, filename = prepare_bytesio_and_filename

        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is True
        )

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", not_a_valid_image, indirect=True
    )
    def test_return_false_if_file_is_not_a_valid_image(
        self, prepare_bytesio_and_filename
    ):
        bytesio, filename = prepare_bytesio_and_filename

        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", wrong_extension_in_name, indirect=True
    )
    def test_return_false_if_extension_from_name_is_not_in_allowed_extensions(
        self, prepare_bytesio_and_filename
    ):
        bytesio, filename = prepare_bytesio_and_filename

        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", different_extensions, indirect=True
    )
    def test_return_false_if_extension_from_name_is_not_extension_from_bytes(
        self, prepare_bytesio_and_filename
    ):
        bytesio, filename = prepare_bytesio_and_filename

        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", wrong_extension_in_bytes, indirect=True
    )
    def test_return_false_if_extension_from_bytes_is_not_in_allowed_extensions(
        self, prepare_bytesio_and_filename
    ):
        bytesio, filename = prepare_bytesio_and_filename

        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", to_much_extensions, indirect=True
    )
    def test_return_false_if_file_had_more_than_one_extension(
        self, prepare_bytesio_and_filename
    ):
        bytesio, filename = prepare_bytesio_and_filename

        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )


class TestDownloadImages:
    url = ("https://pl.wikipedia.org/static/images/project-logos/plwiki.png",)

    @pytest.mark.parametrize("prepare_request_object", url, indirect=True)
    def test_file_should_have_proper_filename_and_be_in_correct_place(
        self, tmp_path_factory, prepare_request_object
    ):
        data_dict = {"filename.png": prepare_request_object}
        temp_folder = tmp_path_factory.mktemp("data")
        file_operations.download_images(data_dict, temp_folder)
        path = Path(temp_folder / "filename.png")
        assert path.exists() is True

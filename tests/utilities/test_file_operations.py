from pathlib import Path
from typing import IO
from io import BytesIO

import requests
import pytest
from _pytest.fixtures import SubRequest

from utilities import file_operations


@pytest.mark.integtests
class TestIsValidImage:
    allowed_extensions = {"JPG", "JPEG", "PNG", "GIF"}
    correct_files = (
        "correct01.jpeg",
        "correct02.png",
        "correct03.jpg",
        "correct04_com.testtest.home.jpg",
    )
    not_a_valid_image = ("incorrect01_empty_file.jpg", "incorrect05.sql.jpg")
    wrong_extension_in_name = ("incorrect02.pdf",)
    different_extensions = ("incorrect03_im_gif.jpg",)
    wrong_extension_in_bytes = ("incorrect04_im_bmp.jpg",)

    @pytest.fixture
    def prepare_bytesio_and_filename(
        self, request: SubRequest
    ) -> tuple[IO[bytes], str]:
        """Takes the name of a file and looks for that file in a folder with
        sample data. Then creates a file-like object and pass it back.

        Args:
            request: filename

        Returns:
            BytesIO: file-like object,
            str: string containing filename.
        """
        filename = request.param
        file_path = (
            Path(__file__).parent
            / f"../fixtures/example_data/example_images/{filename}"
        )
        with open(file_path, "rb") as f:
            yield BytesIO(f.read()), filename

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", correct_files, indirect=True
    )
    def test_return_true_if_image_is_valid(
        self, prepare_bytesio_and_filename: tuple[IO[bytes], str]
    ) -> None:
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
        self, prepare_bytesio_and_filename: tuple[IO[bytes], str]
    ) -> None:
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
        self, prepare_bytesio_and_filename: tuple[IO[bytes], str]
    ) -> None:
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
        self, prepare_bytesio_and_filename: tuple[IO[bytes], str]
    ) -> None:
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
        self, prepare_bytesio_and_filename: tuple[IO[bytes], str]
    ) -> None:
        bytesio, filename = prepare_bytesio_and_filename
        assert (
            file_operations.is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )


@pytest.mark.integtests
class TestDownloadImages:
    url = ("https://pl.wikipedia.org/static/images/project-logos/plwiki.png",)

    @pytest.fixture
    def prepare_request_object(self, request: SubRequest) -> requests.models.Response:
        """Prepare request object based on string containing URL.
        Todo:
            Mock the response object. Do not send requests to external websites."""
        return requests.get(request.param)

    @pytest.mark.parametrize("prepare_request_object", url, indirect=True)
    def test_file_should_have_proper_filename_and_be_in_correct_place(
        self, tmp_path: Path, prepare_request_object: requests.models.Response
    ) -> None:
        data_dict = {"filename.png": prepare_request_object}
        file_operations.download_images(data_dict, tmp_path)
        path = Path(tmp_path / "filename.png")
        assert path.exists() is True

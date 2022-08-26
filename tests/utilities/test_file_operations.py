from typing import IO, Callable
from io import BytesIO

import pytest
from _pytest.fixtures import SubRequest

from utilities.file_operations import is_valid_image


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
            self,
            request: SubRequest,
            bytes_generator: Callable[[str], bytes]
    ) -> tuple[IO[bytes], str]:
        filename = request.param
        bytes_object = bytes_generator(filename)
        yield BytesIO(bytes_object), filename

    @pytest.mark.parametrize(
        "prepare_bytesio_and_filename", correct_files, indirect=True
    )
    def test_return_true_if_image_is_valid(
        self, prepare_bytesio_and_filename: tuple[IO[bytes], str]
    ) -> None:
        bytesio, filename = prepare_bytesio_and_filename
        assert (
            is_valid_image(
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
            is_valid_image(
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
            is_valid_image(
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
            is_valid_image(
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
            is_valid_image(
                self.__class__.allowed_extensions, bytesio, filename
            )
            is False
        )

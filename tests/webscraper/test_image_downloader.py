from pathlib import Path
from typing import Callable

import pytest
from pytest_mock import MockerFixture
from responses import RequestsMock

from webscraper.image_downloader import Downloader


@pytest.fixture()
def prepare_downloader(tmp_path: Path) -> Downloader:
    yield Downloader(tmp_path)


@pytest.mark.unittests
class TestDownloaderInit:
    def test_object_upload_folder_should_have_proper_value(
        self, tmp_path: Path
    ) -> None:
        downloader = Downloader(tmp_path)
        assert downloader.upload_folder == tmp_path


@pytest.mark.unittests
class TestDownloaderSaveImage:
    def test_convert_string_into_bytes_object_should_be_called(
        self, prepare_downloader: Downloader, mocker: MockerFixture
    ) -> None:
        convert_string_into_bytes_object_mock = mocker.patch(
            "webscraper.image_downloader.Downloader._convert_string_into_bytes_object"
        )
        mocker.patch("webscraper.image_downloader.Downloader._write_bytes_to_file")
        filename, file_src = "file_name", "file_src"
        prepare_downloader.save_image(filename, file_src)

        convert_string_into_bytes_object_mock.assert_called_once_with(file_src)

    def test_write_bytes_to_file_should_be_called(
        self, prepare_downloader: Downloader, mocker: MockerFixture
    ) -> None:
        filename, file_src = "file_name", "file_src"

        convert_string_into_bytes_object_mock = mocker.patch(
            "webscraper.image_downloader.Downloader._convert_string_into_bytes_object"
        )
        convert_string_into_bytes_object_mock.return_value = file_src
        write_bytes_to_file_mock = mocker.patch(
            "webscraper.image_downloader.Downloader._write_bytes_to_file"
        )

        prepare_downloader.save_image(filename, file_src)
        write_bytes_to_file_mock.assert_called_once_with(filename, file_src)


@pytest.mark.integtests
class TestWriteBytesToFile:
    def test_file_should_have_proper_name_and_be_in_correct_place(
        self,
        tmp_path: Path,
        mocker: MockerFixture,
        bytes_generator: Callable[[str], bytes],
    ) -> None:
        filename = "correct01.jpeg"
        image_bytes = bytes_generator(filename)
        convert_string_into_bytes_object_mock = mocker.patch(
            "webscraper.image_downloader.Downloader._convert_string_into_bytes_object"
        )
        convert_string_into_bytes_object_mock.return_value = image_bytes
        Downloader(tmp_path).save_image(filename, "")
        file = Path(tmp_path / filename)
        assert file.exists()


@pytest.mark.unittests
class TestConvertStringIntoBytesObject:
    file_scr = ("https://imagocms.com",)

    @pytest.fixture
    def mocked_responses(self):
        with RequestsMock() as rsps:
            yield rsps

    @pytest.mark.parametrize("file_src", file_scr)
    def test_request_get_and_content_should_be_called(
        self,
        mocker: MockerFixture,
        prepare_downloader: Downloader,
        mocked_responses: RequestsMock,
        file_src: str,
    ):
        write_bytes_to_file_mocker = mocker.patch(
            "webscraper.image_downloader.Downloader._write_bytes_to_file"
        )

        filename, bytes_object = "test_filename", b"ImagoCmsRulez"
        mocked_responses.get(
            file_src,
            body=bytes_object,
            status=200,
        )

        prepare_downloader.save_image(filename, file_src)
        write_bytes_to_file_mocker.assert_called_once_with(filename, bytes_object)

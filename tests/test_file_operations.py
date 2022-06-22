from utilities import file_operations

from unittest.mock import patch

import pytest


class TestAllowedFile:
    allowed_extensions = {"jpeg", "png"}
    correct_files = ["correct01.jpeg", "correct02.png"]
    incorrect_files = ["incorrect01.jpg.sql", "incorrect02.pdf", "incorrect03.jpg"]

    @patch("imghdr.what")
    @pytest.mark.parametrize("make_FileStorage", ["correct01.jpeg"], indirect=True)
    def test_imghdr_module_should_be_called(self, imghdr_mock, make_FileStorage):
        imghdr_mock.return_value = "jpeg"
        file_operations.allowed_file(
            self.__class__.allowed_extensions, make_FileStorage
        )
        imghdr_mock.assert_called_once()

    @pytest.mark.parametrize("make_FileStorage", correct_files, indirect=True)
    def test_return_true_if_extension_is_correct(self, make_FileStorage):
        assert (
            file_operations.allowed_file(
                self.__class__.allowed_extensions, make_FileStorage
            )
            is True
        )

    @pytest.mark.parametrize("make_FileStorage", incorrect_files, indirect=True)
    def test_return_false_if_extension_is_incorrect(self, make_FileStorage):
        assert (
            file_operations.allowed_file(
                self.__class__.allowed_extensions, make_FileStorage
            )
            is False
        )


class TestUploadFile:
    def test_secure_filename_should_be_called(self):
        ...

    def test_change_name_should_be_called(self):
        ...

    def test_os_save_should_be_called(self):
        ...

    def test_os_path_join_should_be_called(self):
        ...

    def test_filename_should_be_return(self):
        ...


class TestDownloadImages:
    def test_os_path_join_should_be_called(self):
        ...

    def test_write_should_be_called(self):
        ...

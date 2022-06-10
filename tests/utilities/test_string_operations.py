from utilities import string_operations

from unittest.mock import patch

import pytest


class TestChangeName:

    filenames = (
        ("test_filename.JPG", ".jpg"),
        ("test_filename.jpeg", ".jpeg"),
        ("test_filename.jpg.webp", ".webp"),
        ("TEST_FILENAME.WEBP.JPEG", ".jpeg"),
    )

    @patch('uuid.uuid4')
    @pytest.mark.parametrize("file_name_and_extension", filenames)
    def test_calls_the_(self, uuid4_mock, file_name_and_extension):
        uuid4 = "4d43171d-174b-4501-835b-da5abfbc49d4"
        filename, extension = file_name_and_extension

        uuid4_mock.return_value = uuid4

        new_filename = string_operations.change_name(filename)

        uuid4_mock.assert_called_once()
        assert new_filename == uuid4 + extension


class TestCheckCorrectnessOfTheData:
    ...

class TestPrepareSrcAndAlt:
    ...

from utilities import string_operations

from unittest.mock import patch
from pathlib import Path

import pytest


class TestChangeName:

    filenames = (
        ("test_filename.JPG", ".jpg"),
        ("test_filename.jpeg", ".jpeg"),
        ("test_filename.jpg.webp", ".webp"),
        ("TEST_FILENAME.WEBP.JPEG", ".jpeg"),
    )

    @patch("uuid.uuid4")
    @pytest.mark.parametrize(("file_name", "extension"), filenames)
    def test_extension_should_be_correct_and_uuid4_module_should_be_called(
        self, uuid4_mock, file_name, extension
    ):
        uuid4 = "4d43171d-174b-4501-835b-da5abfbc49d4"
        uuid4_mock.return_value = uuid4

        new_filename = string_operations.change_name(file_name)

        uuid4_mock.assert_called_once()
        assert new_filename == uuid4 + extension


class TestCheckCorrectnessOfTheData:
    forbidden = '"#$%^&*\\()=, „”-/<>|;ąćęłńóśźż{}[]`'
    data_with_none = (
        (None, None),
        ("login", None),
        (None, "password"),
        ("", ""),
        ("login", ""),
        ("", "password"),
    )
    too_long_data = (
        ("fyeUI26DviVq0kFlpsii", "password", "test@test.pl"),
        ("login", "e5hUMP4XirY1qeYXpI5ItNgix", "test@test.pl"),
        (
            "",
            "password",
            "BSkFzGiotqQ5hGS9EhwsgViesK8c8k1h1WVYF1CyONQRy2EUMTbKgcLycXJI773z@test.pl",
        ),
    )
    data_with_forbidden_char = (
        ("login", "pas#sword", "test@test.pl"),
        ("fyeUI26DviV$%", "password", "test@test.pl"),
        ("login", "password", "tes()=,;t@test.pl"),
        ("fyeUI26DviVq0kFlpsii", "password", "test<>|;@test.pl"),
        ("fyeUI26DviVq0kFlpsii", "pas#sword", "test@ąćę.pl"),
    )
    correct_login_and_password = (("login", "password"),)

    @pytest.mark.parametrize(("login", "password"), data_with_none)
    def test_empty_data_should_not_pass(self, login, password):
        assert string_operations.check_correctness_of_the_data(login, password) is False

    @pytest.mark.parametrize(("login", "password", "email"), too_long_data)
    def test_too_long_data_should_be_not_accepted(self, login, password, email):
        assert (
            string_operations.check_correctness_of_the_data(login, password, email)
            is False
        )

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_email_address_without_at_symbol_should_be_not_accepted(
        self, login, password
    ):
        email = "test_email"
        assert (
            string_operations.check_correctness_of_the_data(login, password, email)
            is False
        )

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_email_address_with_more_than_one_at_symbol_should_be_not_accepted(
        self, login, password
    ):
        email = "test_email@wp@wp.pl"
        assert (
            string_operations.check_correctness_of_the_data(login, password, email)
            is False
        )

    @pytest.mark.parametrize(("login", "password", "email"), data_with_forbidden_char)
    def test_data_with_forbidden_char_should_be_not_accepted(
        self, login, password, email
    ):
        assert (
            string_operations.check_correctness_of_the_data(login, password, email)
            is False
        )

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_email_address_is_no_needed_to_pass(self, login, password):
        assert string_operations.check_correctness_of_the_data(login, password) is True

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_correct_data_with_email_should_return_true(self, login, password):
        email = "test@test.pl"
        assert (
            string_operations.check_correctness_of_the_data(login, password, email)
            is True
        )


class TestPrepareSrcAndAlt:
    @pytest.fixture()
    def prepare_ResultSet(self, example_website):
        yield example_website.select("img.full-image")

    def test_output_data_should_be_a_dict(self, prepare_ResultSet):
        assert isinstance(
            string_operations.prepare_src_and_alt(prepare_ResultSet), dict
        )

    def test_output_should_have_valid_data(self, prepare_ResultSet):
        valid_data = {
            "https://example-website.com/contents/1mFjN19GzihJ9K21FoNbeuZGxLZJJQ2s.jpg": "Short alt",
            "https://www.example-another-image.com.pl/contents/2022/06/normal/or_not/6gOXbkxrkHMITAOiNdDsuWu14sIMihrM."
            "jpeg": "This time alt is much longer than before. Sometimes we have to deal with it.",
        }
        assert string_operations.prepare_src_and_alt(prepare_ResultSet) == valid_data

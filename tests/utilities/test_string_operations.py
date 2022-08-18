import uuid
from pathlib import Path

import pytest
from pytest_mock import MockerFixture
import bs4

from utilities import string_operations


@pytest.mark.unittests
class TestChangeName:
    filenames = (
        ("test_filename.JPG", ".jpg"),
        ("test_filename.jpeg", ".jpeg"),
        ("test_filename.jpg.webp", ".webp"),
        ("TEST_FILENAME.WEBP.JPEG", ".jpeg"),
    )

    def test_uuid4_module_should_be_called(self, mocker: MockerFixture) -> None:
        uuid4_mock = mocker.patch("uuid.uuid4")
        string_operations.change_name("test_filename.JPG")

        uuid4_mock.assert_called_once()

    @pytest.mark.parametrize(("file_name", "extension"), filenames)
    def test_extension_should_be_correct(
        self, monkeypatch: pytest.MonkeyPatch, file_name: str, extension: str
    ) -> None:
        fake_uuid4 = "4d43171d-174b-4501-835b-da5abfbc49d4"
        monkeypatch.setattr(uuid, "uuid4", lambda: fake_uuid4)

        assert string_operations.change_name(file_name) == fake_uuid4 + extension


@pytest.mark.unittests
class TestCheckCorrectnessOfTheData:
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
    def test_empty_data_should_not_pass(self, login: str, password: str) -> None:
        assert string_operations.is_data_correct(login, password) is False

    @pytest.mark.parametrize(("login", "password", "email"), too_long_data)
    def test_too_long_data_should_be_not_accepted(
        self, login: str, password: str, email: str
    ):
        assert string_operations.is_data_correct(login, password, email) is False

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_email_address_without_at_symbol_should_be_not_accepted(
        self, login: str, password: str
    ) -> None:
        email = "test_email"
        assert string_operations.is_data_correct(login, password, email) is False

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_email_address_with_more_than_one_at_symbol_should_be_not_accepted(
        self, login: str, password: str
    ) -> None:
        email = "test_email@wp@wp.pl"
        assert string_operations.is_data_correct(login, password, email) is False

    @pytest.mark.parametrize(("login", "password", "email"), data_with_forbidden_char)
    def test_data_with_forbidden_char_should_be_not_accepted(
        self, login: str, password: str, email: str
    ) -> None:
        assert string_operations.is_data_correct(login, password, email) is False

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_email_address_is_no_needed_to_pass(
        self, login: str, password: str
    ) -> None:
        assert string_operations.is_data_correct(login, password) is True

    @pytest.mark.parametrize(("login", "password"), correct_login_and_password)
    def test_correct_data_with_email_should_return_true(
        self, login: str, password: str
    ) -> None:
        email = "test@test.pl"
        assert string_operations.is_data_correct(login, password, email) is True


@pytest.mark.integtests
class TestPrepareSrcAndAlt:
    @pytest.fixture(scope="class")
    def example_website(self) -> bs4.BeautifulSoup:
        """Loads HTML document and prepare BeautifulSoup object based on document data.

        Returns: BeautifulSoup object."""
        example_website_path = (
            Path(__file__).parent / "../fixtures/example_data/example_website.html"
        )
        with open(example_website_path, "r") as f:
            yield bs4.BeautifulSoup(f.read(), "html.parser")

    @pytest.fixture(scope="class")
    def prepare_result_set(
        self, example_website: bs4.BeautifulSoup
    ) -> bs4.element.ResultSet:
        """Prepares ResultSet object based on BeautifulSoup object.

        Returns: ResultSet object."""
        return example_website.select("img.full-image")

    def test_output_data_should_be_a_dict(
        self, prepare_result_set: bs4.element.ResultSet
    ) -> None:
        assert isinstance(
            string_operations.prepare_src_and_alt(prepare_result_set), dict
        )

    def test_output_should_have_valid_data(
        self, prepare_result_set: bs4.element.ResultSet
    ) -> None:
        valid_data = {
            "https://example-website.com/contents/"
            "1mFjN19GzihJ9K21FoNbeuZGxLZJJQ2s.jpg": "Short alt",
            "https://www.example-another-image.com.pl/contents/2022/06/normal/"
            "or_not/6gOXbkxrkHMITAOiNdDsuWu14sIMihrM.jpeg": "This time"
            " alt is much longer than before. Sometimes we have to deal with it.",
        }
        assert string_operations.prepare_src_and_alt(prepare_result_set) == valid_data

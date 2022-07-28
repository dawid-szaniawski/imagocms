from requests.models import Response

from webscraper.scraper import scraper

from bs4 import BeautifulSoup
from bs4.element import ResultSet


class TestGetHtmlDom:
    """All of this can be done at once. Make fixture that mocks get and bs4 (scope="class")."""

    def test_requests_get_should_be_called(self):
        ...

    def test_beautifulsoup_should_be_called(self):
        ...

    def test_return_value_type_should_be_beautiful_soup(self):
        ...


class TestFindAllImages:
    def test_select_method_should_be_called_with_args(self):
        ...

    def test_return_value_type_should_be_result_set(self):
        ...


class TestConvertStringsIntoResponseObjects:
    def test_get_should_be_called_for_all_of_tuple_elements(self):
        ...

    def test_return_value_type_should_be_list_with_response_objects(self):
        ...


class TestFindNextPage:
    ...

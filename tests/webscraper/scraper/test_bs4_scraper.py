from bs4 import BeautifulSoup
from bs4.element import ResultSet
import pytest
from pytest_mock import MockerFixture
import responses

from webscraper.scraper.bs4_scraper import Bs4Scraper
from webscraper.scraper.models import ImagesSource


@pytest.fixture
def prepare_bs4_scraper(
    images_source_mocker: ImagesSource, mocked_responses: responses.RequestsMock
) -> Bs4Scraper:

    mocked_responses.get(images_source_mocker.website_url)

    yield Bs4Scraper(images_source_mocker)


@pytest.mark.unittests
class TestBs4ScraperInit:
    def test_images_source_should_have_proper_value(
        self, images_source_mocker: ImagesSource, prepare_bs4_scraper: Bs4Scraper
    ) -> None:

        assert prepare_bs4_scraper.images_source == images_source_mocker

    def test_get_html_dom_should_be_called(
        self, images_source_mocker: ImagesSource, mocker: MockerFixture
    ) -> None:

        get_html_dom = mocker.patch(
            "webscraper.scraper.bs4_scraper.Bs4Scraper.get_html_dom"
        )

        Bs4Scraper(images_source_mocker)

        get_html_dom.assert_called_once()


@pytest.mark.unittests
class TestBs4ScraperGetHTMLDOM:
    @responses.activate
    def test_request_get_should_be_called(
        self,
        images_source_mocker: ImagesSource,
        mocked_responses: responses.RequestsMock,
    ) -> None:

        images_source_website = responses.get(images_source_mocker.website_url)

        Bs4Scraper(images_source_mocker)

        assert images_source_website.call_count == 1

    def test_return_value_should_be_beautiful_soup_object(
        self, prepare_bs4_scraper: Bs4Scraper
    ) -> None:
        beautiful_soup = prepare_bs4_scraper.get_html_dom()

        assert isinstance(beautiful_soup, BeautifulSoup)


@pytest.mark.integtests
class TestBs4ScraperFindImageHolders:
    def test_return_value_should_have_proper_type_and_length(
        self, mocker: MockerFixture, images_source_mocker: ImagesSource, bs4_html_doc
    ) -> None:
        get_html_dom = mocker.patch(
            "webscraper.scraper.bs4_scraper.Bs4Scraper.get_html_dom"
        )
        get_html_dom.return_value = bs4_html_doc
        image_holders = Bs4Scraper(images_source_mocker).find_image_holders()
        assert isinstance(image_holders, ResultSet)
        assert len(image_holders) == 2


@pytest.mark.integtests
class TestBs4ScraperFindImageSrcAndAlt:
    def test_the_output_should_have_correct_value(
        self, prepare_bs4_scraper: Bs4Scraper
    ) -> None:
        div_data = """<div class="simple-image"><a href="https://webludus.pl">
                        <img src="https://webludus.pl/img/image.jpg" alt="Imagocms"></a>
                        </div>"""
        soup = BeautifulSoup(div_data, "html.parser")
        div = soup.div
        bs4_scraper = prepare_bs4_scraper
        src, alt = bs4_scraper.find_image_src_and_alt(div)
        assert src == "https://webludus.pl/img/image.jpg"
        assert alt == "Imagocms"

    def test_in_case_of_type_error_return_none(
        self, prepare_bs4_scraper: Bs4Scraper
    ) -> None:
        div_data = """<div class="simple-image"></div>"""
        soup = BeautifulSoup(div_data, "html.parser")
        div = soup.div
        bs4_scraper = prepare_bs4_scraper
        assert bs4_scraper.find_image_src_and_alt(div) is None

    def test_in_case_of_key_error_return_none(
        self, prepare_bs4_scraper: Bs4Scraper
    ) -> None:
        div_data = """<div class="simple-image"><a href="https://webludus.pl">
                                <img src="https://webludus.pl/img/image.jpg"></a>
                                </div>"""
        soup = BeautifulSoup(div_data, "html.parser")
        div = soup.div
        bs4_scraper = prepare_bs4_scraper
        assert bs4_scraper.find_image_src_and_alt(div) is None


class TestBs4ScraperFindImagePageUrl:
    ...


class TestBs4ScraperSetNextPage:
    ...

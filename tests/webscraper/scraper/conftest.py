from pytest import fixture
from bs4 import BeautifulSoup

from webscraper.scraper.models import ImagesSource


@fixture(scope="class")
def images_source_mocker() -> ImagesSource:
    yield ImagesSource(
        website_url="https://webludus.pl",
        images_container_class="simple-image",
        pagination_class="pagination",
        pages_to_scan=1,
    )


@fixture
def html_doc():
    yield """<html><head><title>BS4 Mock</title></head>
    <body>
        <div class="simple-image">
            <a href="https://webludus.pl">
                <img src="https://webludus.pl/img/image.jpg" alt="Imagocms">
            </a>
        </div>
        <div class="simple-image">
            <a href="https://webludus.pl">
                <img src="https://webludus.pl/img/image.jpg">
            </a>
        </div>
    </body></html>"""


@fixture
def bs4_html_doc(html_doc) -> BeautifulSoup:
    yield BeautifulSoup(html_doc, "html.parser")

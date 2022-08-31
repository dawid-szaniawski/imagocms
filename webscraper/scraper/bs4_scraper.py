from requests import get
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from webscraper.scraper.models import ImagesSource


class Bs4Scraper:
    def __init__(self, images_source: ImagesSource):
        self.images_source = images_source
        self.html_dom = self.get_html_dom()

    def get_html_dom(self) -> BeautifulSoup:
        """Convert string containing URL address into Response object,
        and then convert it into BeautifulSoup object.

        Returns:
            BeautifulSoup object containing HTML DOM."""
        request = get(self.images_source.website_url)
        return BeautifulSoup(request.text, "html.parser")

    def find_image_holders(self) -> ResultSet:
        return self.html_dom.select("div." + self.images_source.images_container_class)

    @staticmethod
    def find_image_src_and_alt(div: Tag) -> tuple[str, str] | None:
        image = div.find("img")
        try:
            return image["src"], image["alt"]
        except TypeError:
            pass
        except KeyError:
            pass

    @staticmethod
    def find_image_page_url(div: Tag) -> str:
        return div.find("a")["href"]

    def set_next_page(self) -> None:
        """Search the HTML DOM for the next page URL address."""

        def find_pagination_div(html_dom: BeautifulSoup, pagination_class: str):
            return html_dom.find(class_=pagination_class)

        def is_url_correct(new_url, current_url):
            return False if len(new_url) < 2 or new_url == current_url else True

        pagination_div = find_pagination_div(
            self.html_dom, self.images_source.pagination_class
        )
        next_url = pagination_div.find("a")["href"]

        next_url_index = 1
        while not is_url_correct(next_url, self.images_source.website_url):
            next_url_index += 1
            next_url = pagination_div.find_all("a")[next_url_index]["href"]

        self.images_source.website_url = next_url
        self.html_dom = self.get_html_dom()

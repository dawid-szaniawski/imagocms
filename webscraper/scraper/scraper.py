from requests import get
from requests.models import Response

from bs4 import BeautifulSoup
from bs4.element import ResultSet


def get_html_dom(website_url: str) -> BeautifulSoup:
    """Args:
        website_url: string containing url of scraped website
    Returns:
        BeautifulSoup object containing HTML DOM."""
    request = get(website_url)
    return BeautifulSoup(request.text, "html.parser")


def find_all_images(html_dom: BeautifulSoup, img_class: str) -> ResultSet:
    """Takes the HTML DOM and looks for images with the provided class.

    Args:
        html_dom: the BeautifulSoup object containing HTML DOM.
        img_class: class of the images in the HTML DOM.

    Returns:
        ResultSet object containing all images with provided class."""
    return html_dom.select(img_class)


def convert_strings_into_response_objects(
    images_source: tuple[str, ...]
) -> list[Response, ...]:
    """Changes the tuple of image sources into list with Response objects.

    Args:
        images_source: list of strings containing img src from HTML DOM.

    Returns:
        list of request.models.Response objects."""
    return [get(src) for src in images_source]


def find_next_page(
    html_dom: BeautifulSoup, website_url: str, pagination_class: str
) -> str:
    """Search the HTML DOM for the next page URL address.

    Args:
        html_dom: BeautifulSoup object containing HTML DOM.
        website_url: string containing url of scraped website.
        pagination_class: string containing a class of "a" object, which contains a hyperlink to go to the next subpage.

    Returns:
        URL address of the next page."""
    next_url = html_dom.find(class_=pagination_class).find("a")["href"]
    if len(next_url) < 2 or next_url == website_url:
        next_url_index = 2
        while len(next_url) < 2 or next_url == website_url:
            next_url = html_dom.find(class_=pagination_class).find_all("a")[
                next_url_index
            ]["href"]
            next_url_index += 1
    return next_url

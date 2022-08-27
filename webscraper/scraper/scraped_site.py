from dataclasses import dataclass


@dataclass
class ImageSource:
    """An object that represents the page being scraped.
    Takes two arguments when creating the object.

    Args:
        website_url (str): string containing url of scraped website
        images_container_class (str): class of the images in the HTML DOM,
        pagination_class (str): class of the pagination buttons in the HTML DOM."""

    website_url: str
    images_container_class: str
    pagination_class: str
    pages_to_scan: int

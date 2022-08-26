from dataclasses import dataclass, KW_ONLY


@dataclass
class ImageSource:
    """An object that represents the page being scraped.
    Takes two arguments when creating the object.

    Args:
        website_url (str): string containing url of scraped website
        image_class (str): class of the images in the HTML DOM,
        pagination_class (str): class of the pagination buttons in the HTML DOM."""

    website_url: str
    image_class: str
    pagination_class: str
    pages_to_scan: int

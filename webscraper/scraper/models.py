from dataclasses import dataclass, asdict


@dataclass
class ImageSource:
    """An object that represents the page being scraped.
    Takes two arguments when creating the object."""

    website_url: str
    image_class: str
    pagination_class: str
    pages_to_scan: int


@dataclass(frozen=True)
class Image:
    source: str
    title: str
    filename: str
    url_address: str
    author_id: int

    @property
    def as_dict(self):
        return asdict(self)

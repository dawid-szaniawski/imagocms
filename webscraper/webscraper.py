from webscraper.scraper.models import ImageSource, Image
from webscraper.scraper.scraper import Bs4Scraper
from utilities.string_operations import change_name


class WebScraper:
    """Website scraper tool.
    Scans websites for images, then downloads the images to disk and returns information
    about downloaded files.

     Args:
         website_data: a list of sqlite3.Row object. It should contain minimum three
            columns:
            - website_url: string containing url of scraped website,
            - images_container_class: string containing class of the images container,
            - website_user_id: Integer. User ID from database,
            - pagination_class: *optional* string containing a class of link
                to go to the next subpage,
            - pages_to_scan: the number of consecutive subpages of the site
                to be scanned."""

    def __init__(self, website_data: dict[str, str | int]):
        self.author_id = website_data["website_user_id"]
        self.image_source = self.prepare_image_source(website_data)
        self._synchronization_data = []

    def start_synchronization(self) -> None:
        """The method that starts the synchronization process."""
        self.synchronization_data = self._synchronization_process()

    @staticmethod
    def prepare_image_source(website):
        try:
            pagination_class = website["pagination_class"]
        except KeyError:
            pagination_class = "pagination"
        return ImageSource(
            website_url=website["website_url"],
            image_class=website["images_container_class"],
            pagination_class=pagination_class,
            pages_to_scan=website["pages_to_scan"],
        )

    def _synchronization_process(self) -> set[Image]:
        scraper = Bs4Scraper(self.image_source)
        images = set()
        while self.image_source.pages_to_scan > 0:
            images.update(self._prepare_images_data(scraper, self.author_id))
            if self.image_source.pages_to_scan > 1:
                scraper.set_next_page()
            self.image_source.pages_to_scan -= 1
        return images

    @staticmethod
    def _prepare_images_data(scraper: Bs4Scraper, author_id: int) -> list[Image]:
        image_holders = scraper.find_image_holders()
        images = []
        for div in image_holders:
            try:
                image_src, image_alt = scraper.find_image_src_and_alt(div)
            except TypeError:
                continue
            image_name = change_name(image_src)
            image_url_address = scraper.find_image_page_url(div)
            images.append(
                Image(
                    source=image_src,
                    title=image_alt,
                    filename=image_name,
                    url_address=image_url_address,
                    author_id=author_id,
                )
            )
        return images

    @property
    def synchronization_data(self) -> list[dict]:
        """Returns the synchronization results.

        Returns:
            list of  tuples containing website_user_id, image.filename, image.title."""
        return self._synchronization_data

    @synchronization_data.setter
    def synchronization_data(self, images: set[Image]) -> None:
        for image in images:
            self._synchronization_data.append(image.as_dict)

    def clear_synchronization_data(self) -> None:
        """Set synchronization data as an empty list."""
        self._synchronization_data = []

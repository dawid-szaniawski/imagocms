from sqlite3 import Row
from pathlib import Path

from requests import Response

from webscraper.scraper.scraped_site import ImageSource
from webscraper.scraper.scraper import convert_strings_into_response_objects
from utilities.string_operations import prepare_src_and_alt, change_name
from utilities.file_operations import download_images


class WebScraper:
    """Website scraper tool.
    Scans websites for images, then downloads the images to disk and returns information
     about downloaded files.

     Args:
         upload_folder: path where the files should be saved.
         websites_data: a list of sqlite3.Row object. It should contain minimum three
            columns:
            - website_url: string containing url of scraped website,
            - image_class: string containing class of the images in the HTML DOM,
            - website_user_id: Integer. User ID from database,
            - pagination_class: *optional* string containing a class of link
                to go to the next subpage,
            - pages_to_scan: the number of consecutive subpages of the site
                to be scanned."""

    def __init__(self, upload_folder: Path, websites_data: list[Row, ...]):
        self._synchronization_data = []
        self.upload_folder = upload_folder
        self.websites_data = websites_data

    def start_synchronization(self) -> None:
        """The method that starts the synchronization process."""
        for website in self.websites_data:
            pagination_class = (
                website["pagination_class"]
                if website["pagination_class"]
                else "pagination"
            )
            site = ImageSource(
                website_url=website["website_url"],
                image_class=website["image_class"],
                pagination_class=pagination_class,
            )
            self._iterate_over_pages(
                pages=website["pages_to_scan"],
                site=site,
                website_user_id=website["website_user_id"],
            )

    def _iterate_over_pages(
        self, pages: int, site: ImageSource, website_user_id: str
    ) -> None:
        """Scan over pages and download selected (by image class) images.

        Args:
            pages: how many pages of the website should it scan
            site: the ImageSource object. Represents the scraped website.
            website_user_id: string containing user ID from DB. Used for extending the
                synchronization data."""
        while pages > 0:
            image_src_and_alt, image_names, image_requests = self._prepare_images_data(
                site
            )

            download_images(dict(zip(image_names, image_requests)), self.upload_folder)
            self._extend_synchronization_data(
                website_user_id, image_names, list(image_src_and_alt.values())
            )

            if pages > 1:
                site.go_next_page()

            pages -= 1

    @staticmethod
    def _prepare_images_data(
        site: ImageSource,
    ) -> tuple[dict[str, str], list[str, ...], list[Response, ...]]:
        """Prepare images data from an ImageSource object.

        Args:
            site: the ImageSource object. Represents the scraped website.

        Returns:
            - dictionary with image source and alt,
            - list with image names,
            - list with image request objects."""
        image_src_and_alt = prepare_src_and_alt(site.all_images)
        image_src = tuple(image_src_and_alt.keys())
        image_names = [change_name(file_src) for file_src in image_src]
        image_requests = convert_strings_into_response_objects(image_src)
        return image_src_and_alt, image_names, image_requests

    def _extend_synchronization_data(
        self, user_id: str, image_names: list[str, ...], image_alts: list[str, ...]
    ) -> None:
        """Add new synchronization data into synchronization_data variable.

        Args:
            user_id: string containing user ID from DB.
            image_names: filenames of images.
            image_alts: alts of images. It will be title of the images."""
        self._synchronization_data.extend(
            [
                (user_id, filename, title)
                for filename, title in zip(image_names, image_alts)
            ]
        )

    def show_synchronization_data(self) -> list[tuple, ...]:
        """Returns the synchronization results and then clean the data.

        Returns:
            list of  tuples containing website_user_id, image.filename, image.title."""
        try:
            return self._synchronization_data
        finally:
            self._clear_synchronization_data()

    def _clear_synchronization_data(self) -> None:
        """Set synchronization data as an empty list."""
        self._synchronization_data = []

from pathlib import Path
import sqlite3

from imagocms.db import get_db
from webscraper.webscraper import WebScraper
from webscraper.image_downloader import Downloader


class ExternalWebsitesSynchronizer:
    """Prepares demo data."""

    def __init__(self, upload_folder: Path):
        self.upload_folder = upload_folder
        self.images_data = []

    def prepare_images_from_external_websites(self):
        self._prepare_images_data()
        self._add_images_into_database()
        self._download_images()

    def _prepare_images_data(self) -> None:
        external_websites_data = self._ext_websites_data_from_db()
        for website in external_websites_data:
            web_scraper = WebScraper(website)
            web_scraper.start_synchronization()
            self.images_data.extend(web_scraper.synchronization_data)

    def _add_images_into_database(self) -> None:
        db = get_db()
        for image in self.images_data:
            try:
                db.execute(
                    """
                    INSERT INTO images (author_id, filename, title, source, accepted)
                    VALUES (?, ?, ?, ?, 1)""",
                    (
                        image["author_id"],
                        image["filename"],
                        image["title"],
                        image["url_address"],
                    ),
                )
                db.commit()
            except sqlite3.IntegrityError:
                self.images_data.remove(image)

    @staticmethod
    def _ext_websites_data_from_db() -> list[dict]:
        def sqlite_row_into_dict(sqlite_objects: list[sqlite3.Row]) -> list[dict]:
            images_sources = []
            for row in sqlite_objects:
                images_sources.append(
                    {
                        "website_user_id": row["website_user_id"],
                        "website_url": row["website_url"],
                        "images_container_class": row["images_container_class"],
                        "pages_to_scan": row["pages_to_scan"],
                    }
                )

            return images_sources

        db = get_db()
        ext_websites_dict = sqlite_row_into_dict(
            db.execute(
                """SELECT
                website_user_id,
                website_url,
                images_container_class,
                pages_to_scan,
                pagination_class
                FROM ext_websites"""
            ).fetchall()
        )
        return ext_websites_dict

    def _download_images(self) -> None:
        downloader = Downloader(self.upload_folder)
        for image in self.images_data:
            downloader.save_image(image["filename"], image["source"])

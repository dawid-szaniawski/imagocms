"""Prepares demo data."""
from pathlib import Path

from imagocms.db import get_db
from webscraper.webscraper import WebScraper


def prepare_images_from_external_websites(upload_folder: Path) -> None:
    """Starts WebScraper, a tool that prepares demo data based on external websites.

    Args:
        upload_folder: path where the files should be saved."""
    db = get_db()
    websites_data = db.execute(
        "SELECT website_user_id, website_url, image_class, pages_to_scan, pagination_class FROM ext_websites"
    ).fetchall()
    web_scraper = WebScraper(upload_folder, websites_data)
    web_scraper.start_synchronization()
    for i in web_scraper.show_synchronization_data():
        db.execute(
            "INSERT INTO images (author_id, filename, title, accepted) VALUES (?, ?, ?, 1)",
            (i[0], i[1], i[2]),
        )
        db.commit()

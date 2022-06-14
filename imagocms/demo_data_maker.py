"""Prepares demo data."""
from imagocms.db import get_db
from webscraper.webscraper import start_sync


def prepare_images_from_external_websites() -> None:
    """Starts WebScraper, a tool that prepares demo data based on external websites."""
    db = get_db()
    websites_data = db.execute(
        "SELECT website_user_id, website_url, image_class FROM ext_websites"
    ).fetchall()
    sync_data = start_sync(websites_data)
    for i in sync_data:
        db.execute(
            "INSERT INTO images (author_id, filename, title, accepted) VALUES (?, ?, ?, 1)",
            (i[0], i[1], i[2]),
        )
        db.commit()

"""Website scraper tool.
Scans websites for images, then downloads the images to disk and returns information about downloaded files."""
from webscraper.scraper.scraped_site import ImageSource
from utilities.string_operations import prepare_src_and_alt, change_name
from utilities.file_operations import download_images
from pathlib import Path


def start_sync(upload_folder: Path, websites_data: list, pages: int = 2) -> list:
    """The function that starts the synchronization process.
    Takes one argument on the basis of which it scans sites and gets the appropriate graphics.

    Args:
        upload_folder: path where the files should be saved.
        websites_data: a list of sqlite3.Row object. It should contain minimum three columns:
            - website_url: string containing url of scraped website,
            - image_class: string containing class of the images in the HTML DOM,
            - website_user_id: Integer. User ID from database,
            - pagination_class: *optional* string containing a class of link to go to the next subpage.
        pages: the number of consecutive subpages of the site to be scanned.

    Returns:
        list of  tuples containing website_user_id, images.filename, images.title."""
    to_return = []
    for website in websites_data:
        additional_pages = pages

        site = ImageSource(
            website_url=website["website_url"],
            image_class=website["image_class"],
            pagination_class="pagination",
        )

        while additional_pages > 0:
            site_src_and_alt = prepare_src_and_alt(site.all_images)
            site_names = [change_name(file_src) for file_src in site_src_and_alt.keys()]
            site_requests = site.get_requests(site_src_and_alt.keys())
            download_images(dict(zip(site_names, site_requests)), upload_folder)

            to_return.extend(
                [
                    (website["website_user_id"], filename, title)
                    for filename, title in zip(site_names, site_src_and_alt.values())
                ]
            )
            if additional_pages > 1:
                site.go_next_page()

            additional_pages -= 1

    return to_return

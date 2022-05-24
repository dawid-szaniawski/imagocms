"""Website scraper tool.
Scans websites for images, then downloads the images to disk and returns information about downloaded files."""
from webscraper.scraper.scraped_site import ImageSource
from utilities.string_operations import prepare_src_and_alt, change_name
from utilities.file_operations import download_images


def start_sync(websites_data: list, pages: int = 1) -> list:
    """The function that starts the synchronization process.
    Takes one argument on the basis of which it scans sites and gets the appropriate graphics.

    Args:
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
        if "pagination_class" in website:
            site = ImageSource(
                website["website_url"],
                website["image_class"],
                website["pagination_class"],
            )
        else:
            site = ImageSource(
                website["website_url"], website["image_class"], "pagination"
            )

        site_src_and_alt = prepare_src_and_alt(site.all_images)
        site_names = [change_name(file_src) for file_src in site_src_and_alt.keys()]
        site_requests = site.get_requests(site_src_and_alt.keys())
        download_images(dict(zip(site_names, site_requests)))

        to_return.extend(
            [
                (website["website_user_id"], filename, title)
                for filename, title in zip(site_names, site_src_and_alt.values())
            ]
        )

        while additional_pages > 1:
            site.go_next_page()
            site_src_and_alt = prepare_src_and_alt(site.all_images)
            site_names = [change_name(file_src) for file_src in site_src_and_alt.keys()]
            site_requests = site.get_requests(site_src_and_alt.keys())
            download_images(dict(zip(site_names, site_requests)))

            to_return.extend(
                [
                    (website["website_user_id"], filename, title)
                    for filename, title in zip(site_names, site_src_and_alt.values())
                ]
            )
            additional_pages -= 1

    return to_return

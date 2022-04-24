from webscraper.scraper import scraper, scraped_site
from utilities.string_operations import prepare_src_and_alt, change_name
from utilities.file_operations import download_images


def start_sync(websites_data):
    to_return = []
    for website in websites_data:
        site = scraped_site.ImageSource(website['website_url'], website['image_class'])
        site_src_and_alt = prepare_src_and_alt(site.all_images)
        site_names = [change_name(file_src) for file_src in site_src_and_alt.keys()]
        site_requests = site.get_requests(site_src_and_alt.keys())
        download_images(dict(zip(site_names, site_requests)))

        to_return.extend(
            [(website['website_user_id'], filename, title)
             for filename, title in zip(site_names, site_src_and_alt.values())])

        site.go_next_page()
        site_src_and_alt = prepare_src_and_alt(site.all_images)
        site_names = [change_name(file_src) for file_src in site_src_and_alt.keys()]
        site_requests = site.get_requests(site_src_and_alt.keys())
        download_images(dict(zip(site_names, site_requests)))

        to_return.extend(
            [(website['website_user_id'], filename, title)
             for filename, title in zip(site_names, site_src_and_alt.values())])

    return to_return

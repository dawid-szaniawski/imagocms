from webscraper.scraper import scraper


class ImageSource:
    """An object that represents the page being scrapped. Takes two arguments when creating the object.

    Args:
        website_url: string containing url of scraped website
        image_class: class of the images in the HTML DOM."""
    def __init__(self, website_url: str, image_class: str, pagination_class: str):
        self.website_url = website_url
        self.image_class = image_class
        self.pagination_class = pagination_class
        self.html_dom = scraper.get_html_dom(self.website_url)
        self.all_images = scraper.find_all_images(self.html_dom, ('img.' + self.image_class))

    def go_next_page(self):
        """The ImageSource object changes into the next subpage of the website."""
        self.website_url = scraper.find_next_page(self.html_dom, self.website_url, self.pagination_class)
        self.html_dom = scraper.get_html_dom(self.website_url)
        self.all_images = scraper.find_all_images(self.html_dom, ('img.' + self.image_class))

    @staticmethod
    def get_requests(images_source) -> list:
        """Changes the list of image sources into request objects."""
        return [scraper.get_request(src) for src in images_source]

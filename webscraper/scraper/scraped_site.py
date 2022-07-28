from webscraper.scraper import scraper


class ImageSource:
    """An object that represents the page being scraped. Takes two arguments when creating the object.

    Args:
        website_url: string containing url of scraped website
        image_class: class of the images in the HTML DOM,
        pagination_class: class of the pagination buttons in the HTML DOM."""

    def __init__(
        self, website_url: str, image_class: str, pagination_class: str
    ) -> None:
        self.website_url = website_url
        self.image_class = image_class
        self.pagination_class = pagination_class
        self.html_dom = scraper.get_html_dom(self.website_url)
        self.all_images = scraper.find_all_images(
            self.html_dom, ("img." + self.image_class)
        )

    def go_next_page(self) -> None:
        """The ImageSource object changes into the next subpage of the website."""
        self.website_url = scraper.find_next_page(
            self.html_dom, self.website_url, self.pagination_class
        )
        self.html_dom = scraper.get_html_dom(self.website_url)
        self.all_images = scraper.find_all_images(
            self.html_dom, ("img." + self.image_class)
        )

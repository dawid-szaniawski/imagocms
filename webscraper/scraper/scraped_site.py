from webscraper.scraper.scraper import get_html_dom, find_all_images, find_next_page, get_request


class ImageSource:
    website_url = str
    html_dom = str
    all_images = str

    def __init__(self, website_url: str, image_class: str):
        self.website_url = website_url
        self.image_class = image_class
        self.html_dom = get_html_dom(self.website_url)
        self.all_images = find_all_images(self.html_dom, ('img.' + self.image_class))

    def go_next_page(self):
        self.website_url = find_next_page(self.html_dom, self.website_url)
        self.html_dom = get_html_dom(self.website_url)
        self.all_images = find_all_images(self.html_dom, ('img.' + self.image_class))

    @staticmethod
    def get_requests(images_source):
        return [get_request(src) for src in images_source]

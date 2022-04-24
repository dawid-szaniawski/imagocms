import requests
from bs4 import BeautifulSoup


def get_html_dom(website_url: str):
    request = requests.get(website_url)
    return BeautifulSoup(request.text, 'html.parser')


def find_all_images(html_dom, img_class):
    return html_dom.select(img_class)


def find_next_page(html_dom, website_url):
    next_url = html_dom.find(class_='pagination').find('a')['href']
    if len(next_url) < 2 or next_url == website_url:
        next_url = html_dom.find(class_='pagination').find_all('a')[2]['href']
    return next_url


def get_request(src):
    return requests.get(src)

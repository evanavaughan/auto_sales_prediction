import requests
from bs4 import BeautifulSoup

class Scraper:
    def webpage_html(self, url):
        nyc_request = requests.get(url)
        self.timeout_html = nyc_request.text
        return self.timeout_html

    def listing_page(self, timeout_html = None):
        timeout_html = timeout_html or self.timeout_html
        timeout_soup = BeautifulSoup(timeout_html)
        individual_listing =  timeout_soup.findAll('div', {'class': ' non_hotels_like desktop scopedSearch'})
        self.individual_listing = individual_listing
        return self.individual_listing

    def scrape(self, url):
        website = requests.get(url)
        self.auto_data = website.text
        return self.auto_data

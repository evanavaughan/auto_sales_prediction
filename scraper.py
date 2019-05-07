import requests
import re
from bs4 import BeautifulSoup

class Scraper2:
    site = 'http://www.goodcarbadcar.net/2019/05/april-2019-the-best-selling-vehicles-in-america-every-vehicle-ranked/'

    def webpage_html(self, url):
        nyc_request = requests.get(url)
        self.timeout_html = nyc_request.text
        return self.timeout_html

    def listing_page(self, timeout_html = None):
        timeout_html = timeout_html or self.timeout_html
        timeout_soup = BeautifulSoup(timeout_html)
        individual_listing =  timeout_soup.find('tbody')
        self.individual_listing = individual_listing
        return self.individual_listing


class Parser:
    def __init__(self, listing_page):
        self.listing_page = listing_page

    def car_sales(self):
        monthly_sales = []
        table = self.listing_page.findAll('tr', {'id':re.compile('^table_3*')})
        for i in range(0, len(table)-1):
            row = self.table[i].text.split('\n')
            monthly_sales.append(self.row)
        return self.monthly_sales

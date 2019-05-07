import requests
import re
from bs4 import BeautifulSoup

class Scraper:


    def webpage_html(self, url):
        nyc_request = requests.get(url)
        self.timeout_html = nyc_request.text
        return self.timeout_html

    def listing_page(self, timeout_html = None):
        timeout_html = timeout_html or self.timeout_html
        soup = BeautifulSoup(timeout_html, 'html.parser')
        individual_listing =  soup.find('tbody')
        self.individual_listing = individual_listing
        return self.individual_listing

    def car(self, listing_page):
        monthly_sales = []
        table = self.listing_page.findAll('tr', {'id':re.compile('^table_3*')})
        for i in range(0, len(table)-1):
            row = table[i].text.split('\n')
            monthly_sales.append(row)
        return monthly_sales

class Parser:
    def __init__(self, listing_page):
        self.listing_page = listing_page

    def car_sales(self, i):
        table = self.listing_page.findAll('tr', {'id':re.compile('^table_3*')})[i].text
        #for i in range(0, len(table)-1):
        #    row = self.listing_page.findAll('tr', {'id':re.compile('^table_3*')})[i].text.split('\n')
        #    monthly_sales.append(row)
        return table

class Lister:
    def run(self):
        bob = Scraper()
        sales = []
        site = 'http://www.goodcarbadcar.net/2019/05/april-2019-the-best-selling-vehicles-in-america-every-vehicle-ranked/'
        for row in range(0,len(table)-1):
            bob.webpage_html(site)
            for info in bob.restaurants_html():
                for i in range(len(info.findAll('a',{'class':'feature__title'}))):
                    inf_parser  = Parser(info)
                    name = inf_parser.restaurant_name(i)
                    neighborhood = inf_parser.restaurant_neighborhood(i)
                    rating = inf_parser.restaurant_rating(i)
                    price = inf_parser.restaurant_price(i)
                    listings.append({'Name':name, 'Neighborhood': neighborhood,'Rating': rating, 'Price': price})
        return listings

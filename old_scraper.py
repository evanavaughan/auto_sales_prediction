import requests
from bs4 import BeautifulSoup

def url_list():
    individual_listing_urls = []
    for i in range(0,400,30):
        url = 'https://www.tripadvisor.com/Restaurants-g60763-oa{}-New_York_City_New_York.html'.format(i)
        request = requests.get(url).text
        soup = BeautifulSoup(request)
        x = soup.findAll('a', {'class': 'property_title'})
        for item in x:
            prefix = 'https://www.tripadvisor.com/'
            suffix = item.get('href')
            individual_listing_urls.append(prefix + suffix)
    return individual_listing_urls

class ListingBuilder:
    def run(self):
        for restaurant in url_list():
            ta = Scraper()
            listings = []
            ta.webpage_html(restaurant)
            for restaurant in ta.listing_page():
                x  = Parser(restaurant)
                name = x.restaurant_name()
                num_of_reviews = x.num_of_reviews()
                rating = x.rating()
                address = x.address()
                cuisines = x.cuisines()
                ranking = x.ranking()
                price = x.price()
                rating_types = x.rating_types()
                listings.append({'Name': name, 'Number of Reviews': num_of_reviews, 'Rating': rating, 'Address': address, 'Cuisines':cuisines, 'Ranking':ranking, 'Price': price, 'Rating Types': rating_types})
            print(listings)

class Scraper:
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

    def restaurant_name(self):
        return self.listing_page.s.findAll('tr', {'id':re.compile('^table_3*')})[3].text.split('\n')

    def address(self):
        street = self.listing_page.find('span', {'class': 'street-address'}).text
        city_st_zip = self.listing_page.find('span', {'class': 'locality'}).text
        return street + " " + city_st_zip

    def num_of_reviews(self):
        return self.listing_page.find('a', {'class':"seeAllReviews"}).text.replace(' reviews', '')

    def rating(self):
        return self.listing_page.find('span', {'class':'overallRating'}).text

    def cuisines(self):
        return self.listing_page.find('span', {'class':'header_links rating_and_popularity'}).text


    def ranking(self):
        return self.listing_page.b.text.replace('#', '')

    def price(self):
        return self.listing_page.find('span', {'class':'header_tags rating_and_popularity'}).text

    def rating_types(self):
        five = self.listing_page.find_all('span', {'class': 'row_count row_cell'})[0].text
        four = self.listing_page.find_all('span', {'class': 'row_count row_cell'})[1].text
        three = self.listing_page.find_all('span', {'class': 'row_count row_cell'})[2].text
        two = self.listing_page.find_all('span', {'class': 'row_count row_cell'})[3].text
        one = self.listing_page.find_all('span', {'class': 'row_count row_cell'})[4].text
        return {'5':five, '4':four, '3':three, '2':two, '1':one}

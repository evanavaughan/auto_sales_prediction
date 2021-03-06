import requests
from bs4 import BeautifulSoup
import csv
import re
from variables import search_results, pre, suf
from pymongo import MongoClient
from api_keys import client_pass
import math

'''
web scraper used to access attributes and reviews for car models
on kellybluebook.com and insert them in a MongoDB database
'''

class Requests:

    def __init__(self, site=None):
        self.site = site

    def get_lxml(self, site):
        '''url is input, grabs xml from site, outputs as a string'''

        html = requests.get(site).text
        self.site_lxml = BeautifulSoup(html, 'lxml')
        return self.site_lxml

class Scraper(Requests):

    def get_listing_pages(self, prefix, suffix):
        '''scrapes search results to get url list for individual car models'''

        self.urls = []
        for i in range(1,139):
            site  = prefix + str(i) + suffix
            for link in self.get_lxml(site).find_all('a'):
                self.urls.append(link.get('href'))
        return self.urls

    def clean_url_list(self):
        '''string cleaning for the individual car page urls'''

        urls = self.urls
        cleaned_url_list = []
        for url in urls:
            if url.startswith('https://staging'):
                url = url.replace('staging', 'www').split('?', 1)[0]
                cleaned_url_list.append(url)
        self.cleaned_url_list = cleaned_url_list
        return self.cleaned_url_list


    def backup_list_to_csv(self, filename):
        '''write the list to csv file'''

        urls = self.cleaned_url_list
        with open(filename, "w") as outfile:
            for row in urls:
                outfile.write(row)
                outfile.write("\n")


class ModelParser(Requests):

    def __init__(self, model_page):
        self.model_page = model_page

    def combined_mpg(self):
        '''extracts and returns the combined mpg'''
        try:
            combined = self.model_page.find('p', {'class':'label-two'}).text
            combined = int(combined.split()[0])
            return combined
        except:
            return 99

    def city_hwy_mpg(self):
        '''extracts and returns the city and hwy mpg'''

        try:
            mpg = self.model_page.find('p', {'class':'label-three'}).text.split()
            city, hwy = int(mpg[0]), int(mpg[3])
            return city, hwy
        except:
            return 99, 99

    def ratings(self):
        '''extracts and expert and user ratings from page as float'''
        try:
            rating = self.model_page.find_all('p', {'class':'rating-text'})
            expert_rating = float(rating[0].text.split()[0])
            user_rating = float(rating[1].text.split()[0])
            return expert_rating, user_rating
        except:
            return 99, 99

    def price_low_high(self):
        '''extracts price range, parses it, returns the high and low price'''

        try:
            price = self.model_page.find_all('p', {'class':'label-two range'})[0].text
            price = re.sub('\$|,','', price).split()
            low = int(price[0])
            high = int(price[2])
            return low, high
        except:
            pass

    def expert_review(self):
        '''returns raw text of expert review'''
        try:
            model_page = self.model_page.find_all('div', {'class':'expert-review-container'})
            expert_review = model_page[0].text
            return expert_review
        except:
            pass


    def get_reviews_link(self):
        '''extracts the url to the reviews page'''

        url_prefix = 'https://www.kbb.com'
        try:
            url_suffix = self.model_page.find('button', {'id': 'see-all-reviews'}).get('href')
            self.reviews_link = url_prefix + url_suffix
            return self.reviews_link
        except:
            pass

    def vehicle_id(self):
        '''extracts 6 digit KBB vehicle id from webpage'''

        try:
            id = self.model_page.find('button', {'class': 'button-two js-spec-list-link'}).get('data-url')
            return int(id[-6:])
        except:
            pass

    def make_model_year(self):
        '''extracts make, model, and year from webpage'''

        make = self.model_page.find('title').text.split()[1]
        model = self.model_page.find('title').text.split()[2]
        year = self.model_page.find('title').text.split()[0]
        return make, model, int(year)

    def put_models_in_database(self):
        '''runs 'ModelParser' class helper functions to put that data into a MongoDB collection'''

        client = MongoClient(client_pass)
        db = client.autos
        try:
            MODEL = {
                    'Vehicle_id': self.vehicle_id(),
                    'Manufacturer': self.make_model_year()[0],
                    'Model': self.make_model_year()[1],
                    'Year': self.make_model_year()[2],
                    'Combined MPG': self.combined_mpg(),
                    'City MPG': self.city_hwy_mpg()[0],
                    'Hwy MPG': self.city_hwy_mpg()[1],
                    'Expert Rating': self.ratings()[0],
                    'User Rating': self.ratings()[1],
                    'Price': self.price_low_high(),
                    'Expert Review': self.expert_review(),
                }
            db.models.insert(MODEL)
        except:
            pass


class ReviewsParser(ModelParser):

    def __init__(self, reviews_link):
        self.reviews_link = reviews_link
        try:
            self.reviews_lxml = self.get_lxml(reviews_link)
        except:
            pass


    def find_review_page_count(self):
        '''parses xml to extract count of reviews'''

        review_count = self.reviews_lxml.find('span', {'class':'total-consumer-reviews'}).text
        return int(review_count)

    def rating_score(self):
        '''parses xml to extract rating scores for each review on page
        outputs as tuple with count & list (len = 1-3)'''

        rating_scores = []
        rating = self.reviews_lxml.find_all('div', {'class':'rating-number'})
        for i in range(0,3):
            try:
                rating_scores.append(int(rating[i].text))
            except:
                pass
        return len(rating_scores), rating_scores


    def extract_clean_dates(self):
        '''extracts and cleans each of the dates on the review page
        outputs as list (len = 1-3)'''

        dates = []
        for i in range(1,10,4):
            try:
                review = self.reviews_lxml.find_all('p', {'class':'paragraph-two'})[i].text
                date = re.compile('\d+/\d+/\d+')
                cleaned_date = date.findall(review)
                dates.append(cleaned_date[0])
            except:
                pass
        return dates


    def extract_reviews(self):
        '''extracts and cleans each of the (1-3) reviews on page
        outputs as list (len = 1-3)'''

        reviews = []
        for i in range(2,11,4):
            try:
                review = self.reviews_lxml.find_all('p', {'class':'paragraph-two'})
                cleaned_review = re.sub('\n|\t|\r', '', review[i].text)
                reviews.append(cleaned_review)
            except:
                pass
        return reviews


    def extract_scores(self):
        '''
        extracts and cleans each of the numberical categorical review scores
        outputs integers as a list of lists where:
            length of outer list = 1-3 (number of reviews)
            length of inner list = 6 (one for each score)
        scores: value, quality, reliability, performance, comfort, styling
        '''
        scores = []
        for i in range(0,11):
            try:
                review = self.reviews_lxml.find_all('div', {'class':'col-base-6 col-md-5 text-center'})[i]
                numbers = re.compile('\d')
                cleaned_numbers = numbers.findall(review.text)
                cleaned_numbers = [int(number) for number in cleaned_numbers]
                scores.append(cleaned_numbers)
            except:
                pass
        return scores

    def v_id(self):
        '''pulls the vehicle id out of the xml of the review page'''

        id = self.reviews_lxml.find('div', {'class':'modal-scroller'}).get('data-base-panel-url')
        id = id.split('vehicleid=')[1][:6]
        return int(id)


    def extract_all_reviews_urls(self):
        '''goes to first page of review, determines how many pages of reviews
        outputs list of paginated review links'''

        self.reviews_urls = []
        try:
            url_pre = self.reviews_link.split('page=1')[0]
            url_suf = self.reviews_link.split('page=1')[1]
            review_pages_count = math.ceil(self.find_review_page_count()/3)+1
            review_count = 1
            for i in range(1, review_pages_count + 1):
                reviews_paginator = url_pre + 'page=' + str(i) + url_suf
                self.reviews_urls.append(reviews_paginator)
            print(self.reviews_urls)
        except:
            print(self.reviews_urls)


    def put_reviews_in_database(self):
        '''runs 'ReviewsParser' class helper functions to put that data into a MongoDB collection'''

        client = MongoClient(client_pass)
        db = client.autos
        if len(self.reviews_urls) > 0:
            review_count = 1
            for url in self.reviews_urls:
                try:
                    self.reviews_lxml = self.get_lxml(url)
                    for j in range(0, 3):
                        v_id = self.v_id()
                        review_id = review_count
                        date_of_review = self.extract_clean_dates()[j]
                        rating_score = self.rating_score()[1][j]
                        review = self.extract_reviews()[j]
                        value = self.extract_scores()[j][0]
                        quality = self.extract_scores()[j][1]
                        reliability = self.extract_scores()[j][2]
                        performance = self.extract_scores()[j][3]
                        comfort = self.extract_scores()[j][4]
                        styling = self.extract_scores()[j][5]
                        REVIEW = {
                                    'URL': url,
                                    'Vehicle_id': v_id,
                                    'Review_id': review_id,
                                    'Date of Review': date_of_review,
                                    'Rating Score': rating_score,
                                    'Review': review,
                                    'Scores':{'Value': value,
                                            'Quality': quality,
                                            'Reliability': reliability,
                                            'Performance': performance,
                                            'Comfort': comfort,
                                            'Styling': styling,
                                             },
                                }
                        print(url)
                        print(review)
                        db.reviews.insert(REVIEW)
                        review_count += 1
                except:
                    pass


if __name__ == "__main__":
    bob = Scraper()
    bob.get_listing_pages(pre, suf)
    for page in bob.clean_url_list():
        try:
            web = bob.get_lxml(page)
            model = ModelParser(web)
            model.put_models_in_database()
            model.get_reviews_link()
            link = model.get_reviews_link()
            review = ReviewsParser(link)
            review.extract_all_reviews_urls()
            review.put_reviews_in_database()
        except:
            pass

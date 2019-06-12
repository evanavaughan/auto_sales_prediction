import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
from variables import search_results, pre, suf

'''still editing'''

def test():
    bob = Scraper()
    bob.get_listing_pages(pre, suf)
    x = bob.clean_url_list()[20]
    return bob.get_lxml(x)

class Scraper:
    '''
    bob = Scraper()
    bob.get_listing_pages(pre, suf)
    bob.clean_url_list()
    bob.backup_list_to_csv('./urls/url_list.csv')
    for _ in bob.clean_url_list():
        everything in ModelParser
    '''


    def get_lxml(self, site):
        '''url is input, grabs xml from site, outputs as a string'''

        html = requests.get(site).text
        self.site_lxml = BeautifulSoup(html, 'lxml')
        return self.site_lxml

    def get_listing_pages(self, prefix, suffix):
        '''scrapes search results to get url list for individual car models'''

        self.urls = []
        for i in range(1,5):        #change to 139
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


class ModelParser(Scraper):

    def __init__(self, model_page):
        self.model_page = model_page

    def combined_mpg(self):
        '''extracts and returns the combined mpg'''

        combined = self.model_page.find('p', {'class':'label-two'}).text
        combined = int(combined.split()[0])
        return combined

    def city_hwy_mpg(self):
        '''extracts and returns the city and hwy mpg'''

        mpg = self.model_page.find('p', {'class':'label-three'}).text.split()
        city, hwy = int(mpg[0]), int(mpg[3])
        return city, hwy

    def ratings(self):
        '''extracts and expert and user ratings from page as float'''

        rating = self.model_page.find_all('p', {'class':'rating-text'})
        expert_rating = float(rating[0].text.split()[0])
        user_rating = float(rating[1].text.split()[0])
        return expert_rating, user_rating

    def price_low_high(self):
        '''extracts price range, parses it, returns the high and low price'''

        try:
            price = self.model_page.find_all('p', {'class':'label-two range'})[0].text
            price = re.sub('\$|,','', price).split()
            low = int(price[0])
            high = int(price[2])
            return low, high
        except:
            return 'NaN'

    def expert_review(self):
        '''returns raw text of expert review'''

        model_page = self.model_page.find_all('div', {'class':'expert-review-container'})
        expert_review = model_page[0].text
        return expert_review

    def get_reviews_link(self):
        '''extracts the url to the reviews page'''
        #outputting empty list

        url_prefix = 'https://www.kbb.com'
        url_suffix = self.model_page.find('button', {'id': 'see-all-reviews'}).get('href')
        reviews_link = url_prefix + url_suffix
        self.reviews_lxml = get_lxml(reviews_link)
        return self.reviews_lxml

class ReviewsParser():

    def __init__(self, reviews_link):

        self.reviews_link = reviews_link
        #self.Scraper.get_lxml(reviews_link)
        #use get_lxml function from Scraper class

    def find_review_count(self):
        '''parses xml to extract count of reviews'''

        review_count = self.reviews_link.find('span', {'class':'js-review-pager consumer-review-page'})
        return int(review_count.text)

    def find_rating_score(self):
        '''parses xml to extract rating score'''

        rating = self.reviews_link.find('div', {'class':'rating-number'})
        return int(rating.text)


    def extract_clean_dates(self):
        '''extracts and cleans each of the dates on the review page'''

        dates = []
        for i in range(1,10,4):
            try:
                review = self.reviews_link.find_all('p', {'class':'paragraph-two'})[i].text
                date = re.compile('\d+/\d+/\d+')
                cleaned_date = date.findall(review)
                dates.append(cleaned_date[0])
            except:
                pass
        return dates


    def extract_reviews(self):
        '''extracts and cleans each of the (1-3) reviews on page'''

        reviews = []
        for i in range(2,11,4):
            try:
                review = self.reviews_link.find_all('p', {'class':'paragraph-two'})
                cleaned_review = re.sub('\n|\t|\r', '', review[i].text)
                reviews.append(cleaned_review)
            except:
                pass
        return reviews


    def extract_scores(souper):
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
                review = self.reviews_link.find_all('div', {'class':'col-base-6 col-md-5 text-center'})[i]
                numbers = re.compile('\d')
                cleaned_numbers = numbers.findall(review.text)
                cleaned_numbers = [int(number) for number in cleaned_numbers]
                scores.append(cleaned_numbers)
            except:
                pass
        return scores

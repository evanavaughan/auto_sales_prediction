import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
from variables import search_results, pre, suf

def clean(url):
    '''
    felper function for string cleaning the individual car page urls
    '''
    url = url.replace('staging.', '')
    url = url.replace('//', '//www.')
    separator = '?'
    return url.split(separator, 1)[0]

class ListingBuilder:
    pass



class Scraper:

    def __init__(self, url):
        self.url = url

    def get_lxml(self):

    def get_html(self):

    def get_listing_pages(self):
        '''
        scrapes search landing page to get urls for individual car makes/models/year
        '''
        prefix = 'https://www.kbb.com/car-finder/'
        suffix = '/?categories=sedan&years=2006-2020'
        urls = []
        for i in range(1,139):
            site  = prefix + str(i) + suffix
            html = requests.get(site).text
            soup = BeautifulSoup(html, 'lxml')
            for link in soup.find_all('a'):
                urls.append(link.get('href'))
        self.cleaned_list = [clean(url) for url in urls if url.startswith('https://staging')]
        return self.cleaned_list

class Parser:

    def __init__(self, )
    
    def clean_list

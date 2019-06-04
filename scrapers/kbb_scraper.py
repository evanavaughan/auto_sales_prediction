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
    '''
    bob = Scraper()
    bob.get_listing_pages()
    bob.clean_url_list()
    bob.write_list_to_file('./urls/url_list.csv')
    '''

    def get_lxml(self, site):
        html = requests.get(site).text
        self.site_lxml = BeautifulSoup(html, 'lxml')
        return self.site_lxml

    def get_listing_pages(self):
        '''scrapes search results to get url list for individual car models'''

        prefix = 'https://www.kbb.com/car-finder/'
        suffix = '/?categories=sedan&years=2006-2020'
        self.urls = []
        for i in range(1,5):        #change to 139
            site  = prefix + str(i) + suffix
            #html = requests.get(site).text
            #soup = BeautifulSoup(html, 'lxml')
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


    def write_list_to_file(self, filename): #save to './urls/url_list.csv'
        '''write the list to csv file'''
        urls = self.cleaned_url_list
        with open(filename, "w") as outfile:
            for row in urls:
                outfile.write(row)
                outfile.write("\n")

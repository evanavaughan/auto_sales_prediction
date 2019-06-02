#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:57:17 2019

@author: evanvaughan
"""

#test spider

import scrapy

class FirstSpider(scrapy.Spider):
    name = 'UnoSpider'
    
    def start_requests(self):
        urls = [
            'https://www.tripadvisor.com/Hotel_Review-g651973-d6978275-Reviews-Ikos_Olivia-Gerakini_Halkidiki_Region_Central_Macedonia.html',
            'https://www.tripadvisor.com/Hotel_Review-g651973-d8781821-Reviews-Bungalows_Camping_Kouyoni-Gerakini_Halkidiki_Region_Central_Macedonia.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
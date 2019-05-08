import requests
import re
import csv
from bs4 import BeautifulSoup

url = 'http://www.goodcarbadcar.net/2019/05/april-2019-the-best-selling-vehicles-in-america-every-vehicle-ranked/'

site = 'http://www.goodcarbadcar.net/best-sellers/page/'

def request(webpage):
    r = requests.get(webpage)
    html_text = r.text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup

def get_table(soup):
    month_and_year = soup.find('h1', {'class':'vw-post-title'}).text.split()[0:2]
    table = soup.find('tbody').findAll('tr', {'id':re.compile('^table_3*')})
    return month_and_year, table

def webpage_finder(url):
    webpages = []
    for i in range(1,31):
        website = url + str(i) + '/'
        soup = request(website)
        websites = soup.findAll('a' ,{'class':'vw-post-box__link'})
        for i in range(0, len(websites)-1):
            webpages.append(websites[i].get('href'))
    return webpages

def get_sales_data(table):
    auto_sales = []
    for i in range(0, len(table)-1):
        auto_sales.append(table[i].text.split('\n'))
    return auto_sales

def write_monthly_table(month_and_year, table):
    month, year = month_and_year[0], month_and_year[1]
    file = str(month) + '_' + str(year)
    write_to_csv(file, table)

def write_to_csv(filename, table):
    with open(filename, 'w', newline='') as myfile:
        w = csv.writer(myfile)
        w.writerow(table)

#if __name__ == '__main__':

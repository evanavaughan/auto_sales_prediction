import requests
import re
import csv
from bs4 import BeautifulSoup

url = 'http://www.goodcarbadcar.net/2019/05/april-2019-the-best-selling-vehicles-in-america-every-vehicle-ranked/'


def request(webpage):
    r = requests.get(webpage)
    html = r.text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup

def get_table(soup):
    month_and_year = soup.find('h1', {'class':'vw-post-title'}).text.split()[0:2]
    table = soup.find('tbody').findAll('tr', {'id':re.compile('^table_3*')})
    return month_and_year, table

def webpage_finder(soup_input):
    for i in range(1,31):
        webpages = []
        website = url + str(i) + suffix
        soup = request(soup_input)
        websites = soup.findAll('a' ,{'class':'vw-post-box__link'})
        for i in range(0, len(websites)-1):
            links.append(websites[i].get('href'))
    return webpages

def write_table(table):
    auto_sales = []
    for i in range(0, len(table)-1):
        auto_sales.append(table[i].text.split('\n'))
    return auto_sales

def write_to_csv(month_and_year, table):
    month = month_and_year[0]
    year = month_and_year[1]
    file = str(month) + '_' + str(year)
    with open(file, 'w', newline='') as myfile:
        w = csv.writer(myfile)
        w.writerow(table)

if __name__ == '__main__':
    x = request(url)
    y = get_table(x)
    z = write_table(y[1])
    write_to_csv(y[0], z)

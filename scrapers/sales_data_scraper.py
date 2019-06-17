import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from urls.auto_sales_urls import list_of_urls

'''
auto sales scraper
~~~~
- read site html
- extracts tables from page
- finds month/year for table
- changes column names for table
- scrape the tables for the site
- scrape all the tables for all the urls
- merge table data into one dataframe
- run everything and backup as csv
'''

def read_site_html(url):
    '''
    pulls text of tables from inputted url
    returns as list of dataframes
    '''
    html = requests.get(url).text
    dataframes = pd.read_html(html, header=0)
    return dataframes


def pull_useful_tables(dataframes):
    '''
    deletes tables with no data from list of dataframes
    returns single dataframe for month
    '''
    list_of_dfs = []
    if len(dataframes) == 1:
        return dataframes[0]
    else:
        for df in dataframes:
            if df.columns[0] == 'Rank':
                list_of_dfs.append(df)
        try:
            merged_table = pd.concat(list_of_dfs)
            return merged_table
        except:
            return list_of_dfs


months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']
years = list(range(2010,2020))


def find_year_and_month(url):
    '''
    parses url string to find month and year & last year of table
    returns tuple of month as string and year & last year as integers
    '''
    month = [month for month in months if month in url]
    year = min([year for year in years if str(year) in url])
    last_year = year - 1
    try:
        month = month[0]
    except:
        month = 'NULL'
    return month, year, last_year


def change_column_to_month(dataframe, url):
    '''
    changes name of columns in dataframe to proper months, years
    cuts unneeded columns of dataframe
    '''
    alternate_columns = ['Month', 'US']
    dataframe.rename(columns={'Vehicle': 'Model'}, inplace=True)
    dataframe.rename(columns={'Best-Selling Vehicle': 'Model'}, inplace=True)
    if dataframe.columns[1] in alternate_columns:
        table_date = find_year_and_month(url)
        year_month = str(table_date[1]) + '_' + table_date[0]
        prior_year_month = str(table_date[2]) + '_' + table_date[0]
        dataframe.rename(columns={'Month':year_month, 'Month LY':prior_year_month}, inplace=True)
        dataframe.rename(columns={'US':year_month, 'US LY':prior_year_month}, inplace=True)
        return dataframe.iloc[:,0:3]
    else:
        return dataframe.iloc[:,1:4]


def scrape_one_page(url):
    '''
    takes in the site url, scrapes tables, changes column names
    returns dataframes using helper functions
    '''
    tables = read_site_html(url)
    df = pull_useful_tables(tables)
    df = change_column_to_month(df, url)
    return df


def scraper(list_of_websites):
    '''
    takes in a list of urls, scrapes table on each page, regularizes column names,
    and adds the dataframe to a list of dataframes which is returned
    '''
    list_of_dataframes = []
    for url in list_of_urls:
        df = scrape_one_page(url)
        list_of_dataframes.append(df)
    return list_of_dataframes


def merge_dataframes(list_of_df):
    '''
    merges all dataframes on the model column, returns a single dataframe
    '''
    merged_df  = pd.DataFrame(columns=['Model'])
    for df in list_of_df:
        merged_df = merged_df.merge(df, how='outer', on='Model')
        merged_df.drop_duplicates(inplace=True)
    return merged_df


def run(lst_of_urls):
    '''
    runs scraper and merges all dataframes.
    saves dataframe as a csv and returns a dataframe
    '''
    df_list = scraper(lst_of_urls)
    df = merge_dataframes(df_list)
    df.to_csv('merged_dataframe.csv')
    return df


if __main__='__name__':
    run(list_of_urls)

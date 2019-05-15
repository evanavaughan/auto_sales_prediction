import pandas as pd
from scraper_non_obj_oriented import *

website = 'http://www.goodcarbadcar.net/2012/03/us-best-selling-autos-january-2012/#more'

soup = request(site_with_2_tables)

def make_dataframe(soup):
    df = pd.DataFrame(columns=['Rank', 'Auto', 'Current', 'Last'])
    divs = soup.findAll("tbody")
    for div in divs:
        rows = div.findAll('tr')
        for row in rows:
            col = row.findAll('td')
            if len(col) > 0:
                rank = col[0].text
            auto = col[1].text if len(col) > 1 else ''
            curr = col[2].text if len(col) > 2 else ''
            last = col[3].text if len(col) > 3 else ''
            df2 = pd.DataFrame({'Rank':[rank], 'Auto':[auto], 'Current':[curr], 'Last':[last]})
            df = df.append(df2)
    return df

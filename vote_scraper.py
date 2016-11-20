# 2016 Congressional Vote Scraper
# Andrew Kirk
#
# Scrapes data on congressional votes by district, useful stopgap pending final
# counts from the FEC
#
# Uncontested districts are coded as 0 votes. No true 0s exist
#
# Inspiration comes from tonmcg's work on scraping the presidential count by
# county at https://github.com/tonmcg/County_Level_Election_Results_12-16

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# remove DC
states = \
['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

data = [['state', 'district', 'party', 'candidate', 'votes']]

for state in tqdm(states):
    r = requests.get('http://townhall.com/election/2016/results/' + state)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all(lambda tag: \
            tag.name == 'table' and tag.find('a').text == 'House')[0]
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')

        if len(cols) == 1: continue
        
        if cols[0].find('div') != None:
            district = cols[0].find_all('div')[0].text.strip()
            cols = cols[1:]

        party = cols[1]['class'][0]
        candidate = cols[0].text.strip()
        votes = (cols[1].text.strip()
                    .replace(',', '')
                    .replace('-', '0')
                    .replace('Uncontested race', '0'))

        data.append([state, district, party, candidate, votes])

df = pd.DataFrame(data)
header = df.iloc[0]
df = df[1:]
df.columns = header
df['votes'] = df['votes'].astype('int')

df.to_csv('2016_congressional_votes.csv', index=False)


"""
Created on Tue Mar 26 13:13:07 2024

@author: calholt
"""


path = 'https://www.govinfo.gov/content/pkg/CDOC-110hdoc50/html/CDOC-110hdoc50.htm'

import pandas as pd
import requests 
import re 
from dateutil.relativedelta import relativedelta


######### Func ################################################################
def find_dates(text):

    '''
    takes cons text returns df with dates 
    '''
    p0 = []
    p1 = []
    p2 = []
    p0.extend(re.findall(patterns[2], text))
    p1.extend(re.findall(patterns[1], text))
    p2.extend(re.findall(patterns[0], text))
    all_dates = p0 + p1 + p2 
    return pd.DataFrame(all_dates, columns = ['date'])

def summaryStats(df):
    counts = pd.DataFrame(df.clean_date.value_counts().reset_index())
    top = counts['count'].max()
    most_common_dates = counts.query(f'count == {top}')

    early = df.clean_date.min()
    late = df.clean_date.max()
    days_between  = relativedelta(late, early)

    summary = (f'''
          The most common dates are: 
          {most_common_dates}
          
          The earliest date is: {early} 
          The latest date is: {late} 
          The amount of time between these two dates is: {days_between}
          '''
        )

    return print(summary)
    

########################## GET CONS #############################
response = requests.get(path)

#change to error handling
if response.status_code == 200:
    cons = response.text
else:
    pass
    print('Failed')
        

patterns = [r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b', # Matches dates like September 1, 2000
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December),\s+\d{4}\b', #Monthname, Year
                r'\b\s+\d{4}\b',#year only
                r'\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b',#year only
                ]

df = find_dates(cons)
df['clean_date'] = pd.to_datetime(df.date)
summaryStats(df)

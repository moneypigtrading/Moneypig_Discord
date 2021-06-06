import pandas as pd

import sys

target_date='2021-03-10'

input = pd.read_csv('/Users/pin-chihsu/repos/DiscordChatExporter.CLI/sheet_update.csv')

wanted = input[['Date','Content']]

# some alerts comes with leading "-". Try to remove them

wanted['Content']=wanted['Content'].str.replace('-', '', regex=False)

# remove  leading/trailing whitespaces in each columns

wanted['Content']=wanted['Content'].str.strip()

wanted['Date'] = pd.to_datetime(wanted['Date'])

print(wanted.head(n=20))

# this line filter out the Content columns that comes with a # suffix

# https://stackoverflow.com/questions/31830364/pandas-how-to-eliminate-rows-with-value-ending-with-a-specific-character

# filter = wanted[wanted['Content'].str.endswith('#', na=False)]

filter = wanted[wanted['Content'].str.startswith('$', na=False)]

# this line filter out based on the date

filter2 = filter[(filter['Date'].dt.strftime('%Y-%m-%d') == target_date)]

# Because the first word in the Content is usually a ticker name

# split the Content based on white space and separate the first word into the Content2 and the

# rest into Content3


print(filter2)

filter2[['Content2','Content3']] = filter2['Content'].str.split(' ', n=1,expand=True)

# Then sort the data frame by Content2, which is the ticker name, and the Date

filter2=filter2.sort_values(by=['Content2','Date'], ascending=True)

sheet_name='sheet_update' + target_date + ".csv"

filter3=filter2[['Date','Content']]

filter3.to_csv(sheet_name, index=False)

sys.exit()

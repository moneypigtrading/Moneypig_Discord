from iexfinance.stocks import *

from datetime import datetime

import pandas as pd

import os

import shutil

from discord_utility.discord_utility import discord_utility

d=discord_utility() # initiate the class

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, '../config.ini')

# get the iex private key so that we can get historical data

df = pd.read_csv(filename, skipinitialspace=True)

secret=df['secret'].loc[df['name'] == 'iex']

secret=secret.to_string(index=False)

secret=secret.lstrip() # there is a leading space in the private key so need to remove it

class discord_market_movers():

    def __init__(self, params):

        self.webhook_id = params.get('webhook_id', '')  # discord market-flows Channel
        self.webhook_token = params.get('webhook_token', '')  # discord market-flows Channel

    def discord_get_market_gainers(self, secret):

        return get_market_gainers(token=secret)

    def discord_get_market_losers(self, secret):

        return get_market_losers(token=secret)

    def get_market_most_active(self, secret):

        return get_market_losers(token=secret)


    def run(self):

        now = datetime.now()

        timestamp = int(datetime.timestamp(now))

        gainers_csv='gainers_csv_'+str(timestamp)+'.csv'

        losers_csv='losers_csv_'+str(timestamp)+'.csv'

        active_csv='active_csv_'+str(timestamp)+'.csv'

        # movers=discord_market_movers(self.webhook_id, self.webhook_token)

        gainers_df=self.discord_get_market_gainers(secret)

        # print(gainers_df[['companyName','latestPrice','changePercent','marketCap','peRatio','week52High','week52Low','ytdChange']])

        #'marketCap','peRatio','week52High','week52Low','ytdChange',

        gainers_df=gainers_df[['latestPrice','changePercent','companyName']]

        gainers_df['latestPrice']=gainers_df['latestPrice'].round(2)

        gainers_df['changePercent']=gainers_df['changePercent'].round(2)

        gainers_df['changePercent']=gainers_df['changePercent']*100

        gainers_df.to_csv(gainers_csv)

        d.send_format_csv_to_discord('Market Movers', gainers_csv,'gainers_df_reformat.csv',  self.webhook_id, self.webhook_token)

        # shutil.move(gainers_csv, "data/")

        losers_df=self.discord_get_market_losers(secret)

        # print(gainers_df[['companyName','latestPrice','changePercent','marketCap','peRatio','week52High','week52Low','ytdChange']])

        #'marketCap','peRatio','week52High','week52Low','ytdChange',

        losers_df=losers_df[['latestPrice','changePercent','companyName']]

        losers_df['latestPrice']=losers_df['latestPrice'].round(2)

        losers_df['changePercent']=losers_df['changePercent'].round(2)

        losers_df['changePercent']=losers_df['changePercent']*100

        # losers_df['changePercent']=losers_df['changePercent']*100

        losers_df.to_csv(losers_csv)

        d.send_format_csv_to_discord('Market Losers', losers_csv,'gainers_df_reformat.csv',self.webhook_id, self.webhook_token)


        active_df=self.get_market_most_active(secret)

        # print(gainers_df[['companyName','latestPrice','changePercent','marketCap','peRatio','week52High','week52Low','ytdChange']])

        #'marketCap','peRatio','week52High','week52Low','ytdChange',

        active_df=active_df[['latestPrice','changePercent','companyName']]

        active_df['latestPrice']=active_df['latestPrice'].round(2)

        active_df['changePercent']=active_df['changePercent'].round(2)

        active_df['changePercent']=active_df['changePercent']*100

        print(active_df.info())

        active_df.to_csv(active_csv)

        d.send_format_csv_to_discord('Market Most Active', active_csv,'active_df_reformat.csv',self.webhook_id, self.webhook_token)


        shutil.move(gainers_csv, "data/")

        shutil.move(losers_csv, "data/")

        shutil.move(active_csv, "data/")



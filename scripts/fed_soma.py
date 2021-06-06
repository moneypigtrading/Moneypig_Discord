'''
This script get the Fed SOMA data weekly and SPY weekly historical data

And make a plot and send the image and message to Discord automatically

Author: Professor

Email: moneypig@moneypigtrading.com

Command Line Usage:

python3 run_alert.py fed_soma_2020_08_05_start fed_soma
'{"start_date_fed_soma": "2020-08-20",
"webhook_id":"1234567","webhook_token":"abcdefg"

'''

import matplotlib.pyplot as plt

import matplotlib.image as image

from datetime import date

import pandas as pd

from iexfinance.stocks import get_historical_data

import requests

from discord_utility.discord_utility import discord_utility

import os
import shutil

# get the iex private key so that we can get historical data

df = pd.read_csv('config.ini', skipinitialspace=True)

secret=df['secret'].loc[df['name'] == 'iex']

secret=secret.to_string(index=False)

secret=secret.lstrip() # there is a leading space in the private key so need to remove it

class fed_soma():

    def __init__(self, params):

        self.start_date_fed_soma = params.get('start_date', '')  #'2020-08-05'
        self.end_date_fed_soma = params.get('end_date', '')  #'2020-08-05'
        self.webhook_id = params.get('webhook_id','')
        self.webhook_token = params.get('webhook_token','')

    # some cheat sheet
    # http://www.compciv.org/guides/python/how-tos/downloading-files-with-requests/

    def get_soma(self, url, date_above, date_below):

        # Fed SOMA data source

        # https://www.newyorkfed.org/markets/soma-holdings

        rs = requests.get(url)

        with open("summary.csv", "w") as f:

            f.write(rs.text)

        soma=pd.read_csv('summary.csv')

        soma_trim = soma.loc[(soma['As Of Date'] >= date_above) & (soma['As Of Date'] < date_below)]

        soma_trim = soma_trim.rename(columns={"As Of Date": "as_of_date"})

        # divide by 1 billion to make the total displayable

        soma_trim['Total']= soma['Total']/10000000000

        soma_trim = soma_trim.rename(columns={"Total": "Total_10bn"})

        soma_trim['as_of_date']=soma_trim['as_of_date'].astype('datetime64')

        print(soma_trim.head(n=60))

        return soma_trim


    def get_stock_historical(self, ticker, start_date, end_date, secret):

        history=get_historical_data(ticker, start=start_date, end=end_date,
                            output_format='pandas', token=secret)

        history=history.reset_index().rename(columns={'index':'as_of_date'})

        print(history.head(n=50))

        return history


    def run(self): # this function actually runs the Fed SOMA plot generation

        if self.start_date_fed_soma == '':

            self.start_date_fed_soma = '2020-08-05' # make the default start date as 2020-08-05

        start_date_iex = self.start_date_fed_soma.strip('-') #'20200805'

        if self.end_date_fed_soma == '': # if the end date is None, then the default end date is today

            today = date.today()

            end_date_iex = today.strftime("%Y%m%d")

            end_date_soma = today.strftime("%Y-%m-%d")

        df_soma = self.get_soma('http://markets.newyorkfed.org/api/soma/summary.csv', self.start_date_fed_soma, end_date_soma)

        df_SPY = self.get_stock_historical("SPY", start_date_iex , end_date_iex, secret)

        df_merge=pd.merge(df_soma, df_SPY, how="inner", on=["as_of_date", "as_of_date"])

        df_soma_spy=df_merge[['as_of_date','Total_10bn','close']]

        df_soma_spy.to_csv('df_soma_spy.csv')

        df_soma_spy=pd.read_csv('df_soma_spy.csv')

        print(df_soma_spy)

        def plot_double_axis_water_mark_scatter_plot(logo, xlabel, y_left_label, y_right_label, header,
                                                     file_prefix, start_date, end_date):

            # plot the Fed SOMA vs SPY price

            # gs = gridspec.GridSpec(2, 1, height_ratios=[24,1])

            # create figure and axis objects with subplots()

            fig, ax = plt.subplots()

            plt.xticks(rotation=90)

            # put in a logo
            # https://stackoverflow.com/questions/66416268/python-3-matplotlib-add-a-watermark-with-multiple-scale-axis/66416885#66416885

            logo = image.imread(fname=logo)

            fig.figimage(logo, 100, 200, alpha=0.4, resize=True)

            ax.plot(df_soma_spy.as_of_date, df_soma_spy.Total_10bn, color="red")  ## , marker="o"

            # set x-axis label

            ax.set_xlabel(xlabel, fontsize=12)

            # set y-axis label

            ax.set_ylabel(y_left_label, color="red", fontsize=14)

            plt.grid(True, axis='both', which='both')

            # twin object for two different y-axis on the sample plot

            ax2 = ax.twinx()

            # make a plot with different y-axis using second axis object

            ax2.plot(df_soma_spy.as_of_date, df_soma_spy["close"], color="black")  ## , marker="o"

            ax2.set_ylabel(y_right_label, color="black", fontsize=14)

            plt.title(header, fontsize=26)

            # save the plot as a file
            fig.savefig(file_prefix + '_' + start_date + '_' + end_date + '.png',
                        format='jpeg',
                        dpi=300,
                        bbox_inches='tight')

            file_name = str(file_prefix + '_' + start_date + '_' + end_date + '.png')

            return file_name

        image_file=plot_double_axis_water_mark_scatter_plot('2020_looka_purchased_logo.png', "Date", "Fed SOMA ($10bn)", "$SPY Price",
                                                 'Federal Reserves SOMA Total vs $SPY','soma_spy', self.start_date_fed_soma, end_date_soma)

        latest_soma=df_soma['Total_10bn'].iloc[[-1]].to_string(index=False).lstrip()

        latest_soma_float=round(float(latest_soma)/100, 2)

        second_latest_soma=df_soma['Total_10bn'].iloc[[-2]].to_string(index=False).lstrip()

        second_latest_soma_float=round(float(second_latest_soma)/100, 2)

        if second_latest_soma_float > latest_soma_float:

            message = 'Fed decreased its SOMA balance from ${second_latest_soma} tn' \
                      ' to ${latest_soma} tn in the past 7 days. The decrease could elevate $TNX & ' \
                      'lower the tech & growth stocks'.format(second_latest_soma=str(second_latest_soma_float),
                                                               latest_soma=str(latest_soma_float))

        elif second_latest_soma_float < latest_soma_float:

            message = 'Fed increased its SOMA balance from ${second_latest_soma} tn ' \
                      ' to ${latest_soma} tn  in the past 7 days. The increase could lower $TNX & ' \
                      'push the tech & growth stocks higher '.format(second_latest_soma=str(second_latest_soma_float),
                                                                     latest_soma=str(latest_soma_float))

        else:

            message = 'Fed did not change its SOMA balance ${second_latest_soma} tn ' \
                      ' in the past 7 days. This could make $TNX & ' \
                      'tech & growth stocks stay flat'.format(second_latest_soma=str(second_latest_soma_float),
                                                               latest_soma=str(latest_soma_float))


        twitter_hastag="#stockmarket #stocktrading #stocks #investment #stockmarketnews " \
                       "#investing #bonds #trading #forex $SPY $SPX $QQQ $IWM $EF_S $GC $BTC"

        d=discord_utility()

        d.send_file_to_discord(message, image_file, self.webhook_id, self.webhook_token)

        # clean up the file by moving the image into the image folder

        shutil.move(image_file, "image/")




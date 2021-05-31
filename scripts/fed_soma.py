import requests

import matplotlib.pyplot as plt

import matplotlib.image as image

from datetime import date

import pandas as pd

from iexfinance.stocks import get_historical_data

# get the iex private key so that we can get historical data

df = pd.read_csv('config.ini', skipinitialspace=True)

secret=df['secret'].loc[df['name'] == 'iex']

secret=secret.to_string(index=False)

secret=secret.lstrip() # there is a leading space in the private key so need to remove it

class fed_soma():

    def __init__(self, params):

        self.start_date_fed_soma = params.get('start_date', '')  #'2020-08-05'
        self.end_date_fed_soma = params.get('end_date', '')  #'2020-08-05'

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

    def run(self):

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

            # ax3 = plt.axes([0.5,0.8, 0.1, 0.1], frameon=True)  # Change the numbers in this array to position your image [left, bottom, width, height])
            #
            # image=plt.imread('2020_looka_purchased_logo.png')
            #
            # ax.imshow(image)
            #
            # ax3.axis('off')  # get rid of the ticks and ticklabels

            plt.show()

            # save the plot as a file
            fig.savefig(file_prefix + '_' + start_date + '_' + end_date + '.png',
                        format='jpeg',
                        dpi=300,
                        bbox_inches='tight')

        plot_double_axis_water_mark_scatter_plot('2020_looka_purchased_logo.png', "Date", "Fed SOMA ($10bn)", "$SPY Price",
                                                 'Federal Reserves SOMA Total vs $SPY','soma_spy', self.start_date_fed_soma, end_date_soma)



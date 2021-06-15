
from iexfinance.stocks import *



class iex_utility():

    def get_stock_historical(self, ticker, start_date, end_date, secret):
        history = get_historical_data(ticker, start=start_date, end=end_date,
                                      output_format='pandas', token=secret)

        history = history.reset_index().rename(columns={'index': 'as_of_date'})

        print(history.head(n=50))

        return history

    def getEarnings(self, symbol, iex_token):
        print(iex_token)
        stock_batch = Stock(symbol, token=iex_token)
        earnings = stock_batch.get_earnings(last=4)
        return earnings


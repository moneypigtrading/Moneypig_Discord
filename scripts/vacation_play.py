'''
Find stocks that move the least during US holidays

Some tutorials here

Thanksgiving dates list: https://www.theholidayspot.com/thanksgiving/when_is_thanksgiving_day.htm

by Professor

'''

import pandas as pd

from yahoo_fin.stock_info import get_data, tickers_sp500

'''The top 60 companies with at least 10 years of history'''
ticker_list = ['SPY','QQQ','MSFT','AAPL','AMZN','TSLA','GOOGL','NVDA','JPM','HD','JNJ','UNH','PG','BAC'
    ,'V','ADBE','NFLX','CRM','PFE','DIS','MA','XOM','COST','CMCSA','ACN','CSCO','AVGO','PEP','NKE','ABT','CVX'
    ,'KO','VZ','WMT','LLY','WFC','MRK','QCOM','INTC','DHR','AMD','INTU','LOW','TXN','T','UNP','ORCL','UPS','HON'
    ,'MS','PM','C']

# ticker_list=tickers_sp500()

historical_datas = pd.DataFrame(columns=['open', 'high', 'low', 'close','adjclose', 'volume', 'ticker'])

for ticker in ticker_list:

    print(ticker)

    historical_data1=get_data(ticker, start_date="2011/11/23", end_date="2011/11/26", index_as_date = True)
    historical_data2=get_data(ticker, start_date="2012/11/21", end_date="2012/11/24", index_as_date = True)
    historical_data3=get_data(ticker, start_date="2013/11/27", end_date="2013/11/30", index_as_date = True)
    historical_data4=get_data(ticker, start_date="2014/11/26", end_date="2014/11/30", index_as_date = True)
    historical_data5=get_data(ticker, start_date="2015/11/25", end_date="2015/11/28", index_as_date = True)
    historical_data6=get_data(ticker, start_date="2016/11/23", end_date="2016/11/26", index_as_date = True)
    historical_data7=get_data(ticker, start_date="2017/11/22", end_date="2017/11/25", index_as_date = True)
    historical_data8=get_data(ticker, start_date="2018/11/21", end_date="2018/11/24", index_as_date = True)
    historical_data9=get_data(ticker, start_date="2019/11/27", end_date="2019/11/30", index_as_date = True)
    historical_data10=get_data(ticker, start_date="2020/11/25", end_date="2020/11/30", index_as_date = True)

    historical_datas=historical_datas.append(historical_data1)
    historical_datas=historical_datas.append(historical_data2)
    historical_datas=historical_datas.append(historical_data3)
    historical_datas=historical_datas.append(historical_data4)
    historical_datas=historical_datas.append(historical_data5)
    historical_datas=historical_datas.append(historical_data6)
    historical_datas=historical_datas.append(historical_data7)
    historical_datas=historical_datas.append(historical_data8)
    historical_datas=historical_datas.append(historical_data9)
    historical_datas=historical_datas.append(historical_data10)


historical_datas['same_day_change']=historical_datas['close']-historical_datas['open']

historical_datas['same_day_change_percent']=historical_datas['same_day_change'].abs()/historical_datas['open']*100

holiday_volatility_pre=historical_datas[['same_day_change_percent','ticker']]

holiday_volatility=holiday_volatility_pre.groupby(['ticker']).mean()

holiday_volatility=holiday_volatility.reset_index().sort_values(by=['same_day_change_percent'])

holiday_volatility.rename(columns={"same_day_change_percent": "same_day_change_percent_avg"}, errors="raise")

print(holiday_volatility)

holiday_volatility.to_csv('holiday_volatility_2021_thanksgiving_wtih_absolute_values.csv')




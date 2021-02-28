import requests
import csv
import pandas as pd
import numpy as np

# some cheat sheet
# http://www.compciv.org/guides/python/how-tos/downloading-files-with-requests/

def get_soma(url, date_above):

    rs = requests.get(url)

    with open("summary.csv", "w") as f:

        f.write(rs.text)

    soma=pd.read_csv('summary.csv')

    soma_trim = soma.loc[soma['As Of Date'] >= date_above]

    soma_trim = soma_trim.rename(columns={"As Of Date": "as_of_date"})

    # divide by 1 billion to make the total displayable

    soma_trim['Total']= soma['Total']/1000000000

    soma_trim = soma_trim.rename(columns={"Total": "Total_bn"})

    print(soma_trim.head(n=20))

df = get_soma('http://markets.newyorkfed.org/api/soma/summary.csv','2020-08-01')







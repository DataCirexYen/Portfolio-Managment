from flask import Flask, request, render_template
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import webbrowser

#Download multiple assets historys
def download(tickers, start=None, end=None, actions=False, threads=True,
             group_by='column', auto_adjust=False, back_adjust=False,
             progress=True, period="max", show_errors=True, interval="1d", prepost=False,
             proxy=None, rounding=False, timeout=None, **kwargs):
    """Download yahoo tickers
    :Parameters:
        tickers : str, list
            List of tickers to download
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        group_by : str
            Group by 'ticker' or 'column' (default)
        prepost : bool
            Include Pre and Post market data in results?
            Default is False
        auto_adjust: bool
            Adjust all OHLC automatically? Default is False
        actions: bool
            Download dividend + stock splits data. Default is False
        threads: bool / int
            How many threads to use for mass downloading. Default is True
        proxy: str
            Optional. Proxy server URL scheme. Default is None
        rounding: bool
            Optional. Round values to 2 decimal places?
        show_errors: bool
            Optional. Doesn't print errors if True
        timeout: None or float
            If not None stops waiting for a response after given number of
            seconds. (Can also be a fraction of a second e.g. 0.01)
    """
start_date_ = "2020-01-01"
end_date_  = "2022-01-31"
benchmark_ = ["^GSPC",]
portfolio_ = ["123","ETH-USD","ADA-USD"]
df = yf.download(benchmark_, start=start_date_, end=end_date_)

for t in portfolio_:
    Stock=yf.Ticker(t)
    if (Stock.info['regularMarketPrice'] == None):
            #raise NameError("You did not input a correct stock ticker! Try again.")
            portfolio_.remove(t)
            print(portfolio_)
    else:
            print("uwu")
  
  
print("///////////////////")
print(portfolio_)
#df2 = yf.download(portfolio_, start=start_date_, end=end_date_)
#print(df2)



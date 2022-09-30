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
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        a=request.form .get('longitude')
        benchmark_ = ["^GSPC",]
        #portfolio_ = ['ADA-USD', 'BTC-USD','ETH-USD',"SOL-USD","XRP-USD"]

        portfolio_ =[]
        print('Welcome to the portfolio optimizer')
        print( 'Enter each token in XXX-USD format Example: ETH-USD ADA-USD')
        print("///////////////////////////////////////////////////")


        portfolio_ = [item for item in a.split()]

        print(portfolio_)
        
            



        start_date_ = "2020-01-01"
        end_date_  = "2022-01-31"
        number_of_scenarios = 10000

        return_vector = []
        risk_vector = []
        distrib_vector = []

        #Get Information from Benchmark and Portfolio
        df = yf.download(benchmark_, start=start_date_, end=end_date_)
        df2 = yf.download(portfolio_, start=start_date_, end=end_date_)

        #Clean Rows with No Values on both Benchmark and Portfolio
        df = df.dropna(axis=0)
        df2 = df2.dropna(axis=0)

        #Matching the Days
        df = df[df.index.isin(df2.index)]
        df.head()

        # Analysis of Benchmark
        benchmark_vector = np.array(df['Close'])

        #Create our Daily Returns
        benchmark_vector = np.diff(benchmark_vector)/benchmark_vector[1:]

        #Select or Final Return and Risk
        benchmark_return = np.average(benchmark_vector)
        benchmark_risk = np.std(benchmark_vector)

        #Add our Benchmark info to our lists
        return_vector.append(benchmark_return)
        risk_vector.append(benchmark_risk)

        # Analysis of Portfolio
        portfolio_vector = np.array(df2['Close'])

        #Create a loop for the number of scenarios we want:

        for i in range(number_of_scenarios):
            #Create a random distribution that sums 1 
            # and is split by the number of stocks in the portfolio
            random_distribution = np.random.dirichlet(np.ones(len(portfolio_)),size=1)
            distrib_vector.append(random_distribution)
            
            #Find the Closing Price for everyday of the portfolio
            portfolio_matmul = np.matmul(random_distribution,portfolio_vector.T)
            
            #Calculate the daily return
            portfolio_matmul = np.diff(portfolio_matmul)/portfolio_matmul[:,1:]
            
            #Select or Final Return and Risk
            portfolio_return = np.average(portfolio_matmul, axis=1)
            portfolio_risk = np.std(portfolio_matmul, axis=1)
            
            #Add our Benchmark info to our lists
            return_vector.append(portfolio_return[0])
            risk_vector.append(portfolio_risk[0])

            #Create Risk Boundaries
        delta_risk = 0.05
        min_risk = np.min(risk_vector)
        max_risk = risk_vector[0]*(1+delta_risk)
        risk_gap = [min_risk, max_risk]

        portfolio_array = np.column_stack((return_vector,risk_vector))[1:,]

        # Rule to create the best portfolio
        # If the criteria of minimum risk is satisfied then:
        if np.where(((portfolio_array[:,1]<= max_risk)))[0].shape[0]>1:
            min_risk_portfolio = np.where(((portfolio_array[:,1]<= max_risk)))[0]
            best_portfolio_loc = portfolio_array[min_risk_portfolio]
            max_loc = np.argmax(best_portfolio_loc[:,0])
            best_portfolio = best_portfolio_loc[max_loc]

        # If the criteria of minimum risk is not satisfied then:
        else:
            min_risk_portfolio = np.where(((portfolio_array[:,1]== np.min(risk_vector[1:]))))[0]
            best_portfolio_loc = portfolio_array[min_risk_portfolio]
            max_loc = np.argmax(best_portfolio_loc[:,0])
            best_portfolio = best_portfolio_loc[max_loc]
        #Visual Representation
        trade_days_per_year = 252
        risk_gap = np.array(risk_gap)*trade_days_per_year
        best_portfolio[0] = np.array(best_portfolio[0])*trade_days_per_year


       
                    
        #Output Table of Distributions
        portfolio_loc = np.where((portfolio_array[:,0]==(best_portfolio[0]/trade_days_per_year))&(portfolio_array[:,1]==(best_portfolio[1])))[0][0]
        best_distribution = distrib_vector[portfolio_loc][0].tolist()
        d = {"Crypto Name": portfolio_, "crypto % in Portfolio": best_distribution}
        output = pd.DataFrame(d)
        output = output.sort_values(by=["crypto % in Portfolio"],ascending=False)
        output= output.style.format({"crypto % in Portfolio": "{:.2%}"})
        with open('str.html','w') as f:
            output.to_html(f)

        filename = 'str.html'
        webbrowser.open_new_tab(filename)           
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
import scipy.optimize as spo
plt.style.use('ggplot')

class Portfolio:

    def __init__(self, stocks: List[str], allocations: List[float], initial_capital: int) -> None:
        self.allocations = allocations
        self.initial = initial_capital

        self.prices = get_close(stocks)
        self.normed = self.prices / self.prices.iloc[0]
        self.position = self.normed * self.allocations * self.initial
        self.port_val = self.position.sum(1)
        self.daily_returns = get_daily_returns(self.port_val)[1:]

    def get_rolling_position(self) -> pd.DataFrame:
        return self.position.sum(1)

    def get_position(self) -> pd.DataFrame:
        return self.position

    def get_current_position(self) -> pd.DataFrame:
        return self.position.iloc[-1]

    def get_daily_returns(self) -> pd.DataFrame:
        return self.daily_returns

    def get_cumulative_return(self) -> float:
        return self.daily_returns.values.sum()

    def get_value(self) -> float:
        return self.current_position().sum()

    def get_avg_daily_return(self) -> float:
        return self.daily_returns.mean()

    def get_risk(self) -> float:
        return self.daily_returns.std()

    def get_sharpe_ratio(self) -> float:
        return np.sqrt(252) * (self.get_avg_daily_return() / self.get_risk())

# returns a dataframe with the daily returns of the stocks in "df"
def get_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    dreturns = df.copy()
    dreturns.iloc[1:] = (dreturns.iloc[1:] / dreturns.iloc[:-1].values) - 1
    dreturns.iloc[0] = 0
    return dreturns

# returns a dataframe with the adjusted closes of all tickers in "symbols" between the dates 10/1/2017 and 10/1/2018
def get_close(symbols: List[str], dates=pd.date_range('2017-10-1', '2018-10-1')) -> pd.DataFrame:
    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        temp_df = pd.read_csv('./data/{}.csv'.format(symbol),
                              index_col='Date',
                              usecols=['Date', 'Adj Close'])
        temp_df = temp_df.rename(columns={'Adj Close': symbol})
        df = df.join(temp_df)
    return df.dropna()

# returns the negative sharpe ratio of portfolio with given floats
def error(allocations: List[float]) -> float:
    ptemp = Portfolio(['AAPL', 'AMZN', 'SPY', 'MSFT', 'GOOG'], allocations, 1000000)
    return -1.0 * ptemp.get_sharpe_ratio()

# main
if __name__ == "__main__":
    p1 = Portfolio(['AAPL', 'AMZN', 'SPY', 'MSFT', 'GOOG'], [0.1, 0.0, 0.4, 0.3, 0.2], 1000000)
    p2 = Portfolio(['AAPL', 'AMZN', 'SPY', 'MSFT', 'GOOG'], [0.0, 0.0, 1.0, 0.0, 0.0], 1000000)
    
    p1.get_rolling_position().plot(title='Portfolio Optimization', label='Naive Portfolio, Sharpe Ratio: {0:.2f}'.format(p1.get_sharpe_ratio()))
    

    weights = spo.minimize(error, x0=[0.1, 0.0, 0.2, 0.3, 0.4], method='SLSQP',
                 bounds=((0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)),
                 constraints={'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] + x[3] + x[4] - 1.0})

    p3 = Portfolio(['AAPL', 'AMZN', 'SPY', 'MSFT', 'GOOG'], weights.x, 1000000)
    p3.get_rolling_position().plot(label='Optimized Portfolio, Sharpe Ratio: {0:.2f}'.format(p3.get_sharpe_ratio()))
    p2.get_rolling_position().plot(label='S&P 500')

    plt.legend(loc='upper left')
    plt.show()

    
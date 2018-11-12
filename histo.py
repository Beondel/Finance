import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

def main():
    df = get_close(['SPY', 'AAPL'], ['2017-10-18', '2018-10-17'])
    rmean = df['SPY'].rolling(20).mean()
    
    dreturns = df.copy()
    dreturns.iloc[1:] = (dreturns.iloc[1:] / dreturns.iloc[:-1].values) - 1
    dreturns.iloc[0] = 0

    meanSPY = dreturns['SPY'].mean()
    meanAAPL = dreturns['AAPL'].mean()
    dreturns['SPY'].hist(bins=20, label='SPY')
    dreturns['AAPL'].hist(bins=20, label='AAPL')

    plt.axvline(meanSPY, color='w', linestyle='dashed', linewidth=2)
    plt.axvline(meanAAPL, color='b', linestyle='dashed', linewidth=2)
    plt.show()

def get_close(symbols: List[str], dates: List[str]) -> pd.DataFrame:
    range = pd.date_range(dates[0], dates[1])
    df = pd.DataFrame(index=range)

    for symbol in symbols:
        temp_df = pd.read_csv('./data/{}.csv'.format(symbol),
                              index_col='Date',
                              usecols=['Date', 'Adj Close'])
        temp_df = temp_df.rename(columns={'Adj Close': symbol})
        df = df.join(temp_df)

    return df.dropna()

if __name__ == "__main__":
    main()
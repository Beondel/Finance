import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

def main():
    companies = ['GOOG']
    dates = pd.date_range('2017-10-1', '2018-10-1')

    df = get_close(companies, dates)
    rm_GOOG = df['GOOG'].rolling(window=20, center=False).mean()
    rstd_GOOG = df['GOOG'].rolling(window=20, center=False).std()
    upper_band = rm_GOOG + 2 * rstd_GOOG
    lower_band = rm_GOOG - 2 * rstd_GOOG

    ax = df['GOOG'].plot(title="Google, 2017", label='Closing Price')
    rm_GOOG.plot(label="Rolling Mean")
    upper_band.plot(label="upper band")
    lower_band.plot(label="lower band")
    ax.legend(loc='upper left')

    plt.show()

def get_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    dreturns = df.copy()
    dreturns.iloc[1:] = (dreturns.iloc[1:] / dreturns.iloc[:-1].values) - 1
    dreturns.iloc[0] = 0
    return dreturns

def get_close(symbols, dates=pd.date_range('2017-10-1', '2018-10-1')) -> pd.DataFrame:
    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        temp_df = pd.read_csv('./data/{}.csv'.format(symbol),
                              index_col='Date',
                              usecols=['Date', 'Adj Close'])
        temp_df = temp_df.rename(columns={'Adj Close': symbol})
        df = df.join(temp_df)
    return df.dropna()

if __name__ == '__main__':
    main()
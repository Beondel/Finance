from typing import List
import pandas as pd
import matplotlib.pyplot as plt


def main():
    companies = ['AAPL', 'AMZN', 'GOOG', 'MSFT', 'SPY']
    dates = ['2018-6-1', '2018-8-31']
    df_close = get_close(companies, dates)
    df_close = df_close / df_close.ix[0]
    print(df_close)
    plot(df_close)

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

def plot(df: pd.DataFrame) -> None:
    axes = df.plot(title='Closing Prices')
    axes.set_xlabel('Date')
    axes.set_ylabel('Closing Price')
    plt.show()

if __name__ == '__main__':
    main()

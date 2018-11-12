import pandas as pd
import matplotlib.pyplot as plt


def max_close(df: pd.DataFrame, symbol: str) -> float:
    return df['Close'].max()


def mean_volume(df: pd.DataFrame, symbol: str) -> float:
    return df['Volume'].mean()


def get(function, symbol: str) -> float:
    df = pd.read_csv("./data/{}.csv".format(symbol))
    return function(df, symbol)


def graph(symbol: str) -> None:
    df = pd.read_csv("./data/{}.csv".format(symbol))
    df[['Adj Close', 'Close']].plot()
    plt.show()

    
if __name__ == "__main__":
    graph('AAPL')

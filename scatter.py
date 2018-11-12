import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stats import get_close, get_daily_returns

def main():
    df = get_close(['AMZN', 'SPY'])
    df = get_daily_returns(df)
    df.plot(kind='scatter', x='SPY', y='AMZN')
    beta, alpha = np.polyfit(df['SPY'], df['AMZN'], 1)
    plt.plot(df['SPY'], beta * df['SPY'] + alpha, '-', color='r')
    print(alpha, beta)
    plt.show()

if __name__ == '__main__':
    main()
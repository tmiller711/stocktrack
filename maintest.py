import pandas as pd

class Stock(object):
    def __init__(self, data):
        self.data = data

    def print_data(self):
        print(self.data)
    # declare functions to perform on stocks
    # such as calculating different things

def run_strat(data):
    balance = 1000
    num_of_shares = 0
    num_of_trades = 0

    for index, row in data.iterrows():
        # print(row['high'])
        if row['RSI'] < 30 and num_of_shares==0:
            # if rsi < 30 buy $1000 at closing price
            num_of_shares = balance/int(row['close'])
            balance = 0
            num_of_trades += 1
        # check to see if rsi > 70 to sell amount of shares
        if row['RSI'] > 70 and num_of_shares > 0:
            balance = num_of_shares*int(row['close'])
            num_of_shares = 0
            num_of_trades += 1

    # if you still own shares after all of it sell it all at latest price
    if num_of_shares > 0:
        balance = num_of_shares* int(data.iloc[-1]['close'])

    return (balance//1000)*100, round(balance, 2), num_of_trades

def main():
    # get data from csv file
    spy = Stock(pd.read_csv(r'stock data/apple.csv'))
    percent_gain, end_total, num_of_trades = run_strat(spy.data)
    print(f"Percent Gain: {percent_gain}%")
    print(f"Ending Total: ${end_total}")
    print(f"Number of Trades: {num_of_trades}")


if __name__=='__main__':
    main()

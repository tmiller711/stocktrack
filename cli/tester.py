import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import click
from datetime import datetime, timedelta
import pathlib

class Test:
    def __init__(self, balance, stock, buy_criteria, sell_criteria, indicators, start_date, end_date):
        self.balance = balance
        self.stock = stock
        self.buy_criteria = buy_criteria
        self.sell_criteria = sell_criteria
        self.indicators = indicators
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.retrieve_stock_data()
        self.num_of_shares = 0
        self.num_of_trades = 0
        self.output = ""
        self.output += f"\nBuy Criteria: {self.buy_criteria}\nSell criteria: {self.sell_criteria}\n"
        self.output += f"Starting Balance: ${balance} | Running test on {self.stock}\n\n"
        self.graph_output = {'date': [start_date], 'balance': [balance]}

    def run_test(self):
        for index, row in self.data.iterrows():
            if self.balance != 0:
                # look for buying
                # check if each buy criteria is True and then buy if so
                buy = False
                for criteria in self.buy_criteria:
                    # possibly use a switch statement for the different criteria
                    if 'crossing' in criteria:
                        buy = self.crossing(row, criteria.split(' ', 1)[1])
                        if buy == False:
                            break
                        
                if buy == True:
                    # buy as many shares as I can
                    self.num_of_shares = self.balance/int(row['close'])
                    self.balance = 0
                    self.output += f"{row['time']} | Bought {round(self.num_of_shares, 1)} shares @ ${row['close']}\n"

            else:
                # look to sell
                # check if each sell criteria is True and then sell if so
                sell = False
                for criteria in self.sell_criteria:
                    if 'crossing' in criteria:
                        sell = self.crossing(row, criteria.split(' ', 1)[1])
                        if sell == False:
                            break
                if sell == True:
                    self.balance = self.num_of_shares*int(row['close'])
                    self.output += f"{row['time']} | Sold {round(self.num_of_shares, 1)} shares @ ${row['close']}\n"
                    self.output += f"Balance: ${int(self.balance)}\n"
                    self.num_of_shares = 0
                    self.num_of_trades += 1
                    self.graph_output['date'].append(row['time'])
                    self.graph_output['balance'].append(self.balance)


        # if you still own shares after all of it sell it all at latest price
        if self.num_of_shares > 0:
            self.output += f"{row['time']} | Sold {round(self.num_of_shares, 1)} shares @ ${int(self.data.iloc[-1]['close'])}\n"
            self.balance = self.num_of_shares* int(self.data.iloc[-1]['close'])
            self.output += f"Balance: ${int(self.balance)}\n"
            self.num_of_trades += 1

        self.output += f"Number of trades: {self.num_of_trades} | Percent gain: {round((self.balance/1000)*100, 2)}%"
        self.results_graph()
        
    def crossing(self, data, criteria):
        # check the criteria/argument and if it is true return True
        criteria = criteria.split()
        # replace variables with their values
        if criteria[2] == 'open_price':
            criteria[2] = int(data['open'])
        elif criteria[2] == 'close_price':
            criteria[2] = int(data['close'])
        elif criteria[2] == 'high_price':
            criteria[2] = int(data['high'])
        elif criteria[2] == 'low_price':
            criteria[2] = int(data['low'])

        if criteria[1] == '<':
            return (int(data[criteria[0].upper()]) < int(criteria[2]))
        elif criteria[1] == '>':
            return (int(data[criteria[0].upper()]) > int(criteria[2]))
    
    def retrieve_stock_data(self):
        path = pathlib.Path(__file__).parent.resolve()
        with open(f"{path}/credentials.txt", 'r') as file:
            data = file.read()
        token_dict = json.loads(data)
        headers = {"Authorization": f"Bearer {token_dict['access']}"}
        r = requests.post(f"http://127.0.0.1:8000/api/{self.stock}/", json={'indicators': self.indicators, 'start_date': self.start_date, 'end_date': self.end_date}, headers=headers)
        data = json.loads(r.text)
        data = pd.DataFrame(data=data)

        return data

    def save_results(self, output=None):
        if output:
            if '.txt' in output:
                output.replace('.txt', '')
            with open(f"{output}.txt", 'w') as file:
                file.write(self.output)
                file.write(self.buy_and_hold())
                click.echo(f"Results of test saved at {output}.txt")
        else:
            # if no output file just echo results
            self.buy_and_hold()
            click.echo(f"Num of Trades: {self.num_of_trades}")
            click.echo(f"Ending Balance: ${round(self.balance, 2)}")
            click.echo(f"Percent Gain: {round((self.balance/1000)*100, 2)}%")

    def buy_and_hold(self):
        start_price = self.data.iloc[0]['close']
        end_price = self.data.iloc[-1]['close']

        return f"\n\nReturn if you just bought and held {self.stock} from {self.start_date} to {self.end_date}: {round((end_price/start_price)*100, 2)}%"

    def results_graph(self):
        df = pd.DataFrame(self.graph_output)
        plt.plot(df['date'], df['balance'])

        plt.show()


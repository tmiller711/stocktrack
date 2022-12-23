import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import click
from datetime import datetime, timedelta
import pathlib
import os

class HandleResults:
    """ 
    Handles the printing, saving, and showing of results for a stock
    testing scenario
    
    Attributes:
        output (str): the results of the testing scenari as a string
        graph_output (dict): A dictionary containing the dates and balances for each step of the testing scenari
    """
    def __init__(self, output, graph_output):
        self.output = output
        self.graph_output = graph_output

    def print_results(self):
        click.echo(self.output)

    def save_results(self, path):
        if '.txt' in path:
            path.replace('.txt', '')
        with open(f"{path}.txt", 'w') as file:
            file.write(self.output)
            # file.write(self.buy_and_hold())
            click.echo(f"Results of test saved at {path}.txt")
    
    def show_graph(self):
        df = pd.DataFrame(self.graph_output)
        plt.plot(df['date'], df['balance'])

        plt.show()

class Tester:
    """
    Tests a stock based on given criteria and indicators

    Attributes:
        balance (int): The starting balance for the testing scenario.
        stock (str): The ticker symbol for the stock being tested.
        buy_criteria (list): A list of strings representing the criteria to be met for buying the stock.
        sell_criteria (list): A list of strings representing the criteria to be met for selling the stock.
        indicators (list): A list of strings representing the indicators to be used in the testing scenario.
        start_date (str): The start date for the testing scenario in the format 'YYYY-MM-DD'.
        end_date (str): The end date for the testing scenario in the format 'YYYY-MM-DD'.
        stock_data (pandas DataFrame): A DataFrame containing the stock data for the testing scenario.
        num_of_shares (float): The number of shares currently held.
        num_of_trades (int): The number of trades made during the testing scenario.
        last_buy_price (int): The price of the last buy made during the testing scenario.
        output (str): The results of the testing scenario as a string.
        graph_output (dict): A dictionary containing the dates and balances for each step of the testing scenario.
        strategy (Strategy): An object representing the strategies used in the testing scenario.
    """
    def __init__(self, stock, buy_criteria, sell_criteria, indicators, start_date, end_date):
        self.balance = 1000
        self.stock = stock
        self.buy_criteria = buy_criteria
        self.sell_criteria = sell_criteria
        self.indicators = indicators
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = self.retrieve_stock_data()
        self.num_of_shares = 0
        self.num_of_trades = 0
        self.last_buy_price = 0
        self.output = ""
        self.output += f"\nBuy Criteria: {self.buy_criteria}\nSell criteria: {self.sell_criteria}\n"
        self.output += f"Starting Balance: ${self.balance} | Running test on {self.stock}\n\n"
        self.graph_output = {'date': [start_date], 'balance': [self.balance]}
        self.strategy = Strategy(indicators, self.stock_data)

    def run_test(self):
        for index, row in self.stock_data.iterrows():
            if self.balance != 0:
                # look for buying
                # check if each buy criteria is True and then buy if so
                buy = self.check_criteria(row, self.buy_criteria)
                        
                if buy == True:
                    # buy as many shares as I can
                    self.num_of_shares = self.balance/int(row['close'])
                    self.last_buy_price = row['close']
                    self.balance = 0
                    self.output += f"{row['time']} | Bought {round(self.num_of_shares, 1)} shares @ ${row['close']}\n"

            else:
                # look to sell
                # check if each sell criteria is True and then sell if so
                sell = self.check_criteria(row, self.sell_criteria)

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
            self.output += f"{row['time']} | Sold {round(self.num_of_shares, 1)} shares @ ${int(self.stock_data.iloc[-1]['close'])}\n"
            self.balance = self.num_of_shares* int(self.stock_data.iloc[-1]['close'])
            self.output += f"Balance: ${int(self.balance)}\n"
            self.num_of_trades += 1

        self.output += f"Number of trades: {self.num_of_trades} | Percent gain: {round((self.balance/1000)*100, 2)}%"
        self.output += f"\n\nReturn if you just bought and held {self.stock} from {self.start_date} to {self.end_date}: {self.strategy.buy_and_hold()}%"
        
        return self.output, self.graph_output
    
    def check_criteria(self, row, all_criteria):
        for criteria in all_criteria:
                # possibly use a switch statement for the different criteria
                if 'crossing' in criteria:
                    check = self.strategy.crossing(row, criteria.split(' ', 1)[1])
                    if check == False:
                        return False
                elif 'divergence' in criteria:
                    check = self.strategy.divergence(row, criteria.split(' ', 1)[1])
                    if check == False:
                        return False
                elif 'tp' or 'sl' in criteria:
                    check = self.strategy.tp_sl(row, criteria.split(' '), self.last_buy_price)
                    if check == False:
                        return False

        return True

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

def calc_percent_diff(current, previous):
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


class Strategy:
    """
    A class to represent and execute various trading strategies.
    
    Attributes:
        indicators (list): A list of indicators to use in the strategies.
        stock_data (DataFrame): A Pandas DataFrame containing the stock data to use in the strategies.
    """
    def __init__(self, indicators, stock_data):
        self.indicators = indicators
        self.stock_data = stock_data

    def crossing(self, stock_data, criteria):
        # check the criteria/argument and if it is true return True
        criteria = criteria.split()
        # replace variables with their values
        if criteria[2] in ['open', 'close', 'high', 'low']:
            criteria[2] = int(stock_data[criteria[2]])
        if criteria[2] in self.indicators:
            criteria[2] = int(stock_data[criteria[2]])

        if criteria[1] == '<':
            return (int(stock_data[criteria[0]]) < int(criteria[2]))
        elif criteria[1] == '>':
            return (int(stock_data[criteria[0]]) > int(criteria[2]))
    
    def tp_sl(self, stock_data, criteria, last_buy_price):
        # if sl or tp is hit sell/ return True
        take_profit = int(criteria[1].replace('%', ''))
        stop_loss = int(criteria[3].replace('%', ''))
        # check both closing price and high price
        if calc_percent_diff(stock_data['close'], last_buy_price) >= take_profit or calc_percent_diff(stock_data['high'], last_buy_price) >= take_profit:
            return True
        
        elif calc_percent_diff(stock_data['close'], last_buy_price) <= stop_loss or calc_percent_diff(stock_data['low'], last_buy_price) <= stop_loss:
            return True
    
    def divergence(self, stock_data, criteria):
        criteria = criteria.split()
        # get the value 30 rows before the current one or none
        index = self.stock_data.loc[self.stock_data['time'] == stock_data['time']].index
        if index <= int(criteria[2]):
            return False

        x_days_ago_data = self.stock_data.iloc[index-int(criteria[2])]

        if criteria[0] == 'bull':
            # check if price is lower than it was 30 days ago but rsi is higher than it was 30 days ago
            if int(stock_data['close']) < int(x_days_ago_data['close']) and int(stock_data[criteria[1]]) > int(x_days_ago_data[criteria[1]]):
                return True
        
        if criteria[0] == 'bear':
            if int(stock_data['close']) > int(x_days_ago_data['close']) and int(stock_data[criteria[1]]) < int(x_days_ago_data[criteria[1]]):
                return True
        
    def buy_and_hold(self):
        start_price = self.stock_data.iloc[0]['close']
        end_price = self.stock_data.iloc[-1]['close']

        return round((end_price/start_price)*100, 2)
import pandas as pd
import requests
import json

class Test:
    def __init__(self, balance, stock, buy_criteria, sell_criteria, indicators):
        self.balance = balance
        self.stock = stock
        self.buy_criteria = buy_criteria
        self.sell_criteria = sell_criteria
        self.indicators = indicators
        self.data = self.retrieve_stock_data()
        self.num_of_shares = 0
        self.num_of_trades = 0

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
                    self.num_of_shares = 0
                    self.num_of_trades += 1


        # if you still own shares after all of it sell it all at latest price
        if self.num_of_shares > 0:
            self.balance = self.num_of_shares* int(self.data.iloc[-1]['close'])
            self.num_of_trades += 1

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
        with open('credentials.txt', 'r') as file:
            data = file.read()
        token_dict = json.loads(data)
        # print(token_dict['access'])
        headers = {"Authorization": f"Bearer {token_dict['access']}"}
        r = requests.post(f"http://127.0.0.1:8000/api/{self.stock}/", json={'indicators': self.indicators}, headers=headers)
        data = json.loads(r.text)
        data = pd.DataFrame(data=data)

        return data

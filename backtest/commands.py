import click
import pandas as pd
import os

class Interpreter():
    def __init__(self, test):
        self.test = test
        self.available_indicators = ['rsi', '21ma']
        self.used_indicators = []
        self.available_commands = ['crossing']
        self.buy_criteria = []
        self.sell_criteria = []

    def parse_indicators(self):
        # get the first line and see all the indicators they want to use
        indicators = self.test.readline().split()
        for indicator in indicators:
            if indicator in self.available_indicators:
                self.used_indicators.append(indicator)

        return self.used_indicators

    def parse_test_criteria(self):
        buy = False
        sell = False
        for line in self.test:
            if 'buy' in line:
                # loop over the buy criteria until it reaches the }
                buy = True

            if 'sell' in line:
                sell = True
                
            if '}' in line:
                buy = False
                sell = False

            if buy == True:
                # check if the command is available
                if line.strip().split()[0] in self.available_commands:
                    self.buy_criteria.append(line.strip())
                    
            if sell == True:
                # check if the command is available
                if line.strip().split()[0] in self.available_commands:
                    self.sell_criteria.append(line.strip())

        return self.buy_criteria, self.sell_criteria
     
class Test:
    def __init__(self, balance, buy_criteria, sell_criteria):
        self.balance = balance
        self.buy_criteria = buy_criteria
        self.sell_criteria = sell_criteria
        self.data = pd.read_csv(r'backtest/data/spy.csv')
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

        if criteria[1] == '<':
            return (int(data[criteria[0].upper()]) < int(criteria[2]))
        elif criteria[1] == '>':
            return (int(data[criteria[0].upper()]) > int(criteria[2]))


@click.command(name='create')
@click.argument('testname', required=True)
def create_test(testname):
    '''
    Create a test
    '''
    # Create a file with the name they specified
    with open(f'backtest/tests/{testname}.txt', 'w') as file:
        click.echo("file created")
        # after they created the file present them with a text editor to make the test

@click.command(name='run')
@click.argument('testname', required=True)
def run_test(testname):
    '''
    Run a test
    '''
    # have click prompt the user for the stock to run the test on
    # maybe also prompt the user for what test to run instead of having to put it in on run
    test_file = open(f'backtest/tests/{testname}.txt', 'r')
    # make a test to check if the file exists
    # print(test_file.read())
    test = Interpreter(test_file)
    (buy_criteria, sell_criteria) = test.parse_test_criteria()
    run_commands = Test(1000, buy_criteria, sell_criteria)

    run_commands.run_test()
    (ending_bal, num_of_trades) = run_commands.balance, run_commands.num_of_trades 
    click.echo(ending_bal)
    click.echo(num_of_trades)

    test_file.close()

@click.command(name='alltests')
def get_tests():
    '''
    Display all user created tests
    '''
    tests = os.listdir('backtest/tests')
    if len(tests) == 0:
        click.echo('User has not many any tests')

    else:
        for test in tests:
            click.echo(test)

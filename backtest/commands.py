import click
import os

class Interpreter():
    def __init__(self, test):
        self.test = test
        self.available_indicators = ['rsi', '21ma']
        self.used_indicators = []
        self.available_commands = ['crossing']
        self.buy_criteria = []
        self.sell_criteria = []
        self.parse_indicators()
        self.parse_test_criteria()

    def parse_indicators(self):
        # get the first line and see all the indicators they want to use
        indicators = self.test.readline().split()
        for indicator in indicators:
            if indicator in self.available_indicators:
                self.used_indicators.append(indicator)
        click.echo(self.used_indicators)

    def parse_test_criteria(self):
        buy = False
        sell = False
        for line in self.test:
            click.echo(line.strip())
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

        print(self.buy_criteria, self.sell_criteria)


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
    test_file = open(f'backtest/tests/{testname}.txt', 'r')
    # make a test to check if the file exists
    # print(test_file.read())
    test = Interpreter(test_file)

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

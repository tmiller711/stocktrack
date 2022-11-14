import click
import os

def available_indicators():
    return ['rsi', '100ma', 'macd', 'signal', 'volume', 'volumema']

class Interpreter():
    def __init__(self, test):
        self.test = test
        self.available_indicators = available_indicators()
        self.used_indicators = []
        self.available_commands = ['crossing', 'divergence', 'tp', 'sl']
        self.buy_criteria = []
        self.sell_criteria = []

    def parse_indicators(self):
        # get the first line and see all the indicators they want to use
        indicators = self.test.readline().split(' ', 1)[1].split()
        for indicator in indicators:
            if indicator in self.available_indicators:
                self.used_indicators.append(indicator)
            else:
                click.echo(click.style(f"Indicator '{indicator}' not available, please update test", fg='red'))
                quit()

        return self.used_indicators

    def parse_test_criteria(self):
        buy = False
        sell = False
        for line in self.test:
            if '}' in line:
                buy = False
                sell = False

            if buy == True:
                # check if the command is available
                command = line.strip().split()[0]
                if command in self.available_commands:
                    self.buy_criteria.append(line.strip())
                else:
                    click.echo(click.style(f"Command '{command}' not available, please edit test", fg='red'))
                    exit()
                    
            if sell == True:
                # check if the command is available
                command = line.strip().split()[0]
                if command in self.available_commands:
                    self.sell_criteria.append(line.strip())
                else:
                    click.echo(click.style(f"Command '{command}' not available, please edit test", fg='red'))
                    exit()

            if 'buy' in line:
                # loop over the buy criteria until it reaches the }
                buy = True

            if 'sell' in line:
                sell = True


        return self.buy_criteria, self.sell_criteria



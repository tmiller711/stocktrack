import click
import os

class Interpreter():
    available_indicators = ['rsi', '100ma', 'macd', 'signal', 'volume', 'volumema']

    def __init__(self, test):
        self.test = test
        self.used_indicators = []
        self.available_commands = ['crossing', 'divergence', 'tp', 'sl']

    def parse_indicators(self):
        # get the first line and see all the indicators they want to use
        indicators = self.test.readline().split()
        # remove the use word from the line
        indicators.pop(0)

        for indicator in indicators:
            if indicator in self.available_indicators:
                self.used_indicators.append(indicator)
            else:
                click.echo(click.style(f"Indicator '{indicator}' not available, please update test", fg='red'))
                quit()

        return self.used_indicators

    def parse_test_criteria(self):
        criteria = {'buy': [], 'sell': []}
        
        for line in self.test:
            line = line.strip()
            if not line:
                continue

            if "buy" in line:
                current_section = "buy"
                continue
            elif "sell" in line:
                current_section = "sell"
                continue
            elif line == "}":
                current_section == None
                continue

            # check if the command is available
            command = line.split()[0]
            if command not in self.available_commands:
                click.echo(click.style(f"Command '{command}' not available, please edit test", fg='red'))
                exit()
            
            criteria[current_section].append(line)


        return criteria['buy'], criteria['sell']



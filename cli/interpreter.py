class Interpreter():
    def __init__(self, test):
        self.test = test
        self.available_indicators = ['rsi', '100ma', 'macd', 'signal', 'volume', 'volumema']
        self.used_indicators = []
        self.available_commands = ['crossing', 'divergence', 'tp', 'sl']
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



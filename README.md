StockTrack CLI Documentation

StockTrack is a command line interface (CLI) tool that allows users to manage their assets, perform tests on strategies, and edit text files. It provides the following commands:

### create
This command creates a new test. It takes in a single required argument testname, which specifies the name of the test to be created.

To create a test, run the following command:

```stocktrack create <testname>```

### edit
This command allows the user to edit a previously created test.

To edit a test, run the following command:

```stocktrack edit```
This will present the user with a list of all the tests they have created and prompt them to select the test they want to edit. The selected test will then be opened in a text editor for the user to edit.

### run
This command allows the user to run a test. It takes in the following arguments:

- **'testname'**: The name of the test to be run.
- **'startdate'**: The start date for the test in the format YYYY-MM-DD.
- **'enddate'**: The end date for the test in the format YYYY-MM-DD.
It also has the following optional arguments:

- **'-o'**, **'--output'**: The name of the file where the results of the test should be saved. If this argument is not specified, the results are printed to the terminal.
- **'-g'**, **'--graph'**: Whether or not to generate a graph of the test results.
To run a test, run the following command:

```stocktrack run <testname> <startdate> <enddate> [OPTIONS]```

### setdir
This command allows the user to set the directories where the tests and results are stored. It takes in the following arguments:

- **'testdir'**: The directory where the tests should be stored.
- **'resultsdir'**: The directory where the results should be stored.
To set the directories, run the following command:

```stocktrack setdir <testdir> <resultsdir>```

### results
This command allows the user to view the results of a previously run test. It presents the user with a list of all the result files in the directory specified by the results_dir.txt file and prompts the user to select the file they want to view. It then displays the contents of the selected file.

To view the results of a test, run the following command:

```stocktrack results```

### Account commands
- **'account'**: Returns the email of the active account if the user is signed in.
- **'login'**: Logs the user in to the API with the credentials provided.
- **'register'**: Registers an account with the API using the credentials provided.

### Test Language
Tests are created by writing a script using the test language outlined below. The test language consists of a list of indicators to be used in the test and buy and sell criteria specified using the buy and sell keywords. The criteria can be defined using the crossing and divergence commands, which allow the user to specify conditions based on the values of indicators. The tp sl command can be used to specify take profit and stop loss levels for trades.

Here are a few examples of tests written in the test language:

Example 1:

```
use rsi

buy {
    crossing rsi < 30
}

sell {
    crossing rsi > 70
}
```
This test will buy a stock when the rsi is less than 30 and sell when the rsi is greater than 70.


Example 2:

```
use macd signal

buy {
    crossing macd > signal
}

sell {
    tp 7% sl -2%
}
```
This test will buy stock when the macd line crosses the signal line and sell when either the take profit (7%) or the stop loss (-2%) are hit.

Example 3:

```
use rsi

buy {
    divergence bull rsi 15
}

sell {
    crossing rsi > 70
}
```
This test will buy when there is divergence on the rsi looking back 15 days and sell when/if the rsi goes above 70.


### Available Indicators
The following indicators are available to be used in tests:

- rsi
- macd
- signal

### Additional Information

- The **'use'** keyword is used to specify the indicators to be used in the test. The indicators should be separated by a space.
- The **'buy'** and **'sell'** keywords are used to define the criteria for when to buy or sell a stock. The criteria should be defined within curly braces **'{}'**.
- The **'crossing'** command is used to specify when an indicator crosses a certain value. It takes in two arguments: the indicator and the value.
- The **'divergence'** command is used to specify when there is divergence on an indicator. It takes in three arguments: the type of divergence (**'bull'** or **'bear'**), the indicator to use for the divergence, and the number of days to check back for the divergence.
- The **'tp sl'** command is used to specify the take profit and stop loss levels for a trade. It takes in two arguments: the take profit level and the stop loss level. Both arguments should be specified as a percentage.

### Requirements
To use StockTrack, you need the following installed on your system:

- Python 3.6 or higher
- The following Python packages: click, requests, pandas, curses, pathlib
- A text editor (e.g. gedit, vi, emacs)

### Getting Started
To get started with StockTrack, follow these steps:

1. Install Python and the required packages.
2. Clone the StockTrack repository.
3. Run the stocktrack command followed by the desired subcommand and arguments.

For example, to create a new test, run the following command:

```stocktrack create <testname>```

This will create a new test file in the tests directory with the name **'testname'**. The user can then edit the test by opening the file in a text editor.

To run a test, use the **'run'** command:

```stocktrack run <testname> <startdate> <enddate> [OPTIONS]```
This will run the test testname on the specified dates and display or save the results according to the specified options.

### Additional Features
StockTrack also provides the following additional features:

- The **'alltests'** command allows the user to view all the tests they have created.
- The **'delete'** command allows the user to delete a previously created test.

### Troubleshooting
If you encounter any issues while using StockTrack, try the following:

- Make sure you have installed the required packages.
- Make sure you are using the correct syntax for the commands and arguments.
- Check the **'credentials.txt'** file to ensure that your login credentials are correct.
- If you are having issues with the API, make sure that it is running and reachable at the specified address.

If you continue to have issues, please file an issue in the StockTrack repository or reach out to the developers for assistance.
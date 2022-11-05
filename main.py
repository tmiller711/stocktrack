import click
import requests
from backtest import commands as backtest_commands
import pandas as pd
import os
from interpreter import Interpreter
from tester import Test

@click.group()
@click.version_option(package_name='stocktrack')
# @click.pass_context
def main():
    """
    Commands to manage your assets
    """
    pass

@click.command(name='create')
@click.argument('testname', required=True)
def create_test(testname):
    '''
    Create a test
    '''
    # Create a file with the name they specified
    with open(f'backtests/{testname}.txt', 'w') as file:
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
    test_file = open(f'backtests/{testname}.txt', 'r')
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
    tests = os.listdir('backtests')
    if len(tests) == 0:
        click.echo('User has not many any tests')

    else:
        for test in tests:
            click.echo(test.replace('.txt', ''))

main.add_command(run_test)
main.add_command(get_tests)
main.add_command(create_test)


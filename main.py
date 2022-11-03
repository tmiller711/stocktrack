import click
import requests
from backtest import commands as backtest_commands

@click.group()
@click.version_option(package_name='stocktrack')
# @click.pass_context
def main():
    """
    Commands to manage your assets
    """
    pass

@click.group(name='test')
def test_group():
    '''
    Group to test strategies
    '''
    pass

test_group.add_command(backtest_commands.create_test)
test_group.add_command(backtest_commands.run_test)

@click.group(name='get')
def get_group():
    '''
    Group of commands to get something
    '''
    pass

# get_group.add_command(get_stock_price)
main.add_command(get_group)
main.add_command(test_group)


import click

@click.command(name='create')
@click.argument('testname', required=True)
def create_test(testname):
    '''
    Create a test
    '''
    # Create a file with the name they specified
    with open(f'backtest/tests/{testname}.txt', 'w') as file:
        click.echo("file created")

@click.command(name='run')
@click.argument('testname', required=True)
def run_test(testname):
    '''
    Run a test
    '''
    test_file = open(f'backtest/tests/{testname}.txt', 'r')
    # make a test to check if the file exists
    click.echo(test_file.read())
    test_file.close()



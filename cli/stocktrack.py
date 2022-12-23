import click
import requests
import pandas as pd
import os
from cli.interpreter import Interpreter
from cli.strategy_tester import Tester, HandleResults
import json
from datetime import date, timedelta, datetime
import sys
from cli.texteditor import main as texteditor
import curses
import pathlib
import subprocess

def get_path():
    return pathlib.Path(__file__).parent.resolve()

@click.group()
@click.version_option(package_name='stocktrack')
def main():
    """
    Commands to manage your assets
    """
    pass

def check_token():
    try:
        with open(f"{get_path()}/credentials.txt", 'r') as file:
            data = json.loads(file.read())
            r = requests.get('http://127.0.0.1:8000/account/getaccount', headers={'Authorization': f"Bearer {data['access']}"})
            if r.ok:
                pass
            else:
                click.echo(click.style("Not logged in", fg='red'))
                exit()
    except:
        click.echo(click.style("Not logged in", fg='red'))
        exit()

def get_test_dir():
    try:
        with open(f"{get_path()}/test_dir.txt", "r") as f:
            return f.read().strip()
    except:
        click.echo(click.style("Need to specify directory to tests, run 'stocktrack setdir'", fg='red'))
        quit()

def get_results_dir():
    try:
        with open(f"{get_path()}/results_dir.txt", "r") as f:
            return f.read().strip()
    except:
        click.echo(click.style("Need to specify directory to results, run 'stocktrack setdir'", fg='red'))
        quit()

@click.command(name='create')
@click.argument('testname', required=True)
@click.option('-ne', '--noeditor', is_flag=True, help="Don't pop up text editor")
def create_test(testname, noeditor):
    '''
    Create a test
    '''
    # check if the test already exists
    test_dir = get_test_dir()

    if os.path.isfile(f"{test_dir}/{testname}.txt"):
        click.echo(click.style(f"Test '{testname}' already exists, Edit instead", fg='red'))
        exit()
    # Create a file with the name they specified
    with open(f'{test_dir}/{testname}.txt', 'w') as file:
        click.echo(f"Available indicators: {Interpreter.available_indicators}")
        click.echo(click.style(f"{testname} created at {test_dir}", fg='green'))
        # after they created the file present them with a text editor to make the test
    
    if noeditor == False:
        subprocess.run(['gedit', f'{test_dir}/{testname}.txt'])

@click.command(name='edit')
def edit_test():
    '''
    Edit a previously made test
    '''
    # show user all tests they created
    test_dir = get_test_dir()
    tests = os.listdir(test_dir)
    tests = [test.replace(".txt", "") for test in tests]
    if len(tests) == 0:
        click.echo(click.style('User has not made any tests', fg='red'))
        exit()

    for test in tests:
        click.echo(test)

    test_to_edit = click.prompt("Which test would you like to edit?")
    if test_to_edit not in tests:
        click.echo(click.style(f"Test '{test_to_edit}' does not exist", fg='red'))
        exit()

    # open editor with test
    subprocess.run(['gedit', f'{test_dir}/{test_to_edit}.txt'])


@click.command(name='run')
@click.option('-o', '--output')
@click.option('-g', '--graph', is_flag=True, help="Show output graph")
def run_test(output, graph):
    '''
    Run a test
    '''
    test_dir = get_test_dir()
    results_dir = get_results_dir()
    check_token()
    if output == None:
        click.echo(click.style("No output selected. Printing results instead", fg='blue'))
    # prompt user for test name
    test_name = click.prompt("What is the test you'd like to use?")
    try:
        test_file = open(f'{test_dir}/{test_name}.txt', 'r')
    except:
        click.echo(click.style(f"Test: '{test_name}.txt' does not exist", fg='red'))
        exit()
        
    click.echo(f"Available stocks: {avail_stocks()}")
    stock = click.prompt("What stock would you like to test on?").upper()
    while stock not in avail_stocks():
        stock = click.prompt(click.style(f"'{stock}' not available, please select valid stock", fg='red')).upper()
    timeframe = click.prompt("How many years back would you like to test?", type=int)

    # make a test to check if the file exists
    test = Interpreter(test_file)
    indicators = test.parse_indicators()
    (buy_criteria, sell_criteria) = test.parse_test_criteria()

    end_date = date.today()
    start_date = end_date - timedelta(days=(timeframe*365))

    run_commands = Tester(stock, buy_criteria, sell_criteria, indicators, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    results, graph_data = run_commands.run_test()

    o = HandleResults(results, graph_data)
    if output:
        output = results_dir + "/" + output
        o.save_results(output)
    else:
        o.print_results()
        if graph == True:
            o.show_graph()

    test_file.close()

@click.command(name='alltests')
def get_tests():
    '''
    Display all user created tests
    '''
    test_dir = get_test_dir()
    tests = os.listdir(test_dir)
    if len(tests) == 0:
        click.echo(click.style('User has not made any tests', fg='red'))

    else:
        for test in tests:
            click.echo(test.replace('.txt', ''))

@click.command(name="delete")
def delete_test():
    '''
    Delete a back test
    '''
    test_dir = get_test_dir()
    tests = os.listdir(test_dir)
    if len(tests) == 0:
        click.echo(click.style('User has no tests to delete', fg='red'))

    for test in tests:
        click.echo(click.style(test.replace('.txt', ''), fg='green'))
    del_test = click.prompt("Which test would you like to delete?")
    try:
        os.remove(f"{test_dir}/{del_test}.txt")
        click.echo(click.style(f"{del_test} Successfully Deleted", fg='green'))
    except:
        click.echo(click.style(f"Error deleting {del_test}", fg='red'))

@click.command(name="results")
def show_results():
    '''
    Show results of previous tests
    '''
    results_dir = get_results_dir()
    results = os.listdir(f'{results_dir}')
    if len(results) == 0:
        click.echo(click.style("No results to show", fg='red'))
        exit()

    for result in results:
        click.echo(click.style(result.replace(".txt", ''), fg='green'))

    result_to_view = click.prompt("Which test would you like to view?")
    try:
        with open(f"{results_dir}/{result_to_view}.txt", "r") as f:
            click.echo(f.read())
    except:
        click.echo(click.style("Could not find result", fg='red'))

@click.command(name='setdir')
def set_directory():
    '''
    Sets the directory of tests and results
    '''
    test_dir = click.prompt("What is the full path to the directory for where you want to store tests?")
    with open(f"{get_path()}/test_dir.txt", 'w') as file:
        file.write(test_dir)

    results_dir = click.prompt("What is the full path to the directory to store results?")
    with open(f"{get_path()}/results_dir.txt", 'w') as file:
        file.write(results_dir)

def avail_stocks():
    '''
    View all available stocks to test
    '''
    r = requests.get('http://127.0.0.1:8000/api/stocks/')
    stocks = r.text.replace('"', "")    
    return stocks

main.add_command(run_test)
main.add_command(get_tests)
main.add_command(create_test)
main.add_command(edit_test)
main.add_command(show_results)
main.add_command(delete_test)
main.add_command(set_directory)

def check_login():
    try:
        with open(f'{get_path()}/credentials.txt', 'r') as file:
            data = json.loads(file.read())
            r = requests.get('http://127.0.0.1:8000/account/getaccount', headers={'Authorization': f"Bearer {data['access']}"})
            if r.ok:
                click.echo(click.style("Already signed in and token is valid", fg='green'))
                return False
    except:
        pass

@click.command(name='register')
def register():
    '''
    Register new account
    '''
    # check if user already logged in/token is valid
    check_login()

    # make a post request to the api to create a view
    email = click.prompt("Please enter the email to register", type=str)
    while '@' not in email or '.com' not in email:
        email = click.prompt(click.style("Please enter a valid email", fg='red'))

    password1, password2 = '8', ''
    while password1 != password2 or len(password1) < 7:
        password1 = click.prompt("Password | Must be 7 character or more", hide_input=True)
        password2 = click.prompt("Password (Confirm)", hide_input=True)
        if password1 != password2:
            click.echo(click.style("Passwords do not match, please try again", fg='red'))

    r = requests.post('http://127.0.0.1:8000/account/register', json={'email': email, 'password': password1})
    auth = requests.post('http://127.0.0.1:8000/api/token/', json={'email': email, 'password': password1})
    if r.ok and auth.ok:
        with open(f'{get_path()}/credentials.txt', 'w') as cred_file:
            cred_file.write(auth.text)
            click.echo(click.style("Account successfully registered", fg='green'))
            click.echo("Login valid for 30 days")
    else:
        click.echo(click.style("Error creating account, try again later", fg='red'))

@click.command(name='login')
def login():
    '''
    Login to account
    '''
    if check_login() == False:
        exit()

    email = click.prompt("Please enter your email", type=str)
    while '@' not in email or '.com' not in email:
        email = click.prompt(click.style("Please enter a valid email", fg='red'))

    password = click.prompt("Enter password", type=str, hide_input=True)

    r = requests.post('http://127.0.0.1:8000/api/token/', json={'email': email, 'password': password})
    if r.ok:
        # save login token/credentials in file
        with open(f'{get_path()}/credentials.txt', 'w') as cred_file:
            cred_file.write(r.text)
            click.echo(click.style("Successfully Logged In", fg='green'))
            click.echo("Login valid for 30 days")
    else:
        click.echo(click.style("Error logging in", fg='red'))

@click.command(name='account')
def account():
    '''
    View account details
    '''
    try:
        with open(f'{get_path()}/credentials.txt', 'r') as file:
            data = file.read()
    except:
        click.echo(click.style("Credentials do not exist, please login", fg='red'))
        exit()

    token_dict = json.loads(data)
    # print(token_dict['access'])
    headers = {"Authorization": f"Bearer {token_dict['access']}"}

    r = requests.get('http://127.0.0.1:8000/account/getaccount', headers=headers)
    if r.ok:
        user_data = json.loads(r.text)
        click.echo("User email:")
        click.echo(user_data['email'])
    else:
        click.echo(click.style("Error retrieving user data", fg='red'))

@click.command(name='logout')
def logout():
    '''
    Log out of account
    '''
    try:
        os.remove(fr"{get_path()}/credentials.txt")
        click.echo(click.style("Successfully logged out", fg='green'))
    except:
        click.echo(click.style("error logging out", fg='red'))

main.add_command(register)
main.add_command(login)
main.add_command(account)
main.add_command(logout)

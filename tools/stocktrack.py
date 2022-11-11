import click
import requests
import pandas as pd
import os
from tools.interpreter import Interpreter
from tools.tester import Test
import json
from datetime import date, timedelta, datetime
import sys
from tools.texteditor import main as texteditor
import curses

@click.group()
@click.version_option(package_name='stocktrack')
def main():
    """
    Commands to manage your assets
    """
    pass

def check_token():
    try:
        with open('credentials.txt', 'r') as file:
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

@click.command(name='create')
@click.argument('testname', required=True)
def create_test(testname):
    '''
    Create a test
    '''
    # check if the test already exists
    if os.path.isfile(f"backtests/{testname}.txt"):
        click.echo(click.style(f"Test '{testname}' already exists, Edit instead", fg='red'))
        exit()
    # Create a file with the name they specified
    with open(f'backtests/{testname}.txt', 'w') as file:
        curses.wrapper(texteditor, filename=rf"backtests/{testname}.txt")
        click.echo(click.style("file created", fg='green'))
        # after they created the file present them with a text editor to make the test

@click.command(name='edit')
def edit_test():
    '''
    Edit a previously made test
    '''
    # show user all tests they created
    tests = os.listdir('backtests')
    tests = [test.replace(".txt", "") for test in tests]
    print(tests)
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
    curses.wrapper(texteditor, filename=rf"backtests/{test_to_edit}.txt")


@click.command(name='run')
@click.option('-o', '--output')
def run_test(output):
    '''
    Run a test
    '''
    check_token()
    if output == None:
        click.echo(click.style("No output selected. Printing results instead", fg='blue'))
    # prompt user for test name
    test_name = click.prompt("What is the test you'd like to use?")
    try:
        test_file = open(f'backtests/{test_name}.txt', 'r')
    except:
        click.echo(click.style(f"Test: '{test_name}.txt' does not exist", fg='red'))
        exit()
    timeframe = click.prompt("How many years back would you like to test?", type=int)

    # make a test to check if the file exists
    test = Interpreter(test_file)
    indicators = test.parse_indicators()
    (buy_criteria, sell_criteria) = test.parse_test_criteria()

    end_date = date.today()
    start_date = end_date - timedelta(days=(timeframe*365))

    run_commands = Test(1000, "SPY", buy_criteria, sell_criteria, indicators, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    run_commands.run_test()
    run_commands.save_results(output)

    test_file.close()

@click.command(name='alltests')
def get_tests():
    '''
    Display all user created tests
    '''
    tests = os.listdir('backtests')
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
    tests = os.listdir('backtests')
    if len(tests) == 0:
        click.echo(click.style('User has no tests to delete', fg='red'))

    for test in tests:
        click.echo(click.style(test.replace('.txt', ''), fg='green'))
    del_test = click.prompt("Which test would you like to delete?")
    try:
        os.remove(f"backtests/{del_test}.txt")
        click.echo(click.style(f"{del_test} Successfully Deleted", fg='green'))
    except:
        click.echo(click.style(f"Error deleting {del_test}", fg='red'))

@click.command(name="results")
def show_results():
    '''
    Show results of previous tests
    '''
    results = os.listdir('results')
    if len(results) == 0:
        click.echo(click.style("No results to show", fg='red'))
        exit()

    for result in results:
        click.echo(click.style(result.replace(".txt", ''), fg='green'))

    result_to_view = click.prompt("Which test would you like to view?")
    try:
        with open(f"results/{result_to_view}.txt", "r") as f:
            print(f.read())
    except:
        click.echo(click.style("Could not find result", fg='red'))

main.add_command(run_test)
main.add_command(get_tests)
main.add_command(create_test)
main.add_command(edit_test)
main.add_command(show_results)
main.add_command(delete_test)

def check_login():
    try:
        with open('credentials.txt', 'r') as file:
            data = json.loads(file.read())
            r = requests.get('http://127.0.0.1:8000/account/getaccount', headers={'Authorization': f"Bearer {data['access']}"})
            if r.ok:
                click.echo(click.style("Already signed in and token is valid", fg='green'))
                exit()
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
        password1 = click.prompt("Password | Must be 7 character or more")
        password2 = click.prompt("Password (Confirm)")
        if password1 != password2:
            click.echo(click.style("Passwords do not match, please try again", fg='red'))

    r = requests.post('http://127.0.0.1:8000/account/register', json={'email': email, 'password': password1})
    auth = requests.post('http://127.0.0.1:8000/api/token/', json={'email': email, 'password': password1})
    if r.ok and auth.ok:
        with open('credentials.txt', 'w') as cred_file:
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
    # before logging in make a request to api/token and if it returns ok then don't let the user log in as they already are and their token is still valid
    check_login()

    email = click.prompt("Please enter your email", type=str)
    while '@' not in email or '.com' not in email:
        email = click.prompt(click.style("Please enter a valid email", fg='red'))

    password = click.prompt("Enter password", type=str, hide_input=True)

    r = requests.post('http://127.0.0.1:8000/api/token/', json={'email': email, 'password': password})
    if r.ok:
        # save login token/credentials in file
        with open('credentials.txt', 'w') as cred_file:
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
        with open('credentials.txt', 'r') as file:
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
        os.remove(r'credentials.txt')
        click.echo(click.style("Successfully logged out", fg='green'))
    except:
        click.echo(click.style("error logging out", fg='red'))

main.add_command(register)
main.add_command(login)
main.add_command(account)
main.add_command(logout)

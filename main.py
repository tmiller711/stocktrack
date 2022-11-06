import click
import requests
import pandas as pd
import os
from interpreter import Interpreter
from tester import Test
import json

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

def check_login():
    with open('credentials.txt', 'r') as file:
        data = json.loads(file.read())
        r = requests.get('http://127.0.0.1:8000/account/getaccount', headers={'Authorization': f"Bearer {data['access']}"})
        if r.ok:
            click.echo("Already signed in and token is valid")
            exit()

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
        email = click.prompt("Please enter a valid email")

    password1, password2 = '8', ''
    while password1 != password2 or len(password1) < 7:
        password1 = click.prompt("Password | Must be 7 character or more")
        password2 = click.prompt("Password (Confirm)")
        if password1 != password2:
            click.echo("Passwords do not match, please try again")

    r = requests.post('http://127.0.0.1:8000/account/register', json={'email': email, 'password': password1})
    auth = requests.post('http://127.0.0.1:8000/api/token/', json={'email': email, 'password': password1})
    if r.ok and auth.ok:
        with open('credentials.txt', 'w') as cred_file:
            cred_file.write(auth.text)
            click.echo("Account successfully registered")
            click.echo("Login valid for 30 days")
    else:
        click.echo("Error creating account, try again later")

@click.command(name='login')
def login():
    '''
    Login to account
    '''
    # before logging in make a request to api/token and if it returns ok then don't let the user log in as they already are and their token is still valid
    check_login()

    email = click.prompt("Please enter your email", type=str)
    while '@' not in email or '.com' not in email:
        email = click.prompt("Please enter a valid email")

    password = click.prompt("Enter password")

    r = requests.post('http://127.0.0.1:8000/api/token/', json={'email': email, 'password': password})
    if r.ok:
        # save login token/credentials in file
        with open('credentials.txt', 'w') as cred_file:
            cred_file.write(r.text)
            click.echo("Successfully Logged In")
            click.echo("Login valid for 30 days")
    else:
        click.echo("Error logging in")

@click.command(name='account')
def account():
    '''
    View account details
    '''
    with open('credentials.txt', 'r') as file:
        data = file.read()
    token_dict = json.loads(data)
    # print(token_dict['access'])
    headers = {"Authorization": f"Bearer {token_dict['access']}"}

    r = requests.get('http://127.0.0.1:8000/account/getaccount', headers=headers)
    if r.ok:
        user_data = json.loads(r.text)
        click.echo("User email:")
        click.echo(user_data['email'])
    else:
        click.echo("Error retrieving user data")

main.add_command(register)
main.add_command(login)
main.add_command(account)

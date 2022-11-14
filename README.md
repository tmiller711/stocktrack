# stocktrack

CLI to create and tests backtest strategies against stocks

Account commands:

- 'account' : returns the email of the active account if signed in
- 'login' : logs you in to the api with credentials provided
- 'register' : registers an account with the api with the credentials provided

Commands:

- 'setdir' : set the folder you store your created tests in and where you want to output your results to
- 'results' : show all previous results stored in your specified results folder
- 'alltests' : shows all previously made tests stored in your specified tests folder
- 'create TESTNAME' : creates a test in your tests folder and names in TESTNAME
- 'delete' : delete a test stored in your tests folder
- 'run' : run a specified test against a stock

Created Tests:
- After you run the create command you have to go into you tests folder and edit the .txt file. To create the test you have to use the test language that we outline below

Test Language:
- The test outline language has you defining what indicators you want to use on the first row and then specifying buy and sell criteria
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
This test will buy a stock when the rsi is less than 30 and sell when the rsi is greater than 70

- Available Command:
  - 'crossing' : define an indicator and define a condition for when to run
  - 'divergence' : define type of divergence (bull or bear), what indicator to use for the divergence, and how many days to check back for the divergence
  example: 'divergence bull rsi 15'
  - 'tp sl' : this is how you define the take profit and stop loss of a trade. Example: 'tp 7% sl -2%'
  
example 2:
```
use macd signal

buy {
	crossing macd > signal
}

sell {
	tp 7% sl -2%
}

```
This will buy stock when the macd line crosses the signal line and sell when either the take profit (7%) or the stop loss (-2%) are hit

example 3:
```
use rsi

buy {
	divergence bull rsi 15
}

sell {
	crossing rsi > 70
}
```
This test will buy when there is divergence on the rsi looking back 15 days and sell when/if the rsi goes above 70
  

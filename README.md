# SSSTockMarket
### Specs:
	I am not authorized to share the specs here

### Requirements:
	This assignment is written in python 2.7.10.
	Nothing else is needed to run it.
  
### OverView:
There are 3 main components:
#### Stock:
	The representation of the stock object can be found here.
	Every Stock object is able to calculate his own dividend yield and PE ratio.
    
#### Trade Handler:
	This class mimics a database or some other element that can store and return trade elements for a given stock
    
#### Report Builder:
	This is just a collection of methods, that can calculate Valuem weighted stock price and All share index.
    
### Running the tests:
 running 
``` python -m unittest discover -s ```
in the test folder should find and run all tests

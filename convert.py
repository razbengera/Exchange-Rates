#!/usr/bin/env python3
"""
inputs two dates, an amount, and codes of two currencies (lower or upper case strings). 
It then prints a table with the amount converted between those
currencies, in both directions, i.e., conversion of amount from the first currency to the second one
and from the second one to the first one (so, two lines should be printed), using the exchange rates
on the given date period.
--------------------------
amount-float
date1,date2-in this format: YYYY-MM-DD(without quotation marks).
code1,code2-upper/lower case letter string from the currencies dictionary.

the input must be correct and, if it's not, you will need input it again.
None input for date1,2 is today
--------------------------
"""
import exrates
import pandas as pd
import urllib3
from datetime import datetime

while True:                                                              #ensure that all the input is correct and, if it's not,it's ask for it again.
    try:
        amount=float(input("choose amount: "))
        date1=str(input("choose date1 in this format: YYYY-MM-DD(without quotation marks): ")) or datetime.now().strftime('%Y-%m-%d')
        date2=str(input("choose date2 in this format: YYYY-MM-DD(without quotation marks): ")) or datetime.now().strftime('%Y-%m-%d')
        code1=str(input("choose code1: "))
        code2=str(input("choose code2: "))
  
        convert = pd.DataFrame({
                            'convert':[code1+"-->"+code2,code2+"-->"+code1],
                            'amount' :[amount,amount],
                            str(date1):[exrates.convert(amount,code1,code2,date1),exrates.convert(amount,code2,code1,date1)],
                            str(date2):[exrates.convert(amount,code1,code2,date2),exrates.convert(amount,code2,code1,date2)]}).set_index('convert')

        print(convert)
    except urllib3.exceptions.MaxRetryError:          #If no internet connection
        print("Check your Internet connection and try again")
        break
    except exrates.CurrencyDoesntExistError:          #If the currency code does'nt exist
        print("the exchange rate for either of the currency codes from_curr and to_curr does not exist on this date")
        continue
    except exrates.DateDoesntExistError:              #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    except OSError:                                  #If the date doesn't in the format
        print("your date doesn't exist")
        continue
    except ValueError:                                 #If amount doesn't float
        print("amount must be a float")
        continue
    else:
        break

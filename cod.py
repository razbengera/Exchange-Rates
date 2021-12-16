#!/usr/bin/env python3
"""
user inputs a date and prints the list of currencies for
which there is a data on that date (i.e., the keys for the exchange rates dictionary on that date).
The currencies printed in the format "Name (code)", one per line, sorted by their code.
Of course, the names are obtained from the currencies list. 
However, some may be missing there. Those will be print as "<unknonwn> (code)".
date must be in this format: YYYY-MM-DD(without quotation marks).

None input for date is today 
the input must be correct and, if it's not, you will need input it again.
"""

import exrates
import urllib3
from datetime import datetime
while True:                                          #ensure that all the input is correct and, if it's not,it's ask for it again.
    try:
        date=input("choose a date in this format: YYYY-MM-DD(without quotation marks): ") or datetime.now().strftime('%Y-%m-%d')
        currencies=exrates.get_currencies()
        exrates=sorted(exrates.get_exrates(date))

        for Code in exrates:
            if Code in currencies:
                print(str(currencies[Code])+" ("+str(Code)+")")
            else:
                print("<unknonwn>"+" ("+str(Code)+")")

    except urllib3.exceptions.MaxRetryError:          #If no internet connection
        print("Check your Internet connection and try again")
        break
    except exrates.DateDoesntExistError:              #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    except OSError:                                  #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")    
        continue
    else:
        break

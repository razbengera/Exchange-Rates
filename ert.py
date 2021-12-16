#!/usr/bin/env python3
"""
user inputs a date and prints the exchange rates for
that date in a tabular form, sorted by the currencies names, with the first column containing the
string in the form "Name (code)" and the second one containing the exchange rate relative to the
USD, aligned to the right and written to the 5 digits precision. 
it's also save the table without the sort and 5 digits precision rate in a csv file.
date must be in this format: YYYY-MM-DD(without quotation marks).
None input for date is today.
the input must be correct and, if it's not, you will need input it again.
"""
import exrates
import pandas as pd
import urllib3
import os
import csv
from datetime import datetime

while True:                                                              #ensure that all the input is correct and, if it's not,it's ask for it again.
    try:
        date=input("choose a date in this format: YYYY-MM-DD(without quotation marks): ") or datetime.now().strftime('%Y-%m-%d')
        currencies=exrates.get_currencies()
        exrates.get_exrates(date)
        with open(os.path.join('data','rates-{}.csv'.format(date)), mode="rt", encoding="utf8") as exr, \
             open(os.path.join('data','ert-rates-{}.csv'.format(date)), mode="wt", encoding="utf8") as ert:
            exrates = csv.reader(exr, delimiter=",")        
            for row in exrates:
                (Code,Rate)=row
                if Code=="Code":
                    Code="Name (code)" 
                    row=(Code,Rate)
                    ert.write(",".join(row))
                    ert.write("\n")                
                if Code in currencies:
                    Code=str(currencies[Code])+" ("+str(Code)+")"
                    row=(Code,Rate)
                    ert.write(",".join(row))
                    ert.write("\n")
                elif Code not in currencies and Code!="Name (code)":
                    Code="<unknonwn>"+" ("+str(Code)+")"
                    row=(Code,Rate)
                    ert.write(",".join(row))
                    ert.write("\n")
        ert_pd = pd.read_csv(os.path.join('data','ert-rates-{}.csv'.format(date)),sep=',', encoding='utf8')
        ert_pd=ert_pd.sort_values(by="Name (code)")           #sorted by the currencies names.
        pd.options.display.float_format = '{:,.5f}'.format    #for 5 digits precision. 
        print(ert_pd.set_index('Name (code)'))
    except urllib3.exceptions.MaxRetryError:          #If no internet connection
        print("Check your Internet connection")
        break
    except exrates.DateDoesntExistError:              #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    except OSError:                                  #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    else:
        break












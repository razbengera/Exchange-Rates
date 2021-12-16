#!/usr/bin/env python3
"""
user inputs two dates, and list of currencies (lower or upper
case strings). It analyzes the change (in %) of the exchange rate during that period, and prints a
table that lists for each currency the maximal change (in %) of the exchange rate,
the minimal change (in %) of the exchange rate and the diff between the maximal
exchange rate to the minimal exchange rate.
The table is then sorted in descending order of the diff between max to min.

date1,date2-in this format: YYYY-MM-DD(without quotation marks).
None input for date1,2 is today.
the input must be correct and, if it's not, you will need input it again.

"""
import urllib3
import exrates
from datetime import timedelta, datetime
import sys
import os
import pandas as pd

while True:
    try:
        date_format = "%Y-%m-%d"
        start_date = input("choose date1 in this format: YYYY-MM-DD(without quotation marks): ") or datetime.now().strftime('%Y-%m-%d')
        if datetime.strptime(start_date, date_format)>datetime.now():
            raise exrates.DateDoesntExistError()
        end_date = input("choose date2 in this format: YYYY-MM-DD(without quotation marks): ") or datetime.now().strftime('%Y-%m-%d')
        if datetime.strptime(end_date, date_format)>datetime.now():
            raise exrates.DateDoesntExistError()
        currency_lst=str(input("choose a comma-separated list of currency codes: "))
        currency_lst=currency_lst.upper().split(",")
        currency_file=exrates.get_currencies()
        if all(currency.strip(" ") not in currency_file for currency in currency_lst)==True:     #if all currencies not in thr currencies list, the progrem will stop
                sys.stderr.write("\ninvalid input-choose an available currency\n")
                continue
      
        with open(os.path.join('data','exchange rate change for period.csv'), mode="wt", encoding="utf8") as file:
            file.write('date,')
            for currency in currency_lst:                     
                currency=currency.strip(" ")
                if currency in currency_file:              #if not, the currency will not write
                    file.write(str(currency))
                    file.write(",")
            file.write("\n")
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)
            if start_date>end_date:                         #for chronological order
                end_date1=start_date
                start_date1=end_date
            else:
                end_date1=end_date
                start_date1=start_date
            date=start_date1
            exrates2=exrates.get_exrates((date- timedelta(days=1)).strftime(date_format))
            while date<end_date1+ timedelta(days=1):
                exrates1=exrates.get_exrates(date.strftime(date_format))
                file.write(str(date.strftime(date_format)))
                for currency in currency_lst:
                    currency=currency.strip(" ")
                    if currency in currency_file:                        #if not, the currency will not write
                        file.write(",")
                        if currency in exrates1 and currency in exrates2:
                            file.write(str((exrates1[currency]/exrates2[currency]-1)*100))
                        else:
                            file.write("0")
                file.write("\n")
                date = date + timedelta(days=1)
                exrates2=exrates1
        analyze = pd.read_csv(os.path.join('data','exchange rate change for period.csv'),sep=',', encoding='utf8')
        analyze=analyze.describe()
        analyze=analyze.T
        del analyze['count']
        del analyze['mean']
        del analyze['std']
        del analyze['25%']
        del analyze['50%']
        del analyze['75%']
        analyze = analyze.assign(diff=pd.Series(analyze['max']-analyze['min']).values)
        analyze.index.name = 'currencies'
        analyze=analyze.sort_values(by='diff', ascending=False)     
        analyze=analyze.astype(str) + '%'
        print(analyze[:-1])
    except urllib3.exceptions.MaxRetryError:          #If no internet connection
        print("Check your Internet connection and try again")
        break
    except exrates.DateDoesntExistError:              #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    except ValueError:                                  #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    else:
        break

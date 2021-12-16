#!/usr/bin/env python3
"""
user inputs two dates, a comma-separated list of currency codes
(for example: ILS, GBP,eur,cAd(without quotation marks)), and a file name. 
It then saves the exchange rates relative to
the USD between those two dates for the given currencies in CSV file of the given name (in the
current directory if no path is given).
Each date between the two given dates (including both of them) go in its own row, the first
column contain the date of that row, and each of the currencies be in its own column.
Only the currencies contained in the currencies list are taken into account (the rest are ignored; if
there are no valid currencies, the input is considered invalid and the progrem will stop). 
If the value for a certain currency
doesn't exist on some of the dates, save "-" as its value.
The two input dates may be given in any order.the dates in the file
go in the chronological order.

date1,date2-in this format: YYYY-MM-DD(without quotation marks).
None input for date1,2 is today.
the input must be correct and, if it's not, you will need input it again.
currency codes and file name must be a string(without quotation marks).
"""
import urllib3
import exrates
from datetime import timedelta, datetime
import sys
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
        file=input("choose a file name: ")
      

        with open('{}.csv'.format(file), mode="wt", encoding="utf8") as file:
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
            while date<end_date1+ timedelta(days=1):
                exrates1=exrates.get_exrates(date.strftime(date_format))
                file.write(str(date.strftime(date_format)))
                for currency in currency_lst:
                    currency=currency.strip(" ")
                    if currency in currency_file:                        #if not, the currency will not write
                        file.write(",")
                        if currency not in exrates1:
                            file.write("-")
                        else:
                            file.write(str(exrates1[currency]))
                file.write("\n")
                date = date + timedelta(days=1)
    except urllib3.exceptions.MaxRetryError:          #If no internet connection
        print("Check your Internet connection and try again")
        break
    except exrates.DateDoesntExistError:              #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    except ValueError:                                  #If the date doesn't exist or doesn't in the format
        print("your date doesn't exist")
        continue
    except OSError:                                  #If the file name doesn't good
        print("your file name doesn't good")    
        continue
    else:
        break

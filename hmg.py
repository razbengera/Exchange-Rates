#!/usr/bin/env python3
"""
user inputs two integers, year and
month, a comma-separated list of currency codes (for example, "ILS,GBP,eur,cAd"), and a file
name. It then saves the graph of the exchange rates changes (in percentage (%)) relative to the
USD for the given month and year, in a png file. Exchange rate change is defined as the ratio of the
exchange rate on a given date compared to the previos exchange rate 
(dates with missing exchange rates for certain currencies considered zero change). For example: if
today's ILS exchange rate is 3.8242 and previous rate was 3.8091 the exchange rate change is
0.396%. In addition, the progrem start calculating the change only from the 2nd day
(compared to the first day), first day is considered 0 change.

the input must be correct and, if it's not, you will need input it again.
the today month and year consider invalid input.

currency codes and file name must be a string(without quotation marks).
"""
import urllib3
import exrates
import datetime
import matplotlib.pyplot as plt
import sys

while True:
    try:
        date_format = "%Y-%m-%d"
        year = int(input("choose a year: "))
        month = int(input("choose a month: "))
        if year==datetime.datetime.now().year and month==datetime.datetime.now().month:
            raise exrates.DateDoesntExistError()
        currency_lst=str(input("choose a comma-separated list of currency codes: "))
        currency_lst=currency_lst.upper().split(",")
        currency_file=exrates.get_currencies()
        if all(currency.strip(" ") not in currency_file for currency in currency_lst)==True:     #if all currencies not in thr currencies list, the progrem will stop
                sys.stderr.write("\ninvalid input-choose an available currency\n")
                continue
        file=str(input("choose a file name: "))

        for currency in currency_lst:                     
            currency=currency.strip(" ")
            if currency in currency_file:              #if not, the currency will not write
                date = [1] 
                date1=datetime.date(year,month,1).strftime(date_format)
                exrates1=exrates.get_exrates(date1)
                exchange_rates_changes=[0]
                for x in range(2,int((datetime.date(year,month+1,1)-datetime.date(year,month,1)).days)+1):
                    exrates2=exrates.get_exrates(datetime.date(year,month,x).strftime(date_format))
                    date.append(x) 
                    if currency in exrates1 and currency in exrates2:
                        exchange_rates_changes.append((exrates2[currency]/exrates1[currency]-1)*100)
                    else:
                        exchange_rates_changes.append(0)              #if not append zero
                    date1=datetime.date(year,month,x).strftime(date_format)
                    exrates1=exrates2
                plt.plot(date,exchange_rates_changes, '-p',
                                               markersize=5, linewidth=2,
                                                        markeredgewidth=1, label="{}".format(currency))    

        plt.xlabel("day in month")
        plt.ylabel("exchange rates changes(%)")
        plt.title("History of one Month Graph changes\n{},{}".format(month,year))
        plt.legend()
        plt.grid()
        plt.savefig('{}.png'.format(file))
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
        break
    else:
        break

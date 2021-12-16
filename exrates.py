#!/usr/bin/env python3
"""
-module with 9 functions:
    *_fetch_currencies() that fetches the currencies list from this website-
     http://openexchangerates.org/api/currencies.json) and returns it as a dictionary.
    
    *_fetch_exrates(date) that fetches the exchange rates for the date date from the Open Exchange Rates
     (https://openexchangerates.org/) website and returns it as a dictionary.
     Empty strings represent the current date.
    
    *_save_currencies() that saves the dictionary currencies in the currencies CSV file in data directory.
    
    *_save_exrates(date) that saves the exchange rates data for date date in the 
     appropriate exchange rates CSV file in data directory.
     Empty strings represent the current date.
    
    *_load_currencies() that returns the currencies loaded from the currencies file.
    
    *_load_exrates(date) that returns the exchange rates data for date date loaded from the
     appropriate exchange rates file. Empty strings represent the current date.
    
    *get_currencies() that returns the currencies loaded from the currencies file, as a dictionary. If
     the currencies file doesn't exists, the function fetches the data from the internet, 
     saves it to the currencies file and then returns it.
     
    *get_exrates(date) that returns the exchange rates data for date date loaded from the
      appropriate exchange rates file. If that file doesn't exists, the function fetches the data 
      from the internet, saves it to the file, and then returns it.Empty strings represent the current date.
    
     *convert(amount, from_curr, to_curr, date) that returns the value obtained by
      converting the amount amount of the currency from_curr to the currency to_curr 
      on date date. If date is not given, it defaults the current date.
      
      ------------------------------------------------------------------------
      -All dates must be strings in this format: YYYY-MM-DD.
      -You need internet connection for some of this functions.
      ------------------------------------------------------------------------
      
-The module also create the data directory if it doesn't already exist.

-When imported, the module read the App ID from the file named "app.id" in the current directory.
 In case it fails, it print a descriptive message about the problem and stop the program
 with the return value -17.
"""
import urllib3, json
from bs4 import BeautifulSoup
from datetime import datetime
import os
import csv
import sys
url="http://openexchangerates.org/api/currencies.json"
url2="http://openexchangerates.org/api/historical/{}.json?app_id={}"

try:
    app= open('app.id.txt', mode="rt", encoding="utf8")
    appid=str(app.read().strip(" "))
except Exception:
    sys.stderr.write("Error has occurred opening app.id file!")
    sys.exit(-17) 

newpath = r'data' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

class DateDoesntExistError(Exception):
    pass
class CurrencyDoesntExistError(Exception):
    pass

def _fetch_currencies():
    """
    fetches the currencies list from this website-
    http://openexchangerates.org/api/currencies.json) and returns it as a dictionary.
    you need internet for this function.
    """
    http = urllib3.PoolManager()

    response = http.request('GET', url)
    soup =BeautifulSoup(response.data,"html.parser")
    fetch_currencies=json.loads(soup.decode('utf-8'))
    return dict(fetch_currencies)

def _fetch_exrates(date):
    """
    fetches the exchange rates for the date date from the Open Exchange Rates
    (https://openexchangerates.org/) website and returns it as a dictionary.
    Empty strings represent the current date.
    date must be string in this format: YYYY-MM-DD.
    you need internet for this function.
    """
    app= open(os.path.join('app.id.txt'), mode="rt", encoding="utf8")
    appid=str(app.read().strip())
    try:
        http = urllib3.PoolManager()

        response = http.request('GET', url2.format(date,appid))
        soup =BeautifulSoup(response.data,"html.parser")
        fetch_exrates=json.loads(soup.decode('utf-8'))
        return dict(fetch_exrates["rates"])
    except KeyError:
        raise DateDoesntExistError("your date doesn't exist")

def _save_currencies(currencies):
    """
    saves the dictionary currencies in the currencies CSV file in data directory.
    """
    with open(os.path.join('data','currencies.csv'), mode="wt", encoding="utf8") as save_currencies:
        save_currencies.write("Code,Name")
        save_currencies.write("\n")
        for x in currencies:
            save_currencies.write(x)
            save_currencies.write(",")
            save_currencies.write(currencies[x])
            save_currencies.write("\n")

def _save_exrates(date,rates):
    """
    saves the exchange rates in the appropriate exchange rates CSV file in data directory.
    Empty strings represent the current date.
    date must be string in this format: YYYY-MM-DD.
    """
    with open(os.path.join('data','rates-{}.csv'.format(date)), mode="wt", encoding="utf8") as exrates:
        exrates.write("Code,Rate")
        exrates.write("\n")
        for x in rates:
            exrates.write(x)
            exrates.write(",")
            exrates.write(str(rates[x]))
            exrates.write("\n")

def _load_currencies():
    """
    returns the currencies loaded from the currencies file.
    if the file doesn't exist you will get an appropriate message.    
    """
    with open(os.path.join('data','currencies.csv'), mode="rt", encoding="utf8") as currencies:
        reader = csv.reader(currencies)
        load_currencies = {rows[0]:rows[1] for rows in reader}
        del load_currencies["Code"]
    return load_currencies
            
def _load_exrates(date):
    """
    returns the exchange rates data for date date loaded from the
    appropriate exchange rates file. 
    Empty strings represent the current date.
    date must be string in this format: YYYY-MM-DD.
    if the file doesn't exist you will get an appropriate message.
    """
    with open(os.path.join('data','rates-{}.csv'.format(date)), mode="rt", encoding="utf8") as exrates:
        reader = csv.reader(exrates)
        load_exrates = {rows[0]:rows[1] for rows in reader}
        del load_exrates["Code"]
        for x in load_exrates:
            load_exrates[x]=float(load_exrates[x]) 
    return load_exrates


def get_currencies():
    """
    returns the currencies loaded from the currencies file, as a dictionary. If
    the currencies file doesn't exists, the function fetches the data from the internet, 
    saves it to the currencies file and then returns it.
    if the file doesn't exist you will need an internet for this function.
    """
    try:
       return _load_currencies()
    except FileNotFoundError:
        currencies=_fetch_currencies()
        _save_currencies(currencies)
        return _load_currencies()
def get_exrates(date=datetime.now().strftime('%Y-%m-%d')):
    """
    returns the exchange rates data for date date loaded from the
    appropriate exchange rates file. If that file doesn't exists, the function fetches the data 
    from the internet, saves it to the file, and then returns it.Empty strings represent the current date.
    if the file doesn't exist you will need an internet for this function.
    Empty strings represent the current date.
    date must be string in this format: YYYY-MM-DD.    
    """
    try:
        return _load_exrates(date)
    except FileNotFoundError:
        rates=_fetch_exrates(date)
        _save_exrates(date,rates)
        return _load_exrates(date)
        
def convert(amount, from_curr, to_curr, date=datetime.now().strftime('%Y-%m-%d')):
    """
    returns the value obtained by
    converting the amount amount of the currency from_curr to the currency to_curr 
    on date date. If date is not given, it defaults the current date.    
    you need internet for this function.
    If the exchange rate for either of the currency codes from_curr and to_curr does not exist on
    the date date, the function must raise a custom exception CurrencyDoesntExistError with an
    appropriate message.
    ---------------------------------------------
    amount- float
    date must be string in this format: YYYY-MM-DD.
    from_curr, to_curr- upper/lower case letter string from the currencies dictionary.
    ---------------------------------------------
    """
    if from_curr.upper() not in get_exrates(date) or to_curr.upper() not in get_exrates(date):
        raise CurrencyDoesntExistError("the exchange rate for either of the currency codes from_curr and to_curr does not exist on this date")        
    from_value=get_exrates(date)[from_curr.upper()]
    to_value=get_exrates(date)[to_curr.upper()]
    convert= amount*to_value/from_value
    return convert       

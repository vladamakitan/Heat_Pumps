import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    hps = []  # here we will store our hps
    for i in range(1, 8):
        url = f"https://steelsoft.rs/prodavnica/32//{i}?"  # after colecting data form page move on to the next
        page = request(url)
        soup = get_soup(page)
        hp_list = get_list_of_hp(soup)

        for hp in hp_list:
            title = hp.find('a').text
            name = title.split(' ')
            model = ''
            for n in name:
                if n == "LG" or n == "MITSUBISHI" or n == "TRANE":
                    name = n
                # get model from full name
                if contains_number(n):
                    model = n
            if name == 'MITSUBISHI':
                if '100' in model:
                    power = '10'
                if '140' in model:
                    power = '14'
                if '71' in model:
                    power = '6'
                if '80' in model:
                    power = '8'
                if '75' in model:
                    power = '8'
                if '120' in model:
                    power = '12'
                if '200' in model:
                    power = '20'
                if '50' in model:
                    power = '4'
                if '160' in model:
                    power = '16'
                if '230' in model:
                    power = '23'
                if '112' in model:
                    power = '11'

            elif name == 'LG':
                if '16' in model:
                    power = '16'
                if '14' in model:
                    power = '14'
                if '12' in model:
                    power = '12'
                if '09' in model:
                    power = '8'
                if '07' in model:
                    power = '6'
                if '05' in model:
                    power = '4'
            else:
                power = 'NaN'

            price = hp.find('div', class_='pull-left').text.strip()
            price = price.split(" ")[1]
#            price = price.replace(',', '')  # converting string to float
            seller = 'Steelsoft'
            hps.append(
                [name, model, power, price, seller])  # we need to pass list to append 'couse it accepts only one argument

    df = pd.DataFrame(hps, columns=['Brand', 'Model', 'Power','Price', 'Seller'])
    df.to_csv('steelsoft.csv')


# request the web page
def request(url):
    return requests.get(url)


# get soup object
def get_soup(page):
    return BeautifulSoup(page.content, 'html.parser')


# get list of all hp from a page
def get_list_of_hp(soup):
    return soup.find_all('div', class_='col-lg-4 col-md-4 col-sm-6 col-xs-12 uredjaj')


# get part of title that represent model of heat pump
def contains_number(name):
    """Models are ussualy represent with letters and numbers. Numbers represent heat pumps power"""
    return any(char.isdigit() for char in name)  # if there is number return True


main()
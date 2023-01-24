import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def main():
    hps = []  # here we will store our hps
    url = "https://www.etaz.rs/toplotne-pumpe-vazduh-voda"
    page = request(url)
    soup = get_soup(page)
    hp_list = get_list_of_hp(soup)

    for hp in hp_list:
        title = hp.find('a', class_='title').text
        name = title.split(' ')
        model = ''
        power = ''
        for n in name:
            if n == "LG" or n == "MITSUBISHI" or n == "TRANE":
                name = n
            # get model from full name
            if contains_number(n):
                model = n
                if ',' in model: # deleting comma from end of the string
                    model = model.replace(',', '')

        power = get_power(model)

        price = hp.find('span', class_='price').text.strip()
        price = price.split(" ")[0]
        price = price.replace('.', '')  # converting string to int
        seller = 'Etaz'


        hps.append([name, model, power, price, seller]) # we need to pass list to append 'couse it accepts only one argument

    df = pd.DataFrame(hps, columns=['Brand', 'Model', 'Power', 'Price', 'Seller'])
    df.to_csv('etaz.csv')

# request the web page
def request(url):
    return requests.get(url)


# get soup object
def get_soup(page):
    return BeautifulSoup(page.content, 'html.parser')


# get list of all hp from a page
def get_list_of_hp(soup):
    return soup.find_all('div', class_='productPreview transition2s')


# get part of title that represent model of heat pump
def contains_number(name):
    """Models are ussualy represent with letters and numbers. Numbers represent heat pumps power"""
    return any(char.isdigit() for char in name)  # if there is number return True


def get_power(model):
    match model:
        case 'HM051MR.U44':
            return '4'
        case 'HM071MR.U44':
            return '6'
        case 'HM091MR.U44':
            return '8'
        case 'HM121MR.U34' | 'HM123MR.U34':
            return '11'
        case 'HM141MR.U34' | 'HM143MR.U34':
            return '14'
        case 'HM161MR.U34' | 'HM163MR.U34':
            return '16'

main()
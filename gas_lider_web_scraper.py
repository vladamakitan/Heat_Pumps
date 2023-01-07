import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def main():
    hps = []  # here we will store our hps
    url = "https://www.gaslider.rs/catalog.php?prodID=251&lng=srb"
    page = request(url)
    soup = get_soup(page)
    table = get_table(soup)
    rows = table.find_all('tr')

    # Looping through each row:
    for row in rows:
        name = 'Vaillant'
        model = ''
        titles = get_title(row)  # getting every full title so I can extract models from it
        for title in titles:  # for each title
            title = title.find('span').text  # get text
            split_title = title.split(' ')  # got a list of individual words

            # get model from title
            for t in split_title:  # for every word check
                if contains_number(t):
                    model = t  # if contains number that's model name
                    if model == '190' or model == '-190':  # if first finds tank volume, continue search
                        if contains_number(t):
                            model = t
                    else:
                        break
        price = ''
        prices = row.find_all('td',
                              class_='kolonaCena')  # getting list of all containers that have price stored inside
        for price in prices:  # start digging for price
            spans = price.find_all('span')  # getting all spans
            for span in spans:
                price = span
                for p in price:
                    price = p

        seller = 'Gas_Lider'
        hps.append([name, model, price, seller])  # we need to pass list to append 'couse it accepts only one argument

    df = pd.DataFrame(hps, columns=['Brand', 'Model', 'Price', 'Seller'])
    df.to_csv('gaslider.csv')


# request the web page
def request(url):
    return requests.get(url)


# get soup object
def get_soup(page):
    return BeautifulSoup(page.content, 'html.parser')


def get_table(soup):
    return soup.find('table', class_='articleTable tipTabele-1')


def get_title(row):
    return row.find_all('td', class_='kolona_properties')


# get list of all hp from a page
def get_list_of_hp(table):
    return table.find_all('tr', class_='outArtTblRow')


# get part of title that represent model of heat pump
def contains_number(t):
    """Models are usually represent with letters and numbers. Numbers represent heat pumps power"""
    return bool(re.search(r'\d', t))  # if there is a number return True


main()


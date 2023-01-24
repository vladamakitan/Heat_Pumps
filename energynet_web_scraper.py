import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    list_of_hps = []
    url = 'https://www.energynet.rs/1-grejanje-i-oprema/toplotne-pumpe/toplotne-pumpe-vazduh-voda'
    page = request(url)
    soup = get_soup(page)
    hps = get_list_of_hp(soup)
    for hp in hps:
        brand = get_brand(hp)
        model = get_model(hp)
        power = get_power(hp)
        price = get_price(hp)
        seller = 'Energynet'
        list_of_hps.append([brand, model, power, price, seller])
    df = pd.DataFrame(list_of_hps, columns=['Brand', 'Model', 'Power', 'Price', 'Seller'])
    df["Price"] = df["Price"].str.replace("\.00", "")
    df.to_csv('energynet.csv')


def get_power(hp):
    title = hp.find('h4', class_='node__title')
    text = title.text
    list_of_str = text.split(' ')
    power = list_of_str[5]
    return power

def get_price(hp):
    container = hp.find('div', class_='field field--name-commerce-price field--type-commerce-price field--label-hidden')
    infos = container.find_all('div', class_='field__items')
    for info in infos:
        full_price = info.text
        price = full_price.split('R')[0]
        price = price.replace('.', '')
        price = price.replace(',', '.')
        return price


def get_model(hp):
    title = hp.find('h4', class_='node__title')
    text = title.text
    list_of_str = text.split(' ')
    return f"{list_of_str[2]} {list_of_str[3]} {list_of_str[4]} {list_of_str[5]}"


def get_brand(hp):
    titles = hp.find('h4', class_='node__title')
    for title in titles:
        text = title.text
        list_of_str = text.split(' ')
        for string in list_of_str:
            match string:
                case 'Gree' | 'Bergen':
                    return string


# request the web page
def request(url):
    return requests.get(url)


# get soup object
def get_soup(page):
    return BeautifulSoup(page.content, 'html.parser')


# get list of all hp from a page
def get_list_of_hp(soup):
    return soup.find_all('div', class_='product-teaser-holder')


main()

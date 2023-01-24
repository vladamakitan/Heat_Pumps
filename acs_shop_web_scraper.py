import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def main():
    try:
        hps = []  # here we will store our hps
        for i in range(1, 13):

            # bypassing response 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }

            url = f"https://www.acs-klime.rs/toplotne-pumpe.html?p={i}"  # after colecting data form page move on to the next
            page = request(url, headers)
            soup = get_soup(page)
            hp_list = get_list_of_hp(soup)

            # for each model get infromation
            for hp in hp_list:
                title = hp.find('h2', class_='product-name').text
                name = title.split(' ')  # name = brand
                brand = ''
                model = ''
                for n in name:
                    if n == "DAIKIN" or n == "FUJITSU" or n == "GORENJE" or n == "GREE" or n == "HOKKAIDO" or n == 'MIDEA' or n == 'MITSUBISHI' or n == 'PANASONIC' or n == 'TERMAL' or n == 'TOSHIBA':
                        brand = n
                    # get model from full name
                    if contains_number(n):
                        model = n

                if brand == 'DAIKIN':
                    power = model[model.index("0") + 1:model.index("0") + 3]
                    if power == '04':
                        power = '4'
                    elif power == '06':
                        power = '6'
                    elif power == '08':
                        power = '8'
                    elif power == '5A':
                        power = '4'
                    elif re.search("[a-zA-Z]", power):
                        power = 'NaN'
                elif brand == 'FUJITSU':
                    if 'WOYA060LDC' in model:
                        power = '6'
                    elif 'WOYA080LDC' in model:
                        power = '8'
                    elif 'WOYA100LDT' in model:
                        power = '10'
                    elif 'WOYG112LCT' in model:
                        power = '11'
                    elif 'WOYG140LCT' in model:
                        power = '14'
                    elif 'WOYG160LCT' in model:
                        power = '16'
                    elif 'WOYA100LFTA' in model:
                        power = '10'
                    elif 'WOYA160LCTA' in model:
                        power = '16'
                elif brand == 'GORENJE':
                    if '100' in model:
                        power = '10'
                    if '80' in model:
                        power = '8'
                    if '200' in model:
                        power = '20'
                elif brand == 'GREE':
                    if '10' in model:
                        power = '10'
                    if '16' in model:
                        power = '16'
                    if '8' in model:
                        power = '8'
                elif brand == 'HOKKAIDO':
                    if '12' in model:
                        power = '12'
                    if '10' in model:
                        power = '10'
                    if '5' in model:
                        power = '6'
                    if '7' in model:
                        power = '8'
                    if '14' in model:
                        power = '14'
                    if '16' in model:
                        power = '16'
                    if '8' in model:
                        power = '8'
                    if '6' in model:
                        power = '6'
                    if '22' in model:
                        power = '2'
                    if '23' in model:
                        power = '2'
                elif brand == 'MITSUBISHI':
                    if '100' in model:
                        power = '10'
                    if '140' in model:
                        power = '14'
                    if '60' in model:
                        power = '6'
                    if '71' in model:
                        power = '6'
                elif brand == 'PANASONIC':
                    if '09' in model:
                        power = '8'
                    if '05' in model:
                        power = '6'
                    if '06' in model:
                        power = '6'
                    if '07' in model:
                        power = '8'
                    if '12' in model:
                        power = '12'
                    if '16' in model:
                        power = '16'
                elif brand == 'TERMAL':
                    if '10' in model:
                        power = '10'
                    if '12' in model:
                        power = '12'
                    if '14' in model:
                        power = '14'
                    if '16' in model:
                        power = '16'
                elif brand == 'TOSHIBA':
                    if '80' in model:
                        power = '8'
                    if '110' in model:
                        power = '11'
                    if '140' in model:
                        power = '14'
                else:
                    power = 'NaN'

                prices = hp.find('span', class_='price-including-tax')
                price = prices.find('span', class_='price').text.strip()
                price = price.replace('.', '')  # removing '.' from price
                price = price.split(",")[0].strip()  # drop ,00 from price
                seller = 'ACS'
                hps.append(
                    [brand, model, power, price, seller])  # we need to pass list to append 'couse it accepts only one argument

    except ValueError:
        pass

    df = pd.DataFrame(hps, columns=['Brand', 'Model', 'Power', 'Price', 'Seller'])
    df.to_csv('acs.csv')



# request the web page
def request(url, headers):
    return requests.get(url, headers=headers)


# get soup object
def get_soup(page):
    return BeautifulSoup(page.content, 'html.parser')


# get list of all hp from a page
def get_list_of_hp(soup):
    return soup.find_all('div', class_='item-inner product_content')


# get part of title that represent model of heat pump
def contains_number(name):
    """Models are ussualy represent with letters and numbers. Numbers represent heat pumps power"""
    return any(char.isdigit() for char in name)  # if there is number return True


main()

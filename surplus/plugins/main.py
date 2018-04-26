#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs


def main():
    url = 'https://www.pdx.edu/surplus/items-for-sale?page={}'

    for i in [0, 1, 2, 3, 4]:
        page_url = url.format(i)
        content = requests.get(page_url)
        doc = bs(content.text, 'html.parser')
        events = doc.select('.views-row')
        for e in events:
            title = ""
            price = ""
            title_el = e.find_all("div", class_="views-field-title")
            if title_el:
                title = title_el[0].find('a').text
            price_el = e.find_all("div", class_="views-field-field-price")
            if price_el:
                price = price_el[0].find('div', class_='field-content').text
            print("{} - {}".format(title, price))


def run():
    main()

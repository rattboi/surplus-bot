#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import sqlite3
import persistqueue
import pathlib2 as pathlib

class SurplusItem:
    def __init__(self, title, price, image, link):
        self.title = title
        self.price = price
        self.image = image
        self.link  = link

    def print(self):
        print("***** Item *****")
        print("Title: {}".format(self.title))
        print("Price: {}".format(self.price))
        print("Image: {}".format(self.image))
        print("Link : {}".format(self.link))
        print("")

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return (hash(self.title) ^
                hash(self.price) ^
                hash(self.image) ^
                hash(self.link))

class SurplusEvent:
    def __init__(self, event, item):
        self.event = event
        self.title = item.title
        self.price = item.price
        self.image = item.image
        self.link = item.link

class SurplusScraper:
    def scrape(self, bs_item):
        title = SurplusScraper.title(bs_item)
        price = SurplusScraper.price(bs_item)
        image = SurplusScraper.image(bs_item)
        link  = SurplusScraper.link(bs_item)
        return SurplusItem(title, price, image, link)

    def title(item):
        title_el = item.find_all("div", class_="views-field-title")
        if title_el:
            return title_el[0].find('a').text
        return ""

    def price(item):
        price_el = item.find_all("div", class_="views-field-field-price")
        if price_el:
            return price_el[0].find('div', class_='field-content').text
        return ""

    def image(item):
        image_el = item.find_all("div", class_="views-field-field-image")
        if image_el:
            image_src = image_el[0].find('div').find('img')['src']
            if (image_src.startswith('/')):
                image_src = "https://www.pdx.edu{}".format(image_src)
            return image_src
        return ""

    def link(item):
        link_el = item.find_all("div", class_="views-field-title")
        if link_el:
            return "https://www.pdx.edu{}".format(link_el[0].find('a')['href'])
        return ""

class Queues:
    def __init__(self):
        self.q_slack = persistqueue.SQLiteQueue('db/slack', auto_commit=True)
        self.q_irc = persistqueue.SQLiteQueue('db/irc', auto_commit=True)

class SurplusDb:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

        # Create table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS surplus
             (title text, price text, image text, link text)''')

    def get_all(self):
        self.c.execute('SELECT * FROM surplus')
        return [SurplusItem(i[0], i[1], i[2], i[3])
                for i
                in self.c.fetchall()]

    def insert_item(self, surplus_item):
        item = (surplus_item.title,
                surplus_item.price,
                surplus_item.image,
                surplus_item.link,)
        self.c.execute('''INSERT INTO surplus VALUES (?,?,?,?)''', item)
        self.conn.commit()

    def insert_items(self, surplus_item_list):
        for i in surplus_item_list:
            self.insert_item(i)

    def clear(self):
        self.c.execute('''DELETE FROM surplus''')
        self.conn.commit()

def scrape():
    url = 'https://www.pdx.edu/surplus/items-for-sale?page={}'

    all_items = []
    for i in [0, 1, 2, 3, 4, 5]:
        page_url = url.format(i)
        content = requests.get(page_url)
        doc = bs(content.text, 'html.parser')
        items = doc.select('.views-row')
        all_items.extend([SurplusScraper().scrape(i) for i in items])
    return all_items

def run():
    pathlib.Path('db').mkdir(parents=True, exist_ok=True)
    db = SurplusDb('db/surplus.db')

    db_items = db.get_all()
    scraped_items = scrape()

    d_set = set(db_items)
    s_set = set(scraped_items)
    removed = d_set - s_set
    added = s_set - d_set
    generate_events(added, removed)

    db.clear()
    db.insert_items(scraped_items)


def generate_events(added_set, removed_set):
    queues = Queues()

    print("Added:")
    for i in added_set:
        event = {
            'event': 'added',
            'title': i.title,
            'price': i.price,
            'image': i.image,
            'link': i.link,
        }
        queues.q_slack.put(event)
        queues.q_irc.put(event)
        i.print()

    print("Removed:")
    for i in removed_set:
        event = {
            'event': 'removed',
            'title': i.title,
            'price': i.price,
            'image': i.image,
            'link': i.link,
        }
        queues.q_slack.put(event)
        queues.q_irc.put(event)
        i.print()


run()

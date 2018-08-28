#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import sqlite3
import persistqueue
import pathlib2 as pathlib
import re


class SurplusItem:
    def __init__(self, status, title, price, quantity, image, link):
        self.status = status
        self.title = title
        self.price = price
        self.quantity = quantity
        self.image = image
        self.link = link

    def print(self):
        print("***** Item *****")
        print("Title:  {}".format(self.title))
        print("Status: {}".format(self.status))
        print("Price:  {}".format(self.price))
        print("Quant:  {}".format(self.quantity))
        print("Image:  {}".format(self.image))
        print("Link :  {}".format(self.link))
        print("")

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return (hash(self.status) ^
                hash(self.title) ^
                hash(self.price) ^
                hash(self.quantity) ^
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
    def scrape_from_grid(self, bs_item):
        grid_title_el = bs_item.find_all("div", class_="views-field-title")
        if not grid_title_el:
            return None

        base_url = "https://www.pdx.edu"
        node_url = "{}{}".format(base_url, grid_title_el[0].find('a')['href'])
        return self.scrape(node_url)

    def scrape(self, node_url):
        content = requests.get(node_url)
        node = bs(content.text, 'html.parser')

        status = SurplusScraper.status(node)
        title = SurplusScraper.title(node)
        price = SurplusScraper.price(node)
        quantity = SurplusScraper.quantity(node)
        image = SurplusScraper.image(node)
        link = node_url
        item = SurplusItem(status, title, price, quantity, image, link)
        item.print()
        return item

    def status(item):
        status_el = item.find_all("h5", class_="item-sold")
        if status_el:
            status_text = status_el[0].text
            return re.sub(r'^status: ?', '', status_text, flags=re.IGNORECASE)
        return ""

    def title(item):
        title_el = item.find_all("h1", class_="title")
        if title_el:
            return title_el[0].text
        return ""

    def price(item):
        price_el = item.find_all("ul", class_="prices")
        if price_el:
            return price_el[0].find('li').text
        return ""

    def quantity(item):
        quantity_el = item.find_all("div", class_="item-quantity")
        if quantity_el:
            return quantity_el[0].find('p', class_="value").text
        return ""

    def image(item):
        image_el = item.find_all("div", class_="item-image-area")
        if image_el:
            image_src = image_el[0].find('img')['src']
            if (image_src.startswith('/')):
                image_src = "https://www.pdx.edu{}".format(image_src)
            return image_src
        return ""


class Queue:
    def __init__(self, queue_name):
        self.queue = persistqueue.SQLiteQueue("db/{}".format(queue_name),
                                              auto_commit=True)


class SurplusDb:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

        # Create table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS surplus (
             status text,
             title text,
             price text,
             quantity text,
             image text,
             link text
         )''')

    def get_all(self):
        self.c.execute('SELECT * FROM surplus')
        return [SurplusItem(i[0], i[1], i[2], i[3], i[4], i[5])
                for i
                in self.c.fetchall()]

    def insert_item(self, surplus_item):
        item = (surplus_item.status,
                surplus_item.title,
                surplus_item.price,
                surplus_item.quantity,
                surplus_item.image,
                surplus_item.link,)
        self.c.execute('''INSERT INTO surplus VALUES (?,?,?,?,?,?)''', item)
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
        all_items.extend([SurplusScraper().scrape_from_grid(i) for i in items])
    return all_items


def run(db_items, scraped_items):
    change_candidates = []

    removed = []
    not_removed = []
    for cnt_i, i in enumerate(db_items):
        db_item_found = False
        for cnt_j, j in enumerate(scraped_items):
            if i.link == j.link:
                change_candidates.append((cnt_i, cnt_j))
                db_item_found = True
        if not db_item_found:
            removal_candidate = SurplusScraper().scrape(i.link)
            if removal_candidate.status != "Current":
                removed.append(removal_candidate)
            else:
                not_removed.append(removal_candidate)

    added = []
    for i in scraped_items:
        scraped_item_found = False
        for j in db_items:
            if i.link == j.link:
                scraped_item_found = True
        if not scraped_item_found:
            added.append(i)

    modified = []
    marked_for_removal = []
    for i, j in change_candidates:
        if db_items[i] != scraped_items[j]:
            if scraped_items[j].quantity == "SOLD OUT":
                removed.append(scraped_items[j])
                marked_for_removal.append(j)
            else:
                modified.append((db_items[i], scraped_items[j]))

    for index in sorted(marked_for_removal, reverse=True):
        del scraped_items[index]

    return (added, removed, modified, not_removed + scraped_items)


def generate_events(added, removed, modified):
    r_events = []
    m_events = []
    a_events = []

    print("removed:")
    for item in removed:
        event = {
            'event':    'removed',
            'title':    item.title,
            'price':    item.price,
            'quantity': item.quantity,
            'image':    item.image,
            'link':     item.link,
        }
        item.print()
        r_events.append(event)

    print("added:")
    for item in added:
        event = {
            'event':    'added',
            'title':    item.title,
            'price':    item.price,
            'quantity': item.quantity,
            'image':    item.image,
            'link':     item.link,
        }
        item.print()
        a_events.append(event)

    print("modified:")
    for (old_item, new_item) in modified:
        changed_fields = []

        event = {
            'event':    'modified',
            'title':    new_item.title,
            'price':    new_item.price,
            'quantity': new_item.quantity,
            'image':    new_item.image,
            'link':     new_item.link,
            'changed':  changed_fields,
        }
        new_item.print()
        m_events.append(event)

    return r_events + m_events + a_events


def send_to_queues(events):
    queues = [Queue(t) for t in ['slack', 'irc', 'twitter']]

    for event in events:
        for q in queues:
            q.queue.put(event)


if __name__ == "__main__":
    pathlib.Path('db').mkdir(parents=True, exist_ok=True)
    db = SurplusDb('db/surplus.db')

    db_items = db.get_all()
    scraped_items = scrape()

    (added, removed, modified, new_db_items) = run(db_items, scraped_items)

    events = generate_events(added, removed, modified)
    send_to_queues(events)

    db.clear()
    db.insert_items(new_db_items)

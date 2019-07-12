import collect


class FakeScraper:
    def __init__(self, item):
        self.item = item

    def scrape(self, node_url):
        return self.item

def test_simple_modification():
    db_item = collect.SurplusItem('Current', 'test1', '$10', '10', 'http://', 'http://link1')
    scraped_item = collect.SurplusItem('Current', 'test1', '$10', '11', 'http://', 'http://link1')

    (_, _, modified, _) = collect.run([db_item], [scraped_item], FakeScraper(scraped_item))

    assert len(modified) == 1
    assert modified[0] == (db_item, scraped_item)

def test_simple_addition():
    scraped_item = collect.SurplusItem('Current', 'test1', '$10', '11', 'http://', 'http://link1')

    (added, _, _, _) = collect.run([], [scraped_item], FakeScraper(scraped_item))

    assert len(added) == 1
    assert added[0] == scraped_item

def test_simple_removal():
    db_item = collect.SurplusItem('Current', 'test1', '$10', '11', 'http://', 'http://link1')
    scraper_item = collect.SurplusItem('Sold', 'test1', '$10', '11', 'http://', 'http://link1')

    (_, removed, _, _) = collect.run([db_item], [], FakeScraper(scraper_item))

    assert len(removed) == 1
    assert removed[0] == scraper_item

def test_soldout_removal():
    db_item = collect.SurplusItem('Current', 'test1', '$10', '11', 'http://', 'http://link1')
    scraped_item = collect.SurplusItem('Current', 'test1', '$10', 'SOLD OUT', 'http://', 'http://link1')

    (_, removed, _, _) = collect.run([db_item], [scraped_item], FakeScraper(scraped_item))

    assert len(removed) == 1
    assert removed[0] == scraped_item

def test_new_item_soldout_removal():
    scraped_item = collect.SurplusItem('Current', 'test1', '$10', 'SOLD OUT', 'http://', 'http://link1')

    (added, _, _, _) = collect.run([], [scraped_item], FakeScraper(scraped_item))

    assert len(added) == 0

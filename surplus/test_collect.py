from nose.tools import assert_equals
import collect

def test_simple_modification():
    db_items = [collect.SurplusItem('Current', 'test1', '$10', '10', 'http://image', 'http://link1')]
    scraped_items = [collect.SurplusItem('Current', 'test1', '$10', '11', 'http://image', 'http://link1')]

    (_, _, modified, _) = collect.run(db_items, scraped_items)
    assert_equals(len(modified), 1)

def test_simple_addition():
    db_items = []
    scraped_items = [collect.SurplusItem('Current', 'test1', '$10', '11', 'http://image', 'http://link1')]

    (added, _, _, _) = collect.run(db_items, scraped_items)
    assert_equals(len(added), 1)

def test_simple_removal():
    db_items = [collect.SurplusItem('Current', 'test1', '$10', '11', 'http://image', 'http://link1')]
    scraped_items = []

    (_, removed, _, _) = collect.run(db_items, scraped_items)
    assert_equals(len(removed), 1)

def test_soldout_removal():
    db_items = [collect.SurplusItem('Current', 'test1', '$10', '11', 'http://image', 'http://link1')]
    scraped_items = [collect.SurplusItem('Current', 'test1', '$10', 'SOLD OUT', 'http://image', 'http://link1')]

    (_, removed, _, _) = collect.run(db_items, scraped_items)
    assert_equals(len(removed), 1)

import os
import Utils.database_util as dbu
from os import path

cwd = os.getcwd()
db_path = cwd + "/Resources/OncUtil.db"


def test_database_exists():
    assert path.exists(db_path)


def test_database_tables():
    connection = dbu.connect_database(db_path)
    cursor = connection.cursor()
    counter = 0

    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='locations'")
    if cursor.fetchone()[0] == 1:
        counter += 1
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='devices'")
    if cursor.fetchone()[0] == 1:
        counter += 1
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='categories'")
    if cursor.fetchone()[0] == 1:
        counter += 1
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='products'")
    if cursor.fetchone()[0] == 1:
        counter += 1

    connection.commit()
    connection.close()
    assert counter == 4


def test_database_populated():
    connection = dbu.connect_database(db_path)
    cursor = connection.cursor()
    counter = 0

    cursor.execute("SELECT count(*) FROM locations")
    if cursor.fetchone()[0] > 0:
        counter += 1
    cursor.execute("SELECT count(*) FROM devices")
    if cursor.fetchone()[0] > 0:
        counter += 1
    cursor.execute("SELECT count(*) FROM categories")
    if cursor.fetchone()[0] > 0:
        counter += 1
    cursor.execute("SELECT count(*) FROM products")
    if cursor.fetchone()[0] > 0:
        counter += 1

    connection.commit()
    connection.close()
    assert counter == 4


def test_database_search_locations():
    loc_code = "BISS"
    assert dbu.search_locations(loc_code, db_path)


def test_database_search_devices():
    dev_code = "TDKLAMBDA15C3256AB"
    assert dbu.search_devices(dev_code, db_path)


def test_database_search_products():
    pro_code = "TSSD"
    assert dbu.search_products(pro_code, db_path)


def test_database_search_properties():
    dev_code = "TDKLAMBDA15C3256AB"
    prop_code = "voltage"
    assert dbu.search_properties(dev_code, prop_code, db_path)

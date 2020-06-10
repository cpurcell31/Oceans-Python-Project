import os
import Utils.database_util as dbu
from os import path

cwd = os.getcwd()


def test_database_exists():
    db_path = cwd + "/OncUtil.db"
    assert path.exists(db_path)


def test_database_tables():
    db_path = cwd + "/OncUtil.db"
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
    db_path = cwd + "/OncUtil.db"
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
    db_path = cwd + "/OncUtil.db"
    loc_code = "BISS"
    assert dbu.search_locations(loc_code, db_path)
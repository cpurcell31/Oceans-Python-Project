import os
from datetime import datetime
from Utils import oceans2 as o2
import sqlite3
from sqlite3 import Error


def create_database(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(e)
    finally:
        if connection:
            create_table(connection)
            populate_table(connection)
            create_device_tables(connection)
            connection.close()
    return


def connect_database(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(e)

    return connection


def create_table(connection):
    query_locations = """
    CREATE TABLE IF NOT EXISTS locations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    query_devices = """
    CREATE TABLE IF NOT EXISTS devices (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    query_categories = """
    CREATE TABLE IF NOT EXISTS categories (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    );
    """
    query_products = """
    CREATE TABLE IF NOT EXISTS products (
        id TEXT NOT NULL,
        extension TEXT NOT NULL,
        name TEXT NOT NULL,
        PRIMARY KEY (id, extension)
    );
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query_locations)
        cursor.execute(query_devices)
        cursor.execute(query_categories)
        cursor.execute(query_products)
        connection.commit()
    except Error as e:
        print(e)

    return


def populate_table(connection):
    locations = list()
    devices = list()
    categories = list()
    products = list()
    cursor = connection.cursor()
    filters = {}

    results, locs = o2.get_location_codes(filters)
    for key in locs.keys():
        if (locs[key], key) not in locations:
            locations.append((locs[key], key))

    results, devs = o2.get_device_codes(filters)
    for key in devs.keys():
        if (devs[key], key) not in devices:
            devices.append((devs[key], key))

    results, cats = o2.get_device_categories(filters)
    for key in cats.keys():
        if (cats[key][0], key, cats[key][1]) not in categories:
            categories.append((cats[key][0], key, cats[key][1]))

    results, prods = o2.get_data_product_codes(filters)
    for key in prods.keys():
        if (prods[key][0], prods[key][1], key) not in products:
            products.append((prods[key][0], prods[key][1], key))

    cursor.executemany('INSERT INTO locations VALUES(?,?);', locations)
    cursor.executemany('INSERT INTO devices VALUES(?,?);', devices)
    cursor.executemany('INSERT INTO categories VALUES(?, ?, ?);', categories)
    cursor.executemany('INSERT INTO products VALUES(?, ?, ?);', products)
    connection.commit()
    return


def create_device_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM devices")
    devices = cursor.fetchall()

    for device in devices:
        # ensure table names are valid
        device_code = "_" + device[0].replace("-", "").replace(".", "")
        query = "CREATE TABLE IF NOT EXISTS {} (sample_times TEXT PRIMARY KEY);".format(device_code)
        cursor.execute(query)

    connection.commit()
    return


def update_device_tables(path):
    connection = connect_database(path)
    cursor = connection.cursor()
    cursor.execute("SELECT id, location FROM devices")
    devices = cursor.fetchall()

    for device in devices:
        filters = {"deviceCode": device[0],
                   "locationCode": device[1],
                   "startDate": "2015-01-01T00:00:00.000Z",
                   "endDate": datetime.now().isoformat()}
        device_code = "_" + device[0].replace("-", "").replace(".", "")

    connection.commit()
    connection.close()
    return


def search_locations(location_code, path):
    connection = connect_database(path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM locations WHERE id=?", (location_code,))
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    if len(results) == 0:
        return False
    return True


def search_devices(device_code, path):
    connection = connect_database(path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM devices WHERE id=?", (device_code,))
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    if len(results) == 0:
        return False
    return True


def search_products(product_code, path):
    connection = connect_database(path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products where id=?", (product_code,))
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    if len(results) == 0:
        return False
    return True


def get_products(path):
    connection = connect_database(path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products;")
    results = cursor.fetchall()

    connection.commit()
    connection.close()

    extensions = list()
    for result in results:
        if result[1] not in extensions:
            extensions.append(result[1])

    extensions.sort()
    return extensions


def main():
    cwd = os.getcwd()
    create_database(cwd + "/Resources/OncUtil.db")


if __name__ == "__main__":
    main()


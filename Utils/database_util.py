import os
from datetime import datetime, timedelta
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
            populate_tables(connection)
            create_device_tables(connection)
            populate_device_tables(connection)
            connection.close()
    return


def update_database(path):
    connection = connect_database(path)
    if connection:
        populate_tables(connection)
        create_device_tables(connection)
        populate_device_tables(connection)
        connection.close()
    else:
        print("Unable to establish connection to database")
    return


def connect_database(path):
    """

    :param path: Path to database file
    :return connection:
    """
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


def populate_tables(connection):
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

    cursor.executemany('INSERT OR REPLACE INTO locations VALUES(?,?);', locations)
    cursor.executemany('INSERT OR REPLACE INTO devices VALUES(?,?);', devices)
    cursor.executemany('INSERT OR REPLACE INTO categories VALUES(?, ?, ?);', categories)
    cursor.executemany('INSERT OR REPLACE INTO products VALUES(?, ?, ?);', products)
    connection.commit()
    return


def create_device_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM devices")
    devices = cursor.fetchall()

    for device in devices:
        # ensure table names are valid
        device_code = "_" + device[0].replace("-", "").replace(".", "")
        query = "CREATE TABLE IF NOT EXISTS {} (propertyCode TEXT PRIMARY KEY, " \
                "propertyName TEXT, " \
                "description TEXT, " \
                "hasDeviceData INTEGER);".format(device_code)
        cursor.execute(query)

    connection.commit()
    return


def populate_device_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM devices")
    devices = cursor.fetchall()

    for device in devices:
        filters = {"deviceCode": device[0]}
        device_code = convert_device_code(device[0])
        results, properties = o2.get_device_properties(filters)

        properties_adjusted = list()
        if properties is not None:
            for key in properties.keys():
                properties_adjusted.append((key, properties[key][0], properties[key][1], properties[key][2]))

            if properties_adjusted:
                query = "INSERT OR REPLACE INTO {} VALUES(?, ?, ?, ?)".format(device_code)
                cursor.executemany(query, properties_adjusted)

    connection.commit()
    return
    

def convert_device_code(device_code):
    """

    :rtype: str
    :param device_code: str, ONC Device Code
    :return: table_name
    """
    table_name = "_" + device_code.replace("-", "").replace(".", "")
    return table_name


def convert_device_parameter(device_parameter):
    """

    :rtype: str
    :param device_parameter: str, Device Parameter i.e. Depth
    :return: column_name
    """
    column_name = ("_" + device_parameter.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
                   .replace(",", "_").replace(".", "_")).replace("+", "_")
    return column_name


def search_locations(location_code, path):
    """

    :rtype: bool
    :param location_code: str, ONC Location Code
    :param path: str, Path to database file
    :return: bool
    """
    connection = connect_database(path)
    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM locations WHERE id=?", (location_code,))
        results = cursor.fetchall()

        connection.commit()
        connection.close()
        if results:
            return True
        return False
    return False


def search_devices(device_code, path):
    """

    :param device_code: str, ONC Device Code
    :param path: str, Path to database file
    :return: bool
    """
    connection = connect_database(path)
    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM devices WHERE id=?", (device_code,))
        results = cursor.fetchall()

        connection.commit()
        connection.close()
        if results:
            return True
        return False
    return False


def search_products(product_code, path):
    """

    :rtype: bool
    :param product_code: str, ONC Product Code
    :param path: str, Path to database file
    :return: bool
    """
    connection = connect_database(path)
    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM products WHERE id=?", (product_code,))
        results = cursor.fetchall()

        connection.commit()
        connection.close()
        if results:
            return True
        return False
    return False


def search_property_product(property_code, product_code, path):
    """
    UNFINISHED
    :param property_code: str, ONC Property Code
    :param product_code: str, ONC Product Code
    :param path: str, Path to database file
    :return: bool
    """
    connection = connect_database(path)
    if connection:
        cursor = connection.cursor()

        query = ""
        cursor.execute(query)
        results = cursor.fetchall()

        connection.commit()
        connection.close()
        if results:
            return True
        return False
    return False


def search_properties(device_code, property_code, path):
    """

    :param device_code: str, ONC Device Code
    :param property_code: str, ONC Property Code
    :param path: str, Path to database file
    :return: bool
    """
    connection = connect_database(path)
    if connection:
        cursor = connection.cursor()

        dev_code = convert_device_code(device_code)

        query = "SELECT * FROM {} WHERE propertyCode=?".format(dev_code)
        cursor.execute(query, (property_code,))
        results = cursor.fetchall()

        connection.commit()
        connection.close()
        if results:
            return True
        return False
    return False


def get_extensions(path):
    """

    :rtype: list
    :param path: str, Path to database file
    :return: extensions
    """
    connection = connect_database(path)
    if connection:
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
    return list()


def get_device_properties(device_code, path):
    """

    :param device_code: ONC Device Code
    :param path: Path to database file
    :return: properties
    """
    connection = connect_database(path)
    if connection:
        cursor = connection.cursor()
        dev_code = convert_device_code(device_code)

        query = "SELECT * FROM {} (property)".format(dev_code)
        cursor.execute(query)
        results = cursor.fetchall()

        connection.commit()
        connection.close()

        properties = list()
        for result in results:
            if result[1] not in properties:
                properties.append(result[1])

        properties.sort()
        return properties
    return list()


def main():
    cwd = os.getcwd()
    create_database(cwd + "/Resources/OncUtil.db")


if __name__ == "__main__":
    main()

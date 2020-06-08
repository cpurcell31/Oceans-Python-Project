import os
import string
import oceans2 as o2
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
    query = """
    CREATE TABLE IF NOT EXISTS locations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(e)

    return


def populate_table(connection):
    locations = list()
    alpha = list(string.ascii_lowercase)
    cursor = connection.cursor()
    for char in alpha:
        filters = {'locationName': char}
        results, locs = o2.get_location_codes(filters)
        for key in locs.keys():
            if (locs[key], key) not in locations:
                locations.append((locs[key], key))

    cursor.executemany('INSERT INTO locations VALUES(?,?);', locations)
    connection.commit()
    return


def main():
    cwd = os.getcwd()
    create_database(cwd + "/OncUtil.db")


if __name__ == "__main__":
    main()


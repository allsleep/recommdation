# -*- coding: utf-8 -*-
import sqlite3

from database.tables import movie_tables


def init_db(cursor):
    for table_name in movie_tables.keys():
        q = movie_tables[table_name]
        try:
            cursor.execute(q)
        except sqlite3.OperationalError as e:
            if str(e).endswith("already exists"):
                print(table_name, "exists")
                continue


def insert_db(db_path):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

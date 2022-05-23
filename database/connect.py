# -*- coding: utf-8 -*-
import sqlite3

from database.tables import movie_tables
from logs.logRecord import LOG


def restore_db(cursor):
    for table_name in movie_tables.keys():
        q = movie_tables[table_name]
        try:
            cursor.execute(q)
        except sqlite3.OperationalError as e:
            if str(e).endswith("already exists"):
                print(table_name, "exists")
                continue


def db_try_wrapper(cursor, sql):
    try:
        return cursor.execute(sql)
    except sqlite3.OperationalError as e:
        LOG.error('OperationalError during db operation:{}'.format(e))
        if str(e).startswith("no such table:"):
            restore_db(cursor)
            cursor.execute(sql)
    except Exception as e:
        LOG.error(f"Exception during db operation: {e}")


def insert_movie_table(db_path, movie: dict):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    for key, value in movie.items():
        sql = f"INSERT INTO t_movie (name, review) VALUES(\"{key}\", \"{value['review']}\")"
        db_try_wrapper(cursor, sql)
    con.commit()
    cursor.close()
    con.close()
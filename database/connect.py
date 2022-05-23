# -*- coding: utf-8 -*-
import json
import sqlite3

from data.gobledefine import MOVIE_DB, COLLECT_NUMBER
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
            return cursor.execute(sql)
    except Exception as e:
        LOG.error(f"Exception during db operation: {e}")


def insert_movie_table(db_path, movie: dict):
    try:
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        for key, value in movie.items():
            if judge_move_exist(key):
                sql = f"INSERT INTO t_movie (name, review) VALUES(\"{key}\", \"{value['review']}\");"
                db_try_wrapper(cursor, sql)
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        LOG.error(e)


def judge_move_exist(name, db_path=MOVIE_DB) -> bool:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    sql = f"SELECT name, review FROM t_movie WHERE name=\"{name}\";"
    v = db_try_wrapper(cursor, sql).fetchall()
    return len(v) == 0


def get_all_movie_review(db_path) -> dict:
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    sql = f"SELECT name, review FROM t_movie;"
    v = db_try_wrapper(cursor, sql).fetchall()
    temp = {}
    for item in v:
        temp[item[0]] = item[1]
    cursor.close()
    con.close()
    return temp


if __name__ == '__main__':
    print(json.dumps(get_all_movie_review(MOVIE_DB), ensure_ascii=False))
    print(judge_move_exist('长津湖 (2021)'))
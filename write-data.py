#! /usr/bin/env python3

import MySQLdb
import MySQLdb.cursors
import random
import time
import sys

db_config = dict(
    host="127.0.0.1",
    user="kris",
    passwd="geheim",
    db="kris",
    cursorclass=MySQLdb.cursors.DictCursor,
)

db = MySQLdb.connect(**db_config)


def create_table():
    sql = """drop table if exists data"""
    try:
        c = db.cursor()
        c.execute(sql)
    except MySQLdb.Error as e:
        print(f"MySQL Error on drop: {e}")
        sys.exit()

    sql = """create table data (
      x integer unsigned not null,
      y integer unsigned not null,
      z integer unsigned not null,
      data blob,
      primary key(x,y,z)
    )"""
    try:
        c = db.cursor()
        c.execute(sql)
    except MySQLdb.Error as e:
        print(f"MySQL Error on create: {e}")
        sys.exit()


def create_data():
    somestr = "".join(chr(random.randint(0,25) + ord('a')) for x in range(1, 1000))
    sql = "insert into data (x, y, z, data) values (%(x)s, %(y)s, %(z)s, %(data)s)"

    c = db.cursor()
    d = []

    for i in range(0,64):
        for j in range(0,64):
            for k in range(0,64):
                d.append({'x': i, 'y': j, 'z':k, 'data': somestr})

    c.executemany(sql, d)


t1 = time.time_ns()
create_table()
t2 = time.time_ns()
print(f"Create: {t2-t1} ns {(t2-t1)/1000000} ms")
create_data()
t3 = time.time_ns()
print(f"Write: {t3-t2} ns {(t3-t2)/1000000} ms")

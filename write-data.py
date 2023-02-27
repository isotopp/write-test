#! /usr/bin/env python

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


def take_time(label, t_old):
    t_new = time.time_ns()
    runtime = t_new - t_old
    strtime = f"| {label} | {runtime} ns | {runtime / 1000000} ms |"

    return t_new, strtime


def run_command(label, sql):
    try:
        c = db.cursor()
        c.execute(sql)
    except MySQLdb.Error as e:
        print(f"MySQL Error on {label}: {e}")
        sys.exit()


def innodb_yolo_mode():
    set_statement = "set global innodb_flush_log_at_trx_commit = 2"
    run_command("set statement", set_statement)


def innodb_acid_mode():
    set_statement = "set global innodb_flush_log_at_trx_commit = 1"
    run_command("set statement", set_statement)


def create_table():
    sql = """drop table if exists data"""
    run_command("drop table", sql)

    sql = """create table data (
      x integer unsigned not null,
      y integer unsigned not null,
      z integer unsigned not null,
      data blob,
      primary key(x,y,z)
    )"""
    run_command("create table", sql)


def create_data():
    somestr = "".join(chr(random.randint(0, 25) + ord('a')) for x in range(1, 1000))
    insert_statement = "insert into data (x, y, z, data) values (%(x)s, %(y)s, %(z)s, %(data)s)"

    innodb_yolo_mode()

    c = db.cursor()
    d = []

    for i in range(0, 64):
        for j in range(0, 64):
            for k in range(0, 64):
                d.append({'x': i, 'y': j, 'z': k, 'data': somestr})

    c.executemany(insert_statement, d)
    db.commit()


def create_data_slowly():
    somestr = "".join(chr(random.randint(0, 25) + ord('a')) for x in range(1, 1000))
    insert_statement = "insert into data (x, y, z, data) values (%(x)s, %(y)s, %(z)s, %(data)s)"

    innodb_yolo_mode()
    c = db.cursor()
    d = []

    for i in range(0, 64):
        for j in range(0, 64):
            for k in range(0, 64):
                c.execute(insert_statement, {'x': i, 'y': j, 'z': k, 'data': somestr})
                db.commit()


def create_data_very_slowly():
    somestr = "".join(chr(random.randint(0, 25) + ord('a')) for x in range(1, 1000))
    insert_statement = "insert into data (x, y, z, data) values (%(x)s, %(y)s, %(z)s, %(data)s)"

    innodb_acid_mode()
    c = db.cursor()
    d = []

    for i in range(0, 64):
        for j in range(0, 64):
            for k in range(0, 64):
                c.execute(insert_statement, {'x': i, 'y': j, 'z': k, 'data': somestr})
                db.commit()


t = time.time_ns()
print("| Op      | Runtime (ns)  | Runtime (ms) |")
print("|---------|---------------|-------------|")

create_table()
t, result = take_time("Create table", t)
print(result)

create_data()
t, result = take_time("Write data", t)
print(result)

create_table()
t, result = take_time("Recreate table", t)
print(result)

create_data_slowly()
t, result = take_time("Write data slowly", t)
print(result)

create_table()
t, result = take_time("Recreate table again", t)
print(result)

create_data_very_slowly()
t, result = take_time("Write data very slowly", t)
print(result)

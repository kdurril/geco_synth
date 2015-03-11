#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect("basic.db")
curs = conn.cursor()

def qry_commit(qry_string):
    "execute and commit a query"
    curs.execute(qry_string)
    conn.commit()

qry_drop_basic = 'DROP TABLE if exists basic;'
qry_drop_corrupt = 'DROP TABLE if exists corrupt;'

qry_create_basic = ''' CREATE TABLE IF NOT EXISTS basic (
id integer primary key autoincrement,
name_first text, 
name_last text,
name_middle text, 
address_1 text,
address_2 text, 
city text,
state text, 
zip text,
phone text, 
email text,
gender text);'''

qry_create_corrupt = ''' CREATE TABLE IF NOT EXISTS corrupt (
id integer primary key autoincrement,
basic_id integer,
name_first text, 
name_last text,
name_middle text, 
address_1 text,
address_2 text, 
city text,
state text, 
zip text,
phone text, 
email text,
gender text);'''

qry_insert_basic = ''' INSERT INTO basic (
id,
name_first, 
name_last,
name_middle, 
address_1, 
address_2, 
city, 
state,
zip,
phone,
email,
gender) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);'''

#curs.execute(qry_insert_basic)
#conn.commit()

if __name__ == '__main__':
    qry_commit(qry_drop_basic)
    qry_commit(qry_drop_corrupt)
    qry_commit(qry_create_basic)
    qry_commit(qry_create_corrupt)

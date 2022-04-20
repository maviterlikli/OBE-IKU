# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:43:41 2022

@author: f.ozdemir
"""

def table_exists(con, table_str):

    exists = False
    try:
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
        print exists
        cur.close()
    except psycopg2.Error as e:
        print e
    return exists

def get_table_col_names(con, table_str):

    col_names = []
    try:
        cur = con.cursor()
        cur.execute("select * from " + table_str + " LIMIT 0")
        for desc in cur.description:
            col_names.append(desc[0])        
        cur.close()
    except psycopg2.Error as e:
        print e

    return col_names
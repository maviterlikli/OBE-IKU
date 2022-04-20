# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 00:17:40 2022

@author: f.ozdemir
"""
import psycopg2
from psycopg2 import Error

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="4874651",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="IKU-OBE-alfa")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    
    cursor.execute("drop table grade;\
                    drop table copo;\
                    drop table questweight;\
                    drop table student;\
                    drop table assesweight;\
                    drop table course;")
                    
    connection.commit()
    cursor.close()
    connection.close()
                  
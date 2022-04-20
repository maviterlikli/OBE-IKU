# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 21:29:14 2022

@author: f.ozdemir
"""

import pandas as pd
import logging
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

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

CourseFilePath='Input/2020-2021_Guz_INS0000.xlsm'
CourseFileName='2020-2021_Guz_INS0000.xlsm'
Year1 = CourseFileName.split('-')[0]
Year2 = CourseFileName.split('-')[1].split('_')[0]
Semester = CourseFileName.split('_')[1].removesuffix('.xlsm')
CourseTag = CourseFileName.split('_')[2].removesuffix('.xlsm')
UpSupport=3
MidSupport=2
LowSupport=1
NoSupport=0
NoOC=20

CourseName = pd.read_excel(CourseFilePath, sheet_name='AnaSayfa',usecols="H",skiprows=1,nrows=1,header=None).loc[0,7]

cursor.execute("INSERT INTO Course (CourseTag, CourseName, Year1, Year2, Semester) \
               VALUES            (   '{}'    ,    '{}'   ,   {} ,   {},     '{}'  );".format( \
                                  CourseTag  , CourseName, Year1,Year2,  Semester))
connection.commit()

cursor.execute("SELECT CourseID FROM Course WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}';"\
               .format(                           CourseTag   ,      Year1   ,    Year2   ,    Semester    ))
CourseID=cursor.fetchall()
if len(CourseID)>1:
    print('There can be only one unique set of coursetag, year1, year2 and semester. Problem CourseID={}'.format(CourseID))
else:
    cursor.execute("SELECT CourseID FROM Course WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}';"\
                   .format(                           CourseTag   ,      Year1   ,    Year2   ,    Semester    ))
    CourseID=cursor.fetchone()[0]
    
    # cursor.execute("CREATE TABLE Course\
    #           (CourseID    INT PRIMARY KEY      NOT NULL,\
    #            CourseTag   TEXT                 NOT NULL,\
    #            CourseName  TEXT                 NOT NULL,\
    #            Year1       INT                  NOT NULL,\
    #            Year2       INT                  NOT NULL,\
    #            Semester    TEXT                 NOT NULL);")


    COPOTable = pd.read_excel(CourseFilePath, sheet_name='AnaSayfa',usecols="H:S",skiprows=4,nrows=NoOC)
    COPOTable = COPOTable.replace(['Üst Seviyede'],UpSupport)
    COPOTable = COPOTable.replace(['Orta Seviyede'],MidSupport)
    COPOTable = COPOTable.replace(['Alt Seviyede'],LowSupport)
    COPOTable = COPOTable.replace(['Desteklenmiyor '],NoSupport)


    COPOTableSize=COPOTable.shape

    COPOTableHead=COPOTable.columns

    for i in range(COPOTableSize[0]):
        for j in range(COPOTableSize[1]):
            CO=i+1
            PO=j+1
            Support=COPOTable.loc[i,f"{COPOTableHead[j]}"]
            cursor.execute("INSERT INTO COPO (CourseID, CourseTag, Year1, Year2, Semester, CO, PO, Support) \
                           VALUES            ( {}     ,    '{}'  ,  {}  ,   {} ,   '{}'  , {}, {},    {}  );".format(\
                                              CourseID, CourseTag, Year1, Year2, Semester, CO, PO, Support))
            connection.commit()
    cursor.close()
    connection.close()

    # cursor.execute("CREATE TABLE COPO\
    #           (CourseID    INT REFERENCES Course(CourseID)       NOT NULL,\
    #            CourseTag   TEXT                                  NOT NULL,\
    #            Year1       INT                                   NOT NULL,\
    #            Year2       INT                                   NOT NULL,\
    #            Semester    TEXT                                  NOT NULL,\
    #            CO          INT                                   NOT NULL,\
    #            PO          INT                                   NOT NULL,\
    #            Support     INT                                   NOT NULL);")
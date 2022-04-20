# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 00:23:53 2022

@author: f.ozdemir
"""

import pandas as pd
import numpy
from os.path import exists
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

cursor.execute("SELECT CourseID FROM Course WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}';"\
               .format(                           CourseTag   ,      Year1   ,    Year2   ,    Semester    ))
CourseID=cursor.fetchall()

if False:   #len(CourseID)>1
    print('There can be only one unique set of coursetag, year1, year2 and semester. Problem CourseID={}'.format(CourseID))
elif False: #len(CorseID)==0
    print('There can be only one unique set of coursetag, year1, year2 and semester. There is no Course found on this parameters.')
else:
    cursor.execute("SELECT CourseID FROM Course WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}';"\
                   .format(                           CourseTag   ,      Year1   ,    Year2   ,    Semester    ))
    CourseID=cursor.fetchone()[0]
    
    AssesWeightMain = pd.read_excel(CourseFilePath, sheet_name='Notlandirma',usecols="A:B",skiprows=5,nrows=12)
    AssesWeight1= pd.read_excel(CourseFilePath, sheet_name='Notlandirma',usecols="E:F",skiprows=5,nrows=14)
    AssesWeight2 = pd.read_excel(CourseFilePath, sheet_name='Notlandirma',usecols="I:J",skiprows=5,nrows=19)
    AssesWeight3 = pd.read_excel(CourseFilePath, sheet_name='Notlandirma',usecols="M:N",skiprows=5,nrows=5)

    AssesWeight = AssesWeightMain['Değerlendirme Yüzdesi'].to_numpy()
    AssesWeight = numpy.append(AssesWeight,AssesWeight1['Değerlendirme Yüzdesi.1'].to_numpy())
    AssesWeight = numpy.append(AssesWeight,AssesWeight2['Değerlendirme Yüzdesi.2'].to_numpy())
    AssesWeight = numpy.append(AssesWeight,AssesWeight3['Değerlendirme Yüzdesi.3'].to_numpy())
    
    AssesWeight[numpy.isnan(AssesWeight)] = 0    
    
    AssesName = AssesWeightMain['Değerlendirme Adı']
    AssesName = numpy.append(AssesName,AssesWeight1['Değerlendirme Adı.1'])
    AssesName = numpy.append(AssesName,AssesWeight2['Değerlendirme Adı.2'])
    AssesName = numpy.append(AssesName,AssesWeight3['Değerlendirme Adı.3'])

    AssesName=AssesName[AssesWeight!=0]
    AssesWeight=AssesWeight[AssesWeight!=0]
    
    for i in range(len(AssesWeight)):
            cursor.execute("INSERT INTO AssesWeight (CourseID, CourseTag, Year1, Year2, Semester, AssesType, AssesWeight)\
                           VALUES            (          {}   ,    '{}'  ,  {}  ,   {} ,   '{}',      '{}'   ,    {}    );".format(\
                                                     CourseID, CourseTag, Year1, Year2, Semester, AssesName[i], AssesWeight[i]))
            connection.commit()
            
            # cursor.execute("CREATE TABLE AssesWeight\
            #           (AssesWeightID SERIAL PRIMARY KEY                  NOT NULL,\
            #            CourseID    INT REFERENCES Course(CourseID)       NOT NULL,\
            #            CourseTag   TEXT                                  NOT NULL,\
            #            Year1       INT                                   NOT NULL,\
            #            Year2       INT                                   NOT NULL,\
            #            Semester    TEXT                                  NOT NULL,\
            #            AssesType   TEXT                                  NOT NULL,\
            #            AssesWeight INT                                   NOT NULL);")
            
    cursor.close()
    connection.close()
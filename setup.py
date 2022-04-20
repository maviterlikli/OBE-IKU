# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
    
    cursor.execute("CREATE TABLE Course\
              (CourseID    SERIAL PRIMARY KEY   NOT NULL,\
               CourseTag   TEXT                 NOT NULL,\
               CourseName  TEXT                 NOT NULL,\
               Year1       INT                  NOT NULL,\
               Year2       INT                  NOT NULL,\
               Semester    TEXT                 NOT NULL);")
                  
    cursor.execute("CREATE TABLE Student\
              (StuID       SERIAL PRIMARY KEY                                           NOT NULL,\
               StuNo       INT                                                          NOT NULL,\
               Name        TEXT                                                         NOT NULL,\
               CourseID    INT REFERENCES Course(CourseID)                              NOT NULL,\
               CourseTag   TEXT                                                         NOT NULL,\
               Year1       INT                                                          NOT NULL,\
               Year2       INT                                                          NOT NULL,\
               Semester    TEXT                                                         NOT NULL);")
                  
    cursor.execute("CREATE TABLE AssesWeight\
              (AssesWeightID SERIAL PRIMARY KEY                  NOT NULL,\
               CourseID    INT REFERENCES Course(CourseID)       NOT NULL,\
               CourseTag   TEXT                                  NOT NULL,\
               Year1       INT                                   NOT NULL,\
               Year2       INT                                   NOT NULL,\
               Semester    TEXT                                  NOT NULL,\
               AssesType   TEXT                                  NOT NULL,\
               AssesWeight INT                                   NOT NULL);")
                  
    cursor.execute("CREATE TABLE QuestWeight\
              (QuestWeightID SERIAL PRIMARY KEY                  NOT NULL,\
               CourseID    INT REFERENCES Course(CourseID)       NOT NULL,\
               CourseTag   TEXT                                  NOT NULL,\
               Year1       INT                                   NOT NULL,\
               Year2       INT                                   NOT NULL,\
               Semester    TEXT                                  NOT NULL,\
               AssesType   TEXT                                  NOT NULL,\
               QuestNo     INT                                   NOT NULL,\
               QuestWeight INT                                   NOT NULL);")
                  
    cursor.execute("CREATE TABLE COPO\
              (CourseID    INT REFERENCES Course(CourseID)       NOT NULL,\
               CourseTag   TEXT                                  NOT NULL,\
               Year1       INT                                   NOT NULL,\
               Year2       INT                                   NOT NULL,\
               Semester    TEXT                                  NOT NULL,\
               CO          INT                                   NOT NULL,\
               PO          INT                                   NOT NULL,\
               Support     INT                                   NOT NULL);")
                  
    cursor.execute("CREATE TABLE Grade\
              (GradeID       SERIAL PRIMARY KEY                        NOT NULL,\
               CourseID      INT REFERENCES Course(CourseID)           NOT NULL,\
               StuNo         INT                                       NOT NULL,\
               QuestWeightID INT REFERENCES QuestWeight(QuestWeightID) NOT NULL,\
               Grade         INT                                       NOT NULL);")
    
    
    connection.commit()
    cursor.close()
    connection.close()
                  
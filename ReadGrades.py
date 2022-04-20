# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:59:00 2022

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



def CheckSheetExists(FileNamePath,SheetName):
    try:
        pd.read_excel(FileNamePath,sheet_name=SheetName)
        Bool=1
        return Bool
    except:
        Bool=0
        return Bool
    
cursor.execute("SELECT CourseID FROM Course WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}';"\
               .format(                           CourseTag   ,      Year1   ,    Year2   ,    Semester    ))
CourseID=cursor.fetchall()
if len(CourseID)>1:
    print('There can be only one unique set of coursetag, year1, year2 and semester. Problem CourseID={}'.format(CourseID))
else:
    cursor.execute("SELECT CourseID FROM Course WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}';"\
                   .format(                           CourseTag   ,      Year1   ,    Year2   ,    Semester    ))
    CourseID=cursor.fetchone()[0]

#Student List Based On Final Exam

SheetName='Final'

AssesOCTable = pd.read_excel(CourseFilePath, sheet_name=SheetName,usecols="E:AC",nrows=20)  
QuestionWeights = pd.read_excel(CourseFilePath, sheet_name=SheetName,usecols="C:AC",skiprows=28,nrows=1).drop(axis=1,labels="OgrenciNo")
QuestionWeights = QuestionWeights.drop(axis=1,labels="Toplam Puan")
NoofQuestions= int(QuestionWeights[QuestionWeights.any(axis=1)].idxmax(axis=1).iloc[0].split('.')[0])
AssesGrades = pd.read_excel(CourseFilePath, sheet_name=SheetName,usecols="B:AC",skiprows=28)
AssesGrades = AssesGrades.drop(index=0).reset_index()
ListOfStudents = AssesGrades.loc[:,['OgrenciNo','Öğrenci Ad Soyad']]    
for j in range(len(ListOfStudents)):
    
    cursor.execute("INSERT INTO Student (StuNo                            , Name                                    ,CourseID   ,CourseTag, Year1, Year2, Semester )\
                   VALUES               (   {}                            ,    '{}'                                 ,   {}      ,   '{}'  ,  {}     ,   {} ,   '{}');".format(\
                                         ListOfStudents.loc[j,'OgrenciNo'], ListOfStudents.loc[j,'Öğrenci Ad Soyad'], CourseID  ,CourseTag, Year1, Year2, Semester ))

    
    
AssesName=pd.read_csv('GeneratedData/AssesNames.csv',header=None)

for i in range(len(AssesName)):
    Bool=CheckSheetExists(CourseFilePath,AssesName.iloc[i,0])
    if Bool==1:
        SheetName=AssesName.iloc[i,0]
        
        AssesOCTable = pd.read_excel(CourseFilePath, sheet_name=SheetName,usecols="E:AC",nrows=20)  
        QuestionWeights = pd.read_excel(CourseFilePath, sheet_name=SheetName,usecols="C:AC",skiprows=28,nrows=1).drop(axis=1,labels="OgrenciNo")
        QuestionWeights = QuestionWeights.drop(axis=1,labels="Toplam Puan")
        NoofQuestions= int(QuestionWeights[QuestionWeights.any(axis=1)].idxmax(axis=1).iloc[0].split('.')[0])
        AssesGrades = pd.read_excel(CourseFilePath, sheet_name=SheetName,usecols="B:AC",skiprows=28)
        AssesGrades = AssesGrades.drop(index=0).reset_index()
        ListOfStudents = AssesGrades.loc[:,['OgrenciNo','Öğrenci Ad Soyad']]
        
        for j in range(0,NoofQuestions):
            QuestNo=j+1
            QuestNoName=str(QuestNo)+'. Soru'
            QuestionWeight=int(QuestionWeights.loc[0,QuestNoName])

            # for k in range(len(AssesOCTable)):
            #     if AssesOCTable.loc[k,QuestNoName]==True:
            #         QuestOC=k+1
            cursor.execute("INSERT INTO QuestWeight (CourseID, CourseTag, Year1, Year2, Semester, AssesType   , QuestNo, QuestWeight   )\
                           VALUES                   (   {}   ,    '{}'  ,  {}  ,   {} ,   '{}'  ,    '{}'     ,    {}  ,       {}      );".format(\
                                                     CourseID, CourseTag, Year1, Year2, Semester, SheetName, QuestNo, QuestionWeight))
            connection.commit()
            
            # cursor.execute("CREATE TABLE QuestWeight\
            #           (QuestWeightID SERIAL PRIMARY KEY                  NOT NULL,\
            #            CourseID    INT REFERENCES Course(CourseID)       NOT NULL,\
            #            CourseTag   TEXT                                  NOT NULL,\
            #            Year1       INT                                   NOT NULL,\
            #            Year2       INT                                   NOT NULL,\
            #            Semester    TEXT                                  NOT NULL,\
            #            AssesType   TEXT                                  NOT NULL,\
            #            QuestNo     INT                                   NOT NULL,\
            #            QuestWeight INT                                   NOT NULL);")
            
            cursor.execute("SELECT QuestWeightID FROM QuestWeight WHERE CourseTag='{}' AND Year1={} AND Year2={} AND Semester='{}' AND AssesType='{}' AND QuestNo='{}';"\
                            .format(                                    CourseTag   ,      Year1   ,    Year2   ,    Semester   ,     SheetName,         QuestNo  ))
            QuestWeightID=cursor.fetchone()[0]
            
            for k in range(len(ListOfStudents)):
                Grade=AssesGrades.loc[k,QuestNoName]
                cursor.execute("INSERT INTO Grade (CourseID, StuNo,                                QuestWeightID, Grade)\
                               VALUES             (   {}   , {}   ,                                    {}       ,   {} );".format(\
                                                   CourseID, ListOfStudents.loc[k,'OgrenciNo'],    QuestWeightID, Grade))
                connection.commit()

            #     cursor.execute("CREATE TABLE Grade\
            #               (GradeID       SERIAL PRIMARY KEY                        NOT NULL,\
            #                CourseID      INT REFERENCES Course(CourseID)           NOT NULL,\
            #                StuNo         INT REFERENCES Student(StuNo)             NOT NULL,\
            #                QuestWeightID INT REFERENCES QuestWeight(QuestWeightID) NOT NULL,\
            #                Grade         INT                                       NOT NULL);")
            
                
            
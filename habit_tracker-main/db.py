'''
File: db.py
Date: 2023-01-20
Author: Mohammed Wais
Desciption:
This file is to construct the database for the program
'''
from sqlalchemy import create_engine
engine =create_engine('sqlite:///mydb.sqlite')
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date , DateTime 
from datetime import datetime , date, timedelta
base=declarative_base()


import os.path
import sys
from io import StringIO
from sqlalchemy.orm import sessionmaker

class daily_habit(base):  
    '''
    daily_habit class creates a table called Daily Habit in the database
    '''
    __tablename__ =  'Daily Habit'

    daily_habit_ID = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    description = Column(Integer)
    created_date = Column(DateTime)
    no_of_checking = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    counter = Column(String)

class weekly_habit(base):
    '''
    weekly_habit class creates a table called Weekly Habit in the database
    '''
    __tablename__ =  'Weekly Habit'

    weekly_habit_ID = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    description = Column(Integer)
    created_date = Column(DateTime)
    no_of_checking = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    counter = Column(String)


base.metadata.create_all(engine)

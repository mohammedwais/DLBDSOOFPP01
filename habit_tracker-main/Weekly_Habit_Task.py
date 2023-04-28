'''
File: Weekly_Habit_Task.py
Date: 2023-01-20
Author: Mohammed Wais
Descritpion:
This file is to create, retreive, and modifiy weekly habits.
'''
from sqlalchemy import Column, Integer, String,Date
from sqlalchemy import create_engine
from db import daily_habit,weekly_habit,base
from datetime import datetime , date, timedelta
import re
engine = create_engine('sqlite:///mydb.sqlite')
base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
sessionobj = Session()

from Habits_List import Counter as ct
import math


class weekly_habit_task:

    def add():

        '''
        Add a weekly habit to the database. it taskes inputs:
        [1] Name:  name for the weekly task
        [2] Description:  descritpion of the weekly task
        [3] Start date: the start date of the weekly task
        [4] End date: the end date of the weekly task (shouldn't be less than the start date)

        It also return the above mentioned details as dictionary in list.

        '''

        import re
        import datetime

        try:
            name = input('Enter name:')
            description = input('Enter Description: ')
            created_date = datetime.datetime.today()
            no_of_checking = 0 # default value
            format= "%Y-%m-%d"
            start_date = datetime.datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
            end_date = datetime.datetime.strptime(input('Enter end date in format YYYY-MM-DD: '),format)
            diff_st_en = round((end_date -start_date ).days/7) # diffrenec bewteen end date and start date
            if diff_st_en < 0: raise ValueError

            nd_date_end_date = end_date + datetime.timedelta(days=6)
            bd_date_end_date = end_date - datetime.timedelta(days=6)

            nd_date_start_date = start_date + datetime.timedelta(days=6)
            bd_date_start_date = start_date - datetime.timedelta(days=6)

            counter = ''
            if (bd_date_start_date <= end_date <= nd_date_start_date) and (nd_date_end_date <= created_date <= bd_date_end_date) :
                counter =  ct.add_o_left(counter,diff_st_en)
            elif end_date < created_date:
                for x in range(round((end_date - start_date).days/7)):
                    counter =  ct.add_o_left(counter,diff_st_en)
            elif start_date < created_date:
                for x in range(math.ceil((created_date - start_date).days/7)):
                  counter = ct.add_o_right(counter,diff_st_en)



            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            session.add(weekly_habit(\
                name= name,\
                description=description,\
                created_date= created_date ,\
                no_of_checking = no_of_checking,\
                start_date= start_date,\
                end_date=end_date,\
                counter = counter))
            session.commit()
            s = {'name':name,\
                'description':description,\
                'created_date':created_date,\
                'no_of_checking':no_of_checking, \
                'start_date':start_date ,\
                'end_date':end_date,\
                'counter': counter   }
            m = []
            m.append(s)
            return m
        except ValueError:
            print('Failed to process!!')
            print('Please enter date in format of:YYYY-MM-DD and make sure end date not earlier than start date! ')
            pass
        

    def check_off():
        '''
        It checks off the weekly habit(add +1 to no of check off)
        It takes only one parameter (Task ID)

        it returns the no of check off as a dictionary in list.
        '''
        try:
            # find habit by ID number and update the checkoff by +1
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)

            cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
            if cc_weekly_habit != None:
                # if task still active
                if cc_weekly_habit.end_date  >= datetime.today():
                    diff = round((cc_weekly_habit.end_date - cc_weekly_habit.start_date).days/7)
                    cc_weekly_habit.counter = ct.add_x_right(cc_weekly_habit.counter,diff)
                    session.commit()
                    cc_weekly_habit.no_of_checking = ct.counter_x(cc_weekly_habit.counter)
                    session.commit()
                # if task is a decative
                if cc_weekly_habit.end_date < datetime.today():
                    question = input('This habit task is already last, do you want to change specic date?Y/N ')
                    if question == 'Y' or 'y':
                        format= "%Y-%m-%d"
                        specfic_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
                        diff_dates = round((cc_weekly_habit.end_date - cc_weekly_habit.start_date).days/7)
                        index = round((specfic_date - cc_weekly_habit.start_date).days/7)
                        m = cc_weekly_habit.counter
                        cc_weekly_habit.counter =ct.replace_x(m,diff_dates,index)
                        session.commit()
                        cc_weekly_habit.no_of_checking = ct.counter_x(cc_weekly_habit.counter)
                        session.commit()


                session.commit()
                print('Weekly habit has been checked off successufly!')

                s = {'no_of_checking':cc_weekly_habit.no_of_checking}
                m = []
                m.append(s)

                return m
            else:
                print('No data has been found')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def delete():
        '''
        It delete a task from the database.
        It takes only one parameter (Task ID).
        it returns NONE as a dictionary in list if the task sussecfuly has been deleted
        '''
        # find the habit by id number and delete it 
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if query.filter(weekly_habit.weekly_habit_ID== ID) != None: 
                query = query.filter(weekly_habit.weekly_habit_ID== ID)
                dcc_weekly_habit = query.one()
                session.delete(dcc_weekly_habit)
                session.commit()
                print('Weekly habit has been deleted successufly!')

                return None
            else: 
                print('No data has been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def get_created_date():
        '''
        It retrieves the created date for the task.
        It needs only one parameter (Task ID).

        it returns the created date as dictionary in list
        '''
        # find habit by id number and retrieve the created date
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit.weekly_habit_ID)
            if query.filter(weekly_habit.weekly_habit_ID == ID).first() != None:
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                session.commit()
                print(cc_weekly_habit.created_date)
                
                print('Weekly habit has been retrived successufly!')

                return cc_weekly_habit.created_date
            else: 
                print('No data has been found')
                return None 
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass 


    def get_habit_describtion():
        '''
        It retrieves the description for the task.
        It needs only one parameter (Task ID).

        it returns the created date as dictionary in list
        '''
        # find habit by id number and retrieve the description
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if  query.filter(weekly_habit.weekly_habit_ID == ID).first() != None:
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                session.commit()
                print(cc_weekly_habit.description)
                
                print('Weekly habit has been retrived successufly!')

                return cc_weekly_habit.description
            else:
                print('No data has been found')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def get_habit_name():
        '''
        It retrieves the name for the task.
        It needs only one parameter (Task ID).

        it returns the name as dictionary in list
        '''     
        # find habit by id number and retrieve the name
        try:
            ID = int(input('Enter ID number or E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if  query.filter(weekly_habit.weekly_habit_ID== ID).first() != None:
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID== ID).first()
                session.commit()
                print(cc_weekly_habit.name)
                
                print('Weekly habit has been retrived successufly!')
                return cc_weekly_habit.name
            else: 
                print('No data has been found')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def no_of_checking_off():
        '''
        It retrieves the no of cheecking off for the task.
        It needs only one parameter (Task ID).

        it returns the o of cheecking off as dictionary in list
        '''   
        # find habit by id number and retrieve no of checkoff
        try:
            # ID = int(input('Enter ID number or enter E to go back: '))
            # engine = create_engine('sqlite:///mydb.sqlite')
            # base.metadata.create_all(engine)
            # session = Session()
            # query = session.query(weekly_habit)

            ID = int(input('Enter ID number or type E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
            if cc_weekly_habit != None:
                m = cc_weekly_habit.counter
                no_of_checking = ct.counter_x(m)
                session.commit()
                print(no_of_checking)
                s = {'no_of_checking': no_of_checking}
                m = []
                m.append(s)
                print('Weekly habit has been retrived successufly!')
                return m
            else:
                print('No data has been found')
                return None

        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def set_habit_describtion():
        '''
        It modify the description the task.
        It needs only one parameter (Task ID).

        it returns the descriptionas dictionary in list
        '''   
        # find habit by id number and update the description
        try: 
            ID = int(input('Enter ID number or enter E to go back: '))
            habit_describtion = input('Enter new habit description: ')
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if query.filter(weekly_habit.weekly_habit_ID == ID).first() != None:
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                cc_weekly_habit.description = habit_describtion
                session.commit()
                print('Weekly habit has been modifed successufly!')
                s = {'description':cc_weekly_habit.description}
                m = []
                m.append(s)

                return m
            else:
                print('No data has been found with same Id')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def set_habit_name():
        '''
        It modify the name the task.
        It needs only one parameter (Task ID).

        it returns the name dictionary in list
        '''  
        # find habit by id number and update the description
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            habit_name = input('Enter new habit description: ')
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
            if cc_weekly_habit != None:
                cc_weekly_habit.name = habit_name
                session.commit()
                print('Weekly habit has been modifed successufly!')
                s = {'name':cc_weekly_habit.name}
                m = []
                m.append(s)

                return m
            else:
                print('No data has been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def unchecking_off():
        '''
        It unchecks off  the task.
        It needs only one parameter (Task ID).

        it returns the no of checking after modifiication dictionary in list
        '''   
        # find habit by ID number and update the check off by -1 (check zero)
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            #------------------------------------
            cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
            if cc_weekly_habit != None:
                if cc_weekly_habit.no_of_checking == 0:
                    print('Weekly habit has null no of check off!')
                    # session.rollback()
                else:
                    # if task still active
                    if cc_weekly_habit.end_date  >= datetime.today():
                        diff = math.ceil((cc_weekly_habit.end_date - cc_weekly_habit.start_date).days /7)
                        cc_weekly_habit.counter = ct.replace_o(cc_weekly_habit.counter,diff,len(cc_weekly_habit.counter)-1)
                        session.commit()
                        cc_weekly_habit.no_of_checking = ct.counter_x(cc_weekly_habit.counter)
                        session.commit()
                    
                    # if task is a decative
                    if cc_weekly_habit.end_date < datetime.today():
                        question = input('This habit task is already last, do you want to change specic date?Y/N ')
                        if question == 'Y' or 'y':
                            format= "%Y-%m-%d"
                            specfic_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
                            diff_dates = round((cc_weekly_habit.end_date - cc_weekly_habit.start_date).days/7)
                            index = round((specfic_date - cc_weekly_habit.start_date).days/7)
                            m = cc_weekly_habit.counter
                            cc_weekly_habit.counter =ct.replace_o(m,diff_dates,index)
                            session.commit()
                            cc_weekly_habit.no_of_checking = ct.counter_x(cc_weekly_habit.counter)
                            session.commit()

                    print('Weekly habit has been unchecked off successufly!')
            #------------------------------------

                s = {'no_of_checking':cc_weekly_habit.no_of_checking}
                m = []
                m.append(s)

                return m
            else:
                print('No data hsa been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass
    
    

    def get_end_date():
        '''
        It ret=rtrieves end date for the task.
        It needs only one parameter (Task ID).

        it returns the end date dictionary in list
        '''  
        # find habit by id number and retrieve the end date
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if query.filter(weekly_habit.weekly_habit_ID == ID).first() != None: 
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                session.commit()
                print(cc_weekly_habit.end_date)
                
                print('Weekly habit has been retrived successufly!')
                return cc_weekly_habit.end_date
            else:
                print('No data has been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass


    def get_start_date():
        '''
        It retrieves the start date for the task.
        It needs only one parameter (Task ID).

        it returns the start date in dictionary in list
        '''  
        try:
            # find habit by id number and retrieve the start date
            ID = int(input('Enter ID number or enter E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if  query.filter(weekly_habit.weekly_habit_ID == ID).first() != None: 
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                session.commit()
                print(cc_weekly_habit.start_date)
                
                print('Weekly habit has been retrived successufly!')
                return cc_weekly_habit.start_date
            else: 
                print('No data has been found with same Id')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid number: 1,2,3, etc.!')
            pass

    def set_end_date():
        '''
        It modify the end date the task. (end date shouldn't be earlier than the start date)
        It needs only one parameter (Task ID).

        it returns the end date dictionary in list
        '''   
        # find habit by id number and update the end date
        try:
            ID = int(input('Enter ID number or enter E to go back: '))
            format= "%Y-%m-%d"
            end_date = datetime.strptime(input('Enter end date in format YYYY-MM-DD: '),format)
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if  query.filter(weekly_habit.weekly_habit_ID == ID).first() != None:
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                if cc_weekly_habit.start_date > end_date: raise ValueError
                cc_weekly_habit.end_date = end_date
                session.commit()
                print('Weekly habit has been modifed successufly!')
                s = {'end_date':cc_weekly_habit.end_date}
                m = []
                m.append(s)
                return m
            else:
                print('No data has been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid ID number: 1,2,3, etc.! and make sure start date is not earlier than end date')
            pass

    def set_start_date():
        '''
        It modify the start date for  the task.
        It needs only one parameter (Task ID).

        it returns the start date dictionary in list
        '''   
        # find habit by id number and update the start date
        try:
            ID = int(input('Enter ID number or E to go back: '))
            format= "%Y-%m-%d"
            start_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(weekly_habit)
            if query.filter(weekly_habit.weekly_habit_ID == ID).first() != None:
                cc_weekly_habit = query.filter(weekly_habit.weekly_habit_ID == ID).first()
                if cc_weekly_habit.end_date < start_date: raise ValueError
                cc_weekly_habit.start_date = start_date
                session.commit()
                print('Weekly habit has been modifed successufly!')
                s = {'start_date':cc_weekly_habit.start_date}
                m = []
                m.append(s)
                return m
            else:
                print('No data has been found with same ID')
                return None 
        except ValueError:
            print('Failed to process!!')
            print('Please enter valid ID number: 1,2,3, etc.! and make sure start date is not earlier than end date')
            pass


'''
File: Daily_habit_task.py
Date: 2023-01-20
Author: Mohammed Wais
Description:
This file is to create, retreive, and modifiy daily habits.
'''
# import modules 
from sqlalchemy import Column, Integer, String,Date
from sqlalchemy import create_engine
from db import daily_habit,weekly_habit,base
from datetime import datetime , date, timedelta

# connect to SQLAlchecmy engine
engine = create_engine('sqlite:///mydb.sqlite')
base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
sessionobj = Session()

# import Counter class 
from Habits_List import Counter as ct

# Creating daily habit task calss
class daily_habit_task:
    def add():
        '''
        Add a daily habit to the database. it taskes inputs:
        [1] Name:  name for the daily task
        [2] Description:  descritpion of the daily task
        [3] Start date: the start date of the daily task
        [4] End date: the end date of the daily task (shouldn't be less than the start date)

        It also return the above mentioned details as dictionary in list.

        '''
        try:
            name = input('Enter name:') # user to enter habit task name
            description = input('Enter Description: ') # user to enter habit describtion
            created_date = datetime.today() # app to regist creation date 
            no_of_checking = 0 # default value
            # counter = 'o'
            format= "%Y-%m-%d"
            
            start_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format) # start date to be define by user
            end_date = datetime.strptime(input('Enter end date in format YYYY-MM-DD: '),format) # end date to be defined by user
            diff = (end_date- start_date).days # calculate the diffrence between start date and end dae
            #print(diff)
            
            # to update the database by number of checking 
            counter = ''
            if end_date == start_date and end_date < created_date :
                counter =  ct.add_o_left(counter,diff+1)  # "o" reprenests number of missing checking or not checked yet

            elif end_date < created_date:
                for x in range((end_date - start_date).days):
                  counter =  ct.add_o_left(counter,diff) 

            elif start_date < created_date:
                for x in range((created_date - start_date).days):
                  counter = ct.add_o_right(counter,diff) 

            

            diff_st_en = (end_date -start_date ).days # diffrenec bewteen end date and start date
            if diff_st_en < 0: raise ValueError
            # updating the database with attributes values
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            session.add(daily_habit(\
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
                'counter':counter  }
            m = []
            m.append(s)
            return m
        # raise error if any data valuation has detected 
        except ValueError:
            print('Failed to process!!')
            print('Please enter date in format of:YYYY-MM-DD and make sure end date not earlier than start date! ')
            pass

    # function to check off the task base
    def check_off():
        '''
        It checks off the daily habit(add +1 to no of check off)
        It takes only one parameter (Task ID)

        it returns the no of check off as a dictionary in list.
        '''
        # find habit by ID number and update the check off by +1
        try:
            ID = int(input('Enter ID number: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                # if task still active
                if cc_daily_habit.end_date  >= datetime.today():
                    diff = (cc_daily_habit.end_date - cc_daily_habit.start_date).days
                    cc_daily_habit.counter = ct.add_x_right(cc_daily_habit.counter,diff)
                    session.commit()
                    cc_daily_habit.no_of_checking = ct.counter_x(cc_daily_habit.counter)
                    session.commit()
                # if task is a decative
                if cc_daily_habit.end_date < datetime.today():
                    question = input('This habit task is already last, do you want to change specic date?Y/N ')
                    if question == 'Y' or question == 'y':
                        format= "%Y-%m-%d"
                        specfic_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
                        diff_dates = (cc_daily_habit.end_date - cc_daily_habit.start_date).days
                        index = (specfic_date - cc_daily_habit.start_date).days
                        m = cc_daily_habit.counter
                        cc_daily_habit.counter =ct.replace_x(m,diff_dates,index)
                        session.commit()
                        cc_daily_habit.no_of_checking = ct.counter_x(cc_daily_habit.counter)
                        session.commit()
                    elif question == 'N' or 'n':
                        pass

                # retrieve data
                query = session.query(daily_habit)
                cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
                print('Daily habit has been checked off successufly!')
                k = cc_daily_habit.no_of_checking 
                s = {'no_of_checking':k }
                m = []
                m.append(s)
                session.commit()
                return m
            else:
                print("No data found with same ID")
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

        

    def delete():
        '''
        It delete a task from the database.
        It takes only one parameter (Task ID).
        it returns NONE as a dictionary in list if the task sussecfuly has been deleted
        '''
        # find the habit by id number and delete it
        try:
            ID = int(input('Enter ID number: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            query = query.filter(daily_habit.daily_habit_ID == ID)
            if query != None:
                dcc_daily_habit = query.one()
                session.delete(dcc_daily_habit)
                session.commit()
                print('Daily habit has been deleted successufly!')
                session = Session()
                query = session.query(daily_habit)
                s =  { 'delete': query.filter(daily_habit.daily_habit_ID == ID) }
                m = []
                m.append(s)
                session.commit()
                return m
            else:
                print('No data has been found with same Id')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

    def get_created_date():
        '''
        It retrieves the created date for the task.
        It needs only one parameter (Task ID).

        it returns the created date as dictionary in list
        '''
        # find habit by id number and retrieve the created date
        try:
            ID = int(input('Enter ID number or type E to back to menu: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                session.commit()
                # print(cc_daily_habit.created_date)
                
                print('Daily habit has been retrived successufly!')
                return cc_daily_habit.created_date
            else:
                print('No data has been found with same Id')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

    
    def get_habit_describtion():
        '''
        It retrieves the description for the task.
        It needs only one parameter (Task ID).

        it returns the created date as dictionary in list
        '''
        try:
            # find habit by id number and retrieve the description
            ID = int(input('Enter ID number: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                session.commit()
                # print(cc_daily_habit.description)
                
                print('Daily habit has been retrived successufly!')
                return cc_daily_habit.description
            else:
                print('No data has been found')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

    def get_habit_name():
        '''
        It retrieves the name for the task.
        It needs only one parameter (Task ID).

        it returns the name as dictionary in list
        '''       
        # find habit by id number and retrieve the name
        try:
            ID = int(input('Enter ID number or type E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                session.commit()
                # print(cc_daily_habit.name)
                
                print('Daily habit has been retrived successufly!')
                return cc_daily_habit.name
            else:
                print('No data has been found')
                return None
        except:
            print('Please enter a number: 1,2,3, etc!')
            pass

    def no_of_checking_off():
        '''
        It retrieves the no of cheecking off for the task.
        It needs only one parameter (Task ID).

        it returns the o of cheecking off as dictionary in list
        '''   
        # find habit by id number and retrieve no of checkoff
        try:
            ID = int(input('Enter ID number or type E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                m = cc_daily_habit.counter
                no_of_checking = ct.counter_x(m)
                session.commit()
                print(no_of_checking)
                s = {'no_of_checking': no_of_checking}
                m = []
                m.append(s)
                print('Daily habit has been retrived successufly!')
                return m
            else:
                print('No data has been found')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass
        

    def set_habit_describtion():
        '''
        It modify the description the task.
        It needs only one parameter (Task ID).

        it returns the descriptionas dictionary in list
        '''   
        # find habit by id number and update the description
        try:
            ID = int(input('Enter ID number: '))
            habit_describtion = input('Enter new habit description: ')
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                cc_daily_habit.description = habit_describtion
                session.commit()
                print('Daily habit has been modifed successufly!')
                s = {'description':cc_daily_habit.description}
                m = []
                m.append(s)
                return m
            else:
                print('No data has been found')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass
    
    def set_habit_name():
        '''
        It modify the name the task.
        It needs only one parameter (Task ID).

        it returns the name dictionary in list
        '''   
        # find habit by id number and update the description
        try:
            ID = int(input('Enter ID number: '))
            habit_name = input('Enter new habit description: ')
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                cc_daily_habit.name = habit_name
                session.commit()
                print('Daily habit has been modifed successufly!')
                s = {'name':cc_daily_habit.name}
                m = []
                m.append(s)
                return m
            else: 
                print('No data hass been found wiht same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

    def unchecking_off():
        '''
        It unchecks off  the task.
        It needs only one parameter (Task ID).

        it returns the no of checking after modifiication dictionary in list
        '''   
        # find habit by ID number and update the check off by -1 (check zero)
        try:
            ID = int(input('Enter ID number or E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
            if cc_daily_habit != None:
                if cc_daily_habit.no_of_checking == 0:
                    print('Daily habit has null no of check off!')
                    # session.rollback()
                else:
                    # if task still active
                    if cc_daily_habit.end_date  >= datetime.today():
                        diff = (cc_daily_habit.end_date - cc_daily_habit.start_date).days
                        cc_daily_habit.counter = ct.replace_o(cc_daily_habit.counter,diff,len(cc_daily_habit.counter)-1)
                        session.commit()
                        cc_daily_habit.no_of_checking = ct.counter_x(cc_daily_habit.counter)
                        session.commit()
                    
                    # if task is a decative
                    if cc_daily_habit.end_date < datetime.today():
                        question = input('This habit task is already last, do you want to change specic date?Y/N ')
                        if question == 'Y' or 'y':
                            format= "%Y-%m-%d"
                            specfic_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
                            diff_dates = (cc_daily_habit.end_date - cc_daily_habit.start_date).days
                            index = (specfic_date - cc_daily_habit.start_date).days
                            m = cc_daily_habit.counter
                            cc_daily_habit.counter =ct.replace_o(m,diff_dates,index)
                            session.commit()
                            cc_daily_habit.no_of_checking = ct.counter_x(cc_daily_habit.counter)
                            session.commit()

                    print('Daily habit has been unchecked off successufly!')
            # data retreive 
                session = Session()
                query = session.query(daily_habit)
                cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()

                k = cc_daily_habit.no_of_checking 
                s = {'no_of_checking':k }
                m = []
                m.append(s)
                session.commit()
                return m

            else:
                print('No data has been foudn with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass
    

    def get_end_date():
        '''
        It ret=rtrieves end date for the task.
        It needs only one parameter (Task ID).

        it returns the end date dictionary in list
        '''   
        # find habit by id number and retrieve the end date
        try:
            ID = int(input('Enter ID number or E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            if query.filter(daily_habit.daily_habit_ID == ID) != None:
                cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
                session.commit()
                # print(cc_daily_habit.end_date)
                
                print('Daily habit has been retrived successufly!')
                return cc_daily_habit.end_date.date()
            else:
                print('No data has been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

    def get_start_date():
        '''
        It retrieves the start date for the task.
        It needs only one parameter (Task ID).

        it returns the start date in dictionary in list
        '''   
        # find habit by id number and retrieve the start date
        try:
            ID = int(input('Enter ID number or E to go back: '))
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            if query.filter(daily_habit.daily_habit_ID == ID) != None:
                cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
                session.commit()
                # print(cc_daily_habit.start_date)
                print('Daily habit has been retrived successufly!')

                return cc_daily_habit.start_date.date()
            else: 
                print('No data has been found with same ID')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc!')
            pass

    def set_end_date():
        '''
        It modify the end date the task. (end date shouldn't be earlier than the start date)
        It needs only one parameter (Task ID).

        it returns the end date dictionary in list
        '''   
        # find habit by id number and update the end date
        try:
            ID = int(input('Enter ID number or E to go back: '))
            format= "%Y-%m-%d"
            end_date = datetime.strptime(input('Enter end date in format YYYY-MM-DD: '),format)
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            if query.filter(daily_habit.daily_habit_ID == ID) != None:
                # if new end date is later than current date ( nothing to be changed)
                # if new end date is eariler than current date (diff should be filled w/ 'o')
                    # if the new end date is earlier than old end date (some part shall be removed)
                    # if the new end date is later than old end date (some part shall be added)
                cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
                if cc_daily_habit.start_date > end_date: raise ValueError
                cc_daily_habit.end_date = end_date
                session.commit()
                print('Daily habit has been modifed successufly!')
                s = {'end_date':cc_daily_habit.end_date}
                m = []
                m.append(s)
                return m
            else: 
                print('No data has been found with same Id')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter a number: 1,2,3, etc! and make sure the start date is not earlier than end date')
            pass


    def set_start_date():
        '''
        It modify the start date for  the task.
        It needs only one parameter (Task ID).

        it returns the start date dictionary in list
        '''   
        # find habit by id number and update the start date
        try:
            ID = int(input('Enter ID number or E to fo back: '))
            format= "%Y-%m-%d"
            start_date = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
            engine = create_engine('sqlite:///mydb.sqlite')
            base.metadata.create_all(engine)
            session = Session()
            query = session.query(daily_habit)
            if query.filter(daily_habit.daily_habit_ID == ID) != None:
                cc_daily_habit = query.filter(daily_habit.daily_habit_ID == ID).first()
                if  cc_daily_habit.end_date < start_date: raise ValueError
                cc_daily_habit.start_date = start_date
                session.commit()
                print('Daily habit has been modifed successufly!')
                s = {'start_date':cc_daily_habit.start_date}
                m = []
                m.append(s)
                return m
            else: 
                print('No data has been foudn')
                return None
        except ValueError:
            print('Failed to process!!')
            print('Please enter ID as positive integer number and make sure the end date is not earlier than the start date')
            pass

#----------------------#

'''
File: test_project.py
Date: 2023-01-20
Author: Mohammed Wais
Descitpion: 
This file is to test the whole functionality of the programm
'''
import os.path
import sys
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def test_database(monkeypatch):
    '''
    This to test the crreation of the dataase and its functionality 
    '''
    import db
    from sqlalchemy import create_engine
    db.engine = create_engine ('sqlite:///mydb.sqlite')
    assert os.path.isfile("mydb.sqlite")
    assert db.engine.table_names()[0] == 'Daily Habit'
    assert db.engine.table_names()[1] == 'Weekly Habit'

    
# [1] Test Create habit task

    # [1-1] Create a daily habit task
    # create a daily task then check then check if we can retreive it
def test_create_daily_habit_task():
    '''
    This test functionaly of program to create daily habit task
    '''
    from Daily_habit_task import daily_habit_task as dht
    import datetime
    
    # sample data for daily habit task
    m = [{'name':'Test Task 1' ,'description':'D-Task1','start_date':'2022-02-01','end_date':'2022-09-01'},
         {'name':'Test Task 2' ,'description':'D-Task2','start_date':'2022-03-04','end_date':'2022-03-06'},
         {'name':'Test Task 3' ,'description':'D-Task3','start_date':'2021-06-02','end_date':'2022-01-01'},
         {'name':'Test Task 4' ,'description':'D-Task4','start_date':'2021-01-02','end_date':'2022-01-07'},
    ]
    for s in m:
        name = s['name']
        description = s['description']
        start_date = s['start_date']
        end_date = s['end_date']
        oldstdin = sys.stdin
        sys.stdin = StringIO("{}\n{}\n{}\n{}".format(name,description,start_date,end_date))
        x = dht.add()
        sys.stdin = oldstdin
        # # convet date string to date object
        sd_ = [int(s) for s in start_date.split('-') if s.isdigit()]
        sd_date = datetime.datetime(sd_[0] ,sd_[1], sd_[2])
        ed_ = [int(s) for s in end_date.split('-') if s.isdigit()]
        ed_date = datetime.datetime(ed_[0] ,ed_[1], ed_[2])
        # s = {'name':name,\
        #         'description':description,\
        #         'created_date':created_date,\
        #         'no_of_checking':no_of_checking, \
        #         'start_date':start_date ,\
        #         'end_date':end_date    }
        # x = me()
        # assert x[0]  == "1"
        # assert x[1]  == "2"
        
        assert x[0]['name'] == name
        assert x[0]['description'] == description
        assert x[0]['start_date'] == sd_date
        assert x[0]['end_date'] == ed_date
    
    

    # [1-2] Create a weekly habit tasks
    # create a weekly task then check then check if we can retreive it
def test_create_weekly_habit_task():
    '''
    This test functionaly of program to create weekly habit task
    '''
    from Weekly_Habit_Task import weekly_habit_task as wht
    import datetime

    # sample data for weekly habit task
    m = [{'name':'Test Task 1' ,'description':'W-Task1','start_date':'2022-02-01','end_date':'2022-09-01'},
         {'name':'Test Task 2' ,'description':'W-Task2','start_date':'2022-03-04','end_date':'2023-04-05'},
         {'name':'Test Task 3' ,'description':'W-Task3','start_date':'2022-06-02','end_date':'2023-03-03'},
         {'name':'Test Task 4' ,'description':'W-Task4','start_date':'2021-01-02','end_date':'2023-02-07'},
    ]

    for s in m:
        name = s['name']
        description = s['description']
        start_date = s['start_date']
        end_date = s['end_date']
        oldstdin = sys.stdin
        sys.stdin = StringIO("{}\n{}\n{}\n{}".format(name,description,start_date,end_date))
        x = wht.add()
        sys.stdin = oldstdin
        # # convet date string to date object
        sd_ = [int(s) for s in start_date.split('-') if s.isdigit()]
        sd_date = datetime.date(sd_[0] ,sd_[1], sd_[2])
        ed_ = [int(s) for s in end_date.split('-') if s.isdigit()]
        ed_date = datetime.date(ed_[0] ,ed_[1], ed_[2])
        # s = {'name':name,\
        #         'description':description,\
        #         'created_date':created_date,\
        #         'no_of_checking':no_of_checking, \
        #         'start_date':start_date ,\
        #         'end_date':end_date    }
        # x = me()
        # assert x[0]  == "1"
        # assert x[1]  == "2"
        
        assert x[0]['name'] == name
        assert x[0]['description'] == description
        # assert x[0]['start_date'].date == sd_date
        # assert x[0]['end_date'].date == ed_date
    

    # [1-3] Back to main menu
    # check if the option to bck for main menu does work in main ()
def test_main_creat_habit():
    '''
    This test functionaly of CLI in menu of creating habit 
    '''
    from main import main
    input0 = 'n'
    input1 = '1'
    input2 = '3'
    input3 = '6'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n{}\n{}\n{}\n".format(input0,input1,input2,input3))
    x = main()
    sys.stdin = oldstdin
    
    assert x == None
    

# [2] Test View habit
    # [2-1] View daily habit task
    # check if the view does work as well
def test_view_daily_habit_task():
    '''
    This test functionaly of programm to view daily  habit
    '''
    from Habits_List import habit_list as hl
    x = hl.get_all_daily_list()
    for n in x:
       assert n['id'] != None
       assert n['name'] != None
       assert n['start_date'] != None
       assert n['end_date'] != None
       assert n['no_of_checking_of'] != None
    

    # [2-2] View weekly habit task
    # check if the view does work as well
def test_view_weekly_habit_task():
    '''
    This test functionaly of programm to view weekly  habit
    '''
    from Habits_List import habit_list as hl
    x = hl.get_all_weekly_list()
    for n in x:
       assert n['id'] != None
       assert n['name'] != None
       assert n['start_date'] != None
       assert n['end_date'] != None
       assert n['no_of_checking_of'] != None
    

    # [2-3] Back to main menu
    # check if the option to bck for main menu does work in main ()
def test_view_main():
    '''
    This test functionaly of CLI in menu of viewing habit 
    '''
    from main import main
    input0 = 'N'
    input1 = '2'
    input2 = '5'
    input3 = '6'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n{}\n{}\n{}\n".format(input0,input1,input2,input3))
    x = main()
    sys.stdin = oldstdin
    
    assert x == None

    
# [3] Analyze habit

    # [3-1] Daily streak habits
    # test the streak daily habit for 15 days 
def test_streak_daily_habit():
    '''
    This test functionaly of programm to find streaking daily habit
    '''
    from Habits_List import habit_list as hl
    x = hl.daily_broken_habit()
    for n in x:
       assert n['id'] != None
       assert n['name'] != None
       assert n['start_date'] != None
       assert n['end_date'] != None
       assert n['no_of_checking'] != None
    

    # [3-2] weekly streak habits
def test_streak_weekly_habit():
    '''
    This test functionaly of programm to find streaking weekly habit
    '''
    from Habits_List import habit_list as hl
    input = '2'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n".format(input))
    x = hl.weekly_streak()
    sys.stdin = oldstdin
    for n in x:
       assert n['id'] != None
       assert n['name'] != None
       assert n['start_date'] != None
       assert n['end_date'] != None
       assert n['no_of_checking'] != None
    

    # [3-3] Daily broken habits
def test_daily_brocken_habit():
    '''
    This test functionaly of programm to find broken daily habit
    '''
    from Habits_List import habit_list as hl
    x = hl.daily_broken_habit()
    for n in x:
       assert n['id'] != None
       assert n['name'] != None
       assert n['start_date'] != None
       assert n['end_date'] != None
       assert n['no_of_checking'] != None
    

    # [3-4] Weekly broken habits
def test_weekly_brocken_habit():
    '''
    This test functionaly of programm to find broken weekly habit
    '''
    from Habits_List import habit_list as hl
    x = hl.weekly_broken_habit()
    for n in x:
       assert n['id'] != None
       assert n['name'] != None
       assert n['start_date'] != None
       assert n['end_date'] != None
       assert n['no_of_checking'] != None
    

    # [3-5] back to main menu
def test_main_menu_analyse():
    '''
    This test functionaly of CLI in menu of analyzing habit 
    '''
    from main import main
    input0 = 'N'
    input1 = '3'
    input2 = '7'
    input3 = '6'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n{}\n{}\n{}\n".format(input0,input1,input2,input3))
    x = main()
    sys.stdin = oldstdin
    
    assert x == None
    

# [4] Modify habit
    # [4-1] Check off daily habit
def test_check_off_daily():
    '''
    This test functionaly of programm to check off daily habit
    '''
    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()

    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x in last_place_team:
            input_1 = x.daily_habit_ID
            x_1 = x.no_of_checking
            # session.commit()
            # finding intial no of checking off
            # make a check off 
            #-----------------------
            x_date = '{}'.format(x.start_date)
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}\n{}".format(input_1,'Y',x_date[:10]))
            x_2 =  dht.check_off() # make check off
            sys.stdin = oldstdin
            x_2 =  x_2[0]['no_of_checking']
            # x_1 = x.no_of_checking
            #-----------------------
            # input2 = x.daily_habit_ID
            # x_date = '{}'.format(x.start_date)
            # oldstdin = sys.stdin
            # sys.stdin = StringIO("{}\n{}\n{}".format(input2,'Y',x_date))
            # x_2 =  dht.check_off()[0]['no_of_checking'] # make check off for specific date
            # sys.stdin = oldstdin

            if x_1 != x_2:
                assert x_2  == x_1 + 1
            else:
                assert x_2  == x_1 

            # assert x_1 == x.no_of_checking

    # [4-2] Uncheck off daily habit

def test_uncheck_off_daily():
    '''
    This test functionaly of programm to check off daily habit
    '''
    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()

    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x in last_place_team:
            input_1 = x.daily_habit_ID
            x_1 = x.no_of_checking
            # session.commit()
            # finding intial no of checking off
            # make a check off 
            #-----------------------
            x_date = '{}'.format(x.start_date)
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}\n{}".format(input_1,'Y',x_date[:10]))
            x_2 =  dht.unchecking_off() # make check off
            sys.stdin = oldstdin
            x_2 =  x_2[0]['no_of_checking']
            # x_1 = x.no_of_checking
            #-----------------------
            # input2 = x.daily_habit_ID
            # x_date = '{}'.format(x.start_date)
            # oldstdin = sys.stdin
            # sys.stdin = StringIO("{}\n{}\n{}".format(input2,'Y',x_date))
            # x_2 =  dht.check_off()[0]['no_of_checking'] # make check off for specific date
            # sys.stdin = oldstdin

            if x_1 != x_2:
                assert x_2  == x_1 - 1
            else:
                assert x_2  == x_1 

            # assert x_1 == x.no_of_checking

# def test_uncheck_off_daily():
#     '''
#     This test functionaly of programm to uncheck off daily habit
#     '''
#     from Daily_habit_task import daily_habit_task as dht
#     from Habits_List import habit_list as hl
#     from db import daily_habit
#     engine = create_engine('sqlite:///mydb.sqlite')
#     Session = sessionmaker(bind=engine)
#     sessionobj = Session()
#     base=declarative_base()

#     with sessionobj as session:
#         last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
#         for x in last_place_team:
#             input = x.daily_habit_ID
#             x_1 = x.no_of_checking
#             date2str = '{}'.format(x.start_date)
#             input_date = date2str[:10] # convert date to acceptable format for input
#             # session.commit()
#             # input1 = input
#             # oldstdin = sys.stdin
#             # sys.stdin = StringIO("{}".format(input1))
#             # x_1 =  dht.no_of_checking_off()[0]['no_of_checking']
#             # sys.stdin = oldstdin
#             input2 = input
#             if x_1 == 0: 
#                 input2 = input
#                 oldstdin = sys.stdin
#                 sys.stdin = StringIO("{}/n{}/n{}".format(input2))
#                 x_2 =  dht.unchecking_off()[0]['no_of_checking']
#                 sys.stdin = oldstdin
#             else:
#                 input2 = input
#                 oldstdin = sys.stdin
#                 sys.stdin = StringIO("{}/n{}/n{}".format(input2,'Y',input_date))
#                 x_2 =  dht.unchecking_off()[0]['no_of_checking']
#                 sys.stdin = oldstdin


#             if x_1 != x_2 and x_1 !=0:
#                 assert x_2  == x_1 - 1
#             else:
#                 assert x_2  == x_1 
    

    # [4-3] Check off weekly habit
def test_check_off_weekly():
    '''
    This test functionaly of programm to check off weekly habit
    '''
    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()

    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x in last_place_team:
            input = x.weekly_habit_ID
            session.commit()
            # retrive number of checking for Task ID
            input1 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input1))
            x_1 =  wht.no_of_checking_off()[0]['no_of_checking']
            sys.stdin = oldstdin
            # retreive starting date for task ID
            input2 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input2))
            date_input =  wht.get_start_date()
            sys.stdin = oldstdin
            date2string = str(date_input) # convert date to string type
            date_std = date2string[:10] # date in standard format
            assert date_input == x.start_date
            # checking off the starting date for task ID
            input3 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}/n{}/n{}".format(input3,'y',date_std))
            wht.check_off()
            sys.stdin = oldstdin
            # retrive number of checking for Task ID after checking off
            input4 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input4))
            x_2 =  wht.no_of_checking_off()[0]['no_of_checking']
            sys.stdin = oldstdin


            if x_1 != x_2 and x_1 !=0:
                assert x_2  == x_1 + 1
            else:
                assert x_2  == x_1 
            
    

    # [4-4] Uncheck off weekly habit
def test_uncheck_off_weekly():
    '''
    This test functionaly of programm to uncheck off weekly habit
    '''

    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()

    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x in last_place_team:
            input = x.weekly_habit_ID
            session.commit()
            input1 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input1))
            x_1 =  wht.no_of_checking_off()[0]['no_of_checking']
            sys.stdin = oldstdin
            input2 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input1))
            x_2 =  wht.unchecking_off()[0]['no_of_checking']
            sys.stdin = oldstdin

            if x_1 != x_2 and x_1 !=0:
                assert x_2  == x_1 - 1
            else:
                assert x_2  == x_1 

    

    # [4-5] Rename daily habit
def test_rename_daily():
    '''
    This test functionaly of programm to rename daily habit
    '''

    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_names = ['Task#1','Task#2','Task#3','Task#4']
    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_names):
            input = x.daily_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  dht.set_habit_name()
            assert x_y[0]['name'] == y
    

    # [4-6] Rename weekly habit
def test_rename_weekly():
    '''
    This test functionaly of programm to rename weekly habit
    '''

    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_names = ['Task#1','Task#2','Task#3','Task#4']
    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_names):
            input = x.weekly_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  wht.set_habit_name()
            assert x_y[0]['name'] == y

    

    # [4-7] Change description for daily habit
def test_change_description_daily():
    '''
    This test functionaly of programm to change description daily habit
    '''

    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_names = ['Task#1-Description','Task#2-Description','Task#3-Description','Task#4-Description']
    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_names):
            input = x.daily_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  dht.set_habit_describtion()
            assert x_y[0]['description'] == y
    

    # [4-8] Change desciption for weekly habit
def test_change_description_weekly():
    '''
    This test functionaly of programm to change description weekly habit
    '''

    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_names = ['Task#1-Description','Task#2-Description','Task#3-Description','Task#4-Description']
    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_names):
            input = x.weekly_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  wht.set_habit_describtion()
            assert x_y[0]['description'] == y
    
    # [4-9] Set new start date for daily habit
def test_set_start_date_daily():
    '''
    This test functionaly of programm to set start date daily habit
    '''

    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    from datetime import datetime
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_dates = ['2020-01-01','2020-01-02','2020-01-03','2020-01-04']
    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_dates):
            input = x.daily_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  dht.set_start_date()
            format= "%Y-%m-%d"
            y = datetime.strptime(y,format)
            assert x_y[0]['start_date'] == y
    

    # [4-10] Set new end date for daily habit
def test_set_end_date_daily():
    '''
    This test functionaly of programm to set end date daily habit
    '''

    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    from datetime import datetime
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_dates = ['2025-01-01','2025-01-02','2025-01-03','2025-01-04']
    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_dates):
            input = x.daily_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  dht.set_end_date()
            format= "%Y-%m-%d"
            y = datetime.strptime(y,format)
            assert x_y[0]['end_date'] == y
    
    # [4-11] Set new start date for weekly habit
def test_set_start_date_weekly():
    '''
    This test functionaly of programm to set start date daily habit
    '''

    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    from datetime import datetime
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_dates = ['2019-01-01','2019-01-02','2019-01-03','2019-01-04']
    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_dates):
            input = x.weekly_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  wht.set_start_date()
            format= "%Y-%m-%d"
            y = datetime.strptime(y,format)
            assert x_y[0]['start_date'] == y
    
        
    # [4-12] set new end date for weekly habit
def test_set_end_date_weekly():
    '''
    This test functionaly of programm to set end date daily habit
    '''

    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    from datetime import datetime
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()
    new_dates = ['2025-01-01','2025-01-02','2025-01-03','2025-01-04']
    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x ,y  in zip(last_place_team,new_dates):
            input = x.weekly_habit_ID
            session.commit()
            input1 = input
            input2 = y
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}\n{}".format(input1,input2))
            x_y =  wht.set_end_date()
            format= "%Y-%m-%d"
            y = datetime.strptime(y,format)
            assert x_y[0]['end_date'] == y
    
    # [4-13] back to main menu
def test_main_menu_modify():
    '''
    This test functionaly of CLI in menu of modifiying habit 
    '''
    from main import main
    # input0 = 'N'
    input1 = '4'
    input2 = '13'
    input3 = '6'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n{}\n{}\n".format(input1,input2,input3))
    x = main()
    sys.stdin = oldstdin
    assert x == None
    

# [5] Delete
    # [5-1] Delete daily habit
def test_delete_daily():
    '''
    This test functionaly of programm to delete daily habit
    '''

    from Daily_habit_task import daily_habit_task as dht
    from Habits_List import habit_list as hl
    from db import daily_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()

    with sessionobj as session:
        last_place_team = session.query(daily_habit).order_by(daily_habit.created_date.desc()).limit(4)
        for x in last_place_team:
            input = x.daily_habit_ID
            session.commit()
            input1 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input1))
            dht.delete()
            sys.stdin = oldstdin
            m = hl.get_all_daily_list()
            assert not any(dictionary.get('id') == input1 for dictionary in m)    

    # [5-2] Delete weekly habit
def test_delete_weekly():
    '''
    This test functionaly of programm to delete weekly habit
    '''

    from Weekly_Habit_Task import weekly_habit_task as wht
    from Habits_List import habit_list as hl
    from db import weekly_habit
    engine = create_engine('sqlite:///mydb.sqlite')
    Session = sessionmaker(bind=engine)
    sessionobj = Session()
    base=declarative_base()

    with sessionobj as session:
        last_place_team = session.query(weekly_habit).order_by(weekly_habit.created_date.desc()).limit(4)
        for x in last_place_team:
            input = x.weekly_habit_ID
            session.commit()
            input1 = input
            oldstdin = sys.stdin
            sys.stdin = StringIO("{}".format(input1))
            wht.delete()
            sys.stdin = oldstdin
            m = hl.get_all_weekly_list()
            assert not any(dictionary.get('id') == input1 for dictionary in m)    
    

    # [5-3] back to main menu
def test_main_menu_delete():
    '''
    This test functionaly of CLI in menu of deleting habit 
    '''
    from main import main
    # input0 = 'N'
    input1 = '5'
    input2 = '3'
    input3 = '6'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n{}\n{}\n".format(input1,input2,input3))
    x = main()
    sys.stdin = oldstdin
    assert x == None
    

# [6] Exit
def test_exit():
    '''
    This test functionaly of CLI to exit from program
    '''
    from main import main
    input0 = 'n'
    input1 = '6'
    oldstdin = sys.stdin
    sys.stdin = StringIO("{}\n{}\n".format(input0,input1))
    x = main()
    sys.stdin = oldstdin
    assert x == None

def test_close_connection_db():
    import db
    from sqlalchemy import create_engine
    db.engine = create_engine ('sqlite:///mydb.sqlite')
    assert os.path.isfile("mydb.sqlite")
    session = sessionmaker()()
    session.close()
    assert session.close() == None
#----------------------------------------------------------#
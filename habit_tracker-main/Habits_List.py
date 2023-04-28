'''
File: Habits_List.py
Date: 2023-01-20
Author: Mohammed Wais
Description: 
This file to analyze the daily habits and weekly habits for the user
'''
from sqlalchemy import Column, Integer, String,Date
from sqlalchemy import create_engine
from db import daily_habit,weekly_habit,base
from datetime import datetime , date , timedelta
from sqlalchemy import func, cast
import re
from dateutil import relativedelta
from dateutil import rrule

import os.path
import sys
from io import StringIO

import os, sys


from rich.console import Console
from rich.table import Table
console = Console()

engine = create_engine('sqlite:///mydb.sqlite')
base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
sessionobj = Session()


class Counter:

    '''
    This class to monitor the checking thru a counter string constits of:
    'x' :  checked off
    'o' :  unchecked off
    '''

    # Function to convert list to string
    def listToString(s):
        # initialize an empty string
        str1 = ""
    
        # return string 
        return (str1.join(s))


    # add 'x' to the right of counter string
    def add_x_right(m,diff_dates):
        if len(m) < diff_dates:
            m = m + 'x'
            return m        

    # add 'x' to the left of counter string
    def add_x_left(m,diff_dates):
        if len(m) < diff_dates:
            m = 'x' + m
            return m        

    # remove 'x' from the right of counter string
    def remove_x_right(m):
        if m.endswith('x'):
            m_list = list(m)
            m_list.pop(len(m_list) - 1)
            m_string = Counter.listToString(m_list)
            return m_list

    # remove 'x' from the left of counter string
    def remove_x_left(m):
        if m.startswith('x'):
            m_list = list(m)
            m_list.pop(0)
            m_string = Counter.listToString(m_list)
            return m_list

    # replace 'x' based on specific index inside counter striing
    def replace_x(m,diff_dates,index):
        # check the length of the counter string to make no redudnace
        if index - 1 <= diff_dates:

            new_character = "x"

            listed_string = list(m)
            listed_string[index] = new_character

            m = "".join(listed_string)
            return m

    # count number of 'x'
    def counter_x(m):
        return m.count('x')

    # find the longest number of 'x'
    def longest_streak_x(m):
        # define the longest period user keeps checking off 
        res = max(m.split('o'), key = len)
        return len(res)

    # find the longest number of 'x' before break habit
    def streak_x(m):
        # define the maximum inital checking off
        return m.index('o')
        
    # add 'o' to the right side
    def add_o_right(m,diff_dates):
        if len(m) < diff_dates:
            m = m + 'o'
            return m        

    # add 'o' to the left side
    def add_o_left(m,diff_dates):
        if len(m) < diff_dates:
            m = 'o' + m
            return m        

    # remove 'o' from the right side
    def remove_o_right(m):
        if m.endswith('x'):
            m_list = list(m)
            m_list.pop(len(m_list) - 1)
            m_string = Counter.listToString(m_list)
            return m_list

    # remove 'o' from the left side
    def remove_o_left(m):
        if m.startswith('x'):
            m_list = list(m)
            m_list.pop(0)
            m_string = Counter.listToString(m_list)
            return m_list

    # replace charcater in counter string by 'o' based on index
    def replace_o(m,diff_dates,index):
        if index - 1 <= diff_dates:

            new_character = "o"

            listed_string = list(m)
            listed_string[index] = new_character

            m = "".join(listed_string)
            return m

    # count number of 'o'
    def counter_o(m):
        return m.count('o')



class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class habit_list:
    def clear():
        '''
        This is to clear all database
        '''
        # clear the database
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()
        query = session.query(daily_habit).delete()
        query = session.query(weekly_habit).delete()
        session.commit()
        
        print('all daily habits have been delted succesfuly')
        return None

    def daily_broken_habit():
        '''
        This shows all daily borken habits
        It retrieves data as dictionaries in list.
        '''
        # retrive list of daily boken habits
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()

        # query for daily habits
        query = session.query(daily_habit)
        console.print("[bold magenta]--All daily broken Habits--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Period in Days", min_width=12, justify="right")

        # print list of daily borken habits
        # print(''' List of brken habit:\nName : Discribtion : start date :  end date : no of checking : Diff. btw, dates''')
        m = []
        for x in query :
            # check[1] if end date = start date & eend date =< today date
            if x.end_date == x.start_date and x.end_date <= datetime.today() and (x.end_date -x.start_date).days != 1:
                # print(x.name,':',x.start_date,':',x.end_date,':',x.no_of_checking,':',(x.end_date -x.start_date).days)
                table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date-x.start_date).days) )
                s = {'id':x.daily_habit_ID, 'name':x.name, 'start_date':x.start_date, 'end_date':x.end_date, 'no_of_checking':x.no_of_checking }
                m.append(s)
            # check[2] if end date > start date & end date < today dat
            if x.end_date > x.start_date and x.end_date <= datetime.today() and (x.end_date -x.start_date).days >= x.no_of_checking:
                # print(x.name,':',x.start_date,':',x.end_date,':',x.no_of_checking,':',(datetime.today()-x.start_date).days)
                table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date-x.start_date).days) )
                s = {'id':x.daily_habit_ID, 'name':x.name, 'start_date':x.start_date, 'end_date':x.end_date, 'no_of_checking':x.no_of_checking }
                m.append(s)
            # check[3] end date > start date & end date > today
            if x.end_date > x.start_date and x.end_date > datetime.today() and (datetime.today() -x.start_date).days  >= x.no_of_checking:
                # print(x.name,':',x.start_date,':',x.end_date,':',x.no_of_checking,':',(datetime.today()-x.start_date).days)
                table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date-x.start_date).days) )
                s = {'id':x.daily_habit_ID, 'name':x.name, 'start_date':x.start_date, 'end_date':x.end_date, 'no_of_checking':x.no_of_checking }
                m.append(s)
        # for x in m :
        #     table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((datetime.today()-x.start_date).days) )
        session.commit()
        console.print(table)
        return m


    def daily_streak():
        '''
        This shows all daily streaking habits. 
        The only paramter needed is 'no of days' e.g. 15  for 15 days continous checking off
        It retrieves data as dictionaries in list.
        '''
        # retrive list of daily habits with more than conestiives n days checkofff
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()

        # query for daily habits
        query = session.query(daily_habit)
        console.print("[bold magenta]--All daily broken Habits--[/bold magenta]!")

        # create table to populate by data of tasks 
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Period in Days", min_width=12, justify="right")
        
        # ak user to define streaking period
        n = int(input('Enter streaking period: '))

        # empty list to insert data into 
        m =[]

        # loop populate the "m" list by tasks 
        for x in query :
            # check[1] if end date = start date & end date =< today date
            if x.end_date == x.start_date and x.end_date <= datetime.today() and x.no_of_checking == 1 and n == 1:
                 table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date-x.start_date).days) )
                 s = {'id':x.daily_habit_ID,'name':x.name, 'start_date':x.start_date, 'end_date': x.end_date, 'no_of_checking':x.no_of_checking}
                 m.append(s)
            # check[2] if end date > start date & end date < today date
            if x.end_date > x.start_date and x.end_date <= datetime.today() and ((x.end_date -x.start_date).days + 1 )== x.no_of_checking and x.no_of_checking >= n:
                table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date -x.start_date).days ))
                s = {'id':x.daily_habit_ID,'name':x.name, 'start_date':x.start_date, 'end_date': x.end_date, 'no_of_checking':x.no_of_checking}            # check[3] end date > start date & end date > today
                m.append(s)
            # check[3] if end date > start date & end date > today date    
            if x.end_date > x.start_date and x.end_date > datetime.today() and ((datetime.today() -x.start_date).days + 1) == x.no_of_checking and x.no_of_checking >= n:
                table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date-x.start_date).days ))
                s = {'id':x.daily_habit_ID,'name':x.name, 'start_date':x.start_date, 'end_date': x.end_date, 'no_of_checking':x.no_of_checking}
                m.append(s)

        session.commit()
        console.print(table)
        return m

    def get_all_daily_list():
        '''
        This shows all daily  habits. 
        It retrieves data as dictionaries in list.
        '''
        # retrive list of all daily habits in the database
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()

        # query for daily habits
        query = session.query(daily_habit)
        console.print("[bold magenta]--All daily Habits--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Period in Days", min_width=12, justify="right")

        m = []
        for x in query :
            table.add_row(str(x.daily_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str((x.end_date-x.start_date).days) )
            # print(x.name,':',x.start_date,':',x.end_date,':',x.no_of_checking,':',(datetime.today()-x.start_date).days)
            # add dictionary to list "m" 
            n = {'id': x.daily_habit_ID, 'name':x.name, 'start_date':x.start_date,'end_date':x.end_date,'no_of_checking_of':x.no_of_checking, 'counter':x.counter}
            m.append(n)
        session.commit() 
        console.print(table)
        return m
        

    def get_all_weekly_list():
        '''
        This shows all weekly  habits. 
        It retrieves data as dictionaries in list.
        '''
        # retrive list of all weekly habits in the database
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()

        # query for weekly habits
        query = session.query(weekly_habit)
        console.print("[bold magenta]--All weekly Habits--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Period in Weeks", min_width=12, justify="right")

        m = []
        for x in query :
            table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(round((x.end_date-x.start_date).days/7)) )
            # print(x.weekly_habit_ID ,x.name,':',x.start_date,':',x.end_date,':',x.no_of_checking,':',(datetime.today()-x.start_date).days)
            # add dictionary to list "m" 
            n = {'id': x.weekly_habit_ID, 'name':x.name, 'start_date':x.start_date,'end_date':x.end_date,'no_of_checking_of':x.no_of_checking,'counter':x.counter}
            m.append(n)
        session.commit() 
        console.print(table)
        return m

    def weekly_broken_habit():
        '''
        This shows all broke weekly habits. 
        It retrieves data as dictionaries in list.
        '''
        # retrive list of weekly boken habits
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()


        # query for weekly habits
        query = session.query(weekly_habit)
        console.print("[bold magenta]--All weekly brocken Habits--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Period in Weeks", min_width=12, justify="right")

        # get the diffrenece betweeen dates as weeks
        def weeks_between(start_date, end_date):
            weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
            return weeks.count()

        m =[]

        for x in query :
            
            c_st_w = x.start_date.isocalendar().week # start week
            c_st_y = x.start_date.isocalendar().year # start year
            c_ed_w = x.end_date.isocalendar().week # end week
            c_ed_y = x.end_date.isocalendar().year # end year
            c_cd_w = date.today().isocalendar().week # current week
            c_cd_y = date.today().isocalendar().year # current year
            # convert to weeks realteve to year '0'
            period_st = c_st_y * 52 + c_st_w
            period_ed = c_ed_y * 52 + c_ed_w
            period_cd = c_cd_y * 52 + c_cd_w
            
            # check[1] if end week = start week & end week =< current week & checkin no < (end week -start week )
            if (period_ed -period_st )==0 and (period_ed <= period_cd) and x.no_of_checking ==0:
                table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))
                s = {'id':x.weekly_habit_ID,'name':x.name,'start_date':x.start_date,'end_date':x.end_date,'no_of_checking':x.no_of_checking}
                m.append(s)

            # check[2] if end week > start week & end week <  current week & checkin no < (end week - start week)
            if (period_ed -period_st ) > 0 and (period_ed <= period_cd) and x.no_of_checking < (period_ed - period_st):
                table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))
                s = {'id':x.weekly_habit_ID,'name':x.name,'start_date':x.start_date,'end_date':x.end_date,'no_of_checking':x.no_of_checking}
                m.append(s)

            # check[3] end date > start date & end date >= today & checking < (today - start date)
            if (period_ed -period_st ) > 0 and (period_ed > period_cd) and x.no_of_checking < (period_cd - period_st):
                table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))
                s = {'id':x.weekly_habit_ID,'name':x.name,'start_date':x.start_date,'end_date':x.end_date,'no_of_checking':x.no_of_checking}
                m.append(s)
        
        session.commit() 
        console.print(table)
        return m

    def weekly_streak():
        '''
        This shows all weekly streaking habits. 
        The only paramter needed is 'no of weeks' e.g. 15  for 15 weeks continous checking off
        It retrieves data as dictionaries in list.
        '''
        # retrive list of weekly habits with more than conestiives n weeks checkofff
        engine = create_engine('sqlite:///mydb.sqlite')
        base.metadata.create_all(engine)
        session = Session()

        # query for daily habits
        query = session.query(weekly_habit)
        console.print("[bold magenta]--All weekly streak Habits--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Period in Weeks", min_width=12, justify="right")
        
        n = int(input('Enter striking period: '))
        m = []
        for x in query :
            c_st_w = x.start_date.isocalendar().week # start week
            c_st_y = x.start_date.isocalendar().year # start year
            c_ed_w = x.end_date.isocalendar().week # end week
            c_ed_y = x.end_date.isocalendar().year # end year
            c_cd_w = date.today().isocalendar().week # current week
            c_cd_y = date.today().isocalendar().year # current year
            # convert to weeks relative to year '0'
            period_st = c_st_y * 52 + c_st_w
            period_ed = c_ed_y * 52 + c_ed_w
            period_cd = c_cd_y * 52 + c_cd_w
            # print(x. weekly_habit_ID,':',period_st,':',period_ed,':',period_cd)            
            
            # check[1] if end week = start week & no_of_checking = 1 & n = 1
            if (period_ed == period_st ) and (x.no_of_checking == 1) and (n ==1):
                table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))    
                s = {'id':x.weekly_habit_ID,'name':x.name,'start_date':x.start_date,'end_date':x.end_date,'no_of_checking':x.no_of_checking}
                m.append(s)
                
            # check[2] if  end week < current week & no_of_checking = (end week - start week) & no_of_checking >= n 
            if (period_ed != period_st ) and (period_ed > period_st) and (x.no_of_checking == period_ed - period_st + 1) and  x.no_of_checking >= n:
                table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))    
                s = {'id':x.weekly_habit_ID,'name':x.name,'start_date':x.start_date,'end_date':x.end_date,'no_of_checking':x.no_of_checking}
                m.append(s)
            
            # check[3] if end week > current week  & no_of_checking = (current week - start week) & no_of_checking >= n 
            if (period_ed != period_st ) and (period_ed >period_cd ) and (x.no_of_checking == period_cd -period_st + 1) and (x.no_of_checking >= n):
                table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))    
                s = {'id':x.weekly_habit_ID,'name':x.name,'start_date':x.start_date,'end_date':x.end_date,'no_of_checking':x.no_of_checking}
                m.append(s)
               
            # table.add_row(str(x.weekly_habit_ID) , str(x.name), str(x.start_date),str(x.end_date),str(x.no_of_checking),str(period_ed -period_st))    
        

        session.commit() 
        console.print(table)
        return m


    def all_currently_tracked_habits():
        '''
        This returns all habit tasks at database
        '''
        # import sys, os
        # # Disable print
        # def blockPrint():
        #     sys.stdout = open(os.devnull, 'w')

        # # Restore print
        # def enablePrint():
        #     sys.stdout = sys.__stdout__

        with HiddenPrints():
            n = habit_list.get_all_daily_list()
            m = habit_list.get_all_weekly_list()


        console.print("[bold magenta]--All Tacked Habits--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Type", min_width=12, justify="right")

        li = []

        for x in n:
            table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')
            s = {'id': x['id'], 'name': x['name'], 'start_date': x['start_date'], 'end_date':x['end_date'] , 'no_of_checking_of': x['no_of_checking_of'] , 'Type':'Daily'  }
            li.append(s)
     
        for x in m:
            table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')
            s = {'id': x['id'], 'name': x['name'], 'start_date': x['start_date'], 'end_date':x['end_date'] , 'no_of_checking_of': x['no_of_checking_of'] , 'Type':'Weekly'  }
            li.append(s)

        console.print(table)
        return li

    def all_habits_with_the_same_periodicity():
        '''
        This return all habit tasks within specific period e.g. between 2020-01-01 and 2020-06-01
        '''
        with HiddenPrints():
                    n = habit_list.get_all_daily_list()
                    m = habit_list.get_all_weekly_list()
        while True:
            try: 
                format= "%Y-%m-%d"
                
                D_1 = datetime.strptime(input('Enter start date in format YYYY-MM-DD: '),format)
                D_2 = datetime.strptime(input('Enter End date in format YYYY-MM-DD: '),format)

                if D_1 > D_2: raise ValueError

                console.print("[bold magenta]--All Habits with Periodicity--[/bold magenta]!")

                table = Table(show_header=True, header_style="bold blue")
                table.add_column("ID", style="dim", width=6)
                table.add_column("Name", min_width=20)
                table.add_column("Start Date", min_width=12, justify="right")
                table.add_column("End Date", min_width=12, justify="right")
                table.add_column("No of Checking", min_width=12, justify="right")
                table.add_column("Type", min_width=12, justify="right")

                li = []

                # tasks with same periodicity (daily tasks)
                for x in n:
                    if x['start_date'] >= D_1 and x['end_date'] <= D_2:
                        table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')
                        s = {'id': x['id'], 'name': x['name'], 'start_date': x['start_date'], 'end_date':x['end_date'] , 'no_of_checking_of': x['no_of_checking_of'] , 'Type':'Daily'  }
                        li.append(s)

                 # tasks with same periodicity (weekly tasks)           
                for x in m:
                    if x['start_date'] >= D_1 and x['end_date'] <= D_2:
                        table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')
                        s = {'id': x['id'], 'name': x['name'], 'start_date': x['start_date'], 'end_date':x['end_date'] , 'no_of_checking_of': x['no_of_checking_of'] , 'Type':'Weekly'  }
                        li.append(s)

                console.print(table)

                
                return li
                break
      
            except ValueError: 
                print('Please make sure end date is nor earlier than start date! ')                   
                

        

        

    def  longest_run_streak_of_all_defined_habits():
        '''
        This returns three info:
        [1] Longest streak of all daily habits
        [2] Longest streak of all weekly habits
        [3] Longest streak overall and it is type
        '''
        # with HiddenPrints():
        
        #     # system input to function call
        #     input_1 = 1
        #     oldstdin = sys.stdin
        #     sys.stdin = StringIO("{}\n".format(input_1))
        #     m = habit_list.daily_streak()
        #     sys.stdin = oldstdin
        #     # system input to function call
        #     input_2 = 1
        #     oldstdin = sys.stdin
        #     sys.stdin = StringIO("{}\n".format(input_2))
        #     n = habit_list.weekly_streak()
        #     sys.stdin = oldstdin
        #     m_n = m + n

        # call all daily tasks from database and assign it to 'm'
        m = habit_list.get_all_daily_list()
        # call all weekly tasks from database and assign it to 'n'
        n = habit_list.get_all_weekly_list()
        # empty list to insert all daily tasks match the longest streak
        li_daily =[]
        # empty list to insert all weekly tasks math the longest streak
        li_weekly = []


        
        #---------------------------------------
        # Find mxiamum check off for daily tasks
        #----------------------------------------

        console.print("[bold magenta]--Maximum Check off for Daily Tasks--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Type", min_width=12, justify="right")
        
        # if 'm' is not empty i.e. there is a record
        if m: 
            #find maximum streak among daily tasks
            maxDailyHabit = max(m, key=lambda x:Counter.streak_x(x['counter']))

            # add all daily tasks match have the same maximum streak to the list 'li_daily'
            for x in m:
                if Counter.streak_x(maxDailyHabit['counter']) == Counter.streak_x(x['counter']):
                    li_daily.append(x)
            
            # add all daily tasks added in the pervious step to the table to be print
            for x in li_daily:
                table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')

            # print the table
            console.print(table)    
        
        # if there was no any record in the database
        if not m:
            console.print('No records for daily tasks!')


            for x in li_daily:
                table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')


            
        # ---------------------------------------
        # Find mxiamum check off for weekly tasks
        # ---------------------------------------
        

        console.print("[bold magenta]--Maximum Check off for Weekly Tasks--[/bold magenta]!")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", min_width=20)
        table.add_column("Start Date", min_width=12, justify="right")
        table.add_column("End Date", min_width=12, justify="right")
        table.add_column("No of Checking", min_width=12, justify="right")
        table.add_column("Type", min_width=12, justify="right")
        
        # if 'n' is not empty i.e. there is a record
        if n: 
            #find maximum streak among weekly tasks
            maxWeeklyHabit = max(n, key=lambda x:Counter.streak_x(x['counter']))

            # add all daily tasks match have the same maximum streak to the list 'li_daily'
            for x in n:
                if Counter.streak_x(maxWeeklyHabit['counter']) == Counter.streak_x(x['counter']):
                    li_weekly.append(x)
            
            # add all daily tasks added in the pervious step to the table to be print
            for x in li_weekly:
                table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')

            # print the table
            console.print(table)    
        
        # if there was no any record in the database
        if not n:
            console.print('No records for daily tasks!')


            for x in li_weekly:
                table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')
        

        


        #------------------------------------------------
        # Compare between them to find the maximum streak 
        #------------------------------------------------
        if n and m:

            max_daily  = Counter.streak_x(maxDailyHabit['counter']) 
            max_weekly = Counter.streak_x(maxWeeklyHabit['counter'])

            if max_daily > max_weekly:
                max_all = li_daily

                console.print("[bold magenta]--Maximum Check off of all Tasks--[/bold magenta]!")

                table = Table(show_header=True, header_style="bold blue")
                table.add_column("ID", style="dim", width=6)
                table.add_column("Name", min_width=20)
                table.add_column("Start Date", min_width=12, justify="right")
                table.add_column("End Date", min_width=12, justify="right")
                table.add_column("No of Checking", min_width=12, justify="right")
                table.add_column("Type", min_width=12, justify="right")

                for x in li_daily:
                    table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')

                console.print(table)                


                
                return li_daily , li_weekly , max_all
                

            if max_daily < max_weekly:
                max_all = li_weekly

                console.print("[bold magenta]--Maximum Check off of all Tasks--[/bold magenta]!")

                table = Table(show_header=True, header_style="bold blue")
                table.add_column("ID", style="dim", width=6)
                table.add_column("Name", min_width=20)
                table.add_column("Start Date", min_width=12, justify="right")
                table.add_column("End Date", min_width=12, justify="right")
                table.add_column("No of Checking", min_width=12, justify="right")
                table.add_column("Type", min_width=12, justify="right")

                for x in li_weekly:
                    table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')

                console.print(table)

                
                
                return li_daily , li_weekly , max_all
                

            if max_daily == max_weekly:
                max_all = li_daily + li_weekly


                console.print("[bold magenta]--Maximum Check off of all Tasks--[/bold magenta]!")

                table = Table(show_header=True, header_style="bold blue")
                table.add_column("ID", style="dim", width=6)
                table.add_column("Name", min_width=20)
                table.add_column("Start Date", min_width=12, justify="right")
                table.add_column("End Date", min_width=12, justify="right")
                table.add_column("No of Checking", min_width=12, justify="right")
                table.add_column("Type", min_width=12, justify="right")

                for x in li_daily:
                    table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')


                for x in li_weekly:
                    table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')

                console.print(table)   

                
                return li_daily , li_weekly , max_all

        elif len(n) == 0 and m:
            max_all = li_daily

            console.print("[bold magenta]--Maximum Check off of all Tasks--[/bold magenta]!")

            table = Table(show_header=True, header_style="bold blue")
            table.add_column("ID", style="dim", width=6)
            table.add_column("Name", min_width=20)
            table.add_column("Start Date", min_width=12, justify="right")
            table.add_column("End Date", min_width=12, justify="right")
            table.add_column("No of Checking", min_width=12, justify="right")
            table.add_column("Type", min_width=12, justify="right")

            for x in li_daily:
                table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Daily')

            console.print(table)   

            
            return li_daily , li_weekly , max_weekly

        elif len(m) == 0 and n:
            max_all = li_weekly

            console.print("[bold magenta]--Maximum Check off of all Tasks--[/bold magenta]!")

            table = Table(show_header=True, header_style="bold blue")
            table.add_column("ID", style="dim", width=6)
            table.add_column("Name", min_width=20)
            table.add_column("Start Date", min_width=12, justify="right")
            table.add_column("End Date", min_width=12, justify="right")
            table.add_column("No of Checking", min_width=12, justify="right")
            table.add_column("Type", min_width=12, justify="right")

            for x in li_weekly:
                table.add_row(str(x['id']),x['name'],str(x['start_date']),str(x['end_date']),str(x['no_of_checking_of']),'Weekly')

            console.print(table)
                

            
            return li_daily , li_weekly , max_weekly
        
        else: 
            return None
            
         
            

    def longest_run_streak_for_a_given_habit():
        '''
        This returns long streak for a specific habit task, e.g. task ID #1 got 5 days streak
        This function return number of streak only if the task has not broken, if it is borken
        then the return shall be None. However you can see all number of check off from view habit
        function.
        '''
        #  a list to contain the the task details
        li = []
        while True:
            try:
                # user should enter type of task and  its ID number
                answer_1 = input('Enter type of D (Daily task) or W(Weekly task)or E to Exit:')
                if answer_1 == 'E' or answer_1 == 'e': break
                answer_2 = int(input('ID number:'))
                # trigger to stop the while loop
                trigger  = False

                # if the task is a daily task 
                if answer_1 == 'D' or 'd':
                    with HiddenPrints():
                        # call all daily tasks in database 
                        m_0 = habit_list.get_all_daily_list()
                    # empty list to contain details of the daily task
                    m_1 = []
                    
                    # loop to to find the user defined daily task and insert it to "m_1"
                    for x in m_0: 
                        if answer_2 == x['id']:
                            m_1.append(x)
                            
                    # if there was no daily task with the same ID defined by user, a message is returned
                    if not m_1:
                        print('No Task with with same ID found!')
                        return None
                        break 

                    # return value of the longest streak for defined task 
                    if m_1:
                        print( 'longest streak is: {}'.format(Counter.longest_streak_x(m_1[0]['counter']) ))
                        return Counter.longest_streak_x(m_1[0]['counter'])
                        break

                    
                # if the task is a weekly task          
                if answer_1 == 'W' or 'w':
                    with HiddenPrints():
                        # call all weekly tasks in database 
                        m_0 = habit_list.get_all_weekly_list()
                    # empty list to contain details of the weekly task
                    m_1 = []

                    # loop to to find the user defined weekly task and insert it to "m_1"
                    for x in m_0: 
                        if int(answer_2) == x['id']:
                            m_1.append(x)

                    # period in weeks format                 
                    period = (m_1[0]['end_date'] - m_1[0]['start_date']).days / 7
                    period_modified = round(period)
                    if period_modified - period < 0:
                        period_modified +1

                    # if there was no weekly task with the same ID defined by user, a message is returned
                    if not m_1:
                        print('No Task with with same ID found!')
                        return None
                        break 

                    # return value of the longest streak for defined task 
                    if m_1:
                        print( 'longest streak is: {}'.format(Counter.longest_streak_x(m_1[0]['counter']) ))
                        return Counter.longest_streak_x(m_1[0]['counter'])
                        break

                    # for n in list(range(period_modified,-1,-1)):
                    #     with HiddenPrints():
                    #         oldstdin = sys.stdin
                    #         sys.stdin = StringIO("{}\n".format(n))
                    #         m_2 = habit_list.weekly_streak()
                    #         sys.stdin = oldstdin
                        
                    #     for x in m_2:
                    #         if x['id'] == m_1[0]['id']:
                    #             li.append(x)
                    #             print('we found it!')
                    #             print('Longest run streak for ID # {} is {}'.format(m_1[0]['id'],n))
                    #             trigger = True
                    #             break
                    #         else:
                    #             print('No task with same ID found!')
                    #             return None
                    #     if trigger:
                    #         break

                # else: raise ValueError 
            except ValueError:
                print('Please enter "D" or "W" or "E" to Exit! ')



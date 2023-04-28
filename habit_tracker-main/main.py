'''
File: main.py
Date: 2023-01-20
Author: Mohammed Wais
Descitpion: 
Habit tracker is a program to track user's habits at daily or weekly basis. It provides
many options such as: creating habits, modify habits, view all habits, and analyzing.
The user can commincate with the programm thru a CLI. 
'''
from  Daily_habit_task import daily_habit_task as dht
from  Weekly_Habit_Task import weekly_habit_task as wht
from  Habits_List import habit_list as hl

import os.path
import sys
from io import StringIO


# controling factor for inserting sample data
def dummy_data_factor_control():
    '''
    If user choose 'Y' or 'y' the sample dataset shall be loaded
    if uses choose 'N' or 'n' the sample dataset shall not be loaded
    it return the value of 'dummy_data_factor' as 1 or 0
    '''
    dummy_data_factor = 1
    if dummy_data_factor:
        
        while True:
            try:
                question = input('Do you like to load sample data? Y/N: ')

            except ValueError: 
                print('--Please enter valid answer--')
                continue
            if question == 'Y' or question =='y':
                dummy_data_factor = 1
                dummy_data(dummy_data_factor)
                break
            if question == 'N' or question =='n':
                dummy_data_factor = 0
                break
            else:
                print("Please enter only 'Y' or 'N': ")
    return dummy_data_factor

    



#----------------------------------------------#
# creating dummy data for usrer
#----------------------------------------------#

def dummy_create_daily_habit_task():
    '''
    This functtion is to upload the daily sample dataset to the daily tasks table in database 
    '''
    from Daily_habit_task import daily_habit_task as dht
    import datetime
    
    m = [{'name':'sample new task-1' ,'description':'sample Task1','start_date':'2021-01-01','end_date':'2022-01-01'},
         {'name':'sample new task-2' ,'description':'sample Task2','start_date':'2022-02-02','end_date':'2023-02-02'},
         {'name':'sample new task-3' ,'description':'sample Task3','start_date':'2022-03-03','end_date':'2023-03-03'},
         {'name':'sample new task-4' ,'description':'sample  Task4','start_date':'2021-04-04','end_date':'2021-04-04'},
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

def dummy_create_weekly_habit_task():
    '''
    This functtion is to upload the weekly sample dataset to the weekly tasks table in database 
    '''
    from Weekly_Habit_Task import weekly_habit_task as wht
    import datetime

    m = [{'name':'sample Task 1' ,'description':'sample -Task1','start_date':'2022-02-01','end_date':'2022-09-01'},
         {'name':'sample Task 2' ,'description':'sample-Task2','start_date':'2022-03-04','end_date':'2023-03-05'},
         {'name':'sample Task 3' ,'description':'sample-Task3','start_date':'2022-06-02','end_date':'2023-03-03'},
         {'name':'sample Task 4' ,'description':'sample-Task4','start_date':'2021-01-02','end_date':'2021-01-07'},
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


def dummy_data(dummy_data_factor):
    '''
    This function to activate the 'dummy_create_weekly_habit_task()' if 'dummy_data_factor' = 1
    '''
    import db
    from sqlalchemy import create_engine
    db.engine = create_engine ('sqlite:///mydb.sqlite')
    assert os.path.isfile("mydb.sqlite")
    # controlling element 
    if dummy_data_factor:
        if db.engine.table_names()[0] == 'Daily Habit': dummy_create_daily_habit_task()
        if db.engine.table_names()[1] == 'Weekly Habit': dummy_create_weekly_habit_task()
    
    dummy_data_factor = False
    return dummy_data_factor


#----------------------------------------------#
#  Main programm CLI
#----------------------------------------------#


def main():
    '''
    This is CLI for control the follow of programm 
    '''
    while True:
        try:
            # User has to choose an option
            print('-'*50)
            option_general =int(input('''Enter option for yourself:
            [1] Create habit task
            [2] View habit
            [3] Analyze habit
            [4] Modify habit
            [5] Delete
            [6] Exit
            [7] Clear database
            Your choice is? '''))
        
        except ValueError:
            print("Please enter a valid integer 1-6")
            continue   

        if option_general ==1:
            # create habit task
            while True:
                try:
                    option_1 = int(input('''Enter option number:
                    [1] Create a daily habit task
                    [2] Create a weekly habit tasks
                    [3] Back to main menu
                    Your choice is? '''))

                except ValueError:
                    print("Please enter a valid integer 1-3")
                    continue

                if option_1 == 1:
                    # view all daily habit tasks
                    dht.add()
                    print('-'*100)
                    break

                if option_1 == 2:
                    # view all weekly habit tasks
                    wht.add()
                    print('-'*100)
                    break

                if option_1 == 3:
                    # exit the loop
                    print('-'*10)
                    break

                else:
                    # retrun to enter a correct choice
                    print('The integer must be in the range 1-3')

        if option_general ==2:
            # view habit

            while True:
                try:
                    option_2 = int(input('''Enter option number:
                    [1] View daily habit task
                    [2] View weekly habit task
                    [3] View all habit tasks
                    [4] View all habit tasks with same periodicity 
                    [5] Back to main menu
                    Your choice is? '''))

                except ValueError:
                    print("Please enter a valid integer 1-3")
                    continue

                if option_2 == 1:
                    # creat daily habit
                    hl.get_all_daily_list()
                    
                if option_2 == 2:
                    # creat weekly habit
                    hl.get_all_weekly_list()
                
                if option_2 == 3:
                    # creat weekly habit
                    hl.all_currently_tracked_habits()

                if option_2 == 4:
                    # creat weekly habit
                    hl.all_habits_with_the_same_periodicity()


                if option_2 == 5:
                    # Exit the loop
                    break
                    print('You backed to the menu!')
                    
                else:
                    # retrun to enter a correct choice
                    print('The integer must be in the range 1-4')


        if option_general ==3:
            # analyze habit
            while True:
                try:
                    option_3 = int(input('''Enter option number:
                    [1] Daily streak habits
                    [2] weekly streak habits
                    [3] Daily broken habits
                    [4] Weekly broken habits
                    [5] Longest run streak of all defined habit
                    [6] Longest run streak for a given_habit
                    [7] back to main menu
                    Your choice is? '''))

                except ValueError:
                    print("Please enter a valid integer 1-5")
                    continue

                if option_3 == 1:
                    # retrieve all daily streak habits based on specific number
                    hl.daily_streak()
                    
                if option_3 == 2:
                    # retrieve all weekly streak habits based on specific number
                    hl.weekly_streak()
                
                if option_3 == 3:
                    # retrieve all daily broken habits
                    hl.daily_broken_habit()
                
                if option_3 == 4:
                    # retrieve all weekly broken habits
                    hl.weekly_broken_habit()

                if option_3 == 5:
                    # retrieve all weekly broken habits
                    hl.longest_run_streak_of_all_defined_habits()
                    
                if option_3 == 6:
                    # retrieve all weekly broken habits
                    hl.longest_run_streak_for_a_given_habit()

                if option_3 == 7:
                    # Exit the loop
                    break
                    print('You backed to the menu!')
                    
                else:
                    # retrun to enter a correct choice
                    print('The integer must be in the range 1-5')

        if option_general ==4:
            # modify habit
            while True:
                try:
                    option_4 = int(input('''Enter option number:
                    [1] Check off daily habit
                    [2] Uncheck off daily habit
                    [3] Check off weekly habit
                    [4] Uncheck off weekly habit
                    [5] Rename daily habit
                    [6] Rename weekly habit
                    [7] Change description for daily habit
                    [8] Change desciption for weekly habit
                    [9] Set new start date for daily habit
                    [10] Set new end date for daily habit
                    [11] Set new start date for weekly habit
                    [12] Set new end date for weekly habit
                    [13] back to main menu
                    Your choice is? '''))

                except ValueError:
                    print("Please enter a valid integer 1-5")
                    continue

                if option_4 == 1:
                    # Check off daily habit
                    dht.check_off()
                    
                if option_4 == 2:
                    # Uncheck off daily habit
                    dht.unchecking_off()
                
                if option_4 == 3:
                    # Check off weekly habit
                    wht.check_off()
                
                if option_4 == 4:
                    # Uncheck off weekly habit
                    wht.unchecking_off()
                
                if option_4 == 5:
                    # Rename daily habit
                    dht.set_habit_name()
                    
                
                if option_4 == 6:
                    # Rename weekly habit
                    wht.set_habit_name()
                
                if option_4 == 7:
                    # Change description for daily habit
                    dht.set_habit_describtion()
                
                if option_4 == 8:
                    # Change desciption for weekly habit
                    wht.set_habit_describtion()

                if option_4 == 9:
                    # Set new start date for daily habit
                    dht.set_start_date()
                    

                if option_4 == 10:
                    # Set new end date for daily habit
                    dht.set_end_date()
                    

                if option_4 == 11:
                    # Set new start date for weekly habit
                    wht.set_start_date()
                    

                if option_4 == 12:
                    # Set new end date for weekly habit
                    wht.set_end_date()
                    
                    
                if option_4 == 13:
                    # Exit the loop
                    break
                    print('You backed to the menu!')
                    
                else:
                    # retrun to enter a correct choice
                    print('The integer must be in the range 1-13')

        if option_general ==5:
            # delete habit
            while True:
                try:
                    option_4 = int(input('''Enter option number:
                    [1] Delete daily habit
                    [2] Delete weekly habit
                    [3] back to main menu
                    Your choice is? '''))

                except ValueError:
                    print("Please enter a valid integer 1-3")
                    continue

                if option_4 == 1:
                    # Delete daily habit
                    dht.delete()
                    
                if option_4 == 2:
                    # Delete weekly habit
                    wht.delete()
                    
                if option_4 == 3:
                    # Exit the loop
                    break
                    print('You backed to the menu!')
                    
                else:
                    # retrun to enter a correct choice
                    print('The integer must be in the range 1-3')
            

        if option_general ==6:
            # exit
            break

        if option_general ==7:
            # clear database from all habits
            lik = True
            while lik:
                try:
                    question = input('Are you sure you want to clear all tasks (Y/N?')
                    if question == 'Y' or  question == 'y':
                        hl.clear()
                        lik = False
                    elif question == 'N' or  question == 'n':
                        lik = False
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter 'Y' for Yes or 'N' for No!")

           


if __name__ == "__main__":
    dummy_data_factor_control()
    main()




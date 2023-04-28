# **Habit Tacker Project IUBH-DLBDSOOFPP01**

Habit tracker to track daily and weekly basis habits. User can creat habit, check off, uncheck off it, modify it, or delete it.

 ##  **[1] Description:**

This code has been written udner requirements of [IU International University of Applied Sciences](https://www.iu.org/) study module's project. The habit tracker provids ability fr user to track thier habits in daily or weekly periods. The whole programm has been writen in Python and the database used for the programm is sqlite.
 
 ##   **[2] How to Install and Run the Project:**
 descripw to insall and run the project
 To run the code first you need to have a [**Python**](https://www.python.org/downloads/) installed in your machine. 

 You need also to be make sure that [**PIP**](https://pypi.org/project/pip/) is isntalled in your machine. 
 
To install the project you need to download the project folder from Github and unzip in directory of your choice then create a [**virtual environment**](https://docs.python.org/3/library/venv.html) and install the requirements using the **rquirement.txt** file: 

```shell
pip install -r requirments.txt 
```
To run the project change your terminal directory to the project folder location then type:

[Windows Users](https://realpython.com/run-python-scripts/#:~:text=To%20run%20Python%20scripts%20with,see%20the%20phrase%20Hello%20World!)
```shell
python main.py
```
[Mac Users](https://macosx-faq.com/how-to-run-python-script/)
```shell
python3 main.py
```
 ##  **[3] How to Use the Project:**
 The project use CLI to coomincate with users, it is easy to use. After running code the following menu shall appear:
 ```shell
 Enter option for yourself:
            [1] Create habit task
            [2] View habit
            [3] Analyze habit
            [4] Modify habit
            [5] Delete
            [6] Exit
            [7] Clear all habits
            Your choice is?
 ```
 You need to enter a number and press **Enter**, another menu shall appear. You need to follow the same procedure. 

 To enter a **Date**, you have to follow specific format of: YYYY-MM-DD.
## [3-1] Create habit task
This option allows you to creat two kinds of habits: Daily or Weekly:
Daily Habit Task: a task that should be done on daily basis.
Weekly Habit Task: a task that should be done once within a week and weekly basis.

```shell
[1] Create a daily habit task
[2] Create a weekly habit tasks
[3] Back to main menu
Your choice is?
```
You need to enter: Task name, Task description, start date, and end date.

## [3-2] View habit
This option allows you to see all daily habit tasks or all weekly habit tasks. You need use this option to know find a **Task ID**.

```shell
[1] View daily habit task
[2] View weekly habit task
[3] Back to main menu
Your choice is?
```

## [3-3] Analyze habit
This option allows you to get know which habits you have brocken or which you  got a streaking on them based on a **specific period** of your choice. This specific period for daily habits is represtedn by days, and for weekly habits is represented by weeks. 

```shell
[1] Daily streak habits
[2] weekly streak habits
[3] Daily broken habits
[4] Weekly broken habits
[5] back to main menu
Your choice is?
```

## [3-4] Modify habit
This option allows you to check off, uncheck off, rename, and change description for any created task. You need to know and enter the **Task ID**. 

```shell
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
Your choice is?
```

## [3-5] Delete
This option allows you to delete any habit has been created. You need to know and enter the **Task ID**.
```shell
[1] Delete daily habit 
[2] Delete weekly habit
[3] back to main menu  
Your choice is?  
```

## [3-6] Exit
This option allows you to exist from the program. 

## [3-7] Clear databsae
This option allows you to clear all tasks from the database. 

 ## [4] **Testing the project**:
To test the program funuctionality you need to install [**pytest**](https://pypi.org/project/pytest/):
```shell
pip install pytest
````
Then run the following code:
```shell
pytest test_project.py
````
 
 ##  **[5] Contributing:**
 Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
 ## **[6] License:**
[**MIT**](https://choosealicense.com/licenses/mit/)

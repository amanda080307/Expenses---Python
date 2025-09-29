## Expenses tracker
- An expenses tracker made with python which allows useres to store their expenses alongside other additional information

## Features
- User can add the amount spent, category, date, optional description, wether the expense is recurring or not, and add a limit per month, a feature which is optional 
- User can see all the expenses
- To get more data user can see the average of a month or even a day
- User can filter expenses based on the three main features: date, amount and category
- For more statistics, user can see the largest or the smallest expense
- This program makes things more visual by allowing the user to see a graph that shows the expenses throughout a specific month of  their choice
- User can set a limit for a specific month and can be notified when the limit is near or exceeded
- If the expense is recurring the program automatically pastes it when the next month comes
- Data is saved on a CSV file (a sample CSV file is attached to the project)
- The categories of the data are saved in a JSON file 

## Requirements
- python 3
- no external libraries (this program already uses re, datetime, json, csv, collections, matplotlib)

## How to run
- Download or clone the respiratory
- Make sure you use python ver 3
- Run: bash python expenses.py

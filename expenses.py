import re
from datetime import datetime
import csv
from collections import defaultdict
import json
from matplotlib import pyplot as plt

expenses = []
try:
    with open('/workspaces/categories.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {'categories': []}

def load_expenses():
    try:
        with open('/workspaces/expenses.csv') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for line in csv_reader:
                expense ={
                    'amount': float(line['amount']),
                    'category': line['category'],
                    'date': line['date'],
                    'description': line['description'] or None,
                    'recurring': line.get('recurring', 'n'),
                    'last_added_month': line.get('last_added_month') or None,
                    'limit': line.get('limit') or None
                }
                expenses.append(expense)
    except FileNotFoundError:
        pass

def main():
    print('~~~~~~~~~~~Welcome to Expense Tracker~~~~~~~~~~')
    print('In this app you can track your monthly expenses')
    print('''What do you wish to do? (choose a number)
1. Add expenses
2. View expenses
3. Calculate monthly average
4. Calculate daily average
5. Filter expenses based on a feature
6. Get the largest or smallest expense
7. Graphs for month
8. Add limit''')
    load_expenses()
    recurring(expenses)
    while True:
        i = input('Write only the number of the command: ').strip()
    
        if i == '1':
            get_data()
        elif i == '2':
            view_expenses(expenses)
        elif i == '3':
            print(monthly_average(expenses))
        elif i == '4':
            print(daily_average(expenses))
        elif i == '5':
            filter()
        elif i == '6':
            extremes(expenses)
        elif i == '7':
            visual_representation(expenses)
        elif i == '8':
            set_limit(expenses)
        else:
            print('Invalid choice.')

        cont = input('Go again? (y/n): ').lower().strip()
        if cont == 'n':
            break

def get_data():
    while True:
        try:
            amount = float(input('What was the amount spent? '))
            break
        except ValueError:
            print('Please use only numbers.')

    while True:  
        print('Choose a category.')
        print(' - '.join(data['categories']))
        category = input('Category: ').strip().lower()

        if not category:
            print('Please enter the required category')
        else:
            if category not in data['categories']:
                data['categories'].append(category)
                with open('/workspaces/categories.json', 'w') as file:
                    json.dump(data, file, indent=4)
            break
    
    while True:
        datein = input('Enter the date(DD-MM-YYYY): ').strip()
        if not re.match(r'\d{2}-\d{2}-\d{4}', datein):
            print('Invalid date format.')
        else:
            date = datetime.strptime(datein, '%d-%m-%Y')
            break
    
    description = input('Anything to add(optional): ') or None
  
    while True:
        recurring = input('Is this expense recurring? (y/n): ').lower().strip()
        if recurring not in['y', 'n']:
            print('Invalid input.')
        else:
            break

    expense = {
        'amount': amount,
        'category': category,
        'date': date.strftime('%Y-%m-%d'),
        'description': description if description else None,
        'recurring': recurring,
        'last_added_month': None,
        'limit': None
    }
    expenses.append(expense)

    with open('/workspaces/expenses.csv', 'a', newline='') as file:
        fieldnames = ['amount', 'category', 'date', 'description','recurring','last_added_month', 'limit']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        if file.tell() == 0:
            csv_writer.writeheader()
    
        csv_writer.writerow(expense)

def view_expenses(expenses):
    if not expenses:
        print('No expenses yet.')
    for i,expense in enumerate(expenses, start = 1):
        print(f"{i}. Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date']}, Description: {expense['description']}, Limit: {expense['limit']}")

def monthly_average(expenses):
    monthly_totals = defaultdict(float)
    monthly_count = defaultdict(int)
    for expense in expenses:
        month = datetime.strptime(expense['date'],'%Y-%m-%d').strftime('%Y-%m')
        monthly_totals[month] +=  expense['amount']
        monthly_count[month] += 1
        
    avr = {month: monthly_totals[month]/ monthly_count[month] for month in monthly_totals}
    return avr

def daily_average(expenses):
    daily_totals = defaultdict(float)
    daily_count = defaultdict(int)
    dt = input('Date(DD-MM-YYYY): ').strip()
    if not re.match(r'\d{2}-\d{2}-\d{4}', dt):
        print('Invalid date format.')
        return
    else:
        date = datetime.strptime(dt, '%d-%m-%Y')
        match = date.strftime('%Y-%m-%d')
    for expense in expenses:    
        if expense['date'] == match:
            daily_totals[match] += expense['amount']
            daily_count[match] += 1
    if match in daily_totals:
        avr =  daily_totals[match]/ daily_count[match]
        return f'Average: {avr:.2f} for {match}'
    else:
        return 'No matches found'

def filter():
    type0 = input('Which expenses do you wish to see: (amount/category/date) ').lower().strip()

    found = False

    if type0 not in ['amount', 'category', 'date']:
        print('Please enter one of the options.')
    elif type0 == 'amount':
        try:
            am = float(input('What amount: ').strip())
        except ValueError:
            print('Please enter a valid number.')
            return 
        for expense in expenses:
            if expense['amount'] == am:
                print(f"Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date']}, Description: {expense['description']}")
                found = True
    elif type0 == 'category':
        cat = input('Which category: ').lower().strip()
        for expense in expenses:
            if expense['category'] == cat:
                print(f"Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date']}, Description: {expense['description']}")
                found = True
    else:
        dt = input('Date(DD-MM-YYYY): ').strip() 
        if not re.match(r'\d{2}-\d{2}-\d{4}', dt):
            print('Invalid date format.')
        else:
            date = datetime.strptime(dt, '%d-%m-%Y')
            match = date.strftime('%Y-%m-%d')
            for expense in expenses:
                if expense['date'] == match:
                    print(f"Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date']}, Description: {expense['description']}")
                    found = True

    if not found:
        print('No expense found.')

def extremes(expenses):
    if not expenses:
        print('No expenses yet.')
        return 
    
    which = input('Do you want to see the largest or the smallest expense(largest/smallest): ').lower().strip()
    amounts = [expense['amount'] for expense in expenses]

    if which not in ['largest', 'smallest']:
        print('Not a valid answer.')
    elif which == 'largest':
        largest = max(amounts)
        largest_amounts = [exp for exp in expenses if exp['amount'] == largest]
        for ex in largest_amounts:
            print(f"Amount: {ex['amount']}, Category: {ex['category']}, Date: {ex['date']}, Description: {ex['description']}")
    else:
        smallest = min(amounts)
        smallest_amounts = [exp for exp in expenses if exp['amount'] == smallest]
        for ex in smallest_amounts:
            print(f"Amount: {ex['amount']}, Category: {ex['category']}, Date: {ex['date']}, Description: {ex['description']}")

def visual_representation(expenses):
    mth = input('Write the month and year which you want to see(MM-YYYY): ').strip()
    if not re.match(r'\d{2}-\d{4}', mth):
        print('Invalid format.')
        return 
    
    month = datetime.strptime(mth, '%m-%Y').strftime('%Y-%m')
    chosen = [exp for exp in expenses if exp['date'][:7] == month]

    firstx = list(range(1, len(chosen) + 1))
    firsty = [expense['amount'] for expense in chosen]

    plt.plot(firstx, firsty)
    plt.title(f'Expenses graph for {month}')
    plt.xlabel('Dates')
    plt.ylabel('Amount spent')

    plt.show()

def save_expenses(expenses):
     with open('/workspaces/expenses.csv', 'w', newline='') as fl:
        fieldnames = ['amount', 'category', 'date', 'description','recurring','last_added_month', 'limit']
        writer = csv.DictWriter(fl, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses) 

def set_limit(expenses):
    mth = input('Choose which month you want to set a limit for(MM-YYYY): ').strip()
    limit = float(input('Set your monthly limit: ').strip())

    if not re.match(r'\d{2}-\d{4}', mth):
        print('Invdalid input.')
        return
    
    month = datetime.strptime(mth, '%m-%Y').strftime('%Y-%m')
    monthly_cost = 0

    for expense in expenses:
        if expense['date'][:7] == month:
            monthly_cost += expense['amount']
            expense['limit'] = limit
    save_expenses(expenses)

    if monthly_cost >= limit - 50:
        print('Warning! You are close to your budget limit.')
    elif monthly_cost == limit:
        print('You have reached the monthly limit!')
    elif monthly_cost > limit:
        print('!!! You have exceeded the budget limit !!!')

def recurring(expenses):
    current_month = datetime.now().strftime('%Y-%m')
    new_expenses = []

    for exp in expenses:
        if exp['recurring'] == 'y':
            if exp['last_added_month'] != current_month:
                new_expense = exp.copy()
                new_expense['date'] = f'{current_month}-01'
                new_expense['last_added_month'] = current_month
                new_expenses.append(new_expense)
                
    expenses.extend(new_expenses)

    save_expenses(expenses)

if __name__ == '__main__':
    main()
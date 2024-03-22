from enum import Enum
import csv
import requests
import ansitable

class sw_csv_columns(Enum):
    DATE = 0
    DESCRIPTION = 1
    CATEGORY = 2
    COST = 3
    CURRENCY = 4

class Day:

    def __init__(self, date: str, conversion_rate: dict = None, desired_currency = 'EUR') -> None:
        self._date = date
        self._conversion_rate = conversion_rate
        self._desired_currency = desired_currency
        self._expense_category = {}

    def add_new_expense(self, expense: float, currency: str, category: str) -> None:
        if currency != self._desired_currency:
            expense = expense/self._conversion_rate[currency]
        if category not in self._expense_category.keys():
            self._expense_category[category] = expense
        else:            
            self._expense_category[category] += expense

    def get_total_expenses_of_day(self, currency: str = None) -> float:
        total_expense = 0
        if currency is None:
            desired_currency_for_expense_category = self._desired_currency
        else:
            desired_currency_for_expense_category = currency 
        
        for category in self._expense_category.keys():
            total_expense += self._expense_category[category]*self._conversion_rate[desired_currency_for_expense_category]

        return total_expense

    def get_expenses_of_specific_category(self, category: str, currency: str = None) -> float:

        if currency is None:
            desired_currency_for_expense = self._desired_currency
        else:
            desired_currency_for_expense = currency 

        return self._expense_category[category]*self._conversion_rate[desired_currency_for_expense]
    
    def get_date(self):
        return self._date
    
    def get_expense_categories(self):
        return self._expense_category.keys()

def get_cost_currency_and_general_category(row):
    cost = float(row[sw_csv_columns.COST.value]) 
    currency = row[sw_csv_columns.CURRENCY.value]
    category = row[sw_csv_columns.CATEGORY.value]
    general_category = get_general_category(category)
    date = row[sw_csv_columns.DATE.value]

    return cost, currency, general_category, date

def get_general_category(category: str):
    entertainment = ['Games', 'Movies', 'Music', 'Entertainment - Other', 'Sports']
    food_and_drink = ['Dining out', 'Groceries', 'Liquor', 'Food and drink - Other']
    home = ['Electronics', 'Furniture', 'Household supplies', 'Maintenance', 'Mortgage', 'Home - Other', 'Pets', 'Rent', 'Services']
    life = ['Childcare', 'Clothing', 'Education', 'Gifts', 'Insurance', 'Medical expenses', 'Life - Other', 'Taxes']
    transportation = ['Bicycle','Bus/train','Car','Gas/fuel','Transportation - Other', 'Parking', 'Plane', 'Taxi']
    hotel = ['Hotel']
    utilities = ['Cleaning','Electricity','Heat/gas','Utilities - Other','TV/Phone/Internet','Trash','Water']

    if category in entertainment:
        general_category = 'Entertainment'
    elif category in food_and_drink:
        general_category = 'Food and Drink'
    elif category in home:
        general_category = 'Home'
    elif category in life:
        general_category = 'Life'
    elif category in transportation:
        general_category = 'Transportation'
    elif category in hotel:
        general_category = 'Hotel'
    elif category in utilities:
        general_category = 'Utilities'
    else:
        general_category = 'Uncategorized'

    return general_category

def get_conversion_rates(api_key: str, base_currency: str, date: str = None):
    
    if date is None:
        # get the latest conversion rates
        payload = {'api_key': api_key, 'base': base_currency}
        r = requests.get("https://api.currencybeacon.com/v1/latest", params=payload)
    else:
        # get the historical conversion rates for a specific date 
        payload = {'api_key': api_key, 'base': base_currency, 'date': date}
        r = requests.get("https://api.currencybeacon.com/v1/historical", params=payload)

    # extract conversion rates from data
    conversion_rates = r.json()['response']['rates']
    
    return conversion_rates

def get_total_expense_and_category_expenses(days: list[Day]):
    total_expense = 0
    expense_per_category = {}

    for date in days:
        categories_date = date.get_expense_categories()
        total_expense += date.get_total_expenses_of_day()
        for category in categories_date:
            if category not in expense_per_category.keys():
                expense_per_category[category] = date.get_expenses_of_specific_category(category)
            else:            
                expense_per_category[category] += date.get_expenses_of_specific_category(category)
    
    return total_expense, expense_per_category

def get_days_with_expenses(file_path: str, api_key: str, desired_currency: str, use_latest_rates = True):
    
    rows = []
    with open(file_path, newline='') as file:
        csv_reader = csv.reader(file, quotechar='"')
        for row in csv_reader:
            rows.append(row)

    days: list[Day] = list()
    if use_latest_rates:
        conversion_rates = get_conversion_rates(api_key=api_key, base_currency=desired_currency)

    counter_empty_lines = 0

    for row in rows:
        if len(row) == 0:
            counter_empty_lines += 1

        elif counter_empty_lines == 1:
            cost, currency, category, date = get_cost_currency_and_general_category(row)

            if days == []:
                if not use_latest_rates:
                    conversion_rates = get_conversion_rates(api_key=api_key, base_currency=desired_currency, date = date)
                days.append(Day(date, conversion_rates, desired_currency))
                days[-1].add_new_expense(cost,currency,category)
            elif days[-1].get_date() == date:
                days[-1].add_new_expense(cost, currency, category)
            else:
                days.append(Day(date,conversion_rates, desired_currency))
                days[-1].add_new_expense(cost,currency,category)

    return days

def print_table(total_expense: float, expense_per_category: dict, desired_currency: str):
    # create table to print out in the command line
    table = ansitable.ANSITable(
        ansitable.Column("Expense"),
        ansitable.Column("Value ("+ desired_currency + ")", "{:-10.2f}"),
        ansitable.Column("Percentage","{:-10.1f}"),
        border="thick"
    )
    # add expenses per category to the table
    for key in expense_per_category.keys():
            percentage_of_all_expenses = expense_per_category[key]/total_expense*100
            table.row(key, expense_per_category[key], percentage_of_all_expenses)
    print(f"Your total expenses are {total_expense: .2f} {desired_currency}")
    table.print()





        



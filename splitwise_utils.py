import json, urllib.request

def get_cost_currency_and_general_category(line):
    split_line = line.split(',')
    cost = float(split_line[3]) 
    currency = split_line[4]
    category = split_line[2]
    general_category = get_general_category(category)
    date = split_line[0]

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





        



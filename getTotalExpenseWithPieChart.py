import urllib.request, json
import splitwise_utils

import matplotlib.pyplot as plt

with open("./data.csv") as file:
    lines = [line.rstrip() for line in file]

days: list[splitwise_utils.Day] = list()
APIKey = "your-key"
desired_currency = 'EUR'
api_link = "https://v6.exchangerate-api.com/v6/" + APIKey + "/latest/" + desired_currency
with urllib.request.urlopen(api_link) as url:
    exchange_rate_data = json.load(url)

conversion_rates = exchange_rate_data['conversion_rates']

cost_each_currency = {}
counter_empty_lines = 0

for line in lines:
    if not line.strip():
        counter_empty_lines += 1

    elif counter_empty_lines == 1:
        cost, currency, category, date = splitwise_utils.get_cost_currency_and_general_category(line)

        if days == []:
            days.append(splitwise_utils.Day(date, conversion_rates, desired_currency))
            days[-1].add_new_expense(cost,currency,category)
        elif days[-1].get_date() == date:
            days[-1].add_new_expense(cost, currency, category)
        else:
            days.append(splitwise_utils.Day(date,conversion_rates, desired_currency))
            days[-1].add_new_expense(cost,currency,category)

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

fig, ax = plt.subplots()
ax.pie(expense_per_category.values(), labels = expense_per_category.keys(), autopct='%1.1f%%')
plt.title(f"Total expense: {total_expense: .2f} {desired_currency}")

plt.show()
import matplotlib.pyplot as plt
import splitwise_utils

### ADD YOUR DATA HERE ###
# your Currencybeacon API key
APIKey = 'YOUR-API-KEY'
# the path to your Splitewise file
file_path = "./fake_data.csv"
# set the variable below to False to get historical rates
use_latest_exchange_rates = True
# set the desired currency for your expenses
desired_currency = 'EUR'

# get list of days with expenses
days = splitwise_utils.get_days_with_expenses(file_path, APIKey, desired_currency, use_latest_rates=use_latest_exchange_rates)

# compute total expenses and the expenses per category for the days
total_expense, expense_per_category = splitwise_utils.get_total_expense_and_category_expenses(days)

# print expenses as a table in the command line
splitwise_utils.print_table(total_expense,expense_per_category,desired_currency)

# plot pie chart of the expenses
fig, ax = plt.subplots()
ax.pie(expense_per_category.values(), labels = expense_per_category.keys(), autopct='%1.1f%%')
plt.title(f"Total expense: {total_expense: .2f} {desired_currency}")

plt.show()
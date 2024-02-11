import urllib.request, json

def get_cost_and_currency(line):
    split_line = line.split(',')
    cost = float(split_line[3]) 
    currency = split_line[4]

    return cost, currency

def get_total_cost_in_desired_currency(cost_per_currency,desired_currency = 'EUR'):
    if desired_currency not in cost_per_currency.keys():
        print("The desired currency is not in the currently used currencies")
        return -1
    else:
        api_link = "https://v6.exchangerate-api.com/v6/YOUR-API/latest/" + desired_currency
        with urllib.request.urlopen(api_link) as url:
            exchange_rate_data = json.load(url)

        conversion_rates = exchange_rate_data['conversion_rates']
        total_cost = 0
        for key in cost_per_currency.keys():
            if key == desired_currency:
                total_cost += cost_per_currency[key]
            else:
                total_cost += cost_per_currency[key]/conversion_rates[key]

        return total_cost

with open("./data.csv") as file:
    lines = [line.rstrip() for line in file]

cost_each_currency = {}
counter_empty_lines = 0

for line in lines:
    if not line.strip():
        counter_empty_lines+=1
    elif counter_empty_lines == 1:
        cost, currency = get_cost_and_currency(line)
        if currency in cost_each_currency.keys():
            cost_each_currency[currency] += cost
        else:
            cost_each_currency[currency] = cost

desired_currency = "EUR"
print(f"The total cost in {desired_currency} are {get_total_cost_in_desired_currency(cost_each_currency,desired_currency)}")
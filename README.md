# Analyzing Splitwise Data

## About this repository
This repository contains a Python script to analyze the exported data from [Splitwise](https://www.splitwise.com/). 
The current functionality is to sum up all expenses registered to get a total expense in a desired currency as well as a pie chart with the Splitwise categories to show you what the money was spent on.

This can help to keep track on the money spent on a trip and what it was spent on, while not requiring a paid account on Splitwise.

A fake data set ```fake_data.csv``` of a two week trip with three currencies is provided. This data set has the same format as the one obtained by exporting data from Splitwise.


## Currency Exchange Rate API
The current implementation uses the API from [ExchangeRate-API](https://www.exchangerate-api.com/), which allows for 1.5k API request per month in the free subscription. 

An issue with that is that it does not allow to obtain historical rates, which means that depending on the day one checks the total expenses might be different.
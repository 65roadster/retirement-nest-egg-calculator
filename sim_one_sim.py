import csv
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

file_path = 'market_returns.csv'

# this is used to format the Y axis as dollars in the matplotlib figures
def dollar_formatter(x, pos):
    return '${:,.0f}'.format(x)
	
def read_csv_file(file_path):
    """
    Read a CSV file and return its contents as a list of dictionaries.

    Args:
    - file_path (str): The path to the CSV file.

    Returns:
    - list: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    data = []
    with open(file_path, 'r', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

data = read_csv_file(file_path)

portfolio_starting_value_stocks = 100000
portfolio_starting_value_bonds = 100000
sim_num_years = 20
num_rows = len(data)
sim_year = 0
sim_results = []
sim_results.append([ sim_year, portfolio_starting_value_stocks, portfolio_starting_value_bonds, portfolio_starting_value_stocks + portfolio_starting_value_bonds, 0, 0, 0, 0 ])
for _ in range(sim_num_years):
    sim_year += 1
    random_index = random.randint(1, num_rows - 1)
    sim_year_data = data[random_index]
    sim_prior_year_data = data[random_index-1]
    # calendar_year = int( sim_year_data["Year"] )
    nav = float( sim_year_data["SP500 NAV"] )
    prior_nav = float( sim_prior_year_data["SP500 NAV"] )
    nav_change = nav-prior_nav
    stock_dividend = float( sim_year_data["SP500 Dividend"] )
    stock_total_return = (nav_change + stock_dividend) / prior_nav
    bond_return = float( sim_year_data["US T Bond 10yr"] )
    portfolio_stocks_prior = sim_results[len(sim_results)-1][1]
    portfolio_bonds_prior = sim_results[len(sim_results)-1][2]

    portfolio_stocks = portfolio_stocks_prior * (1+stock_total_return)
    portfolio_bonds = portfolio_bonds_prior * (1 + bond_return)
    portfolio_total = portfolio_stocks + portfolio_bonds

#    print("year = " + str(year) + ", nav = " + str(nav) + ", prior_nav = " + str(prior_nav) + ", nav_change = " + str(nav_change) +
#           ", dividend = " + str(stock_dividend) + ", total_return = " + str(stock_total_return) + ", bond_return = " + str(bond_return))
    sim_results.append([ sim_year, portfolio_stocks, portfolio_bonds, portfolio_total, stock_total_return, stock_dividend, bond_return])

for row in sim_results:
    print("year = {:3d}, stocks ${:,.2f}, bonds ${:,.2f}, total ${:,.2f}, stock_returns {:.2f}%, stock_dividend ${:.2f}, bond_yield {:.2f}%".format(row[0], row[1], row[2], row[3], 100*row[4], row[5], 100*row[6]))

years = []
stocks = []
bonds = []
total = []
for row in sim_results:
    years.append(row[0])
    stocks.append(row[1])
    bonds.append(row[2])
    total.append(row[3])


# Create a formatter object
formatter = FuncFormatter(dollar_formatter)

plt.figure(figsize=(8, 4))  # Specify width and height in inches

# Apply the formatter to the y-axis
plt.gca().yaxis.set_major_formatter(formatter)

plt.plot(years, stocks, label='stocks')  # Plot the sine wave and label it
plt.plot(years, bonds, label='bonds')  # Plot the cosine wave and label it
plt.plot(years, total, label='total')  # Plot the cosine wave and label it
plt.legend()

# Add title and labels
plt.title('Portfolio Results')
plt.xlabel('year')
plt.ylabel('value')

# Show the plot
plt.show()
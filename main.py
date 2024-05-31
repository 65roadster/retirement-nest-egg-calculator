####
## go use this code and do what you want with it


import csv
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import PercentFormatter
import numpy as np
import os

####
## simulation parameters
total_initial_portfolio = 2500000
stock_allocation = 0.50
portfolio_annual_withdrawal = 100000
sim_num_years = 40
sim_monte_carlo_iterations = 5000
file_path = 'market_returns.csv'


# reads market returns
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

####
# This handles one iteration of a simulation (one series of years)
# A random year is chosen from historical returns
# Returns are adjusted for inflation
# Returns on the portfolio are calculated for each asset class
# Annual funds are then withdrawn
# Portfolio is rebalanced

def run_simulation(sim_num_years, portfolio_starting_value_stocks, portfolio_starting_value_bonds, annual_withdrawal, stock_allocation):
    global market_return_data
    num_rows = len(market_return_data)
    sim_year = 0
    sim_results = []
    sim_results.append([ int(sim_year), int(0), portfolio_starting_value_stocks, portfolio_starting_value_bonds, portfolio_starting_value_stocks + portfolio_starting_value_bonds, 0, 0, 0, 0 ])
    for _ in range(sim_num_years):
        annual_withdrawal = float(annual_withdrawal)
        sim_year += 1
        random_index = random.randint(1, num_rows - 1)
        sim_year_data = market_return_data[random_index]
        sim_prior_year_data = market_return_data[random_index-1]

        calendar_year = int( sim_year_data["Year"] )
        nav = float( sim_year_data["SP500 NAV"] )
        prior_nav = float( sim_prior_year_data["SP500 NAV"] )
        stock_dividend = float( sim_year_data["SP500 Dividend"] )
        bond_return = float( sim_year_data["US T Bond 10yr"] )
        inflation = float( sim_year_data["Inflation"] )

        nav_change = nav-prior_nav
        stock_total_return = (nav_change + stock_dividend) / prior_nav
        stock_total_return_real = stock_total_return - inflation

        bond_return_real = bond_return - inflation

        # Calculate stock and bond growth
        portfolio_stocks_prior = sim_results[len(sim_results)-1][2]
        portfolio_bonds_prior = sim_results[len(sim_results)-1][3]
        portfolio_total_prior = portfolio_stocks_prior + portfolio_bonds_prior

        portfolio_stocks_new = portfolio_stocks_prior * (1+stock_total_return_real)
        portfolio_bonds_new = portfolio_bonds_prior * (1 + bond_return_real)

        if (portfolio_stocks_new < 0):
            portfolio_stocks_new = 0
        if (portfolio_bonds_new < 0):
            portfolio_bonds_new = 0

        portfolio_total_new = portfolio_stocks_new + portfolio_bonds_new


        # Perform annual withdrawal
        portfolio_total_new -= annual_withdrawal
        if (portfolio_total_new < 0):
            portfolio_total_new = 0


        # Rebalance portfolio
        portfolio_stocks_new = portfolio_total_new * stock_allocation
        portfolio_bonds_new = portfolio_total_new - portfolio_stocks_new
        
#        print(f"{sim_year:3d}, {calendar_year:4d}, stock_return = {100*stock_total_return:.2f}%, stock_return_real = {100*stock_total_return_real:.2f}%, bond_return = {100*bond_return:.2f}%, bond_return_real = {100*bond_return_real:.2f}%, inflation={100*inflation:.2f}%")
#        print(f"           portfolio_stocks_prior = f, portfolio_bonds_prior = ${portfolio_bonds_prior:,.2f}, percent_stocks = {100*percent_stocks:,.2f}%, percent_bonds = {100*percent_bonds:,.2f}%")
#        print(f"           annual_withdrawal = ${annual_withdrawal:,.2f}, withdrawal_stocks = ${withdrawal_stocks:,.2f}, withdrawal_bonds = ${withdrawal_bonds:,.2f} ")
#        print(f"           portfolio_stock_new = ${portfolio_stocks_new:,.2f}, portfolio_bonds_new = ${portfolio_bonds_new:,.2f}, portfolio_total_new = ${portfolio_total_new:,.2f}")

        sim_results.append([ int(sim_year), calendar_year, portfolio_stocks_new, portfolio_bonds_new, portfolio_total_new, stock_total_return_real, stock_dividend, bond_return_real, inflation])
    return (sim_results)


os.system('cls')

####
# Read file with stock, bond, and inflation historical information
market_return_data = read_csv_file(file_path)

####
# Set up simulation parameters
portfolio_starting_value_stocks = total_initial_portfolio * stock_allocation
portfolio_starting_value_bonds = total_initial_portfolio * (1-stock_allocation)

####
# Run simulations
sim_monte_carlo_results = []
for i in range(sim_monte_carlo_iterations):
    sim_single = run_simulation(sim_num_years, portfolio_starting_value_stocks, portfolio_starting_value_bonds, portfolio_annual_withdrawal, stock_allocation)
    sim_monte_carlo_results.append(sim_single)

####
# calculate quantiles for each year
#

quartile_inner = []
q5_stocks = []
q10_stocks = []
q25_stocks = []
q75_stocks = []
q90_stocks = []
q95_stocks = []

q5_bonds = []
q10_bonds = []
q25_bonds = []
q75_bonds = []
q90_bonds = []
q95_bonds = []

q5_portfolio = []
q10_portfolio = []
q25_portfolio = []
q75_portfolio = []
q90_portfolio = []
q95_portfolio = []

for y in range(len(sim_monte_carlo_results[0])):
    year_of_stocks = []
    year_of_bonds = []
    year_of_portfolio = []

    for i in range(sim_monte_carlo_iterations):
        iteration = sim_monte_carlo_results[i]
        year_of_results = iteration[y]
        stocks_value = year_of_results[2]
        bonds_value = year_of_results[3]
        portfolio_value = year_of_results[4]
        year_of_stocks.append(stocks_value)
        year_of_bonds.append(bonds_value)
        year_of_portfolio.append(portfolio_value)

    q5_stocks.append(np.percentile(year_of_stocks, 5))
    q10_stocks.append(np.percentile(year_of_stocks, 10))
    q25_stocks.append(np.percentile(year_of_stocks, 25))
    q75_stocks.append(np.percentile(year_of_stocks, 75))
    q90_stocks.append(np.percentile(year_of_stocks, 90))
    q95_stocks.append(np.percentile(year_of_stocks, 95))

    q5_bonds.append(np.percentile(year_of_bonds, 5))
    q10_bonds.append(np.percentile(year_of_bonds, 10))
    q25_bonds.append(np.percentile(year_of_bonds, 25))
    q75_bonds.append(np.percentile(year_of_bonds, 75))
    q90_bonds.append(np.percentile(year_of_bonds, 90))
    q95_bonds.append(np.percentile(year_of_bonds, 95))

    q5_portfolio.append(np.percentile(year_of_portfolio, 5))
    q10_portfolio.append(np.percentile(year_of_portfolio, 10))
    q25_portfolio.append(np.percentile(year_of_portfolio, 25))
    q75_portfolio.append(np.percentile(year_of_portfolio, 75))
    q90_portfolio.append(np.percentile(year_of_portfolio, 90))
    q95_portfolio.append(np.percentile(year_of_portfolio, 95))

####
# CaLculate # of successful years (portfoliio has > $0.01 at end of year)
# portfolio, stocks and bonds should have identical results since portfolio is rebalanced each year
num_fails_portfolio = 0
num_fails_stocks = 0
num_fails_bonds = 0

for i in range(len(sim_monte_carlo_results)):
    simulation = sim_monte_carlo_results[i]
    
    if (simulation[len(simulation)-1][2] < 0.01):
        num_fails_stocks += 1

    if (simulation[len(simulation)-1][3] < 0.01):
        num_fails_bonds += 1

    if (simulation[len(simulation)-1][4] < 0.01):
        num_fails_portfolio += 1

percent_success_portfolio = 100*(1.0 - (num_fails_portfolio / (len(sim_monte_carlo_results))))
percent_success_stocks = 100*(1.0 - (num_fails_stocks / (len(sim_monte_carlo_results))))
percent_success_bonds = 100*(1.0 - (num_fails_bonds / (len(sim_monte_carlo_results))))

####
# Calculate the chance of failure for each year of the simulation
fails_per_year_portfolio = []
fails_per_year_stocks = []
fails_per_year_bonds = []


for y in range(len(sim_monte_carlo_results[0])):
    stock_fails = 0
    bond_fails = 0
    portfolio_fails = 0

    for i in range(sim_monte_carlo_iterations):
#        print("portfolio value = " + str(sim_monte_carlo_results[i][y][4]))
        if sim_monte_carlo_results[i][y][2] < 0.01:
            stock_fails += 1
        if sim_monte_carlo_results[i][y][3] < 0.01:
            bond_fails += 1
        if sim_monte_carlo_results[i][y][4] < 0.01:
            portfolio_fails += 1

#    print("# fails = " + str(portfolio_fails))
    fails_per_year_stocks.append(1 - (stock_fails / len(sim_monte_carlo_results)))
    fails_per_year_bonds.append(1 - (bond_fails / len(sim_monte_carlo_results)))
    fails_per_year_portfolio.append(1 - (portfolio_fails / len(sim_monte_carlo_results)))

####
## print results to terminal
print()
print("===== Simulation Setup =====")
print(f"Initial portfolio value = ${(total_initial_portfolio):,.0f}")
print(f"Stocks = {(100*portfolio_starting_value_stocks / total_initial_portfolio):.1f}%")
print(f"Bonds = {(100*portfolio_starting_value_bonds / total_initial_portfolio):.1f}%")
print(f"Annual Withdrawal = ${(portfolio_annual_withdrawal):,.0f}")
print(f"Duration of simulation = {sim_num_years:d}")
print(f"Monte Carlo iterations = {sim_monte_carlo_iterations:d}")
print("Returns are adjusted for inflation")
print("Returns are calculated, then annual withdraw is taken")
print("Portfolio is rebalanced each year after growth and withdraw are factored")

print()
print("===== Full Portfolio Results =====")
print("5% quantile = ${:,.2f}".format(q5_portfolio[len(q5_portfolio)-1]))
print("10% quantile = ${:,.2f}".format(q10_portfolio[len(q10_portfolio)-1]))
print("25% quartile = ${:,.2f}".format(q25_portfolio[len(q25_portfolio)-1]))
print("75% quartile = ${:,.2f}".format(q75_portfolio[len(q75_portfolio)-1]))
print("90% quantile = ${:,.2f}".format(q90_portfolio[len(q90_portfolio)-1]))
print("95% quantile = ${:,.2f}".format(q95_portfolio[len(q95_portfolio)-1]))
print(f"Portfolio success rate = {len(sim_monte_carlo_results)-num_fails_portfolio:d}/{len(sim_monte_carlo_results):d} = {percent_success_portfolio:.1f}%")

print()
print("===== Stock Portfolio Results =====")
print("5% quantile = ${:,.2f}".format(q5_stocks[len(q5_stocks)-1]))
print("10% quantile = ${:,.2f}".format(q10_stocks[len(q10_stocks)-1]))
print("25% quartile = ${:,.2f}".format(q25_stocks[len(q25_stocks)-1]))
print("75% quartile = ${:,.2f}".format(q75_stocks[len(q75_stocks)-1]))
print("90% quantile = ${:,.2f}".format(q90_stocks[len(q90_stocks)-1]))
print("95% quantile = ${:,.2f}".format(q95_stocks[len(q95_stocks)-1]))
print(f"Stocks success rate = {len(sim_monte_carlo_results)-num_fails_stocks:d}/{len(sim_monte_carlo_results):d} = {percent_success_stocks:.1f}%")

print()
print("===== Bond Portfolio Results =====")
print("5% quantile = ${:,.2f}".format(q5_bonds[len(q5_bonds)-1]))
print("10% quantile = ${:,.2f}".format(q10_bonds[len(q10_bonds)-1]))
print("25% quartile = ${:,.2f}".format(q25_bonds[len(q25_bonds)-1]))
print("75% quartile = ${:,.2f}".format(q75_bonds[len(q75_bonds)-1]))
print("90% quantile = ${:,.2f}".format(q90_bonds[len(q90_bonds)-1]))
print("95% quantile = ${:,.2f}".format(q95_bonds[len(q95_bonds)-1]))
print(f"Bonds success rate = {len(sim_monte_carlo_results)-num_fails_bonds:d}/{len(sim_monte_carlo_results):d} = {percent_success_bonds:.1f}%")


####
## Graph results

####
# set up years array for x axis for all graphs
years = []
sim_results = sim_monte_carlo_results[0]
for row in sim_results:
    years.append(row[0])

# this is used to format the Y axis as dollars in the matplotlib figures
def dollar_formatter(x, pos):
    return '${:,.0f}'.format(x)

# Create a formatter object for y axis
formatter = FuncFormatter(dollar_formatter)

fig, ax = plt.subplots(2, 2, figsize=(16, 10))
plt.gcf().canvas.manager.set_window_title('Simulation Results')

y_min = 0
y_max = max(q95_portfolio)
y_step = 100000

if (y_max < 15 * 1000): # $15k
    y_max = 15 * 1000
    y_step = 1000
elif (y_max < 15 * 2000): # $30k
    y_max = 15 * 2000
    y_step = 2000
elif (y_max < 15 * 5000): # $75k
    y_max = 15 * 5000
    y_step = 5000
elif (y_max < 15 * 10000): # $150k
    y_max = 15 * 10000
    y_step = 10000
elif (y_max < 15 * 20000): # $300k
    y_max = 15 * 20000
    y_step = 20000
elif (y_max < 15 * 50000): # $750k
    y_max = 15 * 50000
    y_step = 50000
elif (y_max < 15 * 100000): # $1.5M
    y_max = 15 * 100000
    y_step = 100000
elif (y_max < 15 * 200000): # $3M
    y_max = 15 * 200000
    y_step = 200000
elif (y_max < 15 * 500000): # $7.5M
    y_max = 15 * 500000
    y_step = 500000
elif (y_max < 15 * 1000000): # $15M
    y_max = 15 * 1000000
    y_step = 1000000
elif (y_max < 15 * 2000000): # $30M
    y_max = 15 * 2000000
    y_step = 2000000
elif (y_max > 15 * 5000000): # $75M
    y_max = 15 * 5000000
    y_step = 5000000
elif (y_max > 15 * 10000000): # $150M
    y_max = 15 * 10000000
    y_step = 10000000
elif (y_max > 15 * 20000000): # $300M
    y_max = 15 * 20000000
    y_step = 20000000
elif (y_max > 15 * 50000000): # $750M
    y_max = 15 * 50000000
    y_step = 50000000
elif (y_max > 15 * 100000000): # $1.5B
    y_max = 15 * 100000000
    y_step = 100000000

y_ticks = np.arange(0, y_max, y_step)

ax[0,0].yaxis.set_major_formatter(formatter)
ax[0,0].fill_between(years, q5_portfolio, q95_portfolio, alpha=.4, linewidth=0)
ax[0,0].fill_between(years, q10_portfolio, q90_portfolio, alpha=.4, linewidth=0)
ax[0,0].fill_between(years, q25_portfolio, q75_portfolio, alpha=.4, linewidth=0)
ax[0,0].set_yticks(y_ticks)
ax[0,0].set_title('Portfolio Results with 50%, 80%, 90% Quantiles')
ax[0,0].set_xlabel('Year')
ax[0,0].set_ylabel('Portfolio Value')
ax[0,0].set_xticks(years)
ax[0,0].grid(True)

#ylim_values = ax[0, 0].get_ylim()

ax[0,1].yaxis.set_major_formatter(formatter)
ax[0,1].fill_between(years, q5_stocks, q95_stocks, alpha=.4, linewidth=0)
ax[0,1].fill_between(years, q10_stocks, q90_stocks, alpha=.4, linewidth=0)
ax[0,1].fill_between(years, q25_stocks, q75_stocks, alpha=.4, linewidth=0)
ax[0,1].set_yticks(y_ticks)
ax[0,1].set_title('Stocks Results with 50%, 80%, 90% Quantiles')
ax[0,1].set_xlabel('Year')
ax[0,1].set_ylabel('Portfolio Value')
ax[0,1].set_xticks(years)
ax[0,1].grid(True)

ax[1,0].yaxis.set_major_formatter(formatter)
ax[1,0].fill_between(years, q5_bonds, q95_bonds, alpha=.4, linewidth=0)
ax[1,0].fill_between(years, q10_bonds, q90_bonds, alpha=.4, linewidth=0)
ax[1,0].fill_between(years, q25_bonds, q75_bonds, alpha=.4, linewidth=0)
ax[1,0].set_yticks(y_ticks)
ax[1,0].set_title('Bonds Results with 50%, 80%, 90% Quantiles')
ax[1,0].set_xlabel('Year')
ax[1,0].set_ylabel('Portfolio Value')
ax[1,0].set_xticks(years)
ax[1,0].grid(True)

ax[1,1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
ax[1,1].plot(years, fails_per_year_portfolio, label="portfolio")
ax[1,1].set_ylim(0,0.1)
ax[1,1].set_title('Likelihood of success each year')
ax[1,1].set_xlabel('Year')
ax[1,1].set_ylabel('Chance of Success')
ax[1,1].set_xticks(years)
y_ticks = np.arange(0, 1.1, 0.1)
ax[1,1].set_yticks(y_ticks)
ax[1,1].grid(True)

for a in ax.flat:
    a.set_xlim(min(years), max(years))
	
plt.tight_layout()
plt.show(block=True)

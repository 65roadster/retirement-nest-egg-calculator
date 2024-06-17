####
# go do what you want with this code

import csv
import random
import numpy as np

import time


class simulator():
    file_path = 'market_returns.csv'

    market_return_data = []
    sim_monte_carlo_results = []
    fails_per_year_portfolio = []
    fails_per_year_stocks = []
    fails_per_year_bonds = []

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

    def __init__(self):
        self.market_return_data = []
        self.read_csv_file(self.file_path)
        self.clear()

    def clear(self):
        self.sim_monte_carlo_results = []
        self.fails_per_year_portfolio = []
        self.fails_per_year_stocks = []
        self.fails_per_year_bonds = []

        self.q5_stocks = []
        self.q10_stocks = []
        self.q25_stocks = []
        self.q75_stocks = []
        self.q90_stocks = []
        self.q95_stocks = []

        self.q5_bonds = []
        self.q10_bonds = []
        self.q25_bonds = []
        self.q75_bonds = []
        self.q90_bonds = []
        self.q95_bonds = []

        self.q5_portfolio = []
        self.q10_portfolio = []
        self.q25_portfolio = []
        self.q75_portfolio = []
        self.q90_portfolio = []
        self.q95_portfolio = []

    ####
    # Read file with stock, bond, and inflation historical information
    def read_csv_file(self, file_path):
        with open(file_path, 'r', newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.market_return_data.append(row)

    ####
    # stocks are modeled by S&P500 historical returns, dividends are reinvested
    # the balance of the portfolio is modeled as 10 year T bills
    # A random year is chosen from historical returns
    # Returns are adjusted for inflation
    # Returns on the portfolio are calculated for each asset class
    # Annual funds are then withdrawn
    # Portfolio is rebalanced

    def run_simulation(self, portfolio_starting_value_stocks, portfolio_starting_value_bonds,
                             annual_withdrawal1, sim_num_years1,
                             annual_withdrawal2, sim_num_years2,
                             annual_withdrawal3, sim_num_years3,
                             stock_allocation):

        ####
        # This handles one iteration of a simulation (one series of years)
        # A random year is chosen from historical returns
        # Returns are adjusted for inflation
        # Returns on the portfolio are calculated for each asset class
        # Annual funds are then withdrawn
        # Portfolio is rebalanced

        num_rows = len(self.market_return_data)
        sim_year = 0
        sim_results = []
        sim_results.append([ int(sim_year), int(0),
		    portfolio_starting_value_stocks, portfolio_starting_value_bonds,
			portfolio_starting_value_stocks + portfolio_starting_value_bonds,
            0, 0, 0, 0 ])

        for year in range(sim_num_years1+sim_num_years2+sim_num_years3):
            if (year < sim_num_years1):
                annual_withdrawal = float(annual_withdrawal1)
            elif (year < sim_num_years1 + sim_num_years2):
                annual_withdrawal = float(annual_withdrawal2)
            else:
                annual_withdrawal = float(annual_withdrawal3)

            #print(f"year = {year:d}, withdrawal = {annual_withdrawal:f}")
            annual_withdrawal = float(annual_withdrawal)
            sim_year += 1
            random_index = random.randint(1, num_rows - 1)
            sim_year_data = self.market_return_data[random_index]
            sim_prior_year_data = self.market_return_data[random_index-1]

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
            # portfolio_total_prior = portfolio_stocks_prior + portfolio_bonds_prior

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
        
            sim_results.append([ int(sim_year), calendar_year, portfolio_stocks_new, portfolio_bonds_new, portfolio_total_new, stock_total_return_real, stock_dividend, bond_return_real, inflation])
        return (sim_results)

    def simulate(self, total_initial_portfolio, stock_allocation,
                       portfolio_annual_withdrawal1, sim_num_years1,
                       portfolio_annual_withdrawal2, sim_num_years2,
                       portfolio_annual_withdrawal3, sim_num_years3,
                       sim_monte_carlo_iterations):

        ####
        # Set up simulation parameters
        portfolio_starting_value_stocks = total_initial_portfolio * stock_allocation
        portfolio_starting_value_bonds = total_initial_portfolio * (1-stock_allocation)

        ####
        # Run simulations
        for i in range(sim_monte_carlo_iterations):
            sim_single = self.run_simulation(portfolio_starting_value_stocks, portfolio_starting_value_bonds,
			                                 portfolio_annual_withdrawal1, sim_num_years1,
                                             portfolio_annual_withdrawal2, sim_num_years2,
                                             portfolio_annual_withdrawal3, sim_num_years3,
                                             stock_allocation)
            self.sim_monte_carlo_results.append(sim_single)

        ####
        # calculate quantiles for each year
        #

        for y in range(len(self.sim_monte_carlo_results[0])):
            year_of_stocks = []
            year_of_bonds = []
            year_of_portfolio = []

            for i in range(sim_monte_carlo_iterations):
                iteration = self.sim_monte_carlo_results[i]
                year_of_results = iteration[y]
                stocks_value = year_of_results[2]
                bonds_value = year_of_results[3]
                portfolio_value = year_of_results[4]
                year_of_stocks.append(stocks_value)
                year_of_bonds.append(bonds_value)
                year_of_portfolio.append(portfolio_value)

            self.q5_stocks.append(np.percentile(year_of_stocks, 5))
            self.q10_stocks.append(np.percentile(year_of_stocks, 10))
            self.q25_stocks.append(np.percentile(year_of_stocks, 25))
            self.q75_stocks.append(np.percentile(year_of_stocks, 75))
            self.q90_stocks.append(np.percentile(year_of_stocks, 90))
            self.q95_stocks.append(np.percentile(year_of_stocks, 95))

            self.q5_bonds.append(np.percentile(year_of_bonds, 5))
            self.q10_bonds.append(np.percentile(year_of_bonds, 10))
            self.q25_bonds.append(np.percentile(year_of_bonds, 25))
            self.q75_bonds.append(np.percentile(year_of_bonds, 75))
            self.q90_bonds.append(np.percentile(year_of_bonds, 90))
            self.q95_bonds.append(np.percentile(year_of_bonds, 95))

            self.q5_portfolio.append(np.percentile(year_of_portfolio, 5))
            self.q10_portfolio.append(np.percentile(year_of_portfolio, 10))
            self.q25_portfolio.append(np.percentile(year_of_portfolio, 25))
            self.q75_portfolio.append(np.percentile(year_of_portfolio, 75))
            self.q90_portfolio.append(np.percentile(year_of_portfolio, 90))
            self.q95_portfolio.append(np.percentile(year_of_portfolio, 95))


		####
        # CaLculate # of successful years (portfoliio has > $0.01 at end of year)
        # portfolio, stocks and bonds should have identical results since portfolio is rebalanced each year
        num_fails_portfolio = 0
        num_fails_stocks = 0
        num_fails_bonds = 0

        for i in range(len(self.sim_monte_carlo_results)):
            simulation = self.sim_monte_carlo_results[i]
    
            if (simulation[len(simulation)-1][2] < 0.01):
                num_fails_stocks += 1

            if (simulation[len(simulation)-1][3] < 0.01):
                num_fails_bonds += 1

            if (simulation[len(simulation)-1][4] < 0.01):
                num_fails_portfolio += 1

        percent_success_portfolio = 100*(1.0 - (num_fails_portfolio / (len(self.sim_monte_carlo_results))))
        percent_success_stocks = 100*(1.0 - (num_fails_stocks / (len(self.sim_monte_carlo_results))))
        percent_success_bonds = 100*(1.0 - (num_fails_bonds / (len(self.sim_monte_carlo_results))))

        ####
        # Calculate the chance of failure for each year of the simulation

        for y in range(len(self.sim_monte_carlo_results[0])):
            stock_fails = 0
            bond_fails = 0
            portfolio_fails = 0

            for i in range(sim_monte_carlo_iterations):
#                print("portfolio value = " + str(self.sim_monte_carlo_results[i][y][4]))
                if self.sim_monte_carlo_results[i][y][2] < 0.01:
                    stock_fails += 1
                if self.sim_monte_carlo_results[i][y][3] < 0.01:
                    bond_fails += 1
                if self.sim_monte_carlo_results[i][y][4] < 0.01:
                    portfolio_fails += 1

#            print("# fails = " + str(portfolio_fails))
#            fails_per_year_stocks.append(1 - (stock_fails / len(self.sim_monte_carlo_results)))
#            fails_per_year_bonds.append(1 - (bond_fails / len(self.sim_monte_carlo_results)))
            self.fails_per_year_portfolio.append(1 - (portfolio_fails / len(self.sim_monte_carlo_results)))

    ####
        ## print results to terminal
        print()
        print("===== Simulation Setup =====")
        print(f"Initial portfolio value = ${(total_initial_portfolio):,.0f}")
        print(f"Stocks = {(100*portfolio_starting_value_stocks / total_initial_portfolio):.1f}%")
        print(f"Bonds = {(100*portfolio_starting_value_bonds / total_initial_portfolio):.1f}%")
        print(f"Annual Withdrawal, Tranche 1 = ${(portfolio_annual_withdrawal1):,.0f}")
        print(f"Duration of simulation, Tranche 1 = {sim_num_years1:d}")
        print(f"Annual Withdrawal, Tranche 2 = ${(portfolio_annual_withdrawal2):,.0f}")
        print(f"Duration of simulation, Tranche 2 = {sim_num_years2:d}")
        print(f"Annual Withdrawal, Tranche 3 = ${(portfolio_annual_withdrawal2):,.0f}")
        print(f"Duration of simulation, Tranche 3 = {sim_num_years3:d}")
        print(f"Monte Carlo iterations = {sim_monte_carlo_iterations:d}")
        print("Returns are adjusted for inflation")
        print("Returns are calculated, then annual withdraw is taken")
        print("Portfolio is rebalanced each year after growth and withdraw are factored")

        print()
        print("===== Full Portfolio Results =====")
        print("5% quantile = ${:,.2f}".format(self.q5_portfolio[len(self.q5_portfolio)-1]))
        print("10% quantile = ${:,.2f}".format(self.q10_portfolio[len(self.q10_portfolio)-1]))
        print("25% quartile = ${:,.2f}".format(self.q25_portfolio[len(self.q25_portfolio)-1]))
        print("75% quartile = ${:,.2f}".format(self.q75_portfolio[len(self.q75_portfolio)-1]))
        print("90% quantile = ${:,.2f}".format(self.q90_portfolio[len(self.q90_portfolio)-1]))
        print("95% quantile = ${:,.2f}".format(self.q95_portfolio[len(self.q95_portfolio)-1]))
        print(f"Portfolio success rate = {len(self.sim_monte_carlo_results)-num_fails_portfolio:d}/{len(self.sim_monte_carlo_results):d} = {percent_success_portfolio:.1f}%")

        print()
        print("===== Stock Portfolio Results =====")
        print("5% quantile = ${:,.2f}".format(self.q5_stocks[len(self.q5_stocks)-1]))
        print("10% quantile = ${:,.2f}".format(self.q10_stocks[len(self.q10_stocks)-1]))
        print("25% quartile = ${:,.2f}".format(self.q25_stocks[len(self.q25_stocks)-1]))
        print("75% quartile = ${:,.2f}".format(self.q75_stocks[len(self.q75_stocks)-1]))
        print("90% quantile = ${:,.2f}".format(self.q90_stocks[len(self.q90_stocks)-1]))
        print("95% quantile = ${:,.2f}".format(self.q95_stocks[len(self.q95_stocks)-1]))
        print(f"Stocks success rate = {len(self.sim_monte_carlo_results)-num_fails_stocks:d}/{len(self.sim_monte_carlo_results):d} = {percent_success_stocks:.1f}%")

        print()
        print("===== Bond Portfolio Results =====")
        print("5% quantile = ${:,.2f}".format(self.q5_bonds[len(self.q5_bonds)-1]))
        print("10% quantile = ${:,.2f}".format(self.q10_bonds[len(self.q10_bonds)-1]))
        print("25% quartile = ${:,.2f}".format(self.q25_bonds[len(self.q25_bonds)-1]))
        print("75% quartile = ${:,.2f}".format(self.q75_bonds[len(self.q75_bonds)-1]))
        print("90% quantile = ${:,.2f}".format(self.q90_bonds[len(self.q90_bonds)-1]))
        print("95% quantile = ${:,.2f}".format(self.q95_bonds[len(self.q95_bonds)-1]))
        print(f"Bonds success rate = {len(self.sim_monte_carlo_results)-num_fails_bonds:d}/{len(self.sim_monte_carlo_results):d} = {percent_success_bonds:.1f}%")

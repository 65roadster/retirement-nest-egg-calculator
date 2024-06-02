####
# go do what you want with this code

import os
import tkinter as tk
import locale
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FixedLocator
from simulator import simulator

os.system('cls')

####
# Initial values for GUI
total_initial_portfolio = 2.5e6
stock_allocation = 70
portfolio_annual_withdrawal = 100e3
sim_num_years = 40

####
# Simulation parameters not in GUI
sim_monte_carlo_iterations = 10000

sim = simulator()

####
# Performs simulation
def simulate():
    global total_initial_portfolio
    global stock_allocation
    global portfolio_annual_withdrawal
    global sim_num_years
    global sim_monte_carlo_iterations
    global sim

    sim.clear()
    sim.simulate(total_initial_portfolio, stock_allocation/100, portfolio_annual_withdrawal, sim_num_years, sim_monte_carlo_iterations)

####
# Updates GUI graphs
def update_graphs():

    # Create x axis array
    years = []
    sim_results = sim.sim_monte_carlo_results[0]
    for y in range(len(sim_results)):
        years.append(y)

    # Create x axis ticks for GUI graphs
    x_ticks = years[::2]  # Select every other value from x
    plt.gca().xaxis.set_major_locator(FixedLocator(x_ticks))

    # this is used to format the Y axis as dollars in the matplotlib figures
    def dollar_formatter(x, pos):
        return '${:,.0f}'.format(x)

    formatter = FuncFormatter(dollar_formatter)

    # Figure out how to scale the Y axis. This works OK, not the best
    y_min = 0
    y_max = max(sim.q95_portfolio)
    y_step = 100000

    if (y_max < 15 * 1000): # $15k
        y_max = 15 * 1000
        y_step = 1000
    elif (y_max < 15 * 2000): # $30k
        y_max = 15 * 2000
        y_step = 2000
    elif (y_max < 50e3): # $50k
        y_max = 50e3
        y_step = 5000
    elif (y_max < 75e3): # $75k
        y_max = 75e3
        y_step = 5000
    elif (y_max < 150e3): # $150k
        y_max = 150e3
        y_step = 10e3
    elif (y_max < 300e3): # $300k
        y_max = 300e3
        y_step = 20e3
    elif (y_max < 500e3): # $500k
        y_max = 500e3
        y_step = 50e3
    elif (y_max < 750e3): # $750k
        y_max = 750e3
        y_step = 50e3
    elif (y_max < 1.5e6): # $1.5M
        y_max = 1.5e6
        y_step = 100e3
    elif (y_max < 3e6): # $3M
        y_max = 3e6
        y_step = 200e3
    elif (y_max < 5e6): # $5M
        y_max = 5e6
        y_step = 500e3
    elif (y_max < 7.5e6): # $7.5M
        y_max = 7.5e6
        y_step = 500e3
    elif (y_max < 15e6): # $15M
        y_max = 15e6
        y_step = 1e6
    elif (y_max < 30e6): # $30M
        y_max = 30e6
        y_step = 2e6
    elif (y_max < 50e6): # $50M
        y_max = 50e6
        y_step = 5e6
    elif (y_max < 75e6): # $75M
        y_max = 75e6
        y_step = 5e6
    elif (y_max < 150e6): # $150M
        y_max = 150e6
        y_step = 10e6
    elif (y_max < 300e6): # $300M
        y_max = 300e6
        y_step = 20e6
    elif (y_max < 500e6): # $500M
        y_max = 500e6
        y_step = 50e6
    elif (y_max < 750e6): # $750M
        y_max = 750e6
        y_step = 50e6
    elif (y_max < 1.5e9): # $1.5B
        y_max = 1.5e9
        y_step = 100e6
    else:
        y_step = y_max / 15

    # Set the tick marks for the GUI graph
    y_ticks = np.arange(y_min, y_max + y_step, y_step)

    global ax
	
	# Clear prior results from GUI graphs
    ax[0,0].clear()
    ax[0,1].clear()
    ax[1,0].clear()
    ax[1,1].clear()

    ax[0,0].yaxis.set_major_formatter(formatter)
    ax[0,0].fill_between(years, sim.q5_portfolio,  sim.q95_portfolio, alpha=.4, linewidth=0)
    ax[0,0].fill_between(years, sim.q10_portfolio, sim.q90_portfolio, alpha=.4, linewidth=0)
    ax[0,0].fill_between(years, sim.q25_portfolio, sim.q75_portfolio, alpha=.4, linewidth=0)
    ax[0,0].set_yticks(y_ticks)
    ax[0,0].set_ylim(y_min, y_max)
    ax[0,0].set_title('Portfolio Value by Year with 50%, 80%, 90% Quantiles')
    #ax[0,0].set_xlabel('Year')
    #ax[0,0].set_ylabel('Portfolio Value')
    ax[0,0].set_xticks(x_ticks)
    ax[0,0].grid(True)

    ax[0,1].yaxis.set_major_formatter(formatter)
    ax[0,1].fill_between(years, sim.q5_stocks,  sim.q95_stocks, alpha=.4, linewidth=0)
    ax[0,1].fill_between(years, sim.q10_stocks, sim.q90_stocks, alpha=.4, linewidth=0)
    ax[0,1].fill_between(years, sim.q25_stocks, sim.q75_stocks, alpha=.4, linewidth=0)
    ax[0,1].set_yticks(y_ticks)
    ax[0,1].set_ylim(y_min, y_max)
    ax[0,1].set_title('Portfolio Value by Year, Stocks Results with 50%, 80%, 90% Quantiles')
    #ax[0,1].set_xlabel('Year')
    #ax[0,1].set_ylabel('Portfolio Value')
    ax[0,1].set_xticks(x_ticks)
    ax[0,1].grid(True)

    ax[1,0].yaxis.set_major_formatter(formatter)
    ax[1,0].fill_between(years, sim.q5_bonds,  sim.q95_bonds, alpha=.4, linewidth=0)
    ax[1,0].fill_between(years, sim.q10_bonds, sim.q90_bonds, alpha=.4, linewidth=0)
    ax[1,0].fill_between(years, sim.q25_bonds, sim.q75_bonds, alpha=.4, linewidth=0)
    ax[1,0].set_yticks(y_ticks)
    ax[1,1].set_ylim(y_min, y_max)
    ax[1,0].set_title('Portfolio Value by Year, Bonds Results with 50%, 80%, 90% Quantiles')
    #ax[1,0].set_xlabel('Year')
    #ax[1,0].set_ylabel('Portfolio Value')
    ax[1,0].set_xticks(x_ticks)
    ax[1,0].grid(True)



    def linear_interpolation(y, y1, y2, x1, x2):
        return x1 + ((y - y1) / (y2 - y1)) * (x2 - x1)

    def find_interpolated_x(y, x_values, y_values):
        # Find the index of the nearest value less than x
        idx = max([i for i, val in enumerate(y_values) if val > y])
        if (idx == len(y_values)-1):
            idx -= 1
        # Use linear interpolation between the two nearest points
        return linear_interpolation(y, y_values[idx], y_values[idx + 1], x_values[idx], x_values[idx + 1])

    interpolated_x85 = find_interpolated_x(0.85, years, sim.fails_per_year_portfolio)
    interpolated_x80 = find_interpolated_x(0.80, years, sim.fails_per_year_portfolio)
	
    ax[1,1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax[1,1].plot(years, sim.fails_per_year_portfolio, label="portfolio")
    ax[1,1].axhline(y=0.85, color='r', linestyle='--', alpha = 0.3)
    ax[1,1].axhline(y=0.80, color='r', linestyle='--', alpha = 0.3)
    ax[1,1].axvline(x=interpolated_x85, color='r', linestyle='--', alpha = 0.3)
    ax[1,1].axvline(x=interpolated_x80, color='r', linestyle='--', alpha = 0.3)
    ax[1,1].set_ylim(0,0.1)
    ax[1,1].set_title('Likelihood of portfolio lasting each year')
    #ax[1,1].set_xlabel('Year')
    #ax[1,1].set_ylabel('Chance of Success')
    ax[1,1].set_xticks(x_ticks)
    y_ticks = np.arange(0, 1.1, 0.1)
    ax[1,1].set_yticks(y_ticks)
    ax[1,1].grid(True)

    # set x axis scale so it equals the simulation range
    for a in ax.flat:
        a.set_xlim(min(years), max(years))

    # Update the graphs
    canvas.draw()


# Simulation Wrapper
def simulate_wrapper():
    simulate()
    update_graphs()

####
# Update GUI when sliders move
def on_slider_update_allocation(value):
    global stock_allocation
    stock_allocation = int(value)
    label_slider_allocation_value.config(text=f"{value}%")

def on_slider_update_balance(value):
    global total_initial_portfolio
    total_initial_portfolio = int(value)
    
    locale.setlocale(locale.LC_ALL, '')  # Set locale for correct thousand separators
    value_str = locale.format_string("%d", int(value), grouping=True)
    label_balance_slider_value.config(text=f"${value_str}", font=("Helvetica", 14))

    on_slider_update_withdrawal(portfolio_annual_withdrawal)

def on_slider_update_withdrawal(value):
    global portfolio_annual_withdrawal
    portfolio_annual_withdrawal = int(value)
	
    percent_of_portfolio = 100*portfolio_annual_withdrawal/total_initial_portfolio

    locale.setlocale(locale.LC_ALL, '')  # Set locale for correct thousand separators
    value_str = locale.format_string("%d", int(value), grouping=True)
    label_withdrawal_slider_value.config(text=f"${value_str} ({percent_of_portfolio:.2f}%)", font=("Helvetica", 14))

def on_slider_update_duration(value):
    global sim_num_years
    sim_num_years = int(value)
    
    locale.setlocale(locale.LC_ALL, '')  # Set locale for correct thousand separators
    value_str = locale.format_string("%d", int(value), grouping=True)
    label_duration_slider_value.config(text=f"{value_str} years", font=("Helvetica", 14))

def on_closing():
    plt.close()  # This avoids a long shutdown time for the app
    root.destroy()

root = tk.Tk()
root.title("Retirement Nest Egg Simulator")

# Set window size in pixels. This should be improved
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
geo = "" + str(min(0.9*screen_width, 2150)) + "x" + str(min(0.9*screen_height, 1000))
#root.geometry("2150x1000")
root.geometry(geo)

# Create GUI elements
label_balance_slider = tk.Label(root, text="Balance:", font=("Helvetica", 14))
label_balance_slider.grid(row=0, column=0, padx=10, pady=10, sticky="e")

slider_balance = tk.Scale(root, from_=0, to=5000000, orient="horizontal", tickinterval=0, resolution=100000, showvalue=False, command=on_slider_update_balance, length=400)
slider_balance.grid(row=0, column=1, padx=10, pady=10, sticky="w")
slider_balance.set(total_initial_portfolio)

label_balance_slider_value = tk.Label(root, text="$0", font=("Helvetica", 14))
label_balance_slider_value.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Stock Allocation Slider
label_allocation = tk.Label(root, text="Stock Allocation:", font=("Helvetica", 14))
label_allocation.grid(row=1, column=0, padx=10, pady=10, sticky="e")

slider_allocation = tk.Scale(root, from_=0, to=100, orient="horizontal", tickinterval=0, resolution=5, command=on_slider_update_allocation, showvalue=False, length=400)
slider_allocation.grid(row=1, column=1, padx=10, pady=10, sticky="w")
slider_allocation.set(stock_allocation)

label_slider_allocation_value = tk.Label(root, text="0%", font=("Helvetica", 14))
label_slider_allocation_value.grid(row=1, column=2, padx=10, pady=10, sticky="w")

label_withdrawal_slider = tk.Label(root, text="Annual Withdrawal:", font=("Helvetica", 14))
label_withdrawal_slider.grid(row=2, column=0, padx=10, pady=10, sticky="e")

slider_withdrawal = tk.Scale(root, from_=0, to=500000, orient="horizontal", tickinterval=0, resolution=5000, showvalue=False, command=on_slider_update_withdrawal, length=400)
slider_withdrawal.grid(row=2, column=1, padx=10, pady=10, sticky="w")
slider_withdrawal.set(portfolio_annual_withdrawal)

label_withdrawal_slider_value = tk.Label(root, text="$0", font=("Helvetica", 14))
label_withdrawal_slider_value.grid(row=2, column=2, padx=10, pady=10, sticky="w")

label_duration_slider = tk.Label(root, text="Duration of Simulation:", font=("Helvetica", 14))
label_duration_slider.grid(row=3, column=0, padx=10, pady=10, sticky="e")

slider_duration = tk.Scale(root, from_=0, to=50, orient="horizontal", tickinterval=0, resolution=1, showvalue=False, command=on_slider_update_duration, length=400)
slider_duration.grid(row=3, column=1, padx=10, pady=10, sticky="w")
slider_duration.set(sim_num_years)

label_duration_slider_value = tk.Label(root, text="$0", font=("Helvetica", 14))
label_duration_slider_value.grid(row=3, column=2, padx=10, pady=10, sticky="w")

button_simulate = tk.Button(root, text="Simulate", command=simulate_wrapper, font=("Helvetica", 14))
button_simulate.grid(row=4, column=0, columnspan=3, pady=20)

# Customize column 3 (graphs) to stretch with window size
root.grid_columnconfigure(3, weight=1, minsize=800, pad=0)

# Matplotlib Plot
fig, ax = plt.subplots(2, 2, figsize=(16, 10))

ax[0,0].set_title('Portfolio Value by Year with 50%, 80%, 90% Quantiles')
ax[0,0].grid(True)

ax[0,1].set_title('Portfolio Value by Year, Stocks Results with 50%, 80%, 90% Quantiles')
ax[0,1].grid(True)

ax[1,0].set_title('Portfolio Value by Year, Bonds Results with 50%, 80%, 90% Quantiles')
ax[1,0].grid(True)

ax[1,1].set_title('Likelihood of portfolio lasting each year')
ax[1,1].grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=3, rowspan=16, padx=0, pady=0, sticky="nsew")

root.protocol("WM_DELETE_WINDOW", on_closing)  # Call on_closing function when closing window

root.mainloop()
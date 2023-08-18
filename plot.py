
from offer import Bonus, Offer, Level, City 
import taxes
import numpy as np
from typing import List
from analysis import Result 
from matplotlib import pyplot as plt

def plot_values(values, title='plot', names = None):
    for i,Y in enumerate(values):
        X = [i/4.0 for i in range(len(Y))]
        plt.plot(X, Y, label = names[i] if names is not None else None , marker="o")

    if names is not None:
        plt.legend()
    plt.grid(True)
    plt.title(title)
    pass

def plot_cashflows(results : List[Result]):
    noffers = len(results)
    labels = ["%s (%s)" % (result.offer.label, result.city.label) for result in results]
    
    plt.subplot(211)
    plot_values([result.net_worth for result in results], title='Net Worth',names=labels)
    plt.ylabel("Hundred Thousand USD")
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,
        labelbottom=False) # labels along the bottom edge are off
    #plot_values([np.cumsum(headlands), np.cumsum(hrt)], title='Total Cumulative Profits',names=['Headlands', 'HRT'])
    
    plt.subplot(212)
    plot_values([result.net_cashflow for result in results], title='Net Cashflow (quarterly, after-tax)')
    plt.xlabel("Years")

    plt.show()
    pass

def plot_results(results : List[Result]):
    plot_cashflows(results)
    pass
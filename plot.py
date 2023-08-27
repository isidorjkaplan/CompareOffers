
from offer import Bonus, Offer, Level, City 
import taxes
import numpy as np
from typing import List
from analysis import Result 
from matplotlib import pyplot as plt


def plot_values(values, title='plot', names = None, quarterly = True):
    for i,Y in enumerate(values):
        X = [i/4.0 if quarterly else i for i in range(len(Y))]
        plt.plot(X, Y, label = names[i] if names is not None else None , marker="o")

    if names is not None:
        plt.legend()
    plt.grid(True)
    plt.title(title)
    pass

def plot_quarterly(results : List[Result]):
    noffers = len(results)
    labels = ["%s (%s)" % (result.offer.label, result.city.label) for result in results]
    
    plt.subplot(211)
    plot_values([result.net_worth for result in results], title='Net Worth',names=labels)
    plt.ylabel("$1,000 USD")

    #plot_values([np.cumsum(headlands), np.cumsum(hrt)], title='Total Cumulative Profits',names=['Headlands', 'HRT'])
    
    plt.subplot(212)
    plot_values([result.savings_cashflow for result in results], title='Net Savings (quarterly)')
    plt.xlabel("Years")

    plt.show()
    pass

def annualize(arr, agg_func = np.sum) -> list:
    return [agg_func(arr[i:(i+4)]) for i in range(0, len(arr), 4)]

def plot_yearly(results : List[Result]):
    noffers = len(results)
    labels = ["%s (%s)" % (result.offer.label, result.city.label) for result in results]
    
    plt.subplot(221)
    plot_values([annualize(result.net_worth, lambda arr: arr[0]) for result in results], title='Net Worth (Start Of Year)',names=labels, quarterly=False)
    plt.ylabel("Hundred Thousand USD")

    #plot_values([np.cumsum(headlands), np.cumsum(hrt)], title='Total Cumulative Profits',names=['Headlands', 'HRT'])
    
    plt.subplot(222)
    plot_values([annualize(result.raw_cashflow) for result in results], title='Raw TC (yearly)', quarterly=False)

    plt.subplot(223)
    plot_values([annualize(result.taxed_cashflow) for result in results], title='After-Tax TC (yearly)', quarterly=False)

    plt.subplot(224)
    plot_values([annualize(result.savings_cashflow) for result in results], title='Net Savings (yearly)', quarterly=False)
    
    plt.xlabel("Calender Year Number")


    plt.show()

def plot_results(results : List[Result]):
    plot_quarterly(results)
    plot_yearly(results)
    pass
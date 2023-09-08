
from offer import Bonus, Offer, Level, City 
import taxes
import numpy as np
from typing import List
from analysis import Result, annualize
from matplotlib import pyplot as plt

# A global that someone can just set
start_year = 2024

def plot_values(values, title='plot', names = None, x_scalar=1):
    maxX = []
    for i,Y in enumerate(values):
        X = [i/x_scalar for i in range(len(Y))]
        if len(X) > len(maxX):
            maxX = X
        plt.plot(X, Y, label = names[i] if names is not None else None , marker="o")
    
    if start_year is not None:
        plt.xticks([int(x) for x in X if x==int(x)], [int(x+start_year) for x in X if x==int(x)] )

    if names is not None:
        plt.legend()
    plt.grid(True)
    plt.title(title)
    pass

def plot_results(results : List[Result]):
    noffers = len(results)
    labels = ["%s (%s)" % (result.offer.label, result.city.label) for result in results]
    
    plt.subplot(331)
    plot_values([result.net_worth for result in results], title='Net Worth (yearly)',names=labels, x_scalar=4)
    plt.ylabel("$1,000")

    plt.subplot(332)
    plt.ylabel("$1,000")
    plot_values([result.savings_cashflow for result in results], title='Net Savings (quarterly)', x_scalar=4)

    plt.subplot(333)
    plot_values([result.net_worth/results[0].net_worth for result in results], title='Net Worth Normalized (yearly)', x_scalar=4)
    plt.ylabel("Versus %s" % labels[0])
   
    plt.subplot(334)
    plt.ylabel("$1,000")
    plot_values([annualize(result.raw_cashflow) for result in results], title='Raw TC (yearly)')

    plt.subplot(335)
    plt.ylabel("$1,000")
    plot_values([annualize(result.taxed_cashflow) for result in results], title='After-Tax TC (yearly)')

    plt.subplot(336)
    plt.ylabel("$1,000")
    plot_values([annualize(result.savings_cashflow) for result in results], title='Net Savings (yearly)')

    plt.subplot(337)
    plt.ylabel("Percentage")
    plot_values([[100 * taxes.calc_avg_rate(result.city.tax_func, x) for x in annualize(result.raw_cashflow)] for result in results], 
        title='Average Tax Rate')

    plt.subplot(338)
    #plot_values([[100 * taxes.calc_marginal_rate(result.city.tax_func, x) for x in annualize(result.raw_cashflow)] for result in results], title='Marginal Tax Rate')
    plot_values([1000*result.eff_hourly for result in results], title='Effective Hourly Savings')
    plt.ylabel('Dollers')

    plt.subplot(339)
    plt.ylabel("Percentage")
    plot_values([100*np.array(annualize(result.savings_cashflow))/np.array(annualize(result.taxed_cashflow)) for result in results], 
        title='Savings Rate ( savings / taxed TC )')

    plt.subplots_adjust(0.05,0.05,.95,.95)

    plt.show()

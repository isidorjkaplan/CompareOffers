
from offer import Bonus, Offer, Level, City 
from collections import namedtuple
from typing import List
import taxes
import numpy as np

# Superimpose one cashflow onto another starting at start_pos
def grant_bonus(result, bonus : Bonus, grant_pos=0):
    assert isinstance(bonus, Bonus)
    pos = grant_pos
    for pct in bonus.quarterly_vesting:
        if pos >= len(result):
            break
        result[pos] += pct*bonus.face_value
        pos+=1
    
# Conert an offer into a series of quarterly cashflows
def gen_raw_offer_cashflow(offer : Offer, years : int, start_quarter : int = 0) -> np.ndarray:
    print("Generating offer raw cashflow: %s" % offer.label)
    result = np.zeros((years*4,))
    grant_bonus(result, offer.sign_bonus, start_quarter)
    N = len(result)
    pos = start_quarter
    for level_num,duration in enumerate(offer.promotion + [years]):
        if pos >= N: break
        level : Level = offer.levels[level_num]
        print("\tGenerating level %s for %d years" % (level.label, duration))
        # Apply base salary for entire time we spend at this level
        next_pos = min((pos+duration*4), N)
        result[pos : next_pos] += level.base/4
        # Apply bonus for entire time at this level
        for bonus in level.bonus_arr:
            bonus : Bonus
            first_grant = True
            for grant_pos in range(pos, next_pos):
                if grant_pos % bonus.grant_freq == 0 and grant_pos != 0:
                    if first_grant and level_num==0 and start_quarter != 0:
                        # EDGE CASE: Scale down first bonus grant by percentage of the bonus period we worked
                        # i.e, if we start half-way through the year only get half of the first yearly bonus target
                        grant_bonus(result, Bonus(bonus.label, bonus.face_value * (grant_pos-start_quarter)/bonus.grant_freq, bonus.quarterly_vesting, None), grant_pos)
                    else:
                        grant_bonus(result, bonus, grant_pos )
                    first_grant = False
                    pass
        pos = next_pos
        
    return result

def apply_taxes(result, city : City) -> np.ndarray:
    result = np.copy(result)
    for pos in range(0, len(result), 4):
        year_slice = result[pos:min((pos+4), len(result))]
        year_slice *= 1-taxes.calc_avg_rate(city.tax_func, np.sum(year_slice))
    return result

# Apply taxes and cost of living to a cashflow
def apply_col(result, city : City, start_quarter) -> np.ndarray:
    result = np.copy(result)
    result[start_quarter:] -= city.yearly_col/4
    return result 

# Generate the net-worth of a cash-flow at each time interval under some assumed interest rate
def calc_future_value(cashflow, interest_rate : float) -> List[float]:
    quarter_factor = pow(interest_rate+1, 1/4)
    cum = 0
    result = []
    for value in cashflow:
        # Savings grows by this interest rate last quarter
        cum *= quarter_factor
        # We also made this much money over the quarter
        cum += value 
        # Record it
        result.append(cum)
    return result

from collections import namedtuple
Result = namedtuple('Result', 'offer city raw_cashflow taxed_cashflow savings_cashflow net_worth')

# Evaluate an offer in a given city under some specified conditions
def evaluate(offer : Offer, city : City, interest_rate = 0, years : int = 5, start_quarter : int = 0):
    raw_cashflow = gen_raw_offer_cashflow(offer, years, start_quarter)
    taxed_cashflow = apply_taxes(raw_cashflow, city)
    savings_cashflow = apply_col(taxed_cashflow, city, start_quarter)
    net_worth = calc_future_value(savings_cashflow, interest_rate)
    return Result(offer, city, raw_cashflow, taxed_cashflow, savings_cashflow, net_worth)
    pass

def scale_offer(offer : Offer, factor : float) -> Offer:
    return offer #TBD
    pass

def scale_city(city : City, factor : float) -> City:
    return City(city.label, city.yearly_col*factor, lambda x: factor*city.tax_func(x/factor))

# Scale all fields of an offer by an scalar multiple, useful for currency conversions
def scale_result(result : Result, factor : float) -> Result:
    return Result(scale_offer(result.offer, factor), scale_city(result.city, factor), np.array(result.raw_cashflow)*factor, factor*np.array(result.taxed_cashflow), factor*np.array(result.savings_cashflow), factor*np.array(result.net_worth))
    pass

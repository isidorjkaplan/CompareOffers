# FILE CONTAINS ALL INFORMATION NEEDED TO EVALUATE TAXES

# Format for tables is [ (income_bracket, marginal_rate) ]

# US, Federal Taxes
federal_tax_table = [
    (0,         0),
    (11.000, 	12.0 / 100.0),
    (44.725, 	22.0 / 100.0),
    (95.375, 	24.0 / 100.0),
    (182.100, 	32.0 / 100.0),
    (231.250, 	35.0 / 100.0),
    (578.125, 	37.0 / 100.0),
]

# New York, US, State Taxes
new_york_state_tax_table = [
    (0,      4.0 / 100.0),
    (8.500,   4.5 / 100.0),
    (11.700,  5.25 / 100.0),
    (13.900,  5.85 / 100.0),
    (80.650,  6.25 / 100.0),
    (215.400, 6.85 / 100.0),
    (1077.550,9.65 / 100.0)
]

# New York City Taxes
new_york_city_tax_table = [
    (0,         3.078 / 100.0),
    (12.000,     3.762 / 100.0),
    (25.000,     3.819 / 100.0),
    (50.000,     3.876 / 100.0)
]

# New Jersey, US, State Taxes
new_jersey_tax_table = [
    (0, 0.03464), # not strictly accurate, but accurate over 75k
    (75.000, 6.37 / 100.0),
    (500,   8.97 / 100.0),
    (1000,  10.75 / 100.0)
]

# Cakifornia, US, State Taxes
cali_tax_table = [
    (0, 0.02732800362), # accurate over 66k
    (66.296,  9.3 / 100),
    (338.639, 10.3 / 100),
    (406.3,   11.3 / 100),
    (677.275, 12.3 / 100)
]

# Canada + Ontario Tax Table
# Quick and dirty aproximation which should be updated
canada_and_ontario_aproximate_tax_table = [
    (0, 26.35 / 100),
    (100, 33.89 / 100),
    (110, 43.41 / 100),
    (160, 44.97 / 100),
    (170, 47.97 / 100),
    (273, 53.53 / 100)
]

# Some taxes that are flat income based

nyc_commuter_tax_rate = 0.6 / 100.0

illinois_tax_rate = 4.95 / 100.0

fica_max_income =  160.200 
fica_tax_rate = 6.2 / 100.0

medicare_tax_base_rate = 1.45 / 100.0
medicate_tax_bonus_rate = 0.9 / 100.0
medicare_tax_bonus_amount = 200.000


# TAX FUNCTIONS

# This function takes a progressive income tax table and an income and evaluates it
def calc_progressive_tax(table, income : float):
    tax = 0
    last_rate = 0
    last_bracket = 0
    for (bracket, rate) in table:
        tax += (min(bracket,income)-last_bracket)*last_rate
        if bracket >= income:
            return tax
        last_rate, last_bracket = rate, bracket
    
    tax += (income-last_bracket)*last_rate
    return tax

def calc_federal_tax(income : float):
    return calc_progressive_tax(federal_tax_table, income)

def calc_fica_tax(income : float):
    return min(income, fica_max_income)*fica_tax_rate

def calc_medicare_tax(income : float):
    return medicare_tax_base_rate*income + min(medicare_tax_bonus_amount-income, 0)*medicate_tax_bonus_rate

def calc_total_fed_tax(income : float):
    return calc_federal_tax(income) + calc_fica_tax(income) + calc_medicare_tax(income)

def calc_ny_city_tax(income : float):
    return calc_progressive_tax(new_york_city_tax_table, income)

def calc_ny_state_tax(income : float):
    return calc_progressive_tax(new_york_state_tax_table, income)

def calc_il_state_tax(income : float):
    return illinois_tax_rate*income

def calc_nj_state_tax(income : float):
    return calc_progressive_tax(new_jersey_tax_table, income)

def calc_cali_state_tax(income : float):
    return calc_progressive_tax(cali_tax_table, income)

# OVERALL OUTCOMES TAXES

def calc_nyc_total_tax(income : float):
    return calc_ny_city_tax(income) + calc_ny_state_tax(income) + calc_total_fed_tax(income)

def calc_jersey_total_tax(income : float):
    return calc_ny_state_tax(income) + calc_total_fed_tax(income)

def calc_chicago_total_tax(income : float):
    return calc_il_state_tax(income) + calc_total_fed_tax(income)

def calc_jersey_total_tax(income: float):
    return nyc_commuter_tax_rate*income + calc_nj_state_tax(income) + calc_total_fed_tax(income)

def calc_cali_total_tax(income: float):
    return calc_cali_state_tax(income) + calc_total_fed_tax(income)

def calc_ontario_total_tax(income: float):
    return calc_progressive_tax(canada_and_ontario_aproximate_tax_table, income)

# TAX OPERATORS

def calc_marginal_rate(tax_func, income : float):
    return tax_func(income+1)-tax_func(income)

def calc_avg_rate(tax_func, income : float):
    return tax_func(income)/income
    pass

def calc_after_tax(tax_func, income : float):
    return income - tax_func(income)

def noop(income : float):
    return income



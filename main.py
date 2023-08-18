import taxes
from offer import *
from analysis import evaluate
from plot import plot_results

def main():
    # City Guestimates (rent + col)
    # # rent is 2bdrm https://www.zumper.com/rent-research 
    # col is https://www.numbeo.com/cost-of-living/city-estimator
    city_chicago = City('Chicago', (2.795 + 2.770)*12, taxes.calc_chicago_total_tax)
    city_jersey  = City('Jersey' , (3.600 + 2.806)*12, taxes.calc_jersey_total_tax)
    city_nyc     = City('NYC' ,    (4.000 + 3.234)*12, taxes.calc_nyc_total_tax)
    city_sf      = City('Bay Area',(4.100 + 3.199)*12, taxes.calc_cali_total_tax)

    # Some constants that I will use for evaluating all the offers   
    params = {
        "start_quarter":2, # Start at beginning of Q3 since graduate then
        "interest_rate":0.05, #Assumed interest rate
        "years":3, # How many years to simulate
    } 

    # An example of a typical silicon-valley style vested offer with well-defined levels, from levels.fyi
    google_vest_arr = [0.38, 0.32, 0.20, 0.10]
    google_levels = [
        create_simple_level(label="L3", base=145, bonus=create_yearly_vested_bonus(50, google_vest_arr)),
        create_simple_level(label="L4", base=175, bonus=create_yearly_vested_bonus(95, google_vest_arr)),
        create_simple_level(label="L5", base=205, bonus=create_yearly_vested_bonus(168, google_vest_arr)),
        create_simple_level(label="L6", base=248, bonus=create_yearly_vested_bonus(300, google_vest_arr)),
    ]
    # An example of an quarterly-bonus vested offer using numbers for HRT from levels.fyi
    
    results = [
        evaluate(create_simple_offer("HRT", base=200, bonus=create_quarterly_uniform_bonus(150 / 4, 8), sign_bonus=100), city_jersey, **params),
        
        evaluate(create_offer("Google", google_levels, [1,3,5], sign_bonus=10), city_sf,  **params),
    ]

    plot_results(results)

    pass

if __name__ == "__main__":
    main()
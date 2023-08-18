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
        "years":10, # How many years to simulate
    } 


    # An example of a quant-style offer not modelling any leveling, from levels.fyi
    citadel_offer = create_simple_offer("Citadel", base=200, bonus=150, sign_bonus=50)
    # An example of a quant-style offer that vests quarterly, from levels.fyi
    hrt_offer = create_simple_offer("HRT", base=200, bonus=create_quarterly_uniform_bonus("Quarterly Bonus", 150 / 4, 8), sign_bonus=100)

    # An example of a typical silicon-valley style vested offer with well-defined levels
    google_vest_arr = [0.38, 0.32, 0.20, 0.10]
    google_levels = [
        create_simple_level("L3", base=145, bonus=create_yearly_vested_bonus("RSU", 50, google_vest_arr)),
        create_simple_level("L4", base=175, bonus=create_yearly_vested_bonus("RSU", 95, google_vest_arr)),
        create_simple_level("L5", base=205, bonus=create_yearly_vested_bonus("RSU", 168, google_vest_arr)),
        create_simple_level("L6", base=248, bonus=create_yearly_vested_bonus("RSU", 300, google_vest_arr)),
    ]
    google_offer = create_offer("Google", google_levels, [1,3,5], sign_bonus=10)
    
    results = [
        # Evaluating HRT in both New York versus commuting from Jersey (spoiler alert: live in jersey)
        #evaluate(hrt_offer, city_jersey, **params),
        evaluate(hrt_offer, city_nyc   , **params),

        #evaluate(citadel_offer, city_nyc, **params),
        evaluate(citadel_offer, city_chicago, **params),

        # Evaluating Google living in the Bay area
        evaluate(google_offer, city_sf,  **params),
    ]

    plot_results(results)

    pass

if __name__ == "__main__":
    main()
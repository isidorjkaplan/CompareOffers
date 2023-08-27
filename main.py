import taxes
from offer import *
from analysis import evaluate, scale_result
from plot import *

def main():
    # City Guestimates (rent + col)
    # # rent is 2bdrm https://www.zumper.com/rent-research 
    # col is https://www.numbeo.com/cost-of-living/city-estimator
    city_chicago = City('Chicago', (2.795 + 2.770)*12, taxes.calc_chicago_total_tax)
    city_jersey  = City('Jersey' , (3.600 + 2.806)*12, taxes.calc_jersey_total_tax)
    city_nyc     = City('NYC' ,    (4.000 + 3.234)*12, taxes.calc_nyc_total_tax)
    city_sf      = City('Bay Area',(4.100 + 3.199)*12, taxes.calc_cali_total_tax)
    city_seattle = City('Seattle', (2.768 + 3.224)*12, taxes.calc_total_fed_tax)
    city_toronto = City('Toronto', (3.299 + 3.431)*12, taxes.calc_ontario_total_tax)

    # Some constants that I will use for evaluating all the offers   
    params = {
        "start_quarter":2,    # Start at beginning of Q3 since graduate then
        "interest_rate":0.05, #Assumed real-return interest rate on net-worth investments
        "years":6,           # How many years to simulate
    } 

    cad_to_usd = 0.73473

    google_vest_arr = [0.38, 0.32, 0.20, 0.10]
    
    results = [

        evaluate(create_offer("Google", [
            create_simple_level(label="L3", base=145, bonus=create_yearly_vested_bonus(50, google_vest_arr)),
            create_simple_level(label="L4", base=175, bonus=create_yearly_vested_bonus(95, google_vest_arr)),
            create_simple_level(label="L5", base=205, bonus=create_yearly_vested_bonus(168, google_vest_arr)),
            create_simple_level(label="L6", base=248, bonus=create_yearly_vested_bonus(300, google_vest_arr)),
        ], [1,2,2], sign_bonus=10), city_seattle,  **params),

    ]

    plot_results(results)
    pass

if __name__ == "__main__":
    main()
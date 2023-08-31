import taxes
from offer import *
from analysis import evaluate, scale_result
from plot import *

def main():
    # City Guestimates (rent + col) in local currency
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
        "interest_rate":0.03, #Assumed real-return interest rate on net-worth investments
        "years":4,           # How many years to simulate
    } 

    cad_to_usd = 0.73473
    
    plot_results([

        evaluate(create_simple_offer("A", base=200, bonus=create_quarterly_uniform_bonus(100 / 4, 8), sign_bonus=100), city_nyc, **params),
        

        evaluate(create_simple_offer("B", base=200, bonus=100, sign_bonus=100), city_chicago, **params),  
    ] + [
        # GOOGLE
        evaluate(create_offer("Example FAANG style offer", levels=[
            create_simple_level(label=label, base=base, bonus=create_yearly_vested_bonus(bonus_val, [0.38, 0.32, 0.20, 0.10]))
            for (label, base, bonus_val) in [
                ("L3", 145, 50),
                ("L4", 175, 95),
                ("L5", 205, 168),
                ("L6", 248, 300),
            ]
        ], promotions=[1,2,3], sign_bonus=10), city,  **params)
        for city in [city_sf]
    ] + [
        # INTEL
        scale_result(evaluate(
                create_offer("Example Canadian Company", levels=[
                    create_simple_level(label=label, base=base, bonus=[
                        [
                            create_yearly_cash_bonus  (base * 3.3/100),         # APB as pct of base
                            create_quarterly_bonus    (base * 5.5/100/4 ),      # QPB as a pct of base
                            create_yearly_vested_bonus(rsu_grant, [1/3.0]*3)    # RSU stock grants
                        ]
                    ])
                    for (label, base, rsu_grant) in [
                        ("L5", 100, 5),
                        ("L6", 125, 12),
                        ("L7", 143, 23),
                    ]
                ], promotions=[1,1], sign_bonus=10), 
        city_toronto,  **params), cad_to_usd),
    ])
    pass

if __name__ == "__main__":
    main()
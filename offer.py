
# FILE CONTAINS ALL INFORMATION ABOUT YOUR OFFER

from collections import namedtuple 
from typing import Union, List
import numpy as np

# A bonus object representing a particular bonus that a company may have
#   label: What is the name of this bonus
#   face_value: What is the value of the grant (sum of all the vesting)
#   quarterly_vesting: An array containing percentage values of how much is vested over the following quarters (0 = on grant given)
#   grant_freq: Granted every grant_freq quarters. I.e put 4 for yearly and 2 for half-yearly and 1 for quarterly granted
#   raise_pct: A percentage [0,1] that your bonus goes up by annually
Bonus = namedtuple('Bonus', 'label face_value quarterly_vesting grant_freq raise_pct')
# A tuple of your base and target bonus
#   label: What is the name of your promotion level
#   base: What is your annual base salary
#   bonus_arr: A list of different bonus's that you get at this level (example, Intel has quarterly AND stock AND yearly)
Level = namedtuple('Level', 'label base bonus_arr')
# A tuple containing information about your offer including:
#   label: What do you want to label this offer name
#   levels: An array of the diffrent expected promotion levels at your company (see levels.fyi for example)
#   promotions: An array containing how many years you spend at each level. Implicitly tags on "infinity" to end of array.
#      i.e [1,3] would mean spend one year at first level, three at second, and then remaining years at third
#   sign_bonus: The signing bonus is a one-off granted 'Bonus' object (can be vested, grant freq ignored)
Offer = namedtuple('Offer', 'label levels promotion sign_bonus')
# A City object represents the location of your offer. It models cost-of-living, and taxes
City = namedtuple('City', 'label yearly_col tax_func')


# FACTORY FUNCTIONS FOR COMMON STUFF

# Create the Bonus representation from a bonus granted yearly in January
def create_yearly_vested_bonus(face_value, yearly_vesting, raise_pct=0, label='Vested Bonus'):
    quarterly_vesting = []
    for pct in yearly_vesting:
        quarterly_vesting.extend([pct, 0, 0, 0])
    return Bonus(label, face_value, quarterly_vesting, 4, raise_pct)

def create_sign_bonus(value, raise_pct=0, label='Sign Bonus'):
    return Bonus(label, value, [1.0], None, raise_pct)

# Create a bonus that is granted once per year 
def create_yearly_cash_bonus(value, raise_pct=0, label='Annual Cash Bonus'):
    return Bonus(label, value, [1.0], 4, raise_pct)

def create_quarterly_uniform_bonus(value, vest_quarters, raise_pct=0, label='Quarterly Bonus'):
    return Bonus(label, value, [1.0/vest_quarters]*vest_quarters, 1, raise_pct)

def create_quarterly_bonus(value, vesting=[1.0], raise_pct=0, label='Quarterly Bonus'):
    return Bonus(label, value, vesting, 1, raise_pct)

def create_hrt_bonus(total_amount, threshold, raise_pct=0, label='Bonus'):
    initial_amount = min(total_amount, threshold)
    quarterly_value = total_amount - initial_amount
    # Put the vesting portion of it into pct array
    vesting = np.array(create_quarterly_uniform_bonus(value=quarterly_value, vest_quarters=8).quarterly_vesting)
    # Scale down so that only the pct that is vested is vested
    vesting *= (quarterly_value / total_amount)
    # Add the initial threshold amount
    vesting[0] += (initial_amount / total_amount)
    return Bonus(label, total_amount, vesting, 1, raise_pct)
    pass

def create_base_only_level(base, label='Level'):
    return Level(label, base, [])

def create_bonus(bonus : Union[int,Bonus,list]) -> List[Bonus]:
    if isinstance(bonus, Bonus):
        return [bonus]
    if isinstance(bonus, list):
        result = []
        for b in bonus:
            result.extend(create_bonus(b))
        return result
    if isinstance(bonus, int):
        return [create_yearly_cash_bonus(bonus)]


# A level with a single bonus (most companies)
def create_simple_level(base, bonus, label='Level'):
    return Level(label, base, create_bonus(bonus))

# Create an offer 
def create_offer(label, levels : List[Level], promotions : List[int], sign_bonus: Union[int,Bonus]):
    if sign_bonus is not None and not isinstance(sign_bonus, Bonus):
        sign_bonus = create_sign_bonus(sign_bonus)
    return Offer(label, levels, promotions, sign_bonus)

# A simple offer containing only one level and simple bonuses
def create_simple_offer(label, base, bonus: Union[int,Bonus], sign_bonus: Union[int,Bonus]):
    if bonus is not None and not isinstance(bonus, Bonus):
        bonus = create_yearly_cash_bonus(bonus)
    return create_offer(label, [create_simple_level(base, bonus)], [], sign_bonus)


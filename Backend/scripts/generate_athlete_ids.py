from itertools import count
import random 
from countries import country_list
from pprint import pprint

# generate random 8 digit ids for athletes
generate_eight_digit_ids  = lambda: random.randint(100000000, 999999999)
    
# generate random 3 digit ids for ados
generate_five_digit_ids = lambda : random.randint(10000, 99999)


def generate_country_dict():
    country_dict = {}
    
    for country in country_list:
        country_dict[country] = generate_five_digit_ids()
        
    return country_dict 

def check_country_dict_uniqie():
    country_dict = generate_country_dict()
    if len(country_dict) == len(set(country_dict.values())):
        pprint(country_dict)
    else:
        print('feck')

check_country_dict_uniqie()
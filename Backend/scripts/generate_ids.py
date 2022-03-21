from itertools import count
import random 
from countries import country_list, country_dict
from pprint import pprint

# generate random 10 digit ids for athletes
generate_ten_digit_ids  = lambda: random.randint(10000000000, 99999999999)
    
# generate random 5 digit ids for ados
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

def create_country_ado_dict():
    
    all_country_ado_dict = {}
    for key, value in country_dict.items():
        #for testing purposes only
        if key == 'United States of America' or key == 'United Kingdom' or key == 'Canada' or key == 'Ireland':
            all_country_ado_dict[key] = {
                'Country': key,
                'Id': value,
                'Ado': key + ' ' + 'ADO'
            }
    
    for key, value in all_country_ado_dict.items():
        yield value
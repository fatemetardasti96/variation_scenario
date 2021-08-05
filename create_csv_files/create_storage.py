import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from create_block.storage_block import create_storage_block
from write_to_csv import seperator_to_csv
from find_parameters.general_parameter_handler import find_parameter_year_value
from find_parameters.compute_OaM_rate import compute_OaM_rate
from find_parameters.compute_total_cost import compute_total_cost


def create_storage(concrete_data, regions_data, cwd):

    storages = iterate_mapping(regions_data,"group_by(sort_by(scalars[? technology == 'storage'], &join('_',[technology, technology_type, input_energy_vector])),\
         &join('_',[technology, technology_type, input_energy_vector]))")
    
    interest_rate_list = iterate_mapping(concrete_data, "unique(oed_scalars[? parameter_name == 'WACC'].value)")
    
    if len(interest_rate_list) == 1:
        interest_rate = interest_rate_list[0]
    elif not len(interest_rate_list):
        interest_rate = 1
    else:
        logging.info("please consider further adjustment")
        raise Exception("multiple interest rate!")

    storage_list = []
    storage_list.append(["#comment","===============storage-technologies============================================"])
    storage_list.append(["#blockwise"])
    for elem in storages:
        technology, technology_type, inp_energy = elem.split('_')                        
        efficiency_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'efficiency', 2016, 1)
        efficiency_list = [{"year": 1900, "value": efficiency_list[0]["value"]}] + efficiency_list
        lifetime_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'lifetime', 2016, 0)
        lifetime_list = [{"year": 1900, "value": lifetime_list[0]["value"]}] + lifetime_list
        capital_cost_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'capital costs', 2016, 0)
        capital_cost_list = [{"year": 1900, "value": capital_cost_list[0]["value"]}] + capital_cost_list
        fixed_cost_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'fixed costs', 2016, 0)
        fixed_cost_list = [{"year": 1900, "value": fixed_cost_list[0]["value"]}] + fixed_cost_list
                        
        total_cost_list = compute_total_cost(interest_rate, lifetime_list, capital_cost_list)
        OaM_rate_list = compute_OaM_rate(interest_rate, lifetime_list, fixed_cost_list, capital_cost_list)

        create_storage_block(technology_type, efficiency_list, lifetime_list, total_cost_list, OaM_rate_list, storage_list)

    seperator_to_csv(storage_list, cwd+'/Storage.csv')
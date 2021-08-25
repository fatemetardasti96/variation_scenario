import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from find_parameters.transmission_param_handler import handle_transmission_param
from write_to_csv import seperator_to_csv
from create_block.transmission_block import create_transmission_block
from find_parameters.compute_OaM_rate import compute_OaM_rate
from find_parameters.compute_total_cost import compute_total_cost


def create_transmission(concrete_data, regions_data, cwd):

    transmission_installed_capacity = iterate_mapping(concrete_data, "oed_scalars[? (parameter_name == 'installed capacity' || parameter_name == 'expansion limit') && technology== 'transmission' && technology_type== 'hvac']")

    interest_rate_list = iterate_mapping(regions_data, "unique(scalars[? parameter_name == 'WACC'].value)")
    efficiency_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='output ratio'].value)")
    lifetime_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='lifetime'].value)")
    capital_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='capital costs'].value)")
    fixed_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='fixed costs'].value)")
    
    interest_rate = handle_transmission_param(interest_rate_list, 1, 'interest rate')
    efficiency = handle_transmission_param(efficiency_list, 1, 'output ratio')
    lifetime = handle_transmission_param(lifetime_list, 0, 'lifetime')
    capital_cost = handle_transmission_param(capital_cost_list, 0, 'capital cost')
    fixed_cost = handle_transmission_param(fixed_cost_list, 0, 'fixed cost')

    efficiency_list_installing = [{"year": 1900, "value": efficiency}, {"year": 2016, "value": efficiency}]
    lifetime_list_installing = [{"year": 1900, "value": lifetime}, {"year": 2016, "value": lifetime}]
    capital_cost_list_installing = [{"year": 1900, "value": capital_cost}, {"year": 2016, "value": capital_cost}]
    fixed_cost_list_installing = [{"year": 1900, "value": fixed_cost}, {"year": 2016, "value": fixed_cost}]

    total_cost_list = compute_total_cost(interest_rate, lifetime_list_installing, capital_cost_list_installing)
    OaM_rate_list = compute_OaM_rate(interest_rate, lifetime_list_installing, fixed_cost_list_installing, capital_cost_list_installing)
    

    transmission_list = []
    transmission_list.append(["#comment","===============transmission-technologies============================================"])
    transmission_list.append(["#blockwise"])
    code_list = []
    for elem in transmission_installed_capacity:
        region_A, region_B = elem['region']
        code  = 'hvac' + '_' + region_A + '_' + region_B
        if not code in code_list:
            create_transmission_block(code, efficiency_list_installing, total_cost_list, lifetime_list_installing, OaM_rate_list, transmission_list)
            code_list.append(code)
        else:
            continue

    transmission_installed_capacity_DC = iterate_mapping(concrete_data, "oed_scalars[? (parameter_name == 'installed capacity' || parameter_name == 'expansion limit') && technology== 'transmission' && technology_type== 'DC']")

    efficiency_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='output ratio'].value)")
    lifetime_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='lifetime'].value)")
    capital_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='capital costs'].value)")
    fixed_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='fixed costs'].value)")
    
    efficiency = handle_transmission_param(efficiency_list, 1, 'output ratio')
    lifetime = handle_transmission_param(lifetime_list, 0, 'lifetime')
    capital_cost = handle_transmission_param(capital_cost_list, 0, 'capital cost')
    fixed_cost = handle_transmission_param(fixed_cost_list, 0, 'fixed cost')

    efficiency_list_installing = [{"year": 1900, "value": efficiency}, {"year": 2016, "value": efficiency}]
    lifetime_list_installing = [{"year": 1900, "value": lifetime}, {"year": 2016, "value": lifetime}]
    capital_cost_list_installing = [{"year": 1900, "value": capital_cost}, {"year": 2016, "value": capital_cost}]
    fixed_cost_list_installing = [{"year": 1900, "value": fixed_cost}, {"year": 2016, "value": fixed_cost}]

    total_cost_list = compute_total_cost(interest_rate, lifetime_list_installing, capital_cost_list_installing)
    OaM_rate_list = compute_OaM_rate(interest_rate, lifetime_list_installing, fixed_cost_list_installing, capital_cost_list_installing)
    

    code_list = []
    for elem in transmission_installed_capacity_DC:
        region_A, region_B = elem['region']
        code  = 'hvac' + '_' + region_A + '_' + region_B
        if not code in code_list:
            create_transmission_block(code, efficiency_list_installing, total_cost_list, lifetime_list_installing, OaM_rate_list, transmission_list)
            code_list.append(code)
        else:
            continue

    seperator_to_csv(transmission_list, cwd+'/TransmissionConverter.csv')
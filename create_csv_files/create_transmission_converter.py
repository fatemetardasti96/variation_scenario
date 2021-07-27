import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from find_parameters.transmission_param_handler import handle_transmission_param
from write_to_csv import seperator_to_csv
from create_block.transmission_block import create_transmission_block


def create_transmission(concrete_data, regions_data, cwd):

    transmission_installed_capacity = iterate_mapping(concrete_data, "oed_scalars[? parameter_name == 'installed capacity' && technology== 'transmission' && technology_type== 'hvac']")

    interest_rate_list = iterate_mapping(regions_data, "unique(scalars[? parameter_name == 'WACC'].value)")
    efficiency_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='efficiency'].value)")
    lifetime_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='lifetime'].value)")
    capital_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='capital costs'].value)")
    fixed_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'hvac' && parameter_name=='fixed costs'].value)")
    
    interest_rate = handle_transmission_param(interest_rate_list, 1, 'interest rate')
    efficiency = handle_transmission_param(efficiency_list, 1, 'efficiency')
    lifetime = handle_transmission_param(lifetime_list, 0, 'lifetime')
    capital_cost = handle_transmission_param(capital_cost_list, 0, 'capital cost')
    fixed_cost = handle_transmission_param(fixed_cost_list, 0, 'fixed cost')

    ANF = (((1+interest_rate)**(lifetime))*interest_rate)/(((1+interest_rate)**(lifetime))-1)
    OaM_rate = float(fixed_cost)/float(capital_cost * ANF)
    total_cost = capital_cost * (ANF+1)
    

    transmission_list = []
    transmission_list.append(["#comment","===============transmission-technologies============================================"])
    transmission_list.append(["#blockwise"])
    code_list = []
    for elem in transmission_installed_capacity:
        region_A, region_B = elem['region']
        code  = 'hvac' + '_' + region_A + '_' + region_B
        if not code in code_list:
            create_transmission_block(code, efficiency, total_cost, lifetime, OaM_rate, transmission_list)
            code_list.append(code)
        else:
            continue

    transmission_installed_capacity_DC = iterate_mapping(concrete_data, "oed_scalars[? parameter_name == 'installed capacity' && technology== 'transmission' && technology_type== 'DC']")

    efficiency_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='efficiency'].value)")
    lifetime_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='lifetime'].value)")
    capital_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='capital costs'].value)")
    fixed_cost_list = iterate_mapping(concrete_data, "unique(oed_scalars[? technology == 'transmission' && technology_type== 'DC' && parameter_name=='fixed costs'].value)")
    
    efficiency = handle_transmission_param(efficiency_list, 1, 'efficiency')
    lifetime = handle_transmission_param(lifetime_list, 0, 'lifetime')
    capital_cost = handle_transmission_param(capital_cost_list, 0, 'capital cost')
    fixed_cost = handle_transmission_param(fixed_cost_list, 0, 'fixed cost')

    ANF = (((1+interest_rate)**(lifetime))*interest_rate)/(((1+interest_rate)**(lifetime))-1)
    OaM_rate = float(fixed_cost)/float(capital_cost * ANF)
    total_cost = capital_cost * (ANF+1)

    code_list = []
    for elem in transmission_installed_capacity_DC:
        region_A, region_B = elem['region']
        code  = 'hvac' + '_' + region_A + '_' + region_B
        if not code in code_list:
            create_transmission_block(code, efficiency, total_cost, lifetime, OaM_rate, transmission_list)
            code_list.append(code)
        else:
            continue

    seperator_to_csv(transmission_list, cwd+'/TransmissionConverter.csv')
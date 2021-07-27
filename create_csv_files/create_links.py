from build_in_functions import iterate_mapping
from write_to_csv import seperator_to_csv
from create_block.link_block import create_link_block
from find_parameters.link_capacity_handler import find_link_param


def create_links(concrete_data, cwd):
    link_list = []
    link_list.append(["#comment","===============LINK Parameterisation============================================"])
    link_list.append(["#blockwise"])

    transmission_installed_capacity = iterate_mapping(concrete_data, "oed_scalars[? parameter_name == 'installed capacity' && technology== 'transmission' && (technology_type== 'hvac' || technology_type=='DC')]")
    code_list = []
    for elem in transmission_installed_capacity:
        region_A, region_B = elem['region']
        if '{}_{}'.format(region_A, region_B) not in code_list:
            installed_capacity = find_link_param(concrete_data, 'installed capacity', str(elem['region']), 2016, 0)
            length =  find_link_param(concrete_data, 'distance', str(elem['region']), 2016, 300)
            create_link_block(region_A, region_B, length, installed_capacity, link_list)        
            code_list.append('{}_{}'.format(region_A, region_B))
        else:
            continue

    seperator_to_csv(link_list, cwd+'/Link.csv')
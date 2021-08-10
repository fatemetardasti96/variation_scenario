from collections import OrderedDict

from build_in_functions import iterate_mapping
from write_to_csv import seperator_to_csv
from create_block.link_block import create_link_block
from find_parameters.link_capacity_handler import find_link_param



def apply_diff(installed_capacity_tmp, lifetime):
    installed_capacity_dict = {}
    for elem in installed_capacity_tmp:
        y = elem["year"]
        v = elem["value"]
        installed_capacity_dict[y]=v
    available_capacity_years = list(installed_capacity_dict.keys())
    starting_year = available_capacity_years[0]
    ending_year = available_capacity_years[-1]
    capacity_dict_all_years = {key: 0 for key in range(starting_year - int(lifetime) + 1, ending_year - int(lifetime) + 1)}
    #offset_dict = {key: 0 for key in range(starting_year,ending_year+1)}
    # 2016, 2020,2030,2040,2050
    # capacity_dict_all_years[starting_year] = installed_capacity_dict[starting_year]
    for i in range(len(available_capacity_years)-1):
        start = available_capacity_years[i]
        end   = available_capacity_years[i+1]
        if (installed_capacity_dict[start]-installed_capacity_dict[end]) > 0:
            for year in range(start, end):
                count_lifetime = 0
                while year-int(count_lifetime)+1 >= starting_year:
                    try:
                        temp_cap = capacity_dict_all_years[year - int(count_lifetime) - int(lifetime) + 1] + \
                                ((installed_capacity_dict[start]-installed_capacity_dict[end])/(end-start))
                       
                        if temp_cap > 0:
                            capacity_dict_all_years[year-int(count_lifetime)-int(lifetime)+1] = temp_cap/1e3
                    except:
                        temp_cap = ((installed_capacity_dict[start] - installed_capacity_dict[end]) / (end - start))
                       
                        if temp_cap > 0:
                            capacity_dict_all_years[year - int(count_lifetime) - int(lifetime) + 1] = temp_cap/1e3
                    count_lifetime = count_lifetime + int(lifetime)
       
    sorted_capacity_dict_all_years = {k:v for k,v in sorted(capacity_dict_all_years.items())}
    if len(sorted_capacity_dict_all_years) == 0:
        sorted_capacity_dict_all_years[2016]=0
    return sorted_capacity_dict_all_years


def create_links(concrete_data, cwd):
    link_list = []
    link_list.append(["#comment","===============LINK Parameterisation============================================"])
    link_list.append(["#blockwise"])

    transmission_installed_capacity = iterate_mapping(concrete_data, "oed_scalars[? (parameter_name == 'installed capacity' || parameter_name == 'expansion limit') && technology== 'transmission' && (technology_type== 'hvac' || technology_type=='DC')]")
    code_list = []
    for elem in transmission_installed_capacity:
        region_A, region_B = elem['region']
        if '{}_{}'.format(region_A, region_B) not in code_list:
            installed_capacity = find_link_param(concrete_data, 'installed capacity', str(elem['region']), 2016, 0)
            try:
                lifetime = iterate_mapping(concrete_data, "unique(oed_scalars[? parameter_name == 'lifetime' && technology=='transmission' &&\
                (technology_type== 'hvac' || technology_type=='DC')].value)")[0]
            except:
                lifetime = 0
            sorted_installed_capacity = apply_diff(installed_capacity, lifetime)
            length =  find_link_param(concrete_data, 'distance', str(elem['region']), 2016, 300)
            create_link_block(region_A, region_B, length, sorted_installed_capacity, link_list)        
            code_list.append('{}_{}'.format(region_A, region_B))
        else:
            continue

    seperator_to_csv(link_list, cwd+'/Link.csv')
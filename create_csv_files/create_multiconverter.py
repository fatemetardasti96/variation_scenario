import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from code_generator.multiconverter_code_generator import multiconverter_code_generator
from create_block.multiconverter_block import create_multiconverter_block
from type_def.output_energy import OutputEnergy
from write_to_csv import seperator_to_csv
from find_parameters.general_parameter_handler import find_parameter_year_value
from find_parameters.compute_OaM_rate import compute_OaM_rate
from find_parameters.compute_total_cost import compute_total_cost


def create_multiconverter(regions_data, cwd):

    grouped = iterate_mapping(regions_data,"group_by(sort_by(scalars[*], &join('_',[technology, technology_type, input_energy_vector])),\
         &join('_',[technology, technology_type, input_energy_vector]))")

    interest_rate_list = iterate_mapping(regions_data, "unique(scalars[? parameter_name == 'WACC'].value)")
    
    if len(interest_rate_list) == 1:
        interest_rate = interest_rate_list[0]
    elif not len(interest_rate_list):
        interest_rate = 1
    else:
        logging.info("please consider further adjustment")
        raise Exception("multiple interest rate!")

    multiconverter_list = []
    multiconverter_list.append(["#comment","===============multiconverter-technologies============================================"])
    multiconverter_list.append(["#blockwise"])
    
    for elem in grouped.keys():
            technology, technology_type, inp_energy = elem.split('_')                        
            multiconverter_code = multiconverter_code_generator(technology, technology_type, inp_energy)
            if multiconverter_code is not None:
                output_energy = iterate_mapping(grouped,"unique(\"{}\"[*].output_energy_vector)".format(elem))
                output_energy = [OutputEnergy.ELECTRIC_ENERGY if i == OutputEnergy.ELECTRICITY else i for i in output_energy]
                
                efficiency_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'efficiency', 2016, 1)
                efficiency_list = [{"year": 1900, "value": efficiency_list[0]["value"]}] + efficiency_list
                lifetime_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'lifetime', 2016, 0)
                lifetime_list = [{"year": 1900, "value": lifetime_list[0]["value"]}] + lifetime_list
                capital_cost_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'capital costs', 2016, 0)
                capital_cost_list = [{"year": 1900, "value": capital_cost_list[0]["value"]}] + capital_cost_list
                fixed_cost_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'fixed costs', 2016, 0)
                fixed_cost_list = [{"year": 1900, "value": fixed_cost_list[0]["value"]}] + fixed_cost_list
                emission_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'emission factor', 2016, 0)

                total_cost_list = compute_total_cost(interest_rate, lifetime_list, capital_cost_list)
                OaM_rate_list = compute_OaM_rate(interest_rate, lifetime_list, fixed_cost_list, capital_cost_list)


                create_multiconverter_block(multiconverter_code, inp_energy, output_energy, emission_list, efficiency_list, lifetime_list, total_cost_list, OaM_rate_list, multiconverter_list)


    seperator_to_csv(multiconverter_list, cwd+'/MultiConverter.csv')
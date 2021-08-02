import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from build_in_functions import iterate_mapping
from code_generator.converter_code_generator import converter_code_generator
from create_block.converter_block import create_converter_block
from type_def.output_energy import OutputEnergy
from write_to_csv import seperator_to_csv
from find_parameters.general_parameter_handler import find_parameter_year_value
from find_parameters.compute_OaM_rate import compute_OaM_rate
from find_parameters.compute_total_cost import compute_total_cost


def create_converter(regions_data, cwd):

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

    converter_list = []
    converter_list.append(["#comment","===============converter-technologies============================================"])
    converter_list.append(["#blockwise"])
    converter_list.append(["#comment","===============renewable-converter-undispatchable============================================"])
    
    for elem in grouped.keys():
        technology, technology_type, inp_energy = elem.split('_')                        
        converter_code = converter_code_generator(technology, technology_type, inp_energy)
        if converter_code is not None:
            output_energy = iterate_mapping(grouped,"unique(\"{}\"[*].output_energy_vector)".format(elem))
            output_energy = [OutputEnergy.ELECTRIC_ENERGY if i == OutputEnergy.ELECTRICITY else i for i in output_energy]
            
            efficiency_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'efficiency', 2016, 1)
            lifetime_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'lifetime', 2016, 50)
            capital_cost_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'capital costs', 2016, 0)
            fixed_cost_list = find_parameter_year_value(regions_data, technology, technology_type, inp_energy, 'fixed costs', 2016, 0)
                            
            total_cost_list = compute_total_cost(interest_rate, lifetime_list, capital_cost_list)
            OaM_rate_list = compute_OaM_rate(interest_rate, lifetime_list, fixed_cost_list, capital_cost_list)


            create_converter_block(technology, technology_type, inp_energy, output_energy, efficiency_list, lifetime_list, total_cost_list, OaM_rate_list, converter_list)


    seperator_to_csv(converter_list, cwd+'/Converter.csv')
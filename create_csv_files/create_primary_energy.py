from build_in_functions import iterate_mapping
from create_block.create_primary_energy_block import create_primary_energy_block
from write_to_csv import seperator_to_csv
from find_parameters.general_parameter_handler import find_parameter_year_value, find_parameter_year_value_key_val
from type_def.input_energy import InputEnergy
from type_def.technology_type import TechnologyType
from type_def.input_primary_energies import InputPrimaryEnergy


def is_renewable(energy):
    RENEWABLE = [InputEnergy.SOLAR, InputEnergy.AIR, InputEnergy.WATER, InputEnergy.WIND_OFF, InputEnergy.WIND_ONS, InputEnergy.TRADE_IMPORT]
    if energy in RENEWABLE:
        return True
    return False


def create_primary_energies(regions_data, cwd):
    primary_energy_list = []
    primary_energy_list.append(['#comment','===============Primary Energy============================================'])
    primary_energy_list.append(['#blockwise'])

    energies = iterate_mapping(regions_data, "unique(scalars[*].input_energy_vector)")
    energies.append('CO2')
    energies.append(InputEnergy.TRADE_IMPORT)
    for energy in energies:
        if energy == InputEnergy.AIR:
            tech_type_list = iterate_mapping(regions_data, "unique(scalars[? input_energy_vector == 'air'].technology_type)")
            for tech_type in tech_type_list:
                if tech_type == TechnologyType.OFFSHORE:
                    energies.append(InputEnergy.WIND_OFF)
                elif tech_type == TechnologyType.ONSHORE:
                    energies.append(InputEnergy.WIND_ONS)
    
    for energy in energies:
        if energy in [e.value for e in InputPrimaryEnergy]:
            if is_renewable(energy):
                base = [{'year': 2016, 'value': 1}]
                value = [{'year': 2016, 'value': 0}]
            else:
                base = [{'year': 2016, 'value': 1E10}]
                if energy == 'CO2':
                    value = find_parameter_year_value(regions_data, 'unknown', 'unknown', 'unknown', 'emission costs', 2016, 0)
                else:
                    try:
                        value = find_parameter_year_value_key_val(regions_data, 'input_energy_vector', energy, 'fuel costs', 2016, 1E-6)
                        # value =  iterate_mapping(data, "scalars[? input_energy_vector == '{}' && year == `{}` && parameter_name == 'fuel costs'].value".format(energy, year))[0]*1000.0
                    except:
                        value = [{'year': 2016, 'value': 1E-6}]
                    
            energy = energy.replace(" ","_")
            
            create_primary_energy_block(energy, base, value, primary_energy_list)

    seperator_to_csv(primary_energy_list, cwd+'/PrimaryEnergy.csv')
        
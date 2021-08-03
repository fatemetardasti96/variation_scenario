from pathlib import Path

from build_in_functions import iterate_mapping
from code_generator.installation_code_generator import installation_code_generator
from write_to_csv import seperator_to_csv
from find_parameters.installation_handler import handle_multiple_years, handle_multiple_years_transmission
from type_def.technology import Technology
from type_def.technology_type import TechnologyType
from type_def.code import Code
from create_block.create_installation_block import create_installation_list_block


def is_capacity_smaller_than_expansion(installed_capacity, expansion_limit):
    for elem in installed_capacity:
        y = elem['year']
        for elem_ex in expansion_limit:
            if elem_ex['year'] == y:
                if elem_ex['value']>elem['value']:
                    return True

    return False


def create_installation_list(regions_data, concrete_data, cwd):
    dirname = cwd + '/installation_lists/'
    Path(dirname).mkdir(exist_ok=True, parents=True)

    grouped = iterate_mapping(regions_data,"group_by(sort_by(scalars[*], &join('_',[region, technology, technology_type, input_energy_vector])),\
            &join('_',[region, technology, technology_type, input_energy_vector]))")
    
    installation_lists = []
    installation_csv = {}
    installation_lists.append('hvac')
    installation_csv['hvac'] = []
    avoid_repetition = []
    for elem in grouped:
        region, technology, technology_type, inp_energy = elem.split('_')
        if elem not in avoid_repetition:
            avoid_repetition.append(elem)
            expansion_limit = handle_multiple_years(regions_data, technology, technology_type, inp_energy, region, 'expansion limit', 0)
            installed_capacity = handle_multiple_years(regions_data, technology, technology_type, inp_energy, region, 'installed capacity', 0)            
            installation_list_code = installation_code_generator(technology, technology_type, inp_energy)
            if installation_list_code is not None:                                        
                if installation_list_code not in installation_lists:
                    installation_lists.append(installation_list_code)
                    installation_csv[installation_list_code] = []
                #add these extra values for converter
                if technology == Technology.STORAGE:
                    if technology_type == TechnologyType.BATTERY:
                        code_name = Code.BAT1POWER
                    elif technology_type == TechnologyType.HYDROGEN_GAS:
                        code_name = Code.CCH2_TURBINE
                    elif technology_type == TechnologyType.HYDROGEN_FUELCELL:
                        code_name = Code.FUEL_CELL
                    elif technology_type == TechnologyType.PUMPED:
                        code_name = Code.PH_TURBINE
                    if code_name not in installation_lists:
                        installation_lists.append(code_name)                        
                        installation_csv[code_name] = []    
                        if technology_type == TechnologyType.HYDROGEN_GAS:
                            installation_lists.append(Code.H2_ELECTROLYSER)
                            installation_csv[Code.H2_ELECTROLYSER] = []
                        if technology_type == TechnologyType.HYDROGEN_FUELCELL:
                            installation_lists.append(Code.H2_ELECTROLYSER_FC)
                            installation_csv[Code.H2_ELECTROLYSER_FC] = []                                    

                name = region + '.' + installation_list_code

                if is_capacity_smaller_than_expansion(installed_capacity, expansion_limit):
                    if technology == Technology.STORAGE:
                        # for storage : E = p * ratio
                        e2p_ratio = handle_multiple_years(regions_data, 'storage', technology_type, 'electricity', region, 'E2P ratio', 1)

                        create_installation_list_block(name, installed_capacity, e2p_ratio, expansion_limit, installation_csv[installation_list_code])
                        # for converter
                        converter_name = region + '.' + code_name
                        create_installation_list_block(converter_name, installed_capacity, e2p_ratio, expansion_limit, installation_csv[code_name])
                        if technology_type == TechnologyType.HYDROGEN_GAS:
                            create_installation_list_block(region + '.' + Code.H2_ELECTROLYSER, installed_capacity, e2p_ratio, expansion_limit, installation_csv[Code.H2_ELECTROLYSER])
                        elif technology_type == TechnologyType.HYDROGEN_FUELCELL:
                            create_installation_list_block(region + '.' + Code.H2_ELECTROLYSER_FC, installed_capacity, e2p_ratio, expansion_limit, installation_csv[Code.H2_ELECTROLYSER_FC])
                    else:
                        create_installation_list_block(name, installed_capacity, [1], expansion_limit, installation_csv[installation_list_code])
        
        
    transmission_data = iterate_mapping(concrete_data,"oed_scalars[? technology == 'transmission' && (technology_type=='hvac' || technology_type=='DC')]")
    transmission_list = []
    for elem in transmission_data:
        regions = elem['region']
        name = '{0}_{1}.hvac_{0}_{1}'.format(regions[0], regions[1])
        if name not in transmission_list:
            transmission_list.append(name)
            technology_type = elem['technology_type']
            expansion_limit_tranmission = handle_multiple_years_transmission(concrete_data, technology_type, regions, 'expansion limit', 0)
            installed_capacity_transmission = handle_multiple_years_transmission(concrete_data, technology_type, regions, 'installed capacity', 0)
            if is_capacity_smaller_than_expansion(installed_capacity_transmission, expansion_limit_tranmission):                
                create_installation_list_block(name, installed_capacity_transmission, 1, expansion_limit_tranmission, installation_csv['hvac'])

    installationList_csv = [['#comment','MOUNTING-CODE.TECH-CODE;DATA-TYPE;DATA(may contain placeholders varxy)', '(if applicable) next lines:','#varxy', 'INIT-POINT', 'lBOUND', 'uBOUND']]
    for code in installation_lists:
        if installation_csv[code]:
            installation_list_path = './installation_lists/InstallationList_{}.csv'.format(code)
            seperator_to_csv(installation_csv[code], cwd+'/'+installation_list_path)
            installationList_csv.append(['/include({})'.format(installation_list_path)])

    seperator_to_csv(installationList_csv, cwd+'/InstallationList.csv')
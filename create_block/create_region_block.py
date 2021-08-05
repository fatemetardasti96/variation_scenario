from pathlib import Path
from enum import Enum

from type_def.input_energy import InputEnergy
from type_def.technology import Technology
from type_def.technology_type import TechnologyType
from type_def.code import Code
from build_in_functions import iterate_mapping
from code_generator.converter_code_generator import converter_code_generator
from code_generator.multiconverter_code_generator import multiconverter_code_generator
from code_generator.storage_code_generator import storage_code_generator
from code_generator.storage_converter_code_generator import storage_converter_generator


class MultiConverter(Enum):
    GENERATOR = 'generator'
    CHP = 'chp'
    GEOTHERMAL = 'geothermal'
    NUCLEAR = 'nuclear'


def create_demand_electric_dyn_block(region, region_csv):
    region_csv.append(["#code", region, "#name", region])
    type_dyn = "TS_repeat_const"
    start_date = "2015-01-01_00:00"
    
    source_path = "./TimeSeries/" + region + "/demand_elec.csv"
    region_csv.append(["demand_electric_dyn", "#type", type_dyn, "#interval", "1h", "#start", start_date, "#data_source_path", source_path])



def create_demand_electric_per_a_block(demand_dict, region_csv):
    demand_per_a_row = ["demand_electric_per_a","#type","DVP_linear","#data"]
    for year, demand in demand_dict.items():
        timeindex = "{}-01-01_00:00".format(year)
        demand_per_a_row.extend([timeindex, demand])
    region_csv.append(demand_per_a_row)


def create_primary_energy_with_timeseries(primary_energy_with_timeseries, region, avoid_repetition, region_csv):
    avoid_repetition[region].append("ELECTRICITY")
    for elem in primary_energy_with_timeseries:
        input_energy, tech_type = elem['energy'], elem['tech_type']
        if tech_type == 'trade export':
            continue
        if (input_energy == InputEnergy.AIR and tech_type == TechnologyType.ONSHORE):
            input_energy = InputEnergy.WIND_ONS
        elif (input_energy == InputEnergy.AIR and tech_type == TechnologyType.OFFSHORE):
            input_energy = InputEnergy.WIND_OFF
        elif tech_type == TechnologyType.TRADE_IMPORT:
            input_energy = 'TRADE_IMPORT'                        

        energy = input_energy.replace(" ","_").upper()
        if energy not in avoid_repetition[region]:
            avoid_repetition[region].append(energy)
            region_csv.append(["#primary_energy", "#code", input_energy.replace(' ','_').upper()])
            lookUpTable = "TBD_lookupTable"
            source_path = "./TimeSeries/" + region + "/" + region + "_" + energy + ".csv"
            region_csv.append(["potential", "#type", lookUpTable, "#data_source_path", source_path])


def determine_primary_source_path(region, input_energy, cwd):
    domestic_limit_path = '{}/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(cwd, region, input_energy)
    if Path(domestic_limit_path).exists():
        return './TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(region, input_energy)
    else:
        return './TimeSeries/PrimaryEnergyUnlimited_minusOne.csv'


def create_primary_energy_with_unlimited_minus_one(primary_energy_with_unlimited_minus_one, region, avoid_repetition, region_csv, cwd):
    primary_energy_with_unlimited_minus_one_copy = primary_energy_with_unlimited_minus_one.copy()
    if region != 'Baltic' or region != 'North':
        primary_energy_with_unlimited_minus_one_copy.append({'energy':'CO2', 'tech_type':'', 'tech':''})
    for elem in primary_energy_with_unlimited_minus_one_copy:
        input_energy, tech_type = elem['energy'], elem['tech_type']
        if tech_type == 'trade export':
            continue
        if (input_energy == InputEnergy.AIR and tech_type == TechnologyType.ONSHORE):
            input_energy = InputEnergy.WIND_ONS
        elif (input_energy == InputEnergy.AIR and tech_type == TechnologyType.OFFSHORE):
            input_energy = InputEnergy.WIND_OFF
        elif tech_type == TechnologyType.TRADE_IMPORT:
            input_energy = 'TRADE_IMPORT'                        

        energy = input_energy.replace(" ","_").upper()
        if energy not in avoid_repetition[region]:
            avoid_repetition[region].append(energy)
            region_csv.append(["#primary_energy", "#code", input_energy.replace(' ','_').upper()])
            lookUpTable = "TBD_lookupTable"
            source_path = determine_primary_source_path(region, input_energy, cwd)    
            region_csv.append(["potential", "#type", lookUpTable, "#data_source_path", source_path])


def region_converter_block(converter_code, installed_capacity_dict, region_csv):
    region_csv.append(["#converter", "#code", converter_code])
    converter_type = "DVP_const"
    installation_row = ["installation", "#type", converter_type, "#data"]
    for year, value in installed_capacity_dict.items():
        installation_row.extend(["{}-01-01_00:00".format(year), value])
    installation_row.extend(["{}-12-31_00:00".format(year), value])
    region_csv.append(installation_row)


def region_multiconverter_block(code, installed_capacity_dict, region_csv):
    region_csv.append(["#multi-converter", "#code", code])
    multiconverter_type = "DVP_const"
    installation_row = ["installation", "#type", multiconverter_type, "#data"]
    for year, value in installed_capacity_dict.items():
        installation_row.extend(["{}-01-01_00:00".format(year), value])
    installation_row.extend(["{}-12-31_00:00".format(year), value])
    region_csv.append(installation_row)


def region_storage_block(code, installed_capacity_dict, region_csv):
    region_csv.append(["#storage", "#code", code])
    storage_type = "DVP_const"
    installation_row = ["installation", "#type", storage_type, "#data"]
    for year, value in installed_capacity_dict.items():
        installation_row.extend(["{}-01-01_00:00".format(year), value])
    installation_row.extend(["{}-12-31_00:00".format(year), value])
    installation_row.extend(["{}-01-01_00:00".format(year+1), 0])
    region_csv.append(installation_row)



def handle_incerasing_capacity(installed_capacity_dict, lifetime):
    capacity_dict = {}
    flag_2030 = 0
    flag_2040 = 0

    extra_capacity_2020 = installed_capacity_dict[2020] - installed_capacity_dict[2016]
    if extra_capacity_2020<0:
        capacity_dict[2016-int(lifetime)+1] = -extra_capacity_2020/4
        first_installation_year = 2016
        first_installation = -extra_capacity_2020/4
    elif extra_capacity_2020>0:
        capacity_dict[2020] = extra_capacity_2020
        first_installation_year = 2020
        first_installation = extra_capacity_2020

    extra_capacity_2030 = installed_capacity_dict[2030] - installed_capacity_dict[2020]
    if extra_capacity_2030<0:
        if 2030-int(lifetime)+1 < first_installation_year and first_installation>0:
            capacity_dict[2030-int(lifetime)+1] = -extra_capacity_2030/10 - first_installation
        else:      
            capacity_dict[2030-int(lifetime)+1] = -extra_capacity_2030/10
        flag_2030 = 1
    elif extra_capacity_2030>0:
        if 2030-int(lifetime)+1 < first_installation_year and first_installation>0:
            capacity_dict[2030-int(lifetime)+1] = extra_capacity_2030 - first_installation
        else:      
            capacity_dict[2030] = extra_capacity_2030
    extra_capacity_2040 = installed_capacity_dict[2040] - installed_capacity_dict[2030]
    if extra_capacity_2040<0:
        flag_2040 = 1
        if 2040-int(lifetime)+1 < first_installation_year and first_installation>0:
            capacity_dict[2040-int(lifetime)+1] = -extra_capacity_2040/10 - first_installation
        else:      
            capacity_dict[2040-int(lifetime)+1] = -extra_capacity_2040/10

        if 2040-int(lifetime)+1 < first_installation_year and extra_capacity_2030>0:
            capacity_dict[2040-int(lifetime)+1] = -extra_capacity_2040/10 - extra_capacity_2030
        else:      
            capacity_dict[2040-int(lifetime)+1] = -extra_capacity_2040/10


    elif extra_capacity_2040>0:
        if 2040-int(lifetime)+1 < first_installation_year and extra_capacity_2020>0:
            capacity_dict[2040-int(lifetime)+1] = extra_capacity_2040 - extra_capacity_2020
        else:      
            capacity_dict[2040] = extra_capacity_2040

        if 2040-int(lifetime)+1 < 2030 and extra_capacity_2030>0:
            capacity_dict[2040-int(lifetime)+1] = extra_capacity_2040 - extra_capacity_2030
        else:      
            capacity_dict[2040-int(lifetime)+1] = extra_capacity_2040

    
    first_end_of_life = 2020+int(lifetime) 
    while first_end_of_life < 2050:
        capacity_dict[first_end_of_life+1] = extra_capacity_2020
        first_end_of_life += int(lifetime)

    second_end_of_life = 2030+int(lifetime) 
    while second_end_of_life < 2050:
        capacity_dict[second_end_of_life+1] = extra_capacity_2030
        second_end_of_life += int(lifetime)
    
    if 2050 not in installed_capacity_dict:
        installed_capacity_dict[2050] = 0

    if installed_capacity_dict[2050] - abs(extra_capacity_2020) - abs(extra_capacity_2030) > 0:
        capacity_dict[2050-int(lifetime)+1] = installed_capacity_dict[2050] - extra_capacity_2020 - extra_capacity_2030

    if (2050-int(lifetime)+1 > 2016) and (installed_capacity_dict[2050] - abs(extra_capacity_2020) - abs(extra_capacity_2030))>0:
        capacity_dict[2050-int(lifetime)+1-int(lifetime)+1] = installed_capacity_dict[2050] - extra_capacity_2020 - extra_capacity_2030


    sorted_capacitydict = {k:v for k,v in sorted(capacity_dict.items())}
    all_years = list(sorted_capacitydict.keys())
    if flag_2030:
        next_year_idx = [i+1 for i in range(len(all_years)) if all_years[i]==2030-int(lifetime)+1][0]
        for year in range(2030-int(lifetime)+1, all_years[next_year_idx]):
            capacity_dict[year] = capacity_dict[2030-int(lifetime)+1]

    if flag_2040:
        next_year_idx = [i+1 for i in range(len(all_years)) if all_years[i]==2040-int(lifetime)+1][0]
        for year in range(2040-int(lifetime)+1, all_years[next_year_idx]):
            capacity_dict[year] = capacity_dict[2040-int(lifetime)+1]

    sorted_capacitydict = {k:v for k,v in sorted(capacity_dict.items())}

    return sorted_capacitydict






def apply_diff(installed_capacity_dict, tech_type, lifetime):
    if tech_type == TechnologyType.TRADE_IMPORT:
        return {2016: installed_capacity_dict[2016]}

    available_capacity_years = list(installed_capacity_dict.keys())
    starting_year = available_capacity_years[0]
    ending_year = available_capacity_years[-1]
    capacity_dict_all_years = {key:0 for key in range(starting_year-int(lifetime)+1, ending_year-int(lifetime)+1)}
    # 2016, 2020,2030,2040,2050 
    # capacity_dict_all_years[starting_year] = installed_capacity_dict[starting_year]
    for i in range(len(available_capacity_years)-1):
        start = available_capacity_years[i]
        end   = available_capacity_years[i+1]
        for year in range(start, end):
            capacity_dict_all_years[year-int(lifetime)+1] = ((installed_capacity_dict[start]-installed_capacity_dict[end])/(end-start))
            if capacity_dict_all_years[year-int(lifetime)+1]<0:
                return handle_incerasing_capacity(installed_capacity_dict, lifetime)

    if installed_capacity_dict[available_capacity_years[-1]]>installed_capacity_dict[available_capacity_years[0]]:
        capacity_dict_all_years[available_capacity_years[-1]-int(lifetime)+1-int(lifetime)+1] = installed_capacity_dict[available_capacity_years[-1]]

    return capacity_dict_all_years


def create_installation_dict(regions_data, installation_elements, region, avoid_installation_repetition):
    installation_list = []
    for elem in installation_elements:
        input_energy, tech_type, tech = elem['energy'], elem['tech_type'], elem['tech']       
        if (input_energy, tech_type, tech) not in avoid_installation_repetition[region]:
            avoid_installation_repetition[region].append((input_energy, tech_type, tech))
            installed_capacity_dict = {}
            for year in (2016, 2020, 2030, 2040, 2050):            
                try:
                    installed_capacity_dict[year] = iterate_mapping(regions_data, "scalars[? year==`{}` && input_energy_vector=='{}' && technology == '{}' && technology_type == '{}'\
                    && parameter_name == 'installed capacity' && region=='{}'].value".format(year, input_energy, tech, tech_type, region))[0]
                except:
                    try:
                        iterate_mapping(regions_data, "scalars[? year==`{}` && input_energy_vector=='{}' && technology == '{}' && technology_type == '{}'\
                        && parameter_name == 'expansion limit' && region=='{}'].value".format(year, input_energy, tech, tech_type, region))[0]
                        installed_capacity_dict[year] = 0
                    except:
                        continue    
            try:
                lifetime = iterate_mapping(regions_data, "unique(scalars[? parameter_name == 'lifetime' && technology=='{}' &&\
                technology_type=='{}' && input_energy_vector=='{}'].value)".format(tech, tech_type, input_energy))[0]
            except:
                lifetime = 0
            if tech == 'transmission' and tech_type == 'hvac':
                continue
            installation_diff = apply_diff(installed_capacity_dict, tech_type, lifetime)
            installation_list.append({'input_energy': input_energy, 'tech_type': tech_type, 'tech': tech, 'value': installation_diff})    
        else:
            continue            
    
    return installation_list


def create_installation_block(installation_list, region_csv):
    for installation_elem in installation_list:
        converter_code = converter_code_generator(installation_elem['tech'], installation_elem['tech_type'], installation_elem['input_energy'])
        if converter_code is not None:
            region_converter_block(converter_code, installation_elem['value'], region_csv)
        
        if installation_elem['tech_type'] == TechnologyType.HYDROGEN_GAS:
            code = Code.H2_ELECTROLYSER
            region_converter_block(code, installation_elem['value'], region_csv)

        if installation_elem['tech_type'] == TechnologyType.HYDROGEN_FUELCELL:
            code = Code.H2_ELECTROLYSER_FC
            region_converter_block(code, installation_elem['value'], region_csv)


        # if installation_elem['tech'] == 'storage':
        #     code = storage_converter_generator(installation_elem['tech_type'])['code']
        #     region_converter_block(code, installation_elem['value'], region_csv)


    for installation_elem in installation_list:
        multiconverter_code = multiconverter_code_generator(installation_elem['tech'], installation_elem['tech_type'], installation_elem['input_energy'])
        if multiconverter_code is not None:
            region_multiconverter_block(multiconverter_code, installation_elem['value'], region_csv)


    for installation_elem in installation_list:
        if installation_elem['tech'] == 'storage':
            code = storage_code_generator(installation_elem['tech_type'])['code']
            region_storage_block(code, installation_elem['value'], region_csv)



def transform_capacity(installation_list):
    pass


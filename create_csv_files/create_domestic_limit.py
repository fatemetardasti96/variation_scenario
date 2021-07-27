from build_in_functions import iterate_mapping
from write_to_csv import seperator_to_csv
from find_parameters.domestic_limit_handler import find_parameter_year_value
from create_block.create_domesic_limit_block import create_domestic_limit_bloc

def create_domestic_limit(regions_data, cwd):
    grouped = iterate_mapping(regions_data,"group_by(sort_by(scalars[? parameter_name=='natural domestic limit'], &join('_',[region, input_energy_vector])),\
         &join('_',[region, input_energy_vector]))")

    for elem in grouped:
        region, inp_energy = elem.split('_')
        domestic_limit = find_parameter_year_value(regions_data, region, inp_energy,2016, 0)

        limit_list = create_domestic_limit_bloc(inp_energy, domestic_limit)

        limit_filename = cwd + '/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(region, inp_energy)
        seperator_to_csv(limit_list, limit_filename)
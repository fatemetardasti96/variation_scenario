from build_in_functions import iterate_mapping
from write_to_csv import seperator_to_csv
from find_parameters.domestic_limit_handler import find_parameter_year_value
from create_block.create_domesic_limit_block import create_domestic_limit_bloc
from find_parameters.demand_per_year_handler import handle_demand


def find_demand_factor(regions_data, region, year):
    demand_dict =  handle_demand(regions_data, region)
    total_demadn = 0
    all_region_list = iterate_mapping(regions_data, "timeseries[? timeindex_start=='{}-01-01T00:00:00'].region".format(year))
    for reg in all_region_list:
        demand_dict_reg =  handle_demand(regions_data, reg)
        total_demadn += demand_dict_reg[year]

    if not demand_dict[year]:

        return 'dont include this region'
    return demand_dict[year]/total_demadn



def handle_DE_domestic_limit(regions_data, domestic_limit, region):
    limit_list = []
    for elem in domestic_limit:
        year, value = elem["year"], elem["value"]
        factor = find_demand_factor(regions_data, region, year)
        if factor == 'dont include this region':
            return 'dont include this region'
        limit_list.append({"year": year, "value": factor*value})

    return limit_list


def create_domestic_limit(regions_data, cwd):
    grouped = iterate_mapping(regions_data,"group_by(sort_by(scalars[? parameter_name=='natural domestic limit'], &join('_',[region, input_energy_vector])),\
         &join('_',[region, input_energy_vector]))")

    for elem in grouped:
        region, inp_energy = elem.split('_')
        domestic_limit = find_parameter_year_value(regions_data, region, inp_energy,2016, 0)

        if region == 'DE':
            all_region_list = iterate_mapping(regions_data, "timeseries[? timeindex_start=='2016-01-01T00:00:00'].region")
            for domestic_region in all_region_list:
                domestic_limit_region = handle_DE_domestic_limit(regions_data, domestic_limit, domestic_region)
                if domestic_limit_region == 'dont include this region':
                    continue
                limit_list = create_domestic_limit_bloc(inp_energy, domestic_limit_region)
                limit_filename = cwd + '/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(domestic_region, inp_energy)
                seperator_to_csv(limit_list, limit_filename)

        else:

            limit_list = create_domestic_limit_bloc(inp_energy, domestic_limit)
            limit_filename = cwd + '/TimeSeries/PrimaryEnergyLimited_{}_{}.csv'.format(region, inp_energy)
            seperator_to_csv(limit_list, limit_filename)
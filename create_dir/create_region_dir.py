from pathlib import Path

from build_in_functions import iterate_mapping
from create_block.create_region_block import create_demand_electric_dyn_block, create_demand_electric_per_a_block,\
create_primary_energy_with_timeseries, create_primary_energy_with_unlimited_minus_one, create_installation_dict,\
create_installation_block
from write_to_csv import seperator_to_csv
from find_parameters.demand_per_year_handler import handle_demand

def create_region_dir(regions_data, cwd):
    dirname = cwd + '/regions/'
    Path(dirname).mkdir(exist_ok=True, parents=True)
    regions = iterate_mapping(regions_data, "unique(timeseries[*].region)")
    avoid_repetition = {}  
    avoid_installation_repetition = {}  
    for region in regions:
        region_csv = []
        create_demand_electric_dyn_block(region, region_csv)

        demand = handle_demand(regions_data, region)
        create_demand_electric_per_a_block(demand, region_csv)

        #create_primary_energy_with_timeseries
        #capacity factor
        avoid_repetition[region] = []
        primary_energy_with_timeseries = iterate_mapping(regions_data, "timeseries[? (parameter_name == 'capacity factor' || parameter_name == 'trade volume') && region == '{}'].\
                {{energy: input_energy_vector, tech_type: technology_type}}".format(region))
        create_primary_energy_with_timeseries(primary_energy_with_timeseries, region, avoid_repetition,region_csv)
        

        #create_primary_energy_with_unlimited_minus_one
        #installation or expansion limit
        primary_energy_with_unlimited_minus_one = iterate_mapping(regions_data, "scalars[? (parameter_name == 'installed capacity' || parameter_name == 'expansion limit') && region == '{}'].\
                {{energy: input_energy_vector, tech_type: technology_type, tech: technology}}".format(region))
        create_primary_energy_with_unlimited_minus_one(primary_energy_with_unlimited_minus_one, region, avoid_repetition, region_csv, cwd)


        avoid_installation_repetition[region] = []
        # transformed_capacity = transform_capacity(primary_energy_with_unlimited_minus_one)
        installation_list = create_installation_dict(regions_data, primary_energy_with_unlimited_minus_one, region, avoid_installation_repetition)
        
        create_installation_block(installation_list, region_csv)

        region_csv.append(["#endblock"])
        seperator_to_csv(region_csv, cwd+'/regions/'+region+'.csv')
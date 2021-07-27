from pathlib import Path

from build_in_functions import iterate_mapping
from create_block.create_region_block import create_demand_electric_dyn_block, create_demand_electric_per_a_block,\
create_primary_energy_with_timeseries, create_primary_energy_with_unlimited_minus_one, create_installation_dict, create_installation_block
from write_to_csv import seperator_to_csv
from find_parameters.demand_per_year_handler import handle_demand

def create_installation_dir(regions_data, cwd):
    dirname = cwd + '/regions/'
    Path(dirname).mkdir(exist_ok=True, parents=True)
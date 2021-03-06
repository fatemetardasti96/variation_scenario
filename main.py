from pathlib import Path
from datetime import datetime
import logging
import os
import json
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)

from read_write_db import dump_region_db, load_region_db, dump_concrete_db, load_concrete_db
from build_in_functions import iterate_mapping
from create_csv_files.create_converters import create_converter
from create_csv_files.create_multiconverter import create_multiconverter
from create_csv_files.create_storage import create_storage
from create_csv_files.create_transmission_converter import create_transmission
from create_csv_files.create_primary_energy import create_primary_energies
from create_csv_files.create_links import create_links
from create_csv_files.create_region_file import create_region_file
from create_dir.create_timeseries_dir import create_timeseries_dir
from create_csv_files.create_demand_elec import create_demand_elec
from create_csv_files.create_domestic_limit import create_domestic_limit
from create_dir.create_region_dir import create_region_dir
from create_csv_files.create_installation_list import create_installation_list
from create_csv_files.create_config_files import create_config_files
from create_csv_files.create_global_co2 import *


SCENARIO_ID = 55

if __name__ == '__main__':
    if not Path('ID'+str(SCENARIO_ID)).is_dir():
        cwd = 'ID'+str(SCENARIO_ID)
        Path(cwd).mkdir(parents= True)
    else:
        cwd = 'ID'+str(SCENARIO_ID)+'_'+datetime.now().strftime('%Y-%m-%d_%H-%M')
        Path(cwd).mkdir(parents= True)

    if not os.path.exists('db'):
        os.makedirs('db')

    logging.info("start loading data")
    dump_region_db(SCENARIO_ID)
    regions_data = load_region_db(SCENARIO_ID)
    
    dump_concrete_db(SCENARIO_ID)
    concrete_data = load_concrete_db(SCENARIO_ID)    
    
    logging.info('start creating config files')
    create_config_files(regions_data, cwd)

    logging.info('start converter.csv')
    create_converter(regions_data, cwd)
    
    logging.info('start multiconverter.csv')
    create_multiconverter(regions_data, cwd)

    logging.info('start storage.csv')
    create_storage(concrete_data, regions_data, cwd)
    
    logging.info('start transmission_converter.csv')
    create_transmission(concrete_data, regions_data, cwd)
    
    logging.info('start primary_energy.csv')
    create_primary_energies(regions_data, cwd)

    logging.info('start link.csv')
    create_links(concrete_data, cwd)

    logging.info('start region.csv')
    create_region_file(regions_data, cwd)

    logging.info('create timeseries directory')
    create_timeseries_dir(regions_data, cwd)

    create_demand_elec(regions_data, cwd)
    create_domestic_limit(regions_data, cwd)
    
    logging.info('start regions directory')
    installation_dict_for_installation = create_region_dir(regions_data, cwd, False, True)
    # if not os.path.exists('db/installation_dict_for_installation_{}.txt'.format(SCENARIO_ID)):
    #     with open('db/installation_dict_for_installation_{}.txt'.format(SCENARIO_ID), 'w') as f:
    #         f.write(json.dumps(installation_dict_for_installation))

    

    logging.info('start installation directory')
    with open('db/installation_dict_for_installation_{}.txt'.format(SCENARIO_ID), 'r') as f:
        installation_dict_for_installation = json.loads(f.read())
    create_installation_list(regions_data, concrete_data, cwd)
    
    create_global_co2(regions_data, cwd)
    create_global(cwd)
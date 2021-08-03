from pathlib import Path

from build_in_functions import iterate_mapping
from type_def.input_energy import InputEnergy
from type_def.technology_type import TechnologyType
from create_block.create_timeseries import create_timeseries_block, sort_series_timeindex, insert_series_in_between
from create_csv_files.create_primary_energy_minus_one import primary_energy_minus_one_detail_block


def create_timeseries_dir(regions_db, cwd):
    regions = iterate_mapping(regions_db, "unique(timeseries[*].region)")
    for region in regions:
        dirname = cwd + '/' + '/TimeSeries/' + region
        Path(dirname).mkdir(exist_ok=True, parents=True)
        # group based on input energy and technology_type
        grouped = iterate_mapping(regions_db,"group_by(sort_by(timeseries[? (parameter_name == 'capacity factor' || parameter_name == 'trade volume') &&\
             region == '{}'], &join('_',[technology, technology_type, input_energy_vector])),\
         &join('_',[technology, technology_type, input_energy_vector]))".format(region))

        for elem in grouped:
            tech, tech_type, input_energy = elem.split('_')

            series_timeindex = iterate_mapping(regions_db, "timeseries[? (parameter_name == 'capacity factor' || parameter_name == 'trade volume') &&\
             region == '{}' && input_energy_vector == '{}' && technology_type == '{}'].{{series: series, timeindex_start: timeindex_start}}"\
            .format(region, input_energy, tech_type))

            sorted_series_timeindex = sort_series_timeindex(series_timeindex)
            inserted_series = insert_series_in_between(sorted_series_timeindex)

            if tech_type == 'trade export':
                continue
            if (input_energy == InputEnergy.AIR and tech_type == TechnologyType.ONSHORE):
                input_energy = InputEnergy.WIND_ONS
            elif (input_energy == InputEnergy.AIR and tech_type == TechnologyType.OFFSHORE):
                input_energy = InputEnergy.WIND_OFF
            elif tech_type == TechnologyType.TRADE_IMPORT:
                input_energy = 'TRADE_IMPORT'                        
            create_timeseries_block(region, input_energy, inserted_series, cwd)

    primary_energy_minus_one_detail_block(cwd)
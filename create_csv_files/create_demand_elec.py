from build_in_functions import iterate_mapping
from write_to_csv import seperator_to_csv

import numpy as np


def timeseries_length(year):
    year = int(year)
    if (year%4) == 0:
        if year%100 == 0:
            if year%400 == 0:
                return 24*366
            else:
                return 24*365
        else:
            return 24*366
    else:
        return 24*365


def fill_demand_dict(demand_dict):
    for year in demand_dict:
        if len(demand_dict[year]) == 0:
            demand_dict[year] = demand_dict[str(int(year)-1)]


def create_demand_elec(regions_data, cwd):
    regions = iterate_mapping(regions_data, "unique(timeseries[*].region)")
    timeindex_years = iterate_mapping(regions_data, "unique(timeseries[*].timeindex_start)")
    years = np.arange(2016, 2050)
    
    for region in regions:
        demand_dict = {str(year):[] for year in years}
        for timeindex_year in timeindex_years:
            year = timeindex_year.split('-')[0]
            try:            
                timeseries_list = iterate_mapping(regions_data, "timeseries[? parameter_name == 'demand' && region == '{}' && timeindex_start == '{}'].series".format(region, timeindex_year))[0][:8760]
            except:
                timeseries_list = [0] * 8760
            try:
                tradeseries_list = iterate_mapping(regions_data, "timeseries[? parameter_name=='trade volume' && technology_type=='trade export' && region == '{}' && timeindex_start == '{}'].series".format(region, timeindex_year))[0][:8760]
            except:
                tradeseries_list = [0] * 8760

            time_and_trade_list = timeseries_list + tradeseries_list
            abs_time_and_trade_list = [abs(t) for t in time_and_trade_list]
            if sum(abs_time_and_trade_list):
                nfactor = sum(abs_time_and_trade_list)
                time_and_trade_list = [t/nfactor for t in time_and_trade_list]

            
            demand_dict[str(year)] = time_and_trade_list
        
        fill_demand_dict(demand_dict)    

        filename = cwd + '/TimeSeries/' + region + '/demand_elec.csv'
        seperator_to_csv(demand_dict.values(), filename)

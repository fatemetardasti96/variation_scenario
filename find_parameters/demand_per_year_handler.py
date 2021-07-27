from build_in_functions import iterate_mapping



TRADE_DEMAND = {}
TRADE_DEMAND[2016]=[]
TRADE_DEMAND[2020]=[]
TRADE_DEMAND[2030]=[]
TRADE_DEMAND[2040]=[]
TRADE_DEMAND[2050]=[]
TIME_DEMAND={}
TIME_DEMAND[2016]=[]
TIME_DEMAND[2020]=[]
TIME_DEMAND[2030]=[]
TIME_DEMAND[2040]=[]
TIME_DEMAND[2050]=[]
DEMAND={}
DEMAND[2016]=[]
DEMAND[2020]=[]
DEMAND[2030]=[]
DEMAND[2040]=[]
DEMAND[2050]=[]

def handle_demand(regions_data, region):
    for year in (2016, 2020, 2030, 2040, 2050):
        timeindex_start = '{}-01-01T00:00:00'.format(year)
        try:
            TIME_DEMAND[year] = sum(iterate_mapping(regions_data, "timeseries[? parameter_name == 'demand' && region=='{}' && timeindex_start=='{}'].series"\
            .format(region, timeindex_start))[0])/1000.0
        except:
            TIME_DEMAND[year] = 0

        try:
            TRADE_DEMAND[year] = sum(iterate_mapping(regions_data, "timeseries[? parameter_name == 'trade volume' && technology_type=='trade export' \
                && region=='{}' && timeindex_start=='{}'].series".format(region, timeindex_start))[0])/1000.0
        except:
            TRADE_DEMAND[year] = 0
        
        DEMAND[year] = TIME_DEMAND[year] + TRADE_DEMAND[year]

    return DEMAND


























from build_in_functions import iterate_mapping
import numpy as np

from write_to_csv import seperator_to_csv


def create_timeseries_block(region, input_energy, series_timeindex, cwd):
    csv_list = []
    csv_list.append(["#comment","===============generation time series============================================"])
    base_type = "DVP_const"
    base = 1000000
    sdata = series_timeindex[0]["timeindex_start"][:-3]
    csv_list.append(["base", "#type", base_type, "#data", sdata, base])

    value_type = "TS_repeat_const"    
    value_row = ["value", "#type", value_type, "#interval","1h", "#start", sdata, "#data"]
    for elem in series_timeindex:
        series, timeindex = elem["series"], elem["timeindex_start"]
        value_row.extend([*(t for t in series)])
    csv_list.append(value_row)

    csv_list.append(["#endtable"])

    filename = cwd + '/TimeSeries/' + region + '/' + region + '_' + input_energy.replace(" ","_").upper() + '.csv'
    seperator_to_csv(csv_list, filename)


def sort_series_timeindex(series_timeindex):
    sorted_series = sorted(series_timeindex, key=lambda k: k['timeindex_start'])
    result_series = [{"timeindex_start": sorted_series[0]["timeindex_start"], "series": sorted_series[0]["series"]}]
    for i in range(1, len(sorted_series)):
        if sorted_series[i]["series"] == sorted_series[i-1]["series"]:
            continue
        else:
            result_series.append({"timeindex_start": sorted_series[i]["timeindex_start"], "series": sorted_series[i]["series"]})

    return result_series


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


def adjust_series_len(series_len, series):    
    if series_len<=len(series):
        return series[:series_len]
    else:
        series.extend([series[-1]*(series_len-len(series))])
        return series


def insert_series_in_between(sorted_series_timeindex):
    available_years = [int(e["timeindex_start"].split("-")[0]) for e in sorted_series_timeindex]
    all_years = np.arange(available_years[0], available_years[-1])
    result_series = []
    for year in all_years:
        idx = [i for i, elem in enumerate(available_years) if elem<=year][-1]
        expected_series_len = 8760
        series = adjust_series_len(expected_series_len, sorted_series_timeindex[idx]["series"])
        result_series.append({"timeindex_start": "{}-01-01_00:00".format(year), "series": series})

    return result_series

    
def find_capacity_factor(regions_data, region, expected_year):
    all_available_years = [2016, 2020, 2030, 2040, 2050]
    if expected_year in all_available_years:
        year = expected_year
    else:
        expected_year_idx = sorted([2016, 2020, 2030, 2040, 2050, expected_year]).index(expected_year)
        year = all_available_years[expected_year_idx-1]

    installed_capacity_year = iterate_mapping(regions_data, "scalars[? parameter_name=='installed capacity' && technology=='transmission' && technology_type=='trade import'\
        && year==`{}` && region=='{}'].value".format(year, region))[0]

    installed_capacity_all = iterate_mapping(regions_data, "scalars[? parameter_name=='installed capacity' && technology=='transmission' && technology_type=='trade import'\
        && region=='{}'].value".format(region))

    factor = installed_capacity_year/max(installed_capacity_all)
    
    
    return factor



def handle_trade_import_series(regions_data, region, series):
    trade_series = []
    for elem in series:
        year = int(elem['timeindex_start'].split('-')[0])
        series_val = elem['series']
        factor = find_capacity_factor(regions_data, region, year)
        trade_series.append({"timeindex_start": "{}-01-01_00:00".format(year), "series": list(np.array(series_val)*factor)})
    
    return trade_series
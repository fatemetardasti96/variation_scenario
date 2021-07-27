from write_to_csv import seperator_to_csv


def create_timeseries_block(region, input_energy, series_timeindex, cwd):
    csv_list = []
    csv_list.append(["#comment","===============generation time series============================================"])
    base_type = "DVP_const"
    base = 1000000
    csv_list.append(["base", "#type", base_type, "#data", series_timeindex[0]["timeindex_start"].replace('T','_')[:-3], base])

    value_type = "TS_repeat_const"    
    value_row = ["value", "#type", value_type, "#interval","1h", "#start"]
    for elem in series_timeindex:
        series, timeindex = elem["series"], elem["timeindex_start"]
        value_row.extend([timeindex.replace('T','_')[:-3], "#data", *(t for t in series)])
    csv_list.append(value_row)

    csv_list.append(["#endtable"])

    filename = cwd + '/TimeSeries/' + region + '/' + region + '_' + input_energy.replace(" ","_").upper() + '.csv'
    seperator_to_csv(csv_list, filename)
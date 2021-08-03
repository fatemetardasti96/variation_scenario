from write_to_csv import seperator_to_csv
from build_in_functions import iterate_mapping
from find_parameters.general_parameter_handler import find_parameter_year_value


def create_global_co2(regions_data, cwd):
    filename = "{}/TimeSeries/LookupTable_globalCO2.csv".format(cwd)
    emission_limit = find_parameter_year_value(regions_data, 'unknown', 'unknown', 'unknown', 'emission limit', 2016, 0)
    global_csv = []
    global_csv.append(["#comment", "unlimited -1 primary resource"])
    base_row = ["base", "#type", "DVP_const", "#data"]
    val_row = ["value", "#type", "DVP_linear", "#data"]
    
    for elem in emission_limit:
        year = elem["year"]
        val = elem["value"]
        base_row.extend(["{}-01-01_00:00".format(year), 1E10])
        val_row.extend(["{}-01-01_00:00".format(year), val])

    global_csv.append(base_row)
    global_csv.append(val_row)
    global_csv.append(["#endtable"])
    seperator_to_csv(global_csv, filename)


def create_global(cwd):
    global_csv = []
    global_csv.append(["#blockwise", ""])
    global_csv.append(["#code", "CO2", "#name", "global_CO2"])
    global_csv.append(["#primary_energy", "#code", "CO2"])
    global_csv.append(["potential", "#type", "TBD_lookupTable", "#data_source_path", "./TimeSeries/LookupTable_globalCO2.csv"])
    global_csv.append(["#endblock"])
    seperator_to_csv(global_csv, cwd+'/global.csv')
from write_to_csv import seperator_to_csv

def primary_energy_minus_one_detail_block(cwd):
    csv_list = []
    csv_list.append(["#comment","unlimited -1 primary ressource"])
    base_type = "DVP_const"
    base = 1E15
    date = "2016-01-01_00:00"
    csv_list.append(["base", "#type", base_type, "#data", date, base])
    value_type = "DVP_linear"
    value = -1
    csv_list.append(["value", "#type", value_type, "#data", date, value])
    csv_list.append(["#endtable"])

    filename = cwd + '/TimeSeries/PrimaryEnergyUnlimited_minusOne.csv'
    seperator_to_csv(csv_list, filename)
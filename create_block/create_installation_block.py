
def compute_capacity_from_e2p(installed_capacity, e2p_ratio):
    capacity_list = []
    for i, elem in enumerate(installed_capacity):
        try:
            capacity = elem['value']*e2p_ratio[i]['value']/1000.0
        except:
            capacity = elem['value']/1000.0

        capacity_list.append({"year":elem['year'], "value": capacity})
    
    return capacity_list


def apply_difference(capacity, expansion_limit):
    capacity_difference = []
    expansion_difference = []
    for i, elem in enumerate(capacity):
        try:
            diff = round((capacity[i+1]['value'] - elem['value'])/(capacity[i+1]['year'] - elem['year']), 6)
        except:
            diff = elem['value']
        capacity_difference.append({"year": elem["year"], "value":diff})

    for i, elem in enumerate(expansion_limit):
        try:
            diff = round((expansion_limit[i+1]['value'] - elem['value'])/(expansion_limit[i+1]['year'] - elem['year']), 6)
        except:
            diff = elem['value']
        expansion_difference.append({"year": elem["year"], "value":diff})

    return capacity_difference, expansion_difference


def transform_expansion_limit(expansion_limit):
    available_years = [elem['year'] for elem in expansion_limit]
    start_year = available_years[0]
    end_year = available_years[-1]
    expansion_dict_all_years = {key:0 for key in range(start_year, end_year+1)}
    expansion_dict_all_years[start_year] = [e['value'] for e in expansion_limit if e['year']==start_year][0]
    
    for i in range(len(available_years)-1):
        start = available_years[i]
        end   = available_years[i+1]
        start_ex = [e['value'] for e in expansion_limit if e['year']==start][0]
        end_ex   = [e['value'] for e in expansion_limit if e['year']==end][0]
        for year in range(start+1, end+1):
            expansion_dict_all_years[year] = ((start_ex-end_ex)/(end-start))*(year-start)            

    return expansion_dict_all_years


def add_one_year_in_between(expansion_limit):
    expansion_limit_with_additional_years = {expansion_limit[0]['year']:expansion_limit[0]['value']}
    #2020, 2030, 2040, 2050
    for i in range(len(expansion_limit)-1):
        expansion_limit_with_additional_years[expansion_limit[i+1]['year']-1] = expansion_limit[i]['value']
        expansion_limit_with_additional_years[expansion_limit[i+1]['year']] = expansion_limit[i+1]['value']
    
    return expansion_limit_with_additional_years


def create_installation_list_block(name, installed_capacity, e2p_ratio, expansion_limit, installation_csv):
    # transformed_expansion = transform_expansion_limit(expansion_limit)
    capacity = compute_capacity_from_e2p(installed_capacity, e2p_ratio)
    capacity_difference, expansion_difference = apply_difference(capacity, expansion_limit)
    expansion_limit_with_additional_years = add_one_year_in_between(expansion_difference)

    var_row = [name, "#type", "DVP_linear", "#data"]
    for i, year in enumerate(list(expansion_limit_with_additional_years.keys())):
        start_date = "{}-01-01_00:00".format(year)
        var_row.extend([start_date, "var{}".format(i)])    
    var_row.extend(["{}-12-31_00:00".format(year),0,''])
    installation_csv.append(var_row)

    
    j = 0
    for year, val in expansion_limit_with_additional_years.items():
        installation_csv.append(["#var{}".format(j), 0, 0, val/1000.0, ''])        
        j += 1
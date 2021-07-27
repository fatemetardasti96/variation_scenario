from build_in_functions import iterate_mapping


def handle_multiple_years_link_param(db, param, region):
    list_of_param_year_values =  iterate_mapping(db, "oed_scalars[? parameter_name == '{}' && region=={}].{{year: year, value: value}}".format(param, region))

    list_of_unique_param_year_values = [dict(t) for t in {tuple(d.items()) for d in list_of_param_year_values}]
    
    sorted_list_of_unique_param_year_values = sorted(list_of_unique_param_year_values, key=lambda k: k['year']) 
    return sorted_list_of_unique_param_year_values


def find_link_param(concrete_db, param, region, default_year, default_value):
    list_of_param_values = iterate_mapping(concrete_db, "unique(oed_scalars[? parameter_name == '{}' && region=={}].value)".format(param, region))

    if len(list_of_param_values) == 1:
        param_year = sorted(iterate_mapping(concrete_db, "unique(oed_scalars[? parameter_name == '{}' && region=={}].year)".format(param, region)))[0]
        return [{'year': param_year, 'value': list_of_param_values[0]}]
    elif not len(list_of_param_values):
        return [{'year': default_year, 'value': default_value}]
    else:
        return handle_multiple_years_link_param(concrete_db, param, region)

from build_in_functions import iterate_mapping


def handle_multiple_years(db, technology, technology_type, inp_energy, param_name):
    list_of_param_year_values =  iterate_mapping(db, "scalars[? parameter_name == '{}' && technology=='{}' &&\
                     technology_type=='{}' && input_energy_vector=='{}'].{{year: year, value: value}}".format(param_name, technology, technology_type, inp_energy))

    list_of_unique_param_year_values = [dict(t) for t in {tuple(d.items()) for d in list_of_param_year_values}]
    
    sorted_list_of_unique_param_year_values = sorted(list_of_unique_param_year_values, key=lambda k: k['year']) 
            
    return sorted_list_of_unique_param_year_values


def handle_multiple_years_key_val(db, key, val, param_name):
    list_of_param_year_values =  iterate_mapping(db, "scalars[? parameter_name == '{}'&& {}=='{}'].{{year: year, value: value}}".format(param_name, key, val))

    list_of_unique_param_year_values = [dict(t) for t in {tuple(d.items()) for d in list_of_param_year_values}]
    
    sorted_list_of_unique_param_year_values = sorted(list_of_unique_param_year_values, key=lambda k: k['year']) 
    # print('*****', sorted_list_of_unique_param_year_values, '*******')
    return sorted_list_of_unique_param_year_values



def find_parameter_year_value(db, technology, technology_type, inp_energy, param_name, default_year, default_value):
    list_of_param_values = iterate_mapping(db, "unique(scalars[? parameter_name == '{}' && technology=='{}' &&\
        technology_type=='{}' && input_energy_vector=='{}'].value)".format(param_name, technology, technology_type, inp_energy))

    if len(list_of_param_values) == 1:
        param_year = sorted(iterate_mapping(db, "unique(scalars[? parameter_name == '{}' && technology=='{}' &&\
        technology_type=='{}' && input_energy_vector=='{}'].year)".format(param_name, technology, technology_type, inp_energy)))[0]
        return [{'year': param_year, 'value': list_of_param_values[0]}]
    elif not len(list_of_param_values):
        return [{'year': default_year, 'value': default_value}]
    else:
        return handle_multiple_years(db, technology, technology_type, inp_energy, param_name)


def find_parameter_year_value_key_val(db, key, val, param_name, default_year, default_value):
    list_of_param_values = iterate_mapping(db, "unique(scalars[? parameter_name == '{}' && {}=={}].value)".format(param_name, key, val))

    if len(list_of_param_values) == 1:
        param_year = sorted(iterate_mapping(db, "unique(scalars[? parameter_name == '{}' && {}=={}].year)".format(param_name, key, val)))[0]
        return [{'year': param_year, 'value': list_of_param_values[0]}]
    elif not len(list_of_param_values):
        return [{'year': default_year, 'value': default_value}]
    else:
        return handle_multiple_years_key_val(db, key, val, param_name)



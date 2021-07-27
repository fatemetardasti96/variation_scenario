from build_in_functions import iterate_mapping


def handle_multiple_years(db, region, inp_energy):
    list_of_param_year_values =  iterate_mapping(db, "scalars[? parameter_name == 'natural domestic limit' && region=='{}' &&\
                     input_energy_vector=='{}'].{{year: year, value: value}}".format(region, inp_energy))

    list_of_unique_param_year_values = [dict(t) for t in {tuple(d.items()) for d in list_of_param_year_values}]
    
    sorted_list_of_unique_param_year_values = sorted(list_of_unique_param_year_values, key=lambda k: k['year']) 
            
    return sorted_list_of_unique_param_year_values


def find_parameter_year_value(db, region, inp_energy, default_year, default_value):
    list_of_param_values = iterate_mapping(db, "unique(scalars[? parameter_name == 'natural domestic limit' && region=='{}' &&\
        input_energy_vector=='{}'].value)".format(region, inp_energy))

    if len(list_of_param_values) == 1:
        param_year = sorted(iterate_mapping(db, "unique(scalars[? parameter_name == 'natural domestic limit' && region=='{}' &&\
        input_energy_vector=='{}'].year)".format(region, inp_energy)))[0]
        return [{'year': param_year, 'value': list_of_param_values[0]}]
    elif not len(list_of_param_values):
        return [{'year': default_year, 'value': default_value}]
    else:
        return handle_multiple_years(db, region, inp_energy)
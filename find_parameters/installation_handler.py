from build_in_functions import iterate_mapping


def handle_multiple_years(db, technology, technology_type, inp_energy, region, param_name, default_value):
    d = [{'year': 2020, 'value': default_value},{'year': 2030, 'value': default_value},\
            {'year': 2040, 'value': default_value},{'year': 2050, 'value': default_value}]
    for i, year in enumerate((2020 ,2030, 2040, 2050)):
        try:
            value = iterate_mapping(db, "scalars[? parameter_name == '{}' && technology=='{}' &&\
            technology_type=='{}' && input_energy_vector=='{}' && region=='{}' && year==`{}`].value"\
            .format(param_name, technology, technology_type, inp_energy, region, year))[0]  
            
            d[i]['value'] = value
        except:
            continue

    return d


def handle_multiple_years_transmission(db, technology_type, region, param_name, default_value):
    d = [{'year': 2020, 'value': default_value},{'year': 2030, 'value': default_value},\
            {'year': 2040, 'value': default_value},{'year': 2050, 'value': default_value}]
    for i, year in enumerate((2020 ,2030, 2040, 2050)):
        try:
            value = iterate_mapping(db, "oed_scalars[? parameter_name == '{}' && technology=='transmission' &&\
            technology_type=='{}' && region=={} && year==`{}`].value"\
            .format(param_name, technology_type, region, year))[0]  
            
            d[i]['value'] = value
        except:
            continue

    return d


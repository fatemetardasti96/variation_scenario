from numpy.lib.function_base import append
import pandas as pd

from build_in_functions import iterate_mapping


def handle_multiple_years(db, technology, technology_type, inp_energy):
    lifetime_dict =  iterate_mapping(db, "scalars[? parameter_name == 'lifetime' && technology=='{}' &&\
                     technology_type=='{}' && input_energy_vector=='{}'].{{year: year, value: value}}".format(technology, technology_type, inp_energy))

    unique_lifetime_dict = pd.DataFrame([dict(t) for t in {tuple(d.items()) for d in lifetime_dict}])
    
    sorted_lifetime_dict = sorted(unique_lifetime_dict, key=lambda k: k['year']) 
            
    return sorted_lifetime_dict



def find_lifetime(db, technology, technology_type, inp_energy):
    lifetime_list = iterate_mapping(db, "unique(scalars[? parameter_name == 'lifetime' && technology=='{}' &&\
        technology_type=='{}' && input_energy_vector=='{}'].value)".format(technology, technology_type, inp_energy))

    if len(lifetime_list) == 1:
        lifetime_year = sorted(iterate_mapping(db, "unique(scalars[? parameter_name == 'lifetime' && technology=='{}' &&\
        technology_type=='{}' && input_energy_vector=='{}'].year)".format(technology, technology_type, inp_energy)))[0]
        return {'year': lifetime_year, 'value': lifetime_list[0]}
    elif not len(lifetime_list):
        return {'year': 0, 'value': 0}
    else:
        return handle_multiple_years(db, technology, technology_type, inp_energy)



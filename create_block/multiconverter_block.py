from type_def.input_energy import InputEnergy
# from code_generator.multiconverter_code_generator import multiconverter_code_generator


def create_multiconverter_block(code, input_energy, out_energy, emission_list, efficiency_list, lifetime_list,\
    total_cost_list, OaM_rate_list, multiconverter_list):
    # code = multiconverter_code_generator(technology, technology_type, input_energy)
    name = code
    input_energy = input_energy.replace(" ","_")
    input_energy = InputEnergy.ELECTRIC_ENERGY if input_energy == InputEnergy.ELECTRICITY else input_energy.upper()
    multiconverter_list.append(["#code",code,"#name",name,"#input",input_energy])
    #output_energy row
    if ('co2' or 'CO2') not in out_energy:
        out_energy.append('CO2')

    multiconverter_list.append(["#output",*(i for i in out_energy)])
    
    emission_factor = emission_list[0]["value"]
    if emission_factor == 0:
        emission_factor = 1e-9
    else:
        emission_factor = 1000*emission_factor

    multiconverter_list.append(["#conversion",str(-1),emission_factor])
    type_ = "DVP_linear"

    efficiency_row_list = ["efficiency_new","#type",type_,"#data"]
    for efficiency_elem in efficiency_list:
        year, value = efficiency_elem['year'], efficiency_elem['value']
        efficiency_row_list.extend([str(year) + "-01-01_00:00", value])
    efficiency_row_list.extend(["2051-01-01_00:00", value])
    multiconverter_list.append(efficiency_row_list)

    cost_row_list = ["cost","#type",type_,"#data"]
    for cost_elem in total_cost_list:
        year, value = cost_elem['year'], cost_elem['value']
        cost_row_list.extend([str(year) + "-01-01_00:00", value])
    cost_row_list.extend(["2051-01-01_00:00", value])
    multiconverter_list.append(cost_row_list)

    lifetime_row_list = ["lifetime","#type",type_,"#data"]
    for lifetime_elem in lifetime_list:
        year, value = lifetime_elem['year'], lifetime_elem['value']
        lifetime_row_list.extend([str(year) + "-01-01_00:00", value])
    lifetime_row_list.extend(["2051-01-01_00:00", value])
    multiconverter_list.append(lifetime_row_list)

    OaM_rate_row_list = ["OaM_rate","#type",type_,"#data"]
    for OaM_rate_elem in OaM_rate_list:
        year, value = OaM_rate_elem['year'], OaM_rate_elem['value']
        OaM_rate_row_list.extend([str(year) + "-01-01_00:00", value])
    OaM_rate_row_list.extend(["2051-01-01_00:00", value])
    multiconverter_list.append(OaM_rate_row_list)

    multiconverter_list.append(["#endblock"])
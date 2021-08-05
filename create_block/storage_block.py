from code_generator.storage_code_generator import storage_code_generator


def create_storage_block(technology_type, efficiency_list, lifetime_list, total_cost_list, OaM_rate_list, storage_list):
    code = storage_code_generator(technology_type)['code']
    name = code
    input_energy = storage_code_generator(technology_type)['input_energy']

    storage_list.append(["#code",code,"#name",name,"#input",input_energy,"#output", input_energy])

    type_ = "DVP_linear"
    
    efficiency_row_list = ["efficiency_new","#type",type_,"#data"]
    for efficiency_elem in efficiency_list:
        year, value = efficiency_elem['year'], efficiency_elem['value']
        efficiency_row_list.extend([str(year) + "-01-01_00:00", value])
    storage_list.append(efficiency_row_list)

    cost_row_list = ["cost","#type",type_,"#data"]
    for cost_elem in total_cost_list:
        year, value = cost_elem['year'], cost_elem['value']
        cost_row_list.extend([str(year) + "-01-01_00:00", value])
    storage_list.append(cost_row_list)

    lifetime_row_list = ["lifetime","#type",type_,"#data"]
    for lifetime_elem in lifetime_list:
        year, value = lifetime_elem['year'], lifetime_elem['value']
        lifetime_row_list.extend([str(year) + "-01-01_00:00", value])
    storage_list.append(lifetime_row_list)

    OaM_rate_row_list = ["OaM_rate","#type",type_,"#data"]
    for OaM_rate_elem in OaM_rate_list:
        year, value = OaM_rate_elem['year'], OaM_rate_elem['value']
        OaM_rate_row_list.extend([str(year) + "-01-01_00:00", value])
    storage_list.append(OaM_rate_row_list)

    storage_list.append(["#endblock"])
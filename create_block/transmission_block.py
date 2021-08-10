def create_transmission_block(code, efficiency, total_cost, lifetime, OaM_rate, transmission_list):
    name = 'hvac_Elec'
    is_bidirectional = "true"
    input_energy = 'electric_energy'
    output_energy = 'electric_energy'

    transmission_list.append(["#code",code,"#name",name,"#input",input_energy,"#output",output_energy,"#bidirectional",is_bidirectional])
    type_ = "DVP_linear"
    
    start_date = "2016-01-01_00:00"
    efficiency_row_list = ["efficiency_new","#type",type_,"#data"]
    for efficiency_elem in efficiency:
        year, value = efficiency_elem['year'], efficiency_elem['value']
        efficiency_row_list.extend([str(year) + "-01-01_00:00", value])
    efficiency_row_list.extend([str(year+1) + "-01-01_00:00", 0])
    transmission_list.append(efficiency_row_list)
    
    cost_row_list = ["cost","#type",type_,"#data"]
    for cost_elem in total_cost:
        year, value = cost_elem['year'], cost_elem['value']
        cost_row_list.extend([str(year) + "-01-01_00:00", value])
    cost_row_list.extend([str(year+1) + "-01-01_00:00", 0])
    transmission_list.append(cost_row_list)
    
    
    lifetime_row_list = ["lifetime","#type",type_,"#data"]
    for lifetime_elem in lifetime:
        year, value = lifetime_elem['year'], lifetime_elem['value']
        lifetime_row_list.extend([str(year) + "-01-01_00:00", value])
    lifetime_row_list.extend([str(year+1) + "-01-01_00:00", 0])
    transmission_list.append(lifetime_row_list)
    
    OaM_rate_row_list = ["OaM_rate","#type",type_,"#data"]
    for OaM_rate_elem in OaM_rate:
        year, value = OaM_rate_elem['year'], OaM_rate_elem['value']
        OaM_rate_row_list.extend([str(year) + "-01-01_00:00", value])
    OaM_rate_row_list.extend([str(year+1) + "-01-01_00:00", 0])
    transmission_list.append(OaM_rate_row_list)

    transmission_list.append(["length_dep_loss","#type",type_,"#data","1900-01-01_00:00", str(0),start_date,str(0)])
    transmission_list.append(["length_dep_cost","#type",type_,"#data","1900-01-01_00:00", str(0),start_date,str(0)])

    transmission_list.append(["#endblock"])
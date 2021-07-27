def create_transmission_block(code, efficiency, total_cost, lifetime, OaM_rate, transmission_list):
    name = 'hvac_Elec'
    is_bidirectional = "true"
    input_energy = 'electric_energy'
    output_energy = 'electric_energy'

    transmission_list.append(["#code",code,"#name",name,"#input",input_energy,"#output",output_energy,"#bidirectional",is_bidirectional])
    type_ = "DVP_linear"
    
    start_date = "2016-01-01_00:00"
    transmission_list.append(["efficiency_new","#type",type_,"#data",start_date,efficiency])
    
    transmission_list.append(["cost","#type",type_,"#data",start_date,total_cost])
    
    transmission_list.append(["lifetime","#type",type_,"#data",start_date,lifetime])
    
    transmission_list.append(["OaM_rate","#type",type_,"#data",start_date,OaM_rate])

    transmission_list.append(["length_dep_loss","#type",type_,"#data",start_date,str(0)])
    transmission_list.append(["length_dep_cost","#type",type_,"#data",start_date,str(0)])

    transmission_list.append(["#endblock"])
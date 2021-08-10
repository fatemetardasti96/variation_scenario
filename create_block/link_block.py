def create_link_block(region_A, region_B, length, installed_capacity, link_list):
    code = ("_").join([region_A, region_B])
    link_list.append(["#code",code,"#region_A",region_A,"#region_B",region_B])
    type_ = "DVP_const"
    
    len_row_list = ["length","#type",type_,"#data"]
    for len_elem in length:
        year, value = len_elem['year'], len_elem['value']
        len_row_list.extend([str(year) + "-01-01_00:00", value])
    len_row_list.extend([str(year+1) + "-01-01_00:00", 0])
    link_list.append(len_row_list)

    converter_code = 'hvac_' + code
    link_list.append(["#converter","#code",converter_code])

    cap_row_list = ["installation","#type",type_,"#data"]
    for year in installed_capacity:
        value = installed_capacity[year]
        cap_row_list.extend([str(year) + "-01-01_00:00", value])
    cap_row_list.extend([str(year+1) + "-01-01_00:00", 0])
    link_list.append(cap_row_list)

        
    link_list.append(["#endblock"])
from type_def.input_energy import InputEnergy


def create_primary_energy_block(energy, base_list, value_list, energy_list):
    if energy != InputEnergy.ELECTRIC_ENERGY:
        energy = energy.upper()
    energy_list.append(['#code', energy, '#name', energy])
    table = 'TBD_lookupTable'
    energy_list.append(['cost_table', '#type', table])
    type_ = 'DVP_const'
    
    base_row_list = ["base","#type",type_,"#data"]
    for base_elem in base_list:
        year, value = base_elem['year'], base_elem['value']
        base_row_list.extend([str(year) + "-01-01_00:00", value])
    energy_list.append(base_row_list)

    value_row_list = ["value","#type",type_,"#data"]
    for value_elem in value_list:
        year, value = value_elem['year'], value_elem['value']
        value_row_list.extend([str(year) + "-01-01_00:00", value*1000])
    energy_list.append(value_row_list)

    energy_list.append(['#endtable'])
    energy_list.append(['#endblock'])
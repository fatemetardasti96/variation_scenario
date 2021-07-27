from type_def.input_energy import InputEnergy
from type_def.technology import Technology
from type_def.technology_type import TechnologyType
from type_def.output_energy import OutputEnergy
from type_def.code import Code
from code_generator.converter_code_generator import converter_code_generator
from code_generator.storage_converter_code_generator import storage_converter_generator

def handle_converter_detail_block(code, input_energy, out_energy, is_bidirectional, efficiency_list, total_cost_list, lifetime_list, OaM_rate_list, converter_list):
    name = code
    comment = "this is a comment"
    if input_energy != InputEnergy.ELECTRIC_ENERGY:
        input_energy = input_energy.upper()
    converter_list.append(["#code",code,"#name",name,"#input",input_energy,"#output",*(i for i in out_energy),"#bidirectional",is_bidirectional,"#comment",comment])
    #efficiency_list row
    type_ = "DVP_linear"
    
    efficiency_row_list = ["efficiency_new","#type",type_,"#data"]
    for efficiency_elem in efficiency_list:
        year, value = efficiency_elem['year'], efficiency_elem['value']
        efficiency_row_list.extend([str(year) + "-01-01_00:00", value])
    converter_list.append(efficiency_row_list)

    cost_row_list = ["cost","#type",type_,"#data"]
    for cost_elem in total_cost_list:
        year, value = cost_elem['year'], cost_elem['value']
        cost_row_list.extend([str(year) + "-01-01_00:00", value])
    converter_list.append(cost_row_list)

    lifetime_row_list = ["lifetime","#type",type_,"#data"]
    for lifetime_elem in lifetime_list:
        year, value = lifetime_elem['year'], lifetime_elem['value']
        lifetime_row_list.extend([str(year) + "-01-01_00:00", value])
    converter_list.append(lifetime_row_list)

    OaM_rate_row_list = ["OaM_rate","#type",type_,"#data"]
    for OaM_rate_elem in OaM_rate_list:
        year, value = OaM_rate_elem['year'], OaM_rate_elem['value']
        OaM_rate_row_list.extend([str(year) + "-01-01_00:00", value])
    converter_list.append(OaM_rate_row_list)
    
    
    converter_list.append(["#endblock"])


def create_converter_block(technology, technology_type, input_energy, out_energy, efficiency_list, lifetime_list, total_cost_list, OaM_rate_list, converter_list):
    if technology_type in (TechnologyType.BATTERY, TechnologyType.PUMPED):
        is_bidirectional = str(True).lower()
    else:
        is_bidirectional = str(False).lower()

    if technology_type == TechnologyType.HYDROGEN_GAS:
        code = Code.H2_ELECTROLYSER
        inp_energy = InputEnergy.ELECTRIC_ENERGY
        out_energy = [OutputEnergy.H2]
        handle_converter_detail_block(code, inp_energy, out_energy, is_bidirectional, efficiency_list, total_cost_list, lifetime_list, OaM_rate_list, converter_list)

    if technology_type == TechnologyType.HYDROGEN_FUELCELL:
        code = Code.H2_ELECTROLYSER_FC
        inp_energy = InputEnergy.ELECTRIC_ENERGY
        out_energy = [OutputEnergy.H2_FC]
        handle_converter_detail_block(code, inp_energy, out_energy, is_bidirectional, efficiency_list, total_cost_list, lifetime_list, OaM_rate_list, converter_list)

    code = converter_code_generator(technology, technology_type, input_energy)
    if technology in Technology.STORAGE:
        input_energy = storage_converter_generator(technology_type)['input_energy']
        out_energy = [storage_converter_generator(technology_type)['output_energy']]

    if code == Code.WIND_OFF:
        input_energy = InputEnergy.WIND_OFF
    elif code == Code.WIND_ONS:
        input_energy = InputEnergy.WIND_ONS
    elif code == Code.TRANSMISSION_IMPORT:
        input_energy = InputEnergy.TRADE_IMPORT

    input_energy = input_energy.replace(" ","_")
    input_energy = InputEnergy.ELECTRIC_ENERGY if input_energy == InputEnergy.ELECTRICITY else input_energy

    handle_converter_detail_block(code, input_energy, out_energy, is_bidirectional, efficiency_list, total_cost_list, lifetime_list, OaM_rate_list, converter_list)
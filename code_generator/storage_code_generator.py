from type_def.output_energy import OutputEnergy
from type_def.input_energy import InputEnergy
from type_def.technology_type import TechnologyType
from type_def.code import Code


def storage_code_generator(technology_type):

    storage_code_book = [
        {'technology_type': TechnologyType.BATTERY,
        'code': Code.Battery_Energy_storage,
        'input_energy': InputEnergy.BATTERY_ENERGY},
        {'technology_type': TechnologyType.PUMPED,
        'code': Code.PH_storage,
        'input_energy': InputEnergy.HYDRO_ENERGY},
        {'technology_type':TechnologyType.HYDROGEN_GAS,
        'code': Code.H2_storage_GASTURBINE,
        'input_energy': InputEnergy.H2},
        # {'technology_type':TechnologyType.HYDROGEN_FUELCELL,
        # 'code': Code.H2_storage_FUEL,
        # 'input_energy': InputEnergy.H2_FC}
    ]
    return [code_book for code_book in storage_code_book if code_book['technology_type'] == technology_type][0]

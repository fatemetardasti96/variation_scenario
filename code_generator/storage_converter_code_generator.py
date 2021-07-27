from type_def.output_energy import OutputEnergy
from type_def.input_energy import InputEnergy
from type_def.technology_type import TechnologyType
from type_def.code import Code


def storage_converter_generator(technology_type):

    storage_converter_code_book = [
        {'technology_type': TechnologyType.BATTERY,
        'code': Code.BAT1POWER,
        'input_energy': InputEnergy.ELECTRIC_ENERGY,
        'output_energy': OutputEnergy.BATTERY_ENERGY},
        {'technology_type': TechnologyType.PUMPED,
        'code': Code.PH_TURBINE,
        'input_energy': InputEnergy.ELECTRIC_ENERGY,
        'output_energy': OutputEnergy.HYDRO_ENERGY},
        {'technology_type':TechnologyType.HYDROGEN_GAS,
        'code': Code.CCH2_TURBINE,
        'input_energy': InputEnergy.H2,
        'output_energy': OutputEnergy.ELECTRIC_ENERGY},
        {'technology_type':TechnologyType.HYDROGEN_FUELCELL,
        'code': Code.FUEL_CELL,
        'input_energy': InputEnergy.H2_FC,
        'output_energy': OutputEnergy.ELECTRIC_ENERGY}
    ]
    return [code_book for code_book in storage_converter_code_book if code_book['technology_type'] == technology_type][0]

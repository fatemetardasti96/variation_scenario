from type_def.input_energy import InputEnergy
from type_def.technology import Technology
from type_def.technology_type import TechnologyType
from type_def.code import Code
from code_generator.general_code_generator import CodeGenerator


def converter_code_generator(technology, technology_type, inp_energy):
    
    converter_code_book = {        
        CodeGenerator(Technology.HYDRO_TURBINE, TechnologyType.RUN_OF_RIVER, InputEnergy.WATER).to_str(): Code.ROR,
        CodeGenerator(Technology.PHOTOVOLTAICS, TechnologyType.ROOFTOP, InputEnergy.SOLAR).to_str(): Code.PV1,
        CodeGenerator(Technology.PHOTOVOLTAICS, TechnologyType.UTILITY, InputEnergy.SOLAR).to_str(): Code.PV2,
        CodeGenerator(Technology.WIND_TURBINE, TechnologyType.ONSHORE, InputEnergy.AIR).to_str(): Code.WIND_ONS,
        CodeGenerator(Technology.WIND_TURBINE, TechnologyType.OFFSHORE, InputEnergy.AIR).to_str(): Code.WIND_OFF,
        CodeGenerator(Technology.TRANSMISSION, TechnologyType.TRADE_IMPORT, InputEnergy.ELECTRICITY).to_str(): Code.TRANSMISSION_IMPORT,
        CodeGenerator(Technology.STORAGE, TechnologyType.BATTERY, InputEnergy.ELECTRICITY).to_str(): Code.BAT1POWER,
        CodeGenerator(Technology.STORAGE, TechnologyType.HYDROGEN_GAS, InputEnergy.ELECTRICITY).to_str(): Code.CCH2_TURBINE,
        # CodeGenerator(Technology.STORAGE, TechnologyType.HYDROGEN_FUELCELL, InputEnergy.ELECTRICITY).to_str(): Code.FUEL_CELL,
        CodeGenerator(Technology.STORAGE, TechnologyType.PUMPED, InputEnergy.ELECTRICITY).to_str(): Code.PH_TURBINE
    }

    try:
        return converter_code_book[CodeGenerator(technology, technology_type, inp_energy).to_str()]
    except:
        return None
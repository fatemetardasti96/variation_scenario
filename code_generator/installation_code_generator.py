from type_def.input_energy import InputEnergy
from type_def.technology import Technology
from type_def.technology_type import TechnologyType
from type_def.code import Code
from code_generator.general_code_generator import CodeGenerator


def installation_code_generator(technology, technology_type, input_energy):
    CodeBook = {
            CodeGenerator(Technology.CHP, TechnologyType.COMBINED, InputEnergy.NATURALGAS).to_str(): Code.CH4_CCTURBINE_CHP,
            CodeGenerator(Technology.CHP, TechnologyType.COMBUSTION_ENGINE, InputEnergy.NATURALGAS).to_str(): Code.GASN_TURBINE_CHP,
            CodeGenerator(Technology.CHP, TechnologyType.GAS, InputEnergy.LIGHTOIL).to_str(): Code.LIGHT_OIL_CHP,
            CodeGenerator(Technology.CHP, TechnologyType.GAS, InputEnergy.NATURALGAS).to_str(): Code.GAS_TURBINE_CHP,
            CodeGenerator(Technology.CHP, TechnologyType.STEAM, InputEnergy.HARDCOAL).to_str(): Code.HARDCOAL_OCTURBINE_CHP,
            CodeGenerator(Technology.CHP, TechnologyType.STEAM, InputEnergy.LIGNITE).to_str(): Code.LIGNITE_CHP,
            CodeGenerator(Technology.CHP, TechnologyType.STEAM, InputEnergy.WASTE).to_str(): Code.BIOMASS_FURNANCE_CHP,

            CodeGenerator(Technology.GENERATOR, TechnologyType.COMBINED, InputEnergy.NATURALGAS).to_str(): Code.CH4_CCTURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.COMBUSTION_ENGINE, InputEnergy.BIOGAS).to_str(): Code.BIO_CH4_TURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.COMBUSTION_ENGINE, InputEnergy.NATURALGAS).to_str(): Code.GASN_TURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.GAS, InputEnergy.LIGHTOIL).to_str(): Code.LIGHT_OIL,
            CodeGenerator(Technology.GENERATOR, TechnologyType.GAS, InputEnergy.NATURALGAS).to_str(): Code.GAS_TURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.STEAM, InputEnergy.BIOMASS).to_str(): Code.BIOMASS_TURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.STEAM, InputEnergy.HARDCOAL).to_str(): Code.HARDCOAL_OCTURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.STEAM, InputEnergy.LIGNITE).to_str(): Code.LIGNITE_OCTURBINE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.STEAM, InputEnergy.WASTE).to_str(): Code.BIOMASS_FURNANCE,
            CodeGenerator(Technology.GENERATOR, TechnologyType.UNKNOWN, InputEnergy.HEAVYOIL).to_str(): Code.HEAVY_OIL,

            CodeGenerator(Technology.GEOTHERMAL, TechnologyType.UNKNOWN, InputEnergy.HEAT).to_str(): Code.GEO,
            CodeGenerator(Technology.HYDRO_TURBINE, TechnologyType.RUN_OF_RIVER, InputEnergy.WATER).to_str(): Code.ROR,
            CodeGenerator(Technology.NUCLEAR, TechnologyType.UNKNOWN, InputEnergy.URANIUM).to_str(): Code.NUCLEAR_TURBINE,
            CodeGenerator(Technology.PHOTOVOLTAICS, TechnologyType.ROOFTOP, InputEnergy.SOLAR).to_str(): Code.PV1,
            CodeGenerator(Technology.PHOTOVOLTAICS, TechnologyType.UTILITY, InputEnergy.SOLAR).to_str(): Code.PV2,
            CodeGenerator(Technology.WIND_TURBINE, TechnologyType.ONSHORE, InputEnergy.AIR).to_str(): Code.WIND_ONS,
            CodeGenerator(Technology.WIND_TURBINE, TechnologyType.OFFSHORE, InputEnergy.AIR).to_str(): Code.WIND_OFF,
            CodeGenerator(Technology.TRANSMISSION, TechnologyType.TRADE_IMPORT, InputEnergy.ELECTRICITY).to_str(): Code.TRANSMISSION_IMPORT,
            CodeGenerator(Technology.STORAGE, TechnologyType.BATTERY, InputEnergy.ELECTRICITY).to_str(): Code.Battery_Energy_storage,
            CodeGenerator(Technology.STORAGE, TechnologyType.HYDROGEN_GAS, InputEnergy.ELECTRICITY).to_str(): Code.H2_storage_GASTURBINE,
            CodeGenerator(Technology.STORAGE, TechnologyType.HYDROGEN_FUELCELL, InputEnergy.ELECTRICITY).to_str(): Code.H2_storage_FUEL,
            CodeGenerator(Technology.STORAGE, TechnologyType.PUMPED, InputEnergy.ELECTRICITY).to_str(): Code.PH_storage

            }
    try:
        return CodeBook[CodeGenerator(technology, technology_type, input_energy).to_str()]
    except:
        return None
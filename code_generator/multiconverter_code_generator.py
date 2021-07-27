from type_def.input_energy import InputEnergy
from type_def.technology import Technology
from type_def.technology_type import TechnologyType
from type_def.code import Code
from code_generator.general_code_generator import CodeGenerator


def multiconverter_code_generator(technology, technology_type, inp_energy):
    
    multiconverter_code_book = {
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
        CodeGenerator(Technology.NUCLEAR, TechnologyType.UNKNOWN, InputEnergy.URANIUM).to_str(): Code.NUCLEAR_TURBINE,
    }

    try:
        return multiconverter_code_book[CodeGenerator(technology, technology_type, inp_energy).to_str()]
    except:
        return None
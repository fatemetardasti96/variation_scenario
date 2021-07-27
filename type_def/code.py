from dataclasses import dataclass


@dataclass
class Code:
    WIND_ONS = 'WIND_ONS'
    WIND_OFF = 'WIND_OFF'
    PV1 = 'PV1'
    PV2 = 'PV2'
    ROR = 'ROR'
    OIL_TURBINE = 'OIL_TURBINE'
    GASN_TURBINE = 'GASN_TURBINE'
    GASN_TURBINE_CHP = 'GASN_TURBINE_CHP'
    CH4_OCTURBINE = 'CH4_OCTURBINE'
    CH4_TURBINE = 'CH4_TURBINE'
    NUCLEAR_TURBINE = 'NUCLEAR_TURBINE'
    NUCLEAR_TURBINE_GEN = 'NUCLEAR_TURBINE_GEN'
    LIGNITE_OCTURBINE = 'LIGNITE_OCTURBINE'
    LIGNITE_CHP = 'LIGNITE_CHP'
    HARDCOAL_OCTURBINE = 'HARDCOAL_OCTURBINE'
    HARDCOAL_OCTURBINE_CHP = 'HARDCOAL_OCTURBINE_CHP'
    BIOMASS_TURBINE = 'BIOMASS_TURBINE'
    BIOMASS_TURBINE_CHP = 'BIOMASS_TURBINE_CHP'
    BIO_CH4_TURBINE = 'BIO_CH4_TURBINE'
    BIO_CH4_TURBINE_CHP = 'BIO_CH4_TURBINE_CHP'
    BATPOWER = 'BATPOWER'
    BIOMASS_FURNANCE = 'BIOMASS_FURNANCE'
    BIOMASS_FURNANCE_CHP = 'BIOMASS_FURNANCE_CHP'
    GEO = 'GEO'
    LIGHT_OIL = 'LIGHT_OIL'
    LIGHT_OIL_CHP = 'LIGHT_OIL_CHP'
    HEAVY_OIL = 'HEAVY_OIL'
    PH_TURBINE = 'PH_TURBINE'
    PH_TURBINE_PUMP = 'PH_TURBINE_PUMP'
    GAS_TURBINE = 'GAS_TURBINE'
    GAS_TURBINE_CHP = 'GAS_TURBINE_CHP'
    CH4_CCTURBINE = 'CH4_CCTURBINE'
    CH4_CCTURBINE_CHP = 'CH4_CCTURBINE_CHP'
    H2_ELECTROLYSER = 'H2_ELECTROLYSER'
    H2_ELECTROLYSER_FC = 'H2_ELECTROLYSER_FC'
    GAS_H2 = 'GAS_H2'
    H2 = 'H2'
    H2_FC = 'H2_FC'
    H2_storage_GASTURBINE = 'H2_storage_gasturbine'
    H2_storage_FUEL = 'H2_storage_fuel_cell'
    FUEL_CELL = 'FUEL_CELL'
    BAT1POWER = 'BAT1POWER'
    Battery_Energy_storage = 'Battery_Energy_storage'
    PH_storage = 'PH_storage'
    CCH2_TURBINE = 'CCH2_TURBINE'
    TRANSMISSION_IMPORT = 'TRANSMISSION_IMPORT'
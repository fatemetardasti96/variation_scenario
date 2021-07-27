from dataclasses import dataclass


@dataclass
class TechnologyType:
    UTILITY = 'utility'
    ROOFTOP = 'rooftop'
    UNKNOWN = 'unknown'
    HVAC = 'hvac'
    OFFSHORE = 'offshore'
    ONSHORE =  'onshore'
    BATTERY =  'battery'
    PUMPED = 'pumped'
    STEAM = 'steam'
    RUN_OF_RIVER =  'run-of-river'
    GAS =  'gas'
    COMBINED = 'combined cycle'
    COMBUSTION_ENGINE = 'combustion engine'
    HYDROGEN_FUELCELL = 'hydrogen fuelcell'
    HYDROGEN_GAS = 'hydrogen gas'
    TRADE_IMPORT = 'trade import'
    TRADE = 'trade'
    DC = 'DC'
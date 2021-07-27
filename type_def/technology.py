from dataclasses import dataclass

@dataclass
class Technology:
    PHOTOVOLTAICS = 'photovoltaics'
    GENERATOR = 'generator'
    TRANSMISSION = 'transmission'
    WIND_TURBINE = 'wind turbine'
    STORAGE = 'storage'
    CHP = 'chp'
    HYDRO_TURBINE = 'hydro turbine'
    GEOTHERMAL = 'geothermal'
    NUCLEAR = 'nuclear'
    UNKNOWN = 'unknown'
from dataclasses import dataclass

@dataclass
class OutputEnergy:
    ELECTRICITY = 'electricity'
    CO2 = 'co2'
    ELECTRIC_ENERGY = 'electric_energy'
    BATTERY_ENERGY = 'Battery_Energy'
    H2 = 'H2'
    H2_FC = 'H2_FC'
    HYDRO_ENERGY = 'hydro_energy'
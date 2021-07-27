from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeGenerator:
    technology: str 
    input_energy: str
    technology_type: Optional[str] = None


    def to_str(self):
        if not self.technology_type is None:
            return self.technology + '_' + self.input_energy + '_' + self.technology_type
        else:
            return self.technology + '_' + self.input_energy
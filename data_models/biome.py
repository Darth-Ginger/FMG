import json
from typing import List, Optional, Tuple, Dict

from pydantic import BaseModel, Field
from data_models import BiomeType, expandable



class Biome(expandable):
    id            : int                 
    name          : str               
    biome_type    : BiomeType         
    color         : str              
    cost          : int               
    habitability  : int       
    temp_range    : Tuple[int, int]    
    moisture_range: Tuple[int, int]
    icons         : Dict[str, int] 
    options       : Optional[Dict[str, str|int|List|float|bool]]
                
    @property
    def avg_temp(self) -> int:
        return (int)((self.temp_range[1] + self.temp_range[0]) / 2)
    
    @property
    def avg_moisture(self) -> int:
        return (int)((self.moisture_range[1] + self.moisture_range[0]) / 2)
    
    def __str__(self):
        return f"{{\n\t\"{self.name}\": {{\n\t\t\"id\": {self.id},\n\t\t\"color\": \"{self.color}\",\n\t\t\"cost\": {self.cost},\n\t\t\"habitability\": {self.habitability},\n\t\t\"temp_range\": [{self.temp_range[0]}, {self.temp_range[1]}],\n\t\t\"moisture_range\": [{self.moisture_range[0]}, {self.moisture_range[1]}],\n\t\t\"icons\": {json.dumps(self.icons)}\n\t}}\n}}\n"
                    
    def __repr__(self):
        return f"Biome(id={self.id}, name={self.name}, color={self.color}, cost={self.cost}, habitability={self.habitability}, temp_range={self.temp_range}, moisture_range={self.moisture_range}, icons={self.icons})"

class BiomeMatrix(BaseModel):
    """
    A matrix of biomes.
    
        Cold <--------------> Warm <--------------> Hot
    Dry   
     |  (cold, dry)      , (warm, dry)       , (hot, dry)]
     |  (cold, wetter)   , (warm, wetter)    , (hot, wetter)]
     |  (cold, wet)      , (warm, wet)       , (hot, wet)]
    Wet
        
    """
    rows   : int = Field(default=26, description="Number of rows in the matrix")
    columns: int = Field(default=5, description="Number of columns in the matrix")
    matrix : List[List[Optional[str]]]  = Field(default_factory=list, description="Matrix of biomes")
    temp_range: Tuple[float, float]     = Field(default=(float('inf'), float('-inf')), description="Min and max temperature")  # Min and max temperature
    moisture_range: Tuple[float, float] = Field(default=(float('inf'), float('-inf')), description="Min and max moisture")  # Min and max moisture
    
    def __init__(self, **data):
        super().__init__(**data)
        self.matrix = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        
    def set_rows(self, rows: int):
        self.rows = rows
        self.update_matrix()
        
    def update_matrix(self) -> None:
        self.matrix = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        
    def normalize(self, value: float, min_value: float, max_value: float) -> float:
        """Normalize a value to a 0-1 range."""
        return (value - min_value) / (max_value - min_value)

    def update_ranges(self, temp_range: Tuple[float, float], moisture_range: Tuple[float, float]) -> None:
        """Update global temperature and moisture ranges."""
        self.temp_range = (
            min(self.temp_range[0], temp_range[0]),
            max(self.temp_range[1], temp_range[1]),
        )
        self.moisture_range = (
            min(self.moisture_range[0], moisture_range[0]),
            max(self.moisture_range[1], moisture_range[1]),
        )

    def add_biome(self, *args) -> None:
        """Add a biome to the matrix."""
        if len(args) == 1 and isinstance(args[0], Biome):
            biome: Biome = args[0]
            self.add_biome(biome.name, biome.temp_range, biome.moisture_range)
            return
        elif len(args) == 3:
            biome_name, temp_range, moisture_range = args
        else:
            raise ValueError(f"Invalid arguments: {args}")
        
        self.update_ranges(temp_range, moisture_range)
        min_temp_idx = int(self.normalize(temp_range[0], *self.temp_range) * (self.columns - 1))
        max_temp_idx = int(self.normalize(temp_range[1], *self.temp_range) * (self.columns - 1))
        min_moisture_idx = int(self.normalize(moisture_range[0], *self.moisture_range) * (self.rows - 1))
        max_moisture_idx = int(self.normalize(moisture_range[1], *self.moisture_range) * (self.rows - 1))

        for r in range(min_moisture_idx, max_moisture_idx + 1):
            for c in range(min_temp_idx, max_temp_idx + 1):
                self.matrix[r][c] = biome_name

    def get_biome(self, temp: float, moisture: float) -> str|None:
        """Retrieve a biome based on temperature and moisture."""
        row = int(self.normalize(moisture, *self.moisture_range) * (self.rows - 1))
        column = int(self.normalize(temp, *self.temp_range) * (self.columns - 1))
        return self.matrix[row][column]
    
    
    def __getitem__(self, idx) -> List[str]:
        return self.matrix[idx]
    
    def __repr__(self):
        """Developer-friendly representation."""
        return (
            f"BiomeMatrix(rows={self.rows}, columns={self.columns}, "
            f"temp_range={self.temp_range}, moisture_range={self.moisture_range})"
        )

    def __str__(self):
        """User-friendly representation."""
        result = f"BiomeMatrix ({self.rows}x{self.columns})\n"
        result += f"Temperature Range: {self.temp_range}\n"
        result += f"Moisture Range: {self.moisture_range}\n"
        result += "Matrix:\n"
        for row in self.matrix:
            result += ", ".join(str(cell) if cell else "." for cell in row) + "\n"
        return result

class BiomeData(BaseModel):
    _standard_biomes_dict: Dict[str, Biome] = {}
    _special_biomes_dict: Dict[str, Biome] = {}
    temp_range: Tuple[float, float] = (0, 0)
    moisture_range: Tuple[float, float] = (0, 0)
    matrix: BiomeMatrix = BiomeMatrix()
                
    @property
    def _curr_index(self) -> int:
        return len({**self._standard_biomes_dict, **self._special_biomes_dict})

    def display_matrix(self):
        print(self.matrix)
        
    def display_matrix_indexes(self):
        result: str = ""
        for row in self.matrix.matrix:
            result += f"{", ".join(str(self[idx].id) if idx is not None else "." for idx in row)}\n"
        print(result)
        
    def add_biome(self, biome: Biome):
        if biome.name in self._standard_biomes_dict or biome.name in self._special_biomes_dict:
            raise ValueError(f"Biome with name {biome.name} already exists.")

        # Update global temperature and moisture ranges
        self.temp_range = (min(self.temp_range[0], biome.temp_range[0]), max(self.temp_range[1], biome.temp_range[1]))
        self.moisture_range = (min(self.moisture_range[0], biome.moisture_range[0]), max(self.moisture_range[1], biome.moisture_range[1]))
        
        # If the biome is basic or climactic, add it to the matrix
        if biome.biome_type == BiomeType.BASIC or (biome.options and biome.options.get("climactic", False)):
            self.matrix.add_biome(biome) 
            
        # Add the biome to the appropriate dictionary
        if biome.biome_type == BiomeType.BASIC:
            self._standard_biomes_dict[biome.name] = biome
        elif biome.biome_type == BiomeType.SPECIAL:
            self._special_biomes_dict[biome.name]  = biome
    
    def load_from_json(self, biomes_json_file):
        """
        Load biomes from a JSON file.
        The JSON should be an array of objects with 'name', 'description', and 'climate' keys.
        """
        with open(biomes_json_file, 'r') as file:
            data = json.load(file)
            for b_type in data.keys():
                for biome_name, biome_data  in data[b_type].items():
                    biome = Biome(
                        id             = self._curr_index + 1,
                        name           = biome_name,
                        biome_type     = (BiomeType.SPECIAL if b_type == "Special" else BiomeType.BASIC),
                        color          = biome_data['color'],
                        cost           = biome_data['cost'],
                        habitability   = biome_data['habitability'],
                        icons          = biome_data['icons'],
                        temp_range     = (biome_data['min_temp']    , biome_data['max_temp']),
                        moisture_range = (biome_data['min_moisture'], biome_data['max_moisture']),
                        options        = biome_data['options'] if 'options' in biome_data.keys() else {"has_options": False}
                    )
                    self.add_biome(biome)

    def __getitem__(self, biome_name):
        """
        Allow dictionary-like access by biome name.
        """
        return {**self._standard_biomes_dict, **self._special_biomes_dict}[biome_name]

    def __str__(self):
        return f"BiomeData(\n\t\"Basic\":\n\t\t{self._standard_biomes_dict}\t\"Special\":\n\t\t{self._special_biomes_dict})"

    def __repr__(self):
        return f"BiomeData(\"Basic\": {self._standard_biomes_dict},\"Special\": {self._special_biomes_dict})"

Biome.model_rebuild()
BiomeMatrix.model_rebuild()
BiomeData.model_rebuild()
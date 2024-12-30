from typing import List, Optional
from data_models.common import expandable
from data_models.enums import TerrainType


class Cell(expandable):
    """
    Represents a single cell in the map.
    
    Attributes:
        id:      int
        name:    str
        height:  Optional[float] 
        temp:    Optional[float]
        moist:   Optional[float]
        biome:   Optional[str] # Name of the Cells Biome
        terrain: Optional[TerrainType]
    """
    height      : Optional[float] # Height of the cell
    temp        : Optional[float] # Temperature of the cell
    moist       : Optional[float] # Moisture of the cell
    neighbors   : Optional[List[int]] = []  # List of neighboring cells by ID
    biome       : Optional[str]   # Name of the Cells Biom
    terrain     : Optional[TerrainType]
    # Additional attributes as needed
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Cell 1",
                "height": 10.5,
                "biome": "Wetland",
                "terrain": TerrainType.LAND
            }
        }
        
Cell.model_rebuild()
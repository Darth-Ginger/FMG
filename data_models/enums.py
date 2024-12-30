from enum import Enum

    
class TerrainType(str, Enum):
    LAND  = "land"
    WATER = "water"
    
class BiomeType(str, Enum):
    BASIC  = "basic"
    SPECIAL = "special"
from typing import List, Optional
from pydantic import BaseModel

from data_models.grid import Grid
from data_models.pack import Pack
from .cell import Cell


class World(BaseModel):
    width: int
    height: int
    grid: Optional[Grid] = None
    pack: Optional[Pack] = None
    temperature_map: Optional[List[List[float]]] = None
    moisture_map: Optional[List[List[float]]] = None
    height_map: Optional[List[List[float]]] = None
    seed: Optional[int] = None
    name: Optional[str] = "Unnamed World"

    def initialize_grid(self, cells_desired: int, spacing: float):
        """Initialize the Grid for the world."""
        from data_models.grid import GridFactory
        self.grid = GridFactory.create_grid(self.width, self.height, cells_desired, spacing)

    def initialize_pack(self):
        """Initialize the Pack for the world."""
        from data_models.pack import PackFactory
        if self.grid is None:
            raise ValueError("Grid must be initialized before creating a Pack.")
        self.pack = PackFactory.create_pack(self.grid)

    def update_temperature_map(self, modifier: float):
        """Apply a temperature modifier globally."""
        if self.temperature_map is None:
            raise ValueError("Temperature map has not been initialized.")
        self.temperature_map = [
            [temp + modifier for temp in row]
            for row in self.temperature_map
        ]

    def update_moisture_map(self, modifier: float):
        """Apply a moisture modifier globally."""
        if self.moisture_map is None:
            raise ValueError("Moisture map has not been initialized.")
        self.moisture_map = [
            [moist + modifier for moist in row]
            for row in self.moisture_map
        ]
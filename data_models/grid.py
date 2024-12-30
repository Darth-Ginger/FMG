from typing import Dict, List, Tuple

from pydantic import BaseModel, Field
from data_models.cell import Cell
from data_models.enums import TerrainType


class Grid(BaseModel):
    """
    Represents the initial map data structure before repacking.

    """
    
    width:    int = Field(..., default=100)
    height:   int = Field(..., default=100)
    cells:    List[List[Cell]] = []
    _cells_dict: Dict[int, Cell] = {}
    points:   List[Tuple[float, float]] = [] # Jittered points for the grid
    boundary: List[Tuple[int, int]] = []     # Boundary points for edge aproximation
    
    def __init__(self, **data):
        super().__init__(**data)
        self.cells = [[Cell(id=hash(f"{y}-{x}"), name=f"{y}-{x}") for x in range(self.width)] for y in range(self.height)]
        self.initialize_neighbors
    
    def get_cell(self, cell_id: int) -> Cell:
        return next((cell for cell in self.cells if cell.id == cell_id), None)
    
    def initialize_neighbors(self):
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                cell.neighbors = []
                if x > 0:
                    cell.neighbors.append(self.cells[y][x - 1].id) # Left
                if x < self.width - 1:
                    cell.neighbors.append(self.cells[y][x + 1].id) # Right
                if y > 0:
                    cell.neighbors.append(self.cells[y - 1][x].id) # Up
                if y < self.height - 1:
                    cell.neighbors.append(self.cells[y + 1][x].id) # Down
                if x > 0 and y > 0:
                    cell.neighbors.append(self.cells[y - 1][x - 1].id) # Top Left
                if x < self.width - 1 and y > 0:
                    cell.neighbors.append(self.cells[y - 1][x + 1].id) # Top Right
                if x < self.width - 1 and y < self.height - 1:
                    cell.neighbors.append(self.cells[y + 1][x + 1].id) # Bottom Right
                if x > 0 and y < self.height - 1:
                    cell.neighbors.append(self.cells[y + 1][x - 1].id) # Bottom Left
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "cellsDesired": 100,
                "spacing": 10.0,
                "cellsX": 10,
                "cellsY": 10,
                "points": [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)],
                "boundary": [(0, 0), (10, 0), (10, 10), (0, 10)],
                "cells": [
                    {
                        "id": 1,
                        "name": "Cell 1",
                        "height": 10.5,
                        "biome": "Wetland",
                        "terrain": TerrainType.LAND
                    }
                ]
            }
        }
        
Grid.model_rebuild()

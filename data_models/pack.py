from typing import List

from pydantic import BaseModel

from data_models.cell import Cell
from data_models.enums import TerrainType
from data_models.models import Burg, Culture, Feature, Marker, Province, Religion, Road, State


class Pack(BaseModel):
    """
    Represents the optimized map data structure after repacking.

    Attributes:
        cells (List[Cell]): Repacked cell data.
        features (List[Feature]): Geographical features such as islands, lakes, and oceans.
        cultures (List[Culture]): Cultural regions within the map.
        states (List[State]): Political states or countries.
        provinces (List[Province]): Subdivisions within states.
        burgs (List[Burg]): Settlements or towns.
        religions (List[Religion]): Religious regions.
        roads (List[Road]): Transportation routes.
        markers (List[Marker]): Points of interest or annotations.
    """
    cells:     List["Cell"]
    features:  List["Feature"]
    cultures:  List["Culture"]
    states:    List["State"]
    provinces: List["Province"]
    burgs:     List["Burg"]
    religions: List["Religion"]
    roads:     List["Road"]
    markers:   List["Marker"]
    # Additional attributes as needed
    
    class Config:
        json_schema_extra = {
            "example": {
                "cells": [
                    {
                        "id": 1,
                        "name": "Cell 1",
                        "height": 10.5,
                        "biome": "Wetland",
                        "terrain": TerrainType.LAND    
                    }
                ],
                "features": [],
                "cultures": [],
                "states": [],
                "provinces": [],
                "burgs": [],
                "religions": [],
                "roads": [],
                "markers": []
            }
        }
        
Pack.model_rebuild()
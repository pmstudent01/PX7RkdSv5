"""Pydantic request/response schemas for the HTTP API layer.

These mirror the vehicle payload used by the Vehicle Service Collection
(nickName, vin, make, model, year, miles).
"""

from typing import Optional

from pydantic import BaseModel, Field


class VehicleIn(BaseModel):
    """Vehicle payload accepted when creating or updating a vehicle."""

    nick_name: Optional[str] = Field(default=None, alias="nickName")
    vin: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    miles: Optional[int] = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "nickName": "The Lisa Marie",
                "vin": "4M2DV11W4RDJ53329",
                "make": "Mercury",
                "model": "Villager",
                "year": "1994",
                "miles": 159864,
            }
        },
    }

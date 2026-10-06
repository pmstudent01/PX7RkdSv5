"""FastAPI application implementing the Vehicle Service API.

Every endpoint delegates to the Postman-generated SDK
(`vehicle_service_collection_sdk`), which handles auth (X-API-Key),
URL building, and HTTP transport.

Endpoints:
    POST   /vehicles        -> create a vehicle
    GET    /vehicles/{id}   -> retrieve a vehicle
    PATCH  /vehicles/{id}   -> update a vehicle
    DELETE /vehicles/{id}   -> delete a vehicle
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Path

from .config import settings
from .schemas import VehicleIn
from .sdk_client import get_sdk

# Import SDK types lazily-safe: get_sdk() has already added the SDK to sys.path.
from vehicle_service_collection_sdk.models import CreateAVehicleRequest  # noqa: E402

app = FastAPI(
    title="Vehicle Service API",
    description=(
        "A Python app implementing the Vehicle Service Collection, powered by "
        "the Postman-generated SDK."
    ),
    version="1.0.0",
)


def _to_sdk_body(payload: VehicleIn) -> CreateAVehicleRequest:
    """Map the inbound HTTP schema to the SDK request model."""
    return CreateAVehicleRequest(
        nick_name=payload.nick_name,
        vin=payload.vin,
        make=payload.make,
        model=payload.model,
        year=payload.year,
        miles=payload.miles,
    )


def _call_sdk(fn, *args, **kwargs) -> Any:
    """Invoke an SDK method and translate failures into HTTP errors."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - surface SDK/transport errors uniformly
        status_code = getattr(exc, "status", None) or getattr(
            exc, "status_code", None
        )
        detail = getattr(exc, "message", None) or str(exc)
        raise HTTPException(status_code=status_code or 502, detail=detail) from exc


@app.get("/health", tags=["meta"])
def health() -> dict:
    """Simple liveness check that also reports the configured upstream."""
    return {"status": "ok", "base_url": settings.BASE_URL}


@app.post("/vehicles", tags=["vehicles"], status_code=201)
def create_vehicle(payload: VehicleIn) -> Any:
    """Create a new vehicle."""
    sdk = get_sdk()
    return _call_sdk(
        sdk.vehicle_service_collection_sdk.create_a_vehicle,
        _to_sdk_body(payload),
    )


@app.get("/vehicles/{vehicle_id}", tags=["vehicles"])
def retrieve_vehicle(vehicle_id: str = Path(..., description="Vehicle ID")) -> Any:
    """Retrieve a single vehicle by ID."""
    sdk = get_sdk()
    return _call_sdk(
        sdk.vehicle_service_collection_sdk.retrieve_a_vehicle,
        vehicle_id,
    )


@app.patch("/vehicles/{vehicle_id}", tags=["vehicles"])
def update_vehicle(
    payload: VehicleIn,
    vehicle_id: str = Path(..., description="Vehicle ID"),
) -> Any:
    """Update an existing vehicle by ID."""
    sdk = get_sdk()
    return _call_sdk(
        sdk.vehicle_service_collection_sdk.update_a_collection,
        _to_sdk_body(payload),
        vehicle_id,
    )


@app.delete("/vehicles/{vehicle_id}", tags=["vehicles"], status_code=204)
def delete_vehicle(vehicle_id: str = Path(..., description="Vehicle ID")) -> None:
    """Delete a vehicle by ID."""
    sdk = get_sdk()
    _call_sdk(
        sdk.vehicle_service_collection_sdk.delete_a_vehicle,
        vehicle_id,
    )
    return None

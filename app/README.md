# Vehicle Service API (Python)

A [FastAPI](https://fastapi.tiangolo.com/) app that implements the **Vehicle Service Collection**.
Every endpoint delegates to the Postman‑generated Python SDK
(`vehicle_service_collection_sdk`), which handles authentication (`X-API-Key`),
URL construction, and HTTP transport.

## Endpoints

| Method | Path             | SDK method            | Description        |
|--------|------------------|-----------------------|--------------------|
| POST   | `/vehicles`      | `create_a_vehicle`    | Create a vehicle   |
| GET    | `/vehicles/{id}` | `retrieve_a_vehicle`  | Retrieve a vehicle |
| PATCH  | `/vehicles/{id}` | `update_a_collection` | Update a vehicle   |
| DELETE | `/vehicles/{id}` | `delete_a_vehicle`    | Delete a vehicle   |
| GET    | `/health`        | –                     | Liveness check     |

Interactive docs are available at `/docs` once the server is running.

## Project layout

```
app/
├── __init__.py
├── config.py        # Env-driven settings (base URL, API key, timeout)
├── schemas.py       # HTTP request/response models
├── sdk_client.py    # Builds the generated SDK client (adds SDK to sys.path)
├── main.py          # FastAPI app + routes
├── requirements.txt
├── run.sh
└── .env.example
```

The app imports the generated SDK **in place** from
`postman/sdks/Collections SDKs/Vehicle Service Collection/python/src`, so no
separate install of the SDK package is required.

## Setup

```bash
# From the repo root
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r app/requirements.txt
```

## Configuration

Settings are read from environment variables (see `.env.example`):

| Variable                    | Default                 | Description                     |
|-----------------------------|-------------------------|---------------------------------|
| `VEHICLE_SERVICE_BASE_URL`  | `http://localhost:4500` | Upstream Vehicle Service API    |
| `VEHICLE_SERVICE_API_KEY`   | *(empty)*               | Value for the `X-API-Key` header |
| `VEHICLE_SERVICE_TIMEOUT`   | `30`                    | Per-request timeout (seconds)   |

## Run

```bash
# From the repo root
uvicorn app.main:app --reload --port 8000
# or
./app/run.sh
```

## Example requests

```bash
# Create
curl -X POST http://localhost:8000/vehicles \
  -H "Content-Type: application/json" \
  -d '{"nickName":"The Lisa Marie","vin":"4M2DV11W4RDJ53329","make":"Mercury","model":"Villager","year":"1994","miles":159864}'

# Retrieve
curl http://localhost:8000/vehicles/1

# Update
curl -X PATCH http://localhost:8000/vehicles/1 \
  -H "Content-Type: application/json" \
  -d '{"miles":159999}'

# Delete
curl -X DELETE http://localhost:8000/vehicles/1
```

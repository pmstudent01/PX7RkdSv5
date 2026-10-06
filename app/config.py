"""Application configuration.

Reads configuration from environment variables so the app can be pointed at
different Vehicle Service deployments without code changes.
"""

import os


class Settings:
    """Runtime settings for the Vehicle Service app."""

    # Base URL of the Vehicle Service API the SDK talks to.
    # Defaults to the Postman mock/local server used by this workspace.
    BASE_URL: str = os.getenv("VEHICLE_SERVICE_BASE_URL", "http://localhost:4500")

    # API key sent via the X-API-Key header (matches the collection auth).
    API_KEY: str = os.getenv("VEHICLE_SERVICE_API_KEY", "")

    # Per-request timeout in seconds.
    TIMEOUT: float = float(os.getenv("VEHICLE_SERVICE_TIMEOUT", "30"))


settings = Settings()

"""Thin wrapper that constructs the generated Vehicle Service SDK client.

The SDK source lives under:
    postman/sdks/Collections SDKs/Vehicle Service Collection/python/src

We add that path to sys.path at import time so the app can use the SDK
in-place without a separate `pip install` of the generated package.
"""

import os
import sys
from functools import lru_cache

# Resolve the SDK's `src` directory relative to the repo root and make it
# importable.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SDK_SRC = os.path.join(
    _REPO_ROOT,
    "postman",
    "sdks",
    "Collections SDKs",
    "Vehicle Service Collection",
    "python",
    "src",
)
if _SDK_SRC not in sys.path:
    sys.path.insert(0, _SDK_SRC)

from vehicle_service_collection_sdk import VehicleServiceCollectionSdk  # noqa: E402

from .config import settings  # noqa: E402


@lru_cache(maxsize=1)
def get_sdk() -> VehicleServiceCollectionSdk:
    """Return a cached, configured SDK client instance.

    The client is built from app settings (base URL, API key, timeout).
    """
    return VehicleServiceCollectionSdk(
        api_key=settings.API_KEY or None,
        base_url=settings.BASE_URL,
        timeout=settings.TIMEOUT,
    )

#!/usr/bin/env bash
# Start the Vehicle Service API on http://localhost:8000
set -euo pipefail
cd "$(dirname "$0")/.."
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

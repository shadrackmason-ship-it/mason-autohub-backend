#!/bin/bash
# mason-autohub-backend — start the API server
# Usage: ./start.sh
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d "venv" ] || [ ! -f "venv/bin/pip" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

venv/bin/pip install -r requirements.txt -q

echo ""
echo "✅  Backend running at → http://localhost:8001"
echo ""

DATABASE_URL="${DATABASE_URL:-sqlite:///./mason_autohub.db}" \
  venv/bin/uvicorn app.main:app --reload --port 8001

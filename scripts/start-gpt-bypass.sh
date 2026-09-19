#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
CONFIG_SRC="${GPT_BYPASS_CONFIG:-/Users/eidon/Documents/all/ops/inventory/.secrets/gpt-bypass/config.json}"
if [[ ! -f "$ROOT/config.json" ]]; then
  ln -sfn "$CONFIG_SRC" "$ROOT/config.json"
fi
if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  python3 -m venv "$ROOT/.venv"
  "$ROOT/.venv/bin/pip" install -q 'fastapi>=0.100.0' 'uvicorn>=0.23.0' 'httpx>=0.24.0'
fi
HOST="${GPT_BYPASS_HOST:-127.0.0.1}"
PORT="${GPT_BYPASS_PORT:-8999}"
exec "$ROOT/.venv/bin/python" "$ROOT/cli_app.py" serve --host "$HOST" --port "$PORT"

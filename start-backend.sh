#!/bin/bash
# Start Backend API Server

echo "================================================"
echo "🚀 Starting Skin Cancer Detector API"
echo "================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend" || exit 1

choose_python() {
    # Prefer Python 3.11 for compatibility with pinned ML stack (TF 2.15 / sklearn 1.3 / numpy 1.24).
    for c in python3.11 python3.12 python3.10 python3; do
        if command -v "$c" >/dev/null 2>&1; then
            echo "$c"
            return 0
        fi
    done
    return 1
}

PYTHON_BIN="${PYTHON_BIN:-$(choose_python)}"
if [ -z "$PYTHON_BIN" ]; then
    echo "❌ No python3 found on PATH."
    exit 1
fi

echo "Using Python: $PYTHON_BIN ($($PYTHON_BIN --version 2>/dev/null || echo 'unknown'))"

# If an existing venv was created with a different Python minor version, recreate it.
DESIRED_PY_MM="$($PYTHON_BIN -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')" 2>/dev/null || echo '')"
if [ -d ".venv" ] && [ -x ".venv/bin/python" ] && [ -n "$DESIRED_PY_MM" ]; then
    VENV_PY_MM="$(.venv/bin/python -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')" 2>/dev/null || echo '')"
    if [ -n "$VENV_PY_MM" ] && [ "$VENV_PY_MM" != "$DESIRED_PY_MM" ]; then
        echo "♻️  Recreating .venv (was Python $VENV_PY_MM, need $DESIRED_PY_MM)..."
        rm -rf .venv
    fi
fi

# Use a local venv to avoid system/pip mismatches
if [ ! -d ".venv" ]; then
    echo "🧰 Creating virtual environment (.venv)..."
    "$PYTHON_BIN" -m venv .venv || { echo "❌ Failed to create venv. Ensure python3 + venv are installed."; exit 1; }
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Venv Python: $(python --version 2>/dev/null || echo 'unknown')"

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Installing Python dependencies into venv..."
    python -m pip install --upgrade pip setuptools wheel || true
    python -m pip install -r requirements.txt || { echo "❌ pip install failed. See errors above."; exit 1; }
    echo ""
fi

echo "Starting Flask API server..."
echo "API will be available at: http://localhost:5001 (override with API_PORT=...)"
echo ""
echo "Press Ctrl+C to stop"
echo "================================================"
echo ""

python api.py

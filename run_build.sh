#!/usr/bin/env sh
set -e

if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# Activate the virtual environment.
# shellcheck source=/dev/null
. ./venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build complete."
echo "Run the app with: . ./venv/bin/activate && python app.py"

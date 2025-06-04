#!/bin/bash

set -e

PROJECT_NAME="Apolo Automation Tests"
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

echo "Setting up your $PROJECT_NAME environment..."

# --- 1. Install uv if missing ---
if ! command -v uv &>/dev/null; then
  echo "📦 Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
else
  echo "✅ uv is already installed."
fi

# --- 2. Create virtual environment ---
echo "📁 Creating virtual environment in ${VENV_DIR}"
uv venv "${VENV_DIR}"

# --- 3. Activate virtual environment ---
echo "🔁 Activating virtual environment..."
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

# --- 4. Install dependencies ---
if [[ -f "$REQUIREMENTS_FILE" ]]; then
  echo "📦 Installing dependencies from ${REQUIREMENTS_FILE}"
  uv pip install -r "${REQUIREMENTS_FILE}"
else
  echo "⚠️ ${REQUIREMENTS_FILE} not found. Skipping dependency install."
fi

# --- 5. Install Allure CLI if not available ---
if ! command -v allure &>/dev/null; then
  echo "📦 Installing Allure CLI via Homebrew..."
  if command -v brew &>/dev/null; then
    brew install allure
  else
    echo "❌ Homebrew not found. Please install Allure CLI manually:"
    echo "👉 https://docs.qameta.io/allure/#_installing_a_commandline"
  fi
else
  echo "✅ Allure CLI is already installed."
fi

# --- 6. Done ---
echo "✅ Setup complete!"
echo ""
echo "👉 To activate the environment: source ${VENV_DIR}/bin/activate"
echo "👉 To run tests:                  pytest tests/"
echo "👉 Allure report will be generated automatically"
echo "👉 To view the report:            open reports/allure-report/index.html"
echo "👉 To view the log file:          open reports/log/test_run.log"

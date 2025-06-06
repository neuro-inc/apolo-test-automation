#!/bin/bash

set -e

PROJECT_NAME="apolo-test-automation"
VENV_DIR=".venv"

echo "🚀 Setting up your ${PROJECT_NAME} environment..."

# --- 1. Install uv if not present ---
if ! command -v uv &> /dev/null; then
  echo "📦 uv not found. Installing..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
else
  echo "✅ uv is already installed."
fi

# --- 2. Install project dependencies ---
echo "📦 Installing dependencies from pyproject.toml"
uv sync

# --- 3. Install Allure CLI if not present ---
if ! command -v allure &> /dev/null; then
  echo "📦 Installing Allure CLI via Homebrew..."
  if command -v brew &> /dev/null; then
    brew install allure
  else
    echo "❌ Homebrew not found. Please install Allure CLI manually:"
    echo "👉 https://docs.qameta.io/allure/#_installing_a_commandline"
  fi
else
  echo "✅ Allure CLI is already installed."
fi

# --- 4. Done ---
echo ""
echo "✅ Setup complete!"
echo "👉 To activate the environment: source ${VENV_DIR}/bin/activate"
echo "👉 To run tests:                uv run pytest tests"
echo "👉 To view report:              open reports/allure-report/index.html"

# 🧪 Apolo Test Automation

All test execution and reporting is managed automatically using:

- [pytest](https://docs.pytest.org/)
- [allure-pytest](https://docs.qameta.io/allure/)
- [uv](https://github.com/astral-sh/uv) — fast dependency and virtual environment manager

---

## 🚀 Setup Instructions (macOS/Linux)

### 1. Clone the repository

```bash
git clone git@github.com:neuro-inc/apolo_test_automation.git
cd apolo_test_automation
```

### 2. Run the setup script

```bash
./setup.sh
```

This will:
- Install `uv` if it's not already installed
- Create a `.venv` virtual environment
- Install project dependencies from `pyproject.toml`
- Install Allure CLI (via Homebrew if available)

---

## ✅ Running Tests

### 1. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 2. Run the tests

```bash
pytest tests/
```

Tests will automatically generate Allure results and produce a report at:

```
reports/allure-report/index.html
```

And log file at:

```
reports/logs/test_run.log
```

---

## 📊 Viewing the Allure Report

After test execution, open the report in a browser:

### macOS
```bash
open reports/allure-report/index.html
```

### Linux
```bash
xdg-open reports/allure-report/index.html
```

---

## 📦 Dependency Management with `uv`

This project uses `uv` with `pyproject.toml` and `uv.lock`.

### Common commands:

```bash
uv sync                       # Install all project dependencies
uv add pytest                 # Add a new dependency
uv remove <package>           # Remove a dependency
uv pip list                   # Show installed packages
```

> Do not use `pip install` or `requirements.txt`.

---

## 🧼 Cleanup

All generated log and report files are deleted automatically before each test run.

To fully clean your local environment:

```bash
rm -rf .venv reports/
```

---

## 📁 Project Structure(to be updated...)

```
.
├── .venv/                     # Virtual environment (created automatically)
├── tests/                     # Test cases and steps
├── reports/                   # Allure results and logs
│   ├── allure-report/
│   ├── allure-results/
│   └── logs/
├── pyproject.toml             # Dependency + project config
├── uv.lock                    # Locked dependency versions
├── setup.sh                   # Setup script
└── README.md
```

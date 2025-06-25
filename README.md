# 🧪 Apolo Test Automation
### [📊 View Latest Allure Report](https://neuro-inc.github.io/apolo-test-automation/run-test-latest/index.html)

---
All test execution and reporting is managed automatically using:

- [pytest](https://docs.pytest.org/)
- [allure-pytest](https://docs.qameta.io/allure/)
- [uv](https://github.com/astral-sh/uv) — fast dependency and virtual environment manager

---

🕛 A nightly test run is executed from the `master` branch, and the latest Allure Reportis published automatically.
The link to the most recent test results is available at the top of this page.

---
## 🚀 Setup Instructions (macOS/Linux)

### 1. Clone the repository

```bash
git clone git@github.com:neuro-inc/apolo_test_automation.git
cd apolo
```

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies from pyproject.toml

```bash
uv sync
```

### 4. Install Playwright browsers

```bash
uv run python -m playwright install --with-deps
```

### 5. Install Allure

With brew:
```bash
brew install allure
```

Without brew:
```bash
mkdir -p allure-bin
curl -sSL -o allure.zip https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip
unzip -q allure.zip -d allure-bin
export PATH="$PWD/allure-bin/allure-2.27.0/bin:$PATH"
```

Check with:
```bash
allure --version
```


## ✅ Running Tests

```bash
uv run pytest tests/
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
└── README.md
```

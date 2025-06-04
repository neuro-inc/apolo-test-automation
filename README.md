# 🧪 Apolo Test Automation

All test execution and reporting is managed automatically.

---

## 🚀 Setup Instructions (macOS/Linux)

### 1. Clone the repository

```bash
git clone git@github.com:neuro-inc/apolo_test_automation.git
cd apolo
```

### 2. Run the setup script

```bash
./setup.sh
```

This will:
- Install `uv` if it's not already installed
- Create a `.venv` virtual environment
- Install project dependencies from `requirements.txt`
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

## 🔧 Dependencies

Dependencies are listed in `requirements.txt`. To manually install them:

```bash
uv pip install -r requirements.txt
```

---

## 🧼 Cleanup

All generated log and report files are deleted automatically before each test run.
To remove the virtual environment and Allure reports:

```bash
rm -rf .venv reports/
```

---

## 📁 Project Structure(to be updated...)

```
.
├── .venv/                     # Virtual environment (created automatically)
├── tests/                     # Your test cases
├── reports/                   # Allure results and report output
│   ├── allure-report/
│   ├── allure-results/
│   └── logs/
├── requirements.txt           # Dependencies
├── setup.sh                   # Project setup script
└── README.md
```

<div id="top"></div>

<!-- Shields -->
<p style="display: inline">
	<img alt="Static Badge" src="https://img.shields.io/badge/python-blue">
</p>

# Budgeting Application
GUI budgeting application with python and Qt.

## Table of Contents
- About the Project
- ScreenShots
- Environment
- Directory
- How to Build
- How to Use

## About the Project
A GUI budgeting application that tracks and calculates monthly balance based on user input.

## ScreenShots
<img width=50% alt="Image" src="https://github.com/user-attachments/assets/1506b816-6197-4888-8929-be9673fd5812" />

<img width=50% alt="Image" src="https://github.com/user-attachments/assets/824f8d63-2b8e-4a72-8341-95ad145a634e" />

<img width=50% alt="Image" src="https://github.com/user-attachments/assets/3bae948e-3656-4db5-af02-7e6bad74d237" />

<img width=50% alt="Image" src="https://github.com/user-attachments/assets/94315fb8-d8a6-467c-9d01-7dfa72922f70" />

## Environment
```text
Package    Version
---------- -------
pandas     3.1.1
PySide6    6.12.0
```

## Directory
```text
.
├── aggregate.py
├── database.db
├── database.py
├── input_subwin.py
├── input_tab_widget.py
├── main.py
├── my_proxystyle.py
├── piechart.py
├── README.md
├── requirements.txt
├── summary_subwin.py
├── summary_tab_widget.py
├── tab_widget.py
```

## Installation (Linux/Mac)
1.Install Python.

2.Clone the repository to your local environment.
```bash
git clone https://github.com/NNM-V/BudgetingApp.git
```

3.Move to the project directory in the terminal.

5.pip install required library with command below:
```bash
pip install -r requirements.txt
```

6.Run program with command below:
```bash
python3 main.py  
```

## How to Use
1.Press "Input" tab and choose either "expence/income" tab.

2.Set the date, content, amount, category and account of income/expenditure to record and press the record button.

3.Press "+" button besides the combo box to add category or account.

4.Open summary tab to check the aggregated data. Press the setting box to set the budget data for each month.
# Employee Salary Predictor

A basic employee salary regression project using the supplied `EMPLOYEES_SYSTEM.csv`, a Random Forest model, and a Flask form.

## Setup

Run these commands from this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Train and run

1. Open `ML models/train_model.ipynb` in VS Code and run all cells to train and save the model.
2. Start Flask from this folder:

```powershell
python app.py
```

Open http://127.0.0.1:5000. Training cleans duplicate rows, converts columns to numeric values, imputes missing feature values, evaluates on a held-out test split, then saves the full preprocessing/model pipeline to `artifacts/salary_model.joblib`. Flask loads that saved pipeline for predictions. The artifact is generated locally and is not committed.

The form asks for age, years of experience, years at the company, number of projects, and salary growth. The remaining model inputs use the training-data defaults. Predictions are shown in INR using the values in `CurrentSalary` without exchange-rate conversion. The CSV does not define a currency or pay period, so ensure its salaries are Indian rupees and consistently monthly or annual before treating predictions as Indian-market estimates.

## EDA notebook

Open `ML models/ML.ipynb` for the initial data inspection. The CSV is stored in the project root, one directory above the notebook.

## Notes

The dataset does not specify a pay period or provide code-to-name lookups for education and department. Predictions are estimates based on this dataset and should not be treated as compensation recommendations.
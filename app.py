from pathlib import Path
import math

import joblib
import pandas as pd
from flask import Flask, render_template, request

from salary_currency import format_indian_number


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "artifacts" / "salary_model.joblib"
app = Flask(__name__)
INPUT_FIELDS = (
    "Age",
    "YearsExperience",
    "NumProjects",
    "SalaryGrowthPercent",
    "YearsAtCompany",
)


def load_bundle():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    bundle = load_bundle()
    all_fields = bundle["fields"] if bundle else []
    fields_by_name = {field["name"]: field for field in all_fields}
    fields = [fields_by_name[name] for name in INPUT_FIELDS if name in fields_by_name]
    metrics = bundle["metrics"] if bundle else None
    values = {}
    prediction = None
    display_mae = format_indian_number(metrics["mae"]) if metrics else None
    error = None

    if request.method == "POST":
        if bundle is None:
            error = "Open ML models/train_model.ipynb and run all cells before making predictions."
        else:
            row = {field["name"]: field["default"] for field in all_fields}
            try:
                for field in fields:
                    name = field["name"]
                    raw_value = request.form.get(name, "").strip()
                    value = float(raw_value)
                    if not math.isfinite(value):
                        raise ValueError(f"{field['label']} must be a finite number.")
                    if not field["min"] <= value <= field["max"]:
                        raise ValueError(
                            f"{field['label']} must be between {field['min']:g} and {field['max']:g}."
                        )
                    if field["categorical"]:
                        valid_options = {option["value"] for option in field["options"]}
                        if not value.is_integer() or int(value) not in valid_options:
                            raise ValueError(f"Choose a valid {field['label'].lower()}.")
                        row[name] = int(value)
                    else:
                        row[name] = value
                    values[name] = raw_value

                input_data = pd.DataFrame([row], columns=bundle["feature_columns"])
                prediction = format_indian_number(float(bundle["model"].predict(input_data)[0]))
            except (ValueError, TypeError) as exc:
                error = str(exc) or "Enter valid values for all fields."

    return render_template(
        "index.html",
        fields=fields,
        metrics=metrics,
        display_mae=display_mae,
        values=values,
        prediction=prediction,
        error=error,
        model_ready=bundle is not None,
        rows_used=bundle["rows_used"] if bundle else None,
    )


if __name__ == "__main__":
    app.run(debug=True)
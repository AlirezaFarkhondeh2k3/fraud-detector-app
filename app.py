from flask import Flask, request, render_template
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import joblib
import os

# === Model Definition ===
class FraudNet(nn.Module):
    def __init__(self, input_dim):
        super(FraudNet, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# === Load Model and Scaler ===
MODEL_PATH = os.path.join("model", "fraud_model.pth")
SCALER_PATH = os.path.join("model", "scaler.save")

scaler = joblib.load(SCALER_PATH)
model = FraudNet(input_dim=30)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# === Flask App ===
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    table = None

    if request.method == "POST":
        if "file" in request.files and request.files["file"].filename != "":
            try:
                file = request.files["file"]
                df = pd.read_csv(file)

                required_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
                missing = [col for col in required_cols if col not in df.columns]
                if missing:
                    return render_template("index.html", prediction=f"CSV is missing required columns: {missing}")

                df = df[required_cols]

                # Scale 'Time' and 'Amount'
                df[['Time', 'Amount']] = scaler.transform(df[['Time', 'Amount']])

                # Rename to model-compatible format
                df.columns = [f'v{i}' for i in range(30)]

                inputs = torch.tensor(df.values, dtype=torch.float32)

                with torch.no_grad():
                    preds = model(inputs).numpy()
                    classes = (preds > 0.5).astype(int).flatten()

                df["Prediction"] = classes
                table = df.to_html(classes="table table-bordered", index=False)
                return render_template("results.html", prediction="Batch predictions generated.", table=table)

            except Exception as e:
                prediction = f"CSV Error: {str(e)}"
                return render_template("index.html", prediction=prediction)

        elif "manual" in request.form:
            try:
                values = [float(request.form.get(f'v{i}')) for i in range(30)]
                df = pd.DataFrame([values], columns=[f'v{i}' for i in range(30)])

                df_for_scaling = df[['v0', 'v29']].copy()
                df_for_scaling.columns = ['Time', 'Amount']
                scaled = scaler.transform(df_for_scaling)
                df.loc[:, ['v0', 'v29']] = scaled

                inputs = torch.tensor(df.values, dtype=torch.float32)

                with torch.no_grad():
                    pred = model(inputs).item()
                    pred_class = int(pred > 0.5)
                    prediction = f"Predicted: {'🚨 FRAUD' if pred_class == 1 else '✅ NOT FRAUD'} (Confidence: {pred:.4f})"
            except Exception as e:
                prediction = f"Manual Input Error: {str(e)}"

    return render_template("index.html", prediction=prediction, table=table)

if __name__ == "__main__":
    app.run(debug=True)

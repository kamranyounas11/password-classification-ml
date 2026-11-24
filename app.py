"""Password Strength Checker - Flask backend.
Loads the trained model (password_model.pkl) and predicts Weak / Medium / Strong.
Passwords are never stored or logged: they are only used in memory to compute features.
"""
import os
import pickle
import logging

import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "password_model.pkl")
FEATURES = ["length", "uppercase", "lowercase", "numeric", "special"]
LABELS = {0: "Weak", 1: "Medium", 2: "Strong"}

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
# Do not log request bodies (they contain passwords)
logging.getLogger("werkzeug").setLevel(logging.ERROR)


def extract_features(pw: str):
    """Same feature extraction used during training in the Colab notebook."""
    return [
        len(pw),
        sum(c.isupper() for c in pw),
        sum(c.islower() for c in pw),
        sum(c.isdigit() for c in pw),
        sum(not c.isalnum() for c in pw),
    ]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    pw = data.get("password", "")
    if not isinstance(pw, str) or not pw:
        return jsonify(error="Please enter a password."), 400
    if len(pw) > 256:
        return jsonify(error="Password is too long (max 256 characters)."), 400
    feats = extract_features(pw)
    del pw  # discard the password as soon as features are extracted
    X = pd.DataFrame([feats], columns=FEATURES)
    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0].max() if hasattr(model, "predict_proba") else None
    resp = jsonify(
        strength=LABELS[pred],
        label=pred,
        confidence=round(float(proba) * 100, 1) if proba is not None else None,
        features=dict(zip(FEATURES, feats)),
    )
    resp.headers["Cache-Control"] = "no-store"
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

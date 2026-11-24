# Password Classification Using Machine Learning

Classifies a password as **Weak**, **Medium** or **Strong** with a Random Forest model, and serves it through a responsive HTML/CSS website with a Python (Flask) backend.

## Project files
| File | Purpose |
|---|---|
| `Password_Classification.ipynb` | Google Colab notebook: dataset download, cleaning, feature extraction, training, testing, saving |
| `password_model.pkl` | Trained Random Forest model (Pickle) |
| `app.py` | Flask backend: extracts features and predicts with the `.pkl` model |
| `templates/index.html` | Frontend page |
| `static/style.css` | Styling (responsive) |
| `static/script.js` | Live feature display and call to the backend |
| `requirements.txt` | Python dependencies |

## Dataset
[Password Strength Classifier Dataset](https://www.kaggle.com/datasets/bhavikbb/password-strength-classifier-dataset) by Bhavik Bansal on Kaggle (`data.csv`, columns `password`, `strength`: 0 = Weak, 1 = Medium, 2 = Strong). The notebook downloads it automatically with `kagglehub`.

After cleaning (nulls, duplicates, invalid labels and empty passwords removed): **669,639 passwords** (Weak 89,701 · Medium 496,801 · Strong 83,137).

## Features
Length · Uppercase letters · Lowercase letters · Digits · Special characters

## Model and results
- Random Forest (50 trees, max depth 15), stratified 80/20 split, duplicates removed before splitting (no leakage)
- **Test accuracy: 100.00%** on 133,928 unseen passwords (precision/recall/F1 = 1.00 for all classes)
- Why so high: the dataset's labels were produced by commercial strength meters that rate passwords on these same length and character-type properties, so the five features fully determine the label.

## Run the website
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 and enter a password.

**Privacy:** passwords are sent only to the local backend, used in memory to compute features, and never stored or logged.

# 🎯 Hiring Intelligence — Streamlit App

An interactive recruitment analytics and prediction app built on a **Tuned Gradient Boosting** model trained on 1,500 candidate records.

| Metric | Score |
|---|---|
| Hired Precision | 94.7% |
| F1-macro | 89.7% |
| ROC-AUC | 93.3% |

🔗 **Live demo:** `https://YOUR-APP-NAME.streamlit.app` ← replace after deploying

---

## Features

- **EDA Explorer** — Dataset overview, feature distributions by hiring outcome, recruitment strategy breakdown, and Pearson correlation chart
- **Hiring Predictor** — Enter candidate details and get an instant hire/reject recommendation with probability gauge, profile radar, and composite score

---

## Project Structure

```
hiring_app/
├── app.py                        # Main Streamlit app
├── requirements.txt              # Python dependencies
├── tuned_gb_hiring_model.pkl     # Trained model
├── recruitment_data.csv          # Dataset
└── .streamlit/
    └── config.toml               # Theme config
```

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/hiring-app.git
cd hiring-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

App opens at: http://localhost:8501

---

## Deploy to Streamlit Community Cloud (free)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "initial hiring app"
git remote add origin https://github.com/YOUR_USERNAME/hiring-app.git
git push -u origin main
```

### 2. Deploy
- Visit: https://share.streamlit.io
- Sign in with GitHub
- Click **New app**
- Select your repo → branch: `main` → file: `app.py`
- Click **Deploy** — live in ~2 minutes

### 3. Note on large files
If `tuned_gb_hiring_model.pkl` is over 100MB, track it with Git LFS:
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git commit -m "track pkl with lfs"
git push
```

For files under 100MB, committing directly to the repo is fine.

---

## Data Source

[Predicting Hiring Decisions in Recruitment — Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/predicting-hiring-decisions-in-recruitment-data/data)

A synthetic dataset of 1,500 candidates with demographic, experience, and assessment features used to model binary hiring decisions across three recruitment strategies.

---

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Plotly](https://plotly.com/python/) — Interactive charts
- [scikit-learn](https://scikit-learn.org/) — Gradient Boosting model
- [pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — Data processing
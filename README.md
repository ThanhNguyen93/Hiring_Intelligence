# 🎯 Hiring Intelligence

> An end-to-end machine learning app that predicts hiring outcomes and surfaces recruitment insights from candidate data.

🔗 **Live App:** [hiring-intelligence.streamlit.app](https://hiring-intelligence.streamlit.app)

---

## Overview

Hiring Intelligence is an interactive data science web app built to help HR teams understand what drives hiring decisions and predict whether a candidate will be hired — before the final call.

The app combines **exploratory data analysis** with a **Tuned Gradient Boosting model** trained on 1,500 synthetic recruitment records, achieving 94.7% precision on hired candidates.

---

## Demo

| EDA Explorer | Hiring Predictor |
|---|---|
| Feature distributions, strategy breakdown, signal strength chart | Candidate form, hire/reject prediction, probability gauge, profile radar |

---

## Key Findings

- **Recruitment strategy is the #1 predictor** (SHAP = 3.052) — stronger than any candidate quality signal
- Aggressive recruitment yields the highest share of hires (68.6% of all hired candidates)
- Interview Score, Skill Score, and Education Level are the top candidate-level signals

---

## Model Performance

| Metric | Score |
|---|---|
| Hired Precision | 94.7% |
| F1-macro | 89.7% |
| ROC-AUC | 93.3% |

---

## Tech Stack

| Layer | Tools |
|---|---|
| App framework | Streamlit |
| Visualization | Plotly |
| ML model | scikit-learn — Gradient Boosting (tuned) |
| Data processing | pandas, NumPy |
| Deployment | Streamlit Community Cloud |

---

## Project Structure

```
Hiring_Intelligence/
└── streamlit_deployment/
    ├── app.py                      # Main Streamlit app
    ├── requirements.txt            # Python dependencies
    ├── tuned_gb_hiring_model.pkl   # Trained model
    └── recruitment_data.csv        # Dataset
```

---

## Run Locally

```bash
git clone https://github.com/ThanhNguyen93/Hiring_Intelligence.git
cd Hiring_Intelligence/streamlit_deployment
pip install -r requirements.txt
streamlit run app.py
```

App opens at: http://localhost:8501

---

## Data Source

[Predicting Hiring Decisions in Recruitment — Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/predicting-hiring-decisions-in-recruitment-data/data)

A synthetic dataset of 1,500 candidates with demographic, experience, and assessment features across three recruitment strategies (Aggressive, Moderate, Conservative).

---

## Author

**Thanh Brown**  
[GitHub](https://github.com/ThanhNguyen93) 

# 📊 BPD - Business Performance Dashboard

A comprehensive Streamlit dashboard for business analytics and predictive modeling.

## 🛠️ Key Features

- **Interactive Data Exploration**
  - Multi-page streamlined interface
  - Automated data visualizations with Plotly
  - Real-time KPI tracking

- **Advanced Analytics**
  - Time series forecasting (Prophet)
  - ML model training and evaluation
  - Feature importance analysis with SHAP

- **Business Intelligence Tools**
  - PDF report generation
  - Excel/CSV exports
  - Automated email reporting

## 🔧 Project Structure

```
bpd/
├── app.py              # Main application entry
├── data/              # Data storage
├── models/            # Trained models
├── pages/             # Streamlit pages
│   ├── home.py
│   ├── dashboard.py
│   ├── forecasting.py
│   ├── ml_insights.py
│   ├── export.py
│   └── settings.py
├── utils/             # Helper functions
└── requirements.txt   # Dependencies
```

## ⚡ Quick Start

1. Clone repository:
```bash
git clone https://github.com/MrPrince419/bpd.git
cd bpd
```

2. Setup virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Launch dashboard:
```bash
streamlit run app.py
```

## 📫 Contact

- GitHub: [MrPrince419](https://github.com/MrPrince419)
- Project Issues: [Bug Reports](https://github.com/MrPrince419/bpd/issues)

---

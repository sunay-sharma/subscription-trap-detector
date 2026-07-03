# subscription-trap-detector
 Detects subscription overspending automatically from banking transactions — ML anomaly detection + interactive Streamlit dashboard. 600K transactions, 12K anomalies found.

# 🔍 Subscription Trap Detector

**Machine Learning system that detects subscription overspending from banking transactions**

> Right now, money is leaving people's bank accounts through forgotten, unused, and overpriced subscriptions — and most of them don't even know it. This project detects it automatically.

Built by **Sunay Sharma**

---

## 📌 What It Does

The Subscription Trap Detector is an **end-to-end analytics pipeline** that processes banking transactions to automatically identify customers who are overspending on subscriptions — including "zombie subscriptions" (paid but unused services).

**Key results:**

| Metric | Value |
|---|---|
| Transactions analysed | **600,000** (BankSim dataset) |
| Subscription customers profiled | **239,785** |
| Anomalies detected (Isolation Forest) | **11,990** (5.00%) |
| Overspenders flagged (95th percentile) | **11,987** (5.00%) |
| Total at-risk customers | **18,996** (7.92%) |
| Avg annual subscription cost | **€214.51** per customer |

Two independent detection methods — a machine learning model and a statistical threshold — converged on nearly identical results, confirming the signal is real.

---

## 🖥️ The Dashboard

A 5-page interactive **Streamlit** app with real-time filtering:

- **Overview** — KPI cards + monthly spending trend (January sign-up spike clearly visible)
- **EDA** — category, gender, and age group breakdowns
- **Anomalies** — Isolation Forest scatter plot + customer risk table (High / Medium / Low)
- **Zombie Subs** — flagged low-activity subscription accounts
- **Customer View** — look up any customer by ID and see their full risk profile instantly

All pages respond in real time to **Gender**, **Age Group**, and **Category** filters.

---

## ⚙️ How It Works — Pipeline

```
Raw Data (BankSim) → Clean & Filter → EDA → Feature Engineering → Anomaly Detection → Streamlit Dashboard
```

1. **Data Collection & Cleaning** — 600K rows loaded, duplicates removed, dates parsed, subscription transactions tagged via merchant category (`es_health`, `es_tech`)
2. **Exploratory Data Analysis** — monthly trends, demographic breakdowns, correlation analysis
3. **Feature Engineering** — 5 customer-level metrics: total spend, average spend, subscription count, monthly cost, annual cost
4. **Anomaly Detection** — three complementary methods:
   - **Isolation Forest** (`contamination=0.05`, `random_state=42`) — unsupervised ML, detects both high and low spending extremes
   - **DBSCAN** (`eps=0.8`, `min_samples=5`) — density-based clustering on a 5,000-customer sample
   - **95th Percentile Threshold** (~€474.75) — transparent, auditable statistical flag
5. **Dashboard Deployment** — interactive Streamlit app

---

## 🛠️ Tech Stack

| Component | Tools |
|---|---|
| Language | Python 3 |
| Data handling | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn (Isolation Forest, DBSCAN, StandardScaler) |
| Dashboard | Streamlit |
| Environment | Jupyter Notebook, VS Code |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/subscription-trap-detector.git
cd subscription-trap-detector
```

### 2. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn streamlit
```

### 3. Get the dataset

The BankSim dataset (600K transactions) is not included in this repo due to file size.
Download it from the source: [Sparkov Data Generation](https://github.com/namebrandon/Sparkov_Data_Generation)
Place `banksim.csv` in the project root.

### 4. Run the analysis notebook (optional)

```bash
jupyter notebook Subscription_trap_detector_eda.ipynb
```

This generates `cleaned_subscription_data.csv` and `customer_subscription_features.csv`.

### 5. Launch the dashboard

```bash
python -m streamlit run streamlit_dashboard.py
```

Open **http://localhost:8501** in your browser.

---

## 📊 Key Findings

- **The January Spike** — subscription spending surges to ~€9M in January (new-year sign-ups) before stabilising at ~€4.4M/month. The subscription trap, visible in the data.
- **Bimodal anomalies** — Isolation Forest flags both extremely low spenders (likely dormant subscriptions, avg ~€9) and extreme overspenders (avg ~€493).
- **Overspenders average €487.44** — nearly 2× the dataset mean of €250.27.
- **Demographics don't predict risk** — gender differences are under €0.50 per transaction; overspending is behavioural, not demographic.

---

## 💼 Why It Matters

The average customer in this data wastes **€214.51 per year** on subscriptions. Scaled to a bank with a million customers, that's over **€200 million in recoverable savings** — value a bank or fintech could surface automatically to build customer loyalty.

- **Banks** → customer retention through financial wellness features
- **Fintechs** → a ready-made subscription-audit product feature
- **Consumers** → direct money back in their pockets

---

## ⚠️ Limitations

- BankSim is a **simulated** dataset (based on real Spanish banking patterns) — a privacy advantage (no real customer data at risk), but findings need validation on live data
- No usage-frequency data → zombie subscription detection is approximated via transaction patterns
- DBSCAN applied to a 5,000-customer sample due to memory constraints
- Static 14-month window — no real-time ingestion (yet)

## 🔮 Roadmap

- Real-time integration via Open Banking / PSD2 APIs
- LSTM / Autoencoder models for temporal anomaly patterns
- App-usage data integration for true zombie detection
- Personalised AI alerts — *"cancel X to save €Y per year"*
- Public deployment on Streamlit Community Cloud

---

## 📁 Project Structure

```
subscription-trap-detector/
├── streamlit_dashboard.py                  # 5-page interactive dashboard
├── Subscription_trap_detector_eda.ipynb    # Full analysis notebook
├── cleaned_subscription_data.csv           # Processed subscription transactions
├── customer_subscription_features.csv      # Customer-level ML features
├── README.md
└── .gitignore                              # excludes banksim.csv (too large)
```

---

## 👤 Author

**Sunay Sharma**

*If this project interests you, feel free to open an issue or connect!*

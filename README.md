# Real Madrid Financial Intelligence & Strategic Analytics Platform

A professional-grade, 100% Pure Python interactive sports finance analytics system built for executives, sports investors, and football finance analysts. The dashboard evaluates Real Madrid CF's financial transformation, revenue engines, cost efficiency, squad investment ROI, Santiago Bernabéu renovation business impact, downside stress testing, 3-statement cash flow decomposition, and European elite club benchmarking across 10+ seasons (2014/15 – 2024/25) with 3-season ML forecasts.

---

## 🏗️ Pure Python Tech Stack

- **Dashboard UI**: [Streamlit](https://streamlit.io/) (100% Python interactive web framework)
- **Visualizations**: [Plotly Express & Graph Objects](https://plotly.com/python/) (Stacked Area, P&L Waterfall, Scatter Plots, Indicators, Dual-Axis Charts)
- **REST API & Export Engine**: [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **Data Engineering & ML**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [Scikit-Learn](https://scikit-learn.org/) (Ridge Time-Series Regression)
- **Database**: SQLite3 (Star Schema Data Warehouse)
- **Automated Testing**: [pytest](https://docs.pytest.org/)

---

## 🌟 Key Features & Pages

1. **Page 1: Executive Financial Overview**
   - 8 KPI cards (Revenue, YoY growth %, EBITDA, Net profit, Cash, Net Debt, Wage/Rev %, Squad Market Value).
   - Financial Health Index breakdown (0-100 score).
   - **3-Statement Cash Flow Decomposition** (Operating, Investing, Financing cash flows).

2. **Page 2: Revenue Engine**
   - Stacked area evolution of Commercial, Broadcasting, and Matchday revenue.
   - **Granular Commercial Sub-Segment Breakdown** (Adidas, Emirates, HP sleeve, Global partners, Retail/Merchandise, Tours).

3. **Page 3: Cost Structure & Efficiency**
   - P&L Expense Waterfall chart for latest season.
   - Wage-to-Revenue Ratio trend vs UEFA Financial Fair Play (FFP) 70% threshold limit.

4. **Page 4: Squad Investment Analytics**
   - Interactive Scatter Plot (X: Annual Salary, Y: Performance Score, Bubble Size: Market Value).
   - **Capital Gains on Player Sales (*Plusvalías*)** accounting table.

5. **Page 5: Sporting Success vs Financial Power**
   - Revenue & Wage bill vs Trophies won per season.
   - Football ROI Score formula calculator ($\text{Success Points} / \text{Financial Investment}$).

6. **Page 6: Santiago Bernabéu & Risk**
   - Interactive scenario simulator (Conservative, Base, Optimistic).
   - **Downside Stress Testing Simulator** (UCL Early Exit shock, Wage Inflation shock, Combined shock).

7. **Page 7: European Benchmark**
   - Multi-club benchmark comparing Real Madrid, Manchester City, FC Barcelona, Bayern Munich, Liverpool, and PSG.
   - Competitive Positioning Matrix (Financial Power vs Sporting Success).

8. **Page 8: ESG & Femenino**
   - Real Madrid Femenino commercial & wage ratio evolution.
   - ESG Governance & Sustainability metrics (LEED Gold, 100% renewable energy, €450M Madrid GDP impact).

---

## 🚀 Quick Start Guide

### 1. Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Data Pipeline & Launch App

Run the master launcher script to execute ETL ingestion, ML forecasting, and start both the REST API and Streamlit dashboard:

```bash
python run_app.py
```

Access the Streamlit Dashboard at `http://localhost:8501`.
Access the FastAPI Documentation at `http://localhost:8000/docs`.

### 3. Individual Execution Commands

- **Run Data Pipeline Only**:
  ```bash
  python run_app.py --pipeline
  ```

- **Run FastAPI Backend Server Only**:
  ```bash
  python run_app.py --backend
  ```

- **Run Streamlit Dashboard Only**:
  ```bash
  python run_app.py --dashboard
  ```

### 4. Run Automated Tests

Execute the complete pytest suite:
```bash
pytest tests/ -v
```

---

## 📁 Repository Structure

```
real-madrid-analytics/
├── backend/                  # FastAPI REST API Backend
│   ├── main.py
│   └── routes/
│       └── analytics.py
├── dashboard/                # Streamlit Pure Python Executive Dashboard
│   ├── app.py                # Main application entry point
│   ├── components/           # Reusable UI components (header, kpi_card)
│   ├── pages/                # 8 Interactive analytics dashboard pages
│   └── utils/                # API client data fetcher & custom CSS design system
├── data/                     # SQLite database & exported JSON dataset warehouse
├── data_pipeline/            # ETL pipeline and ML forecasting scripts
│   ├── ingest_data.py
│   ├── forecasting.py
│   └── star_schema.sql
├── tests/                    # Automated pytest test suite
│   ├── test_api.py
│   ├── test_pipeline.py
│   └── test_dashboard.py
├── notebooks/                # Financial intelligence exploratory Jupyter notebook
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
├── run_app.py                # Master CLI application launcher
└── README.md
```

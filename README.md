# Real Madrid Financial Intelligence Dashboard

A professional-grade interactive sports finance analytics system built for executives, sports investors, and football finance analysts. The dashboard evaluates Real Madrid CF's financial transformation, revenue engines, cost efficiency, squad investment ROI, Bernabéu renovation business impact, downside stress testing, cash flow decomposition, and European elite club benchmarking across 10+ seasons (2014/15 – 2024/25) with 3-season ML forecasts.

---

## 🌟 Key Features

1. **Page 1: Executive Financial Overview**
   - 8 KPI cards (Revenue, YoY growth %, EBITDA, Net profit, Cash, Net Debt, Wage/Rev %, Squad Market Value).
   - Financial Strength Index (0-100 gauge).
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
   - Football ROI Score formula calculator ($(\text{Success Points}) / (\text{Financial Investment})$).

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

### Start Backend & Pipeline
```bash
python data_pipeline/ingest_data.py
python data_pipeline/forecasting.py
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Start Frontend Dashboard
```bash
cd frontend
npm run dev
```
Open browser at `http://localhost:5173`.

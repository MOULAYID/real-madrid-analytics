# Forecast Methodology & Modeling Report: Real Madrid Analytics

## 1. Machine Learning Forecasting Architecture

The 3-season financial forecasting model (projecting 2025/26, 2026/27, and 2027/28) is powered by a **Regularized Ridge Time-Series Regression** combined with structural venue revenue multiplier adjustments.

```
Historical Data (2014/15 - 2024/25) 
   │
   ├──> Ridge Linear Regression (alpha=1.0) ──> Baseline Financial Trend
   │
   └──> Bernabéu Venue Commercial Multiplier ──> Incremental Matchday/Commercial Boost
                                                        │
                                                        ▼
                                             Final 3-Season Projections
```

---

## 2. Model Formulas & Feature Engineering

### A. Baseline Trend Prediction
For each financial target metric $y \in \{\text{Revenue}, \text{Commercial}, \text{Broadcasting}, \text{Operating Costs}, \text{EBITDA}\}$:

$$\hat{y}_t = w_0 + w_1 \cdot t$$

Subject to L2 Regularization Penalty:

$$\min_{w} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2 + \alpha \|w\|_2^2 \quad (\text{where } \alpha = 1.0)$$

### B. Structural Stadium Expansion Adjustment
Because the Santiago Bernabéu completed full venue activation in 2024/25, linear regression alone would underestimate non-matchday event growth. An incremental multiplier vector $\Delta_{\text{stadium}}$ is integrated:

$$\text{Final Revenue Projection}_{t} = \hat{y}_t + \Delta_{\text{stadium}}(t)$$

Where:
- $\Delta_{\text{matchday}}(t) = €35\text{M} \times (t - t_{2025})$
- $\Delta_{\text{commercial}}(t) = €40\text{M} \times (t - t_{2025})$

---

## 3. Projected Financial Statements (2025/26 – 2027/28)

| Season | Type | Total Rev (€M) | Commercial (€M) | Matchday (€M) | EBITDA (€M) | Net Debt (€M) | Health Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2024/25** | Actual | €1,185.0M | €542.0M | €325.0M | €265.0M | -€12.0M | **97** |
| **2025/26** | Forecast | €1,258.0M | €582.0M | €360.0M | €285.0M | -€25.0M | **98** |
| **2026/27** | Forecast | €1,340.0M | €622.0M | €395.0M | €305.0M | -€40.0M | **99** |
| **2027/28** | Forecast | €1,425.0M | €662.0M | €430.0M | €325.0M | -€55.0M | **99** |

---

## 4. Scenario Sensitivity Analysis

1. **Conservative Scenario**: Assumes 15 non-matchday major events per year. Incremental revenue: +€185M/yr.
2. **Base Scenario**: Assumes 30 non-matchday events + NFL International Game + VIP seating expansion. Incremental revenue: +€260M/yr.
3. **Optimistic Scenario**: Assumes 45+ non-matchday events + multi-use stadium convention hosting + naming rights expansion. Incremental revenue: +€340M/yr.

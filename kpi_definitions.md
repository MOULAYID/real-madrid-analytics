# KPI Definitions & Formula Reference: Real Madrid Analytics

This document provides formal mathematical definitions, business logic, and benchmark thresholds for all Key Performance Indicators used across the dashboard.

---

## 1. Executive Financial & Accounting Metrics

### Financial Health Score (0-100)
$$\text{Financial Score} = \min\Big(99, \big(1.2 \times \Delta\text{Rev}\%\big) + \big(1.5 \times \text{EBITDA Margin}\%\big) + \big(0.3 \times \text{Debt Factor}\big) + \big(0.2 \times \text{Cash Factor}\big) + \big(0.4 \times \text{Comm Share}\%\big)\Big)$$

### Capital Gain on Player Sale (*Plusvalía en Traspasos*)
$$\text{Net Capital Gain} = \text{Gross Sale Price} - \text{Remaining Unamortized Book Value}$$
Where $\text{Remaining Book Value} = \text{Initial Transfer Fee} - \sum \text{Accumulated Amortization}$.

### Wage-to-Revenue Ratio (%)
$$\text{Wage Ratio} = \left( \frac{\text{Total Wages \& Staff Costs}}{\text{Total Operating Revenue}} \right) \times 100$$
- **UEFA FFP Benchmark Threshold**: $< 70\%$
- **Optimal Target**: $\le 55\%$ (Real Madrid: 45.6% in 2024/25)

---

## 2. 3-Statement Cash Flow Metrics

### Net Cash Flow Change (€ Millions)
$$\Delta\text{Cash} = \text{Operating Cash Flow} + \text{Investing Cash Flow} + \text{Financing Cash Flow}$$

Where:
- $\text{Operating Cash Flow} = \text{Net Profit} + \text{Amortization} \pm \Delta\text{Working Capital}$
- $\text{Investing Cash Flow} = -(\text{Bernabéu Capex} + \text{Net Player Transfer Cash Outflows})$
- $\text{Financing Cash Flow} = \text{Debt Drawdowns} - \text{Debt Repayments} - \text{Interest Expenses}$

---

## 3. Downside Risk & Stress Testing Metrics

### Stress Net Profit Impact (€ Millions)
$$\text{Net Profit}_{\text{stress}} = \text{Baseline Net Profit} + \Delta\text{UCL Prize Money} - \Delta\text{Wage Inflation}$$

Where:
- $\Delta\text{UCL Prize Money} = \text{UCL Prize Money}_{\text{R16}} - \text{UCL Prize Money}_{\text{Winner}} = €65\text{M} - €140\text{M} = -€75\text{M}$

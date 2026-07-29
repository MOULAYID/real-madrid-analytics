# Data Model Documentation: Real Madrid Analytics

## Expanded Star Schema Architecture

The analytical backend utilizes an enriched **Star Schema** with 5 new institutional data domains:
1. `commercial_breakdown.json` (Kit, Shirt, Sleeve, Global, Retail, Tour sub-segments)
2. `capital_gains.json` (Player sale price, unamortized book value, plusvalías)
3. `cash_flow.json` (Operating, Investing, Financing cash flows)
4. `stress_testing.json` (Downside sporting & macro shocks)
5. `esg_femenino.json` (Women's team economics & ESG sustainability metrics)

```mermaid
erDiagram
    Dim_Date ||--o{ Fact_Financials : "has season"
    Dim_Date ||--o{ Fact_Transfers : "recorded in"
    Dim_Date ||--o{ Fact_Sporting_Performance : "achieved in"
    Dim_Date ||--o{ Fact_Player_Economics : "evaluates"
    Dim_Date ||--o{ Fact_Commercial_Breakdown : "breaks down"
    Dim_Date ||--o{ Fact_Cash_Flow : "decomposes"

    Dim_Date {
        string season PK
        int year
        boolean is_forecast
    }

    Fact_Commercial_Breakdown {
        string season PK, FK
        double adidas_kit_supplier
        double emirates_main_sponsor
        double hp_sleeve_sponsor
        double global_partners
        double retail_merchandise
        double tours_exhibition
        double total_commercial
    }

    Fact_Capital_Gains {
        string season FK
        string player_sold
        double sale_price
        double book_value
        double capital_gain
    }

    Fact_Cash_Flow {
        string season PK, FK
        double operating_cash_flow
        double investing_cash_flow
        double financing_cash_flow
        double net_cash_change
        double ending_cash_balance
    }

    Fact_Stress_Testing {
        string scenario_id PK
        string scenario_name
        double ucl_prize_money
        double revenue_impact
        double net_profit_impact
        double result_profit
        string status
    }
```

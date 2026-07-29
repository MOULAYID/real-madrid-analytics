-- Star Schema for Real Madrid Financial Intelligence Dashboard

-- Dimension Tables
CREATE TABLE IF NOT EXISTS Dim_Date (
    season VARCHAR PRIMARY KEY,
    year INT NOT NULL,
    is_forecast BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Dim_Player (
    player_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    position VARCHAR NOT NULL,
    nationality VARCHAR NOT NULL,
    birth_year INT
);

CREATE TABLE IF NOT EXISTS Dim_Competition (
    competition_id VARCHAR PRIMARY KEY,
    competition VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    importance INT NOT NULL
);

-- Fact Tables
CREATE TABLE IF NOT EXISTS Fact_Financials (
    season VARCHAR PRIMARY KEY FOREIGN KEY REFERENCES Dim_Date(season),
    revenue_total DOUBLE NOT NULL,
    commercial_revenue DOUBLE NOT NULL,
    broadcasting_revenue DOUBLE NOT NULL,
    matchday_revenue DOUBLE NOT NULL,
    operating_costs DOUBLE NOT NULL,
    wages DOUBLE NOT NULL,
    player_amortization DOUBLE NOT NULL,
    ebitda DOUBLE NOT NULL,
    net_profit DOUBLE NOT NULL,
    cash DOUBLE NOT NULL,
    debt DOUBLE NOT NULL,
    net_debt DOUBLE NOT NULL,
    assets DOUBLE NOT NULL,
    liabilities DOUBLE NOT NULL,
    financial_health_score INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Fact_Transfers (
    transfer_id VARCHAR PRIMARY KEY,
    season VARCHAR FOREIGN KEY REFERENCES Dim_Date(season),
    player VARCHAR NOT NULL,
    age INT NOT NULL,
    position VARCHAR NOT NULL,
    transfer_fee_paid DOUBLE DEFAULT 0.0,
    transfer_fee_received DOUBLE DEFAULT 0.0,
    net_transfer_spend DOUBLE DEFAULT 0.0,
    market_value DOUBLE NOT NULL
);

CREATE TABLE IF NOT EXISTS Fact_Sporting_Performance (
    performance_id VARCHAR PRIMARY KEY,
    season VARCHAR FOREIGN KEY REFERENCES Dim_Date(season),
    competition VARCHAR NOT NULL,
    games INT NOT NULL,
    wins INT NOT NULL,
    draws INT NOT NULL,
    losses INT NOT NULL,
    goals_for INT NOT NULL,
    goals_against INT NOT NULL,
    points INT NOT NULL,
    league_position INT,
    champions_league_result VARCHAR,
    trophies INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Fact_Player_Economics (
    player_econ_id VARCHAR PRIMARY KEY,
    player VARCHAR NOT NULL,
    season VARCHAR FOREIGN KEY REFERENCES Dim_Date(season),
    salary_estimate DOUBLE NOT NULL,
    market_value DOUBLE NOT NULL,
    minutes_played INT NOT NULL,
    goals INT NOT NULL,
    assists INT NOT NULL,
    performance_score DOUBLE NOT NULL
);

-- European Benchmark Fact Table
CREATE TABLE IF NOT EXISTS Fact_European_Benchmark (
    benchmark_id VARCHAR PRIMARY KEY,
    club VARCHAR NOT NULL,
    season VARCHAR NOT NULL,
    revenue DOUBLE NOT NULL,
    commercial_revenue DOUBLE NOT NULL,
    broadcasting_revenue DOUBLE NOT NULL,
    matchday_revenue DOUBLE NOT NULL,
    wages DOUBLE NOT NULL,
    wage_ratio DOUBLE NOT NULL,
    net_debt DOUBLE NOT NULL,
    squad_value DOUBLE NOT NULL,
    five_yr_net_transfer_spend DOUBLE NOT NULL,
    five_yr_trophies INT NOT NULL,
    financial_power_index DOUBLE NOT NULL,
    sporting_success_index DOUBLE NOT NULL
);

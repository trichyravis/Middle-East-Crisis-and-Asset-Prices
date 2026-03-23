# Middle East Crisis – Market Impact Analyzer
### The Mountain Path – World of Finance
**Prof. V. Ravichandran** | https://themountainpathacademy.com

---

## Overview
A comprehensive Streamlit application that analyzes how global financial markets
behaved **2 months before** and **2 months after** the October 7, 2023 Hamas attack
on Israel — the trigger event for the current Middle East Crisis.

## Assets Covered
| Category | Assets |
|----------|--------|
| **Commodities** | WTI Crude Oil, Brent Crude, Gold, Silver |
| **US Indices** | S&P 500, NASDAQ 100, Dow Jones, VIX |
| **Global Indices** | FTSE 100, DAX, Nikkei 225, Nifty 50 |
| **Energy & Defense** | Natural Gas, XLE ETF, ITA Defense ETF, USO Oil ETF |

## Analysis Modules
1. **Price Dashboard** – Raw price trajectories with crisis overlay
2. **Normalized Returns** – % change from Oct 7 for cross-asset comparison
3. **Pre vs Post Analysis** – Return, volatility, Sharpe, Max Drawdown, t-test
4. **Volatility & Risk** – Rolling volatility, regime shifts, return distributions
5. **Correlation Matrix** – Pre/Post/Δ correlation heatmaps
6. **Statistical Summary** – Full metrics table with CSV export

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Crisis Event
- **Date**: October 7, 2023
- **Event**: Hamas surprise attack on Israel
- **Analysis Window**: August 3 – December 11, 2023

## Data Source
Yahoo Finance (via `yfinance`) — real-time data fetched on launch.

---
*For educational purposes only. Not financial advice.*
*© The Mountain Path – World of Finance*

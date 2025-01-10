# Investment dashboard app
This repository is for an app to visualize various investable securities, including:
- Individual stocks
- Exchange-traded funds (ETF's)
- Commodities
- US treasuries

## File structure:
- The primary app .py file (Investment_dashboard_app) is located at the highest level in the repository. There is also a secondary .py file with supplemental functions for the app (Supplmental_functions_investment_dashboard) also located in the same location.
- The assets folder contains the files necessary for dash bootstrap components to format the app layout
- The inputs folder contains the files that contains reference data necessary for the app to function
- The requirements.txt file indicates the required packages needed to create the environment (TBD following app completion)

## Summary of Key Package Requirements:
- Dash (2.14.2)
- Dash Bootstrap Components (1.6.0)
- yfinance (0.2.50)
- Requests (2.32.3)
- Plotly (5.24.1)
- pandas (2.2.3)
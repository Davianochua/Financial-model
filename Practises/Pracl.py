import pandas as pd

data = {
    "Year" : [2023,2024,2025],
    "Revenue" : [20134,22218,22895],
    "Cost" : [718,916,525],
    "Asset" : [7393,8270,8974],
    "Equity" : [6224,6883,6891],
    "Debt" : [448,649,750],

}

df = pd.DataFrame(data)
df["Profit"] = df["Revenue"] - df["Cost"]
df["ROA"] = df["Profit"] / df["Asset"]
df["ROE"] = df["Profit"] / df["Equity"]
df["DER"] = df["Debt"] / df["Equity"] 

import numpy as np

def project_financials(df, projection_years = 10):
    rev_growth = df["Revenue"].pct_change().mean()
    cost_growth = df["Cost"].pct_change().mean()
    debt_growth = df["Debt"].pct_change().mean()
    asset_growth = df["Asset"].pct_change().mean()
    equity_growth = df["Equity"].pct_change().mean()

    last_year = df["Year"].iloc[-1]
    last_rev = df["Revenue"].iloc[-1]
    last_cost = df["Cost"].iloc[-1]
    last_debt = df["Debt"].iloc[-1]
    last_asset = df["Asset"].iloc[-1]
    last_equity = df["Equity"].iloc[-1]

    proj_rows = []

    for i in range(1, projection_years + 1):
        year = last_year + i
        revenue = last_rev * (1+ rev_growth) **i
        cost = last_cost * (1 + cost_growth) **i
        debt = last_debt * (1 + debt_growth) **i
        asset = last_asset * (1 + asset_growth) **i
        equity = last_equity * (1 + equity_growth) **i
        profit = revenue - cost
        ROA = profit / asset
        ROE = profit / equity 
        DER = debt / equity 

        proj_rows.append({
            "Year" : int(year),
            "Revenue" : round(revenue, 2),
            "Cost" : round(cost,2),
            "Debt" : round(debt,2),
            "Asset" : round(asset,2),
            "Equity" : round(equity,2),
            "ROA" : round(ROA,2),
            "ROE" : round(ROE,2),
            "DER" : round(DER,2)

        })

    return pd.DataFrame(proj_rows)

df_proj = project_financials(df, projection_years =10 )
print(df_proj)

import pandas as pd

data = {
    "Year": [2019, 2020, 2021, 2022],
    "Revenue": [12000, 13000, 12500, 14000],
    "Cost": [3000, 3010, 3500, 4000],
    "Assets": [2000, 3000, 3500, 3900],
    "Equity": [1500, 2000, 2300, 2500]
}

df = pd.DataFrame(data)
df["Profit"] = df["Revenue"] - df["Cost"]
df["ROA"] = df["Profit"] / df["Assets"]
df["ROE"] = df["Profit"] / df["Equity"]

print(df)
print("\nRounded to 2 decimals:")
print(df.round(2))

import numpy as np

def project_financials(df, projection_years = 5): 

    rev_growth = df["Revenue"].pct_change().mean()
    cost_growth = df["Cost"].pct_change().mean()
    asset_growth = df["Assets"].pct_change().mean()
    equity_growth = df["Equity"].pct_change().mean()

    last_year = df["Year"].iloc[-1]
    last_rev = df["Revenue"].iloc[-1]
    last_cost = df["Cost"].iloc[-1]
    last_asset = df["Assets"].iloc[-1]
    last_equity = df["Equity"].iloc[-1]

    proj_rows = []

    for i in range(1, projection_years + 1 ):
        year = last_year + i
        revenue = last_rev * (1 + rev_growth) ** i
        cost = last_cost * (1 + cost_growth) ** i
        asset = last_asset * (1 + asset_growth) ** i 
        equity = last_equity * (1+ equity_growth) ** i
        profit = revenue - cost 
        ROE = profit / equity
        ROA = profit / asset

        proj_rows.append({
            "Year" : int(year), 
            "Revenue" : round(revenue,2),
            "Cost" : round(cost,2),
            "Assets" : round(asset,2),
            "Equity" : round(equity,2),
            "Profit" : round(profit,2),
            "ROA" : round(ROA,2),
            "ROE" : round(ROE,2)

        })
    return pd.DataFrame(proj_rows)

df_proj = project_financials(df, projection_years = 5)


df_hist = df[["Year", "Revenue", "Cost",
              "Assets", "Equity", "Profit",
              "ROA", "ROE"]].copy()

df_combined = pd.concat([df_hist, df_proj], ignore_index = True)
df_combined["Type"] = (["Historical"] * len(df_hist)) + (["Projected"] * len(df_proj))

print("Overall Financial Overview:")
print(df_combined)
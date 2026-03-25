import pandas as pd 
import numpy as np


data = { 
    "Year" : [2019,2020,2021,2022],
    "Revenue" : [6000, 7000, 7500, 8300],
    "Cost" : [1200,2500,3000,3200],
    "Debt" : [200,250,300,390],
    "Asset" : [1500,2000,2900,4000],
    "Equity" : [1800,2400,2800,3500],

}

df = pd.DataFrame(data)
df["Profit"] = df["Revenue"] - df["Cost"]
df["ROE"] = df["Profit"] / df["Equity"]
df["ROA"] = df["Profit"] / df["Asset"]
df["DER"] = df["Debt"] / df["Equity"]


def project_financials(df, projection_years = 5):

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

    for i in range(1, projection_years +1):
        year = last_year + i
        revenue = last_rev * (1 + rev_growth) **i
        cost = last_cost *(1 + cost_growth) **i
        debt = last_debt *(1 + debt_growth) **i
        asset = last_asset *(1 + asset_growth) **i
        equity = last_equity *(1 + equity_growth) **i
        profit = revenue - cost
        ROE = profit / equity
        ROA = profit / asset
        DER = debt / equity

        proj_rows.append({
            "Year" : int(year),
            "Revenue" : round(revenue,2),
            "Cost" : round(cost,2),
            "Debt" : round(debt,2),
            "Asset" : round(asset, 2),
            "Equity" : round(equity,2 ),
            "Profit" : round(profit, 2),
            "ROE" : round(ROE,2),
            "ROA" : round(ROA, 2),
            "DER" : round(DER, 2)

        })


    return pd.DataFrame(proj_rows)

df_proj = project_financials(df, projection_years = 5)





    
    


import pandas as pd
import numpy as np

data = {
    "Year" : [2009,2010,2011,2012],
    "Revenue" : [1000,1200,1400,1800],
    "Cost" : [200,300,350,400],
    "Debt" : [150,200,230,260],
    "Asset" : [500,550,610,670],
    "Equity" : [300,340,390,450],
}

df = pd.DataFrame(data)
df["Profit"] = df["Revenue"] - df["Cost"]
df["ROA"] = df["Profit"] / df["Asset"]
df["ROE"] = df["Profit"] / df["Equity"]
df["DER"] = df["Debt"] / df["Equity"]

def project_financials(df, projection_years = 5):
    rev_growth = df["Revenue"].pct_change().mean()
    cost_growth = df["Cost"].pct_change().mean()
    debt_growth = df["Debt"].pct_change().mean()
    asset_growth = df["Asset"].pct_change().mean()
    equity_growth = df["Equity"].pct_change().mean()
    
    last_year = df["Year"].iloc[-1]
    last_revenue = df["Revenue"].iloc[-1]
    last_cost = df["Cost"].iloc[-1]
    last_debt = df["Debt"].iloc[-1]
    last_asset = df["Asset"].iloc[-1]
    last_equity = df["Equity"].iloc[-1]

    proj_rows = []

    for i in range(1, projection_years + 1): 
        year = last_year + i 
        revenue = last_revenue * (1 + rev_growth) **i
        cost = last_cost * (1 + cost_growth) **i
        debt = last_debt * (1 + debt_growth) **i
        asset = last_asset * (1 + asset_growth) **i
        equity = last_equity * (1 + equity_growth) **i
        profit = revenue - cost
        ROE = profit / equity 
        ROA = profit / asset 
        DER = debt / equity 

        proj_rows.append({
            "Year" : int(year),
            "Revenue" : round(revenue, 2),
            "Cost" : round(cost,2),
            "Debt" : round(debt,2), 
            "Asset" : round(asset,2 ),
            "Equity" : round(equity,2),
            "Profit" : round(profit,2),
            "ROE" : round(ROE, 2),
            "ROA" : round(ROA,2),
            "DER" : round(DER,2),


        })                                           

    return pd.DataFrame(proj_rows)
    
df_project = project_financials(df, projection_years =5)
print(df_project)
import pandas as  pd

data = {
    "Year" : [2019,2020,2021],
    "Revenue" : [11000,9000,10000],
    "Cost" : [2000,1000,1500],
    "Debt" : [1000,900,850],
    "Asset" : [1500,2000,2300],
    "Equity" : [1000,1200,1500]

}

df = pd.DataFrame(data)
df["Profit"] = df["Revenue"] - df["Cost"]
df["ROA"] = df["Profit"] / df["Asset"]
df["ROE"] = df["Profit"] / df["Equity"]
df["DER"] = df["Debt"] / df["Equity"]

import numpy as np

def project_financials(df, projection_years = 7):

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
        revenue = last_rev * (1 + rev_growth) ** i
        cost = last_cost * (1 + cost_growth) ** i
        debt = last_debt * (1 + debt_growth) ** i
        asset = last_asset * (1 + rev_growth) ** i
        equity = last_equity * (1 + equity_growth) ** i
        profit = revenue - cost
        ROA = profit / asset
        ROE = profit / equity
        DER = debt / equity


        proj_rows.append({
            "Year" : int(year),
            "Revenue" : round(revenue, 2),
            "Cost" : round(cost, 2),
            "Debt" : round(debt, 2),
            "Asset" : round(asset,2),
            "Equity" : round(equity,2),
            "Profit" : round(profit, 2),
            "ROA" : round(ROA, 2),
            "ROE" : round(ROE, 2),
            "DER" : round(DER, 2)

        })

        
    return pd.DataFrame(proj_rows)            
            


df_proj = project_financials(df, projection_years = 7)


    

df_hist = df[["Year", "Revenue", "Cost", "Debt",
              "Asset", "Equity", "Profit", "ROA",
              "ROE", "DER"]].copy()

df_combined = pd.concat([df_hist, df_proj],ignore_index = True)
df_combined["Type"] = (["Historical"] * len(df_hist) +
                       ["Projected"] * len(df_proj))

print(" Complete Financial overview:")

profit_margin = (df["Profit"].iloc[-1] / df["Revenue"].iloc[-1]) * 100
if profit_margin > 20: 
    print(f" PROFIT MARGIN: Strong")
elif profit_margin > 10:
    print(f" PROFIT MARGIN: Moderate")
else: print(f" PROFIT MARGIN: Weak, evaluate cost structure")

ROA = df["ROE"].iloc[-1]
if ROA > 4: 
    print(f" ROA: High asset efficiency")
elif ROA > 2:
    print(f" ROA: Moderate asset efficiency")
else: print(f" **WARNING** ROA: Weak asset efficiency, assets are underperforming")

ROE = df["ROE"].iloc[-1]
if ROE > 3.4: 
    print(f" ROE: Stable and strong")
elif ROE > 2:
    print(f" ROE: Moderate")
else: print(f" **WARNING** ROE: Weak, ROE underperforming")
    
rev_growth = df["Revenue"].pct_change().mean() *100
if rev_growth > 10:
    print(f" REVENUE TREND: Strong growth")
elif rev_growth > 0:
    print(f" REVENUE TREND: Moderate and stable growth")
else: print(f" **WARNING** REVENUE TREND: Decling revenue - SERIOUS CONCERN")

profit_growth = df["Profit"].pct_change().mean() *100
if profit_growth > 5:
    print(f" PROFIT TREND: Strong profitability")
elif profit_growth > 0:
    print(f" PROFIT TREND: Stable profitability")
else: print(f" **WARNING** PROFIT TREND: Profits declining - URGENT REVISION, CHECK COSTS")

asset_growth = df["Asset"].pct_change().mean() *100
if asset_growth > 5:
    print(f" ASSET TREND: Strong asset expansion")
elif asset_growth > 0:
    print(f" ASSET TREND: Stable asset expansion")
else: print(f" **WARNING** ASSET TREND: Assets shrinking - Possible losses")

equity_growth = df["Equity"].pct_change().mean()* 100
if equity_growth > 10:
    print(f" EQUITY TREND: Strong equity building")
elif equity_growth >0:
    print(f" EQUITY TREND: Slow equity building ")
else: print(f" **WARNING** EQUITY TREND: Equity shrinking - Shareholder at risk")

print()
print("=" * 45)
signals = [profit_margin > 10, ROA > 4, ROE >2, rev_growth>0, profit_growth>0, asset_growth>0, equity_growth>0]

score = sum(signals)
print(f" OVERALL HEALTH SCORE: {score} / 7")

if score>= 5:
    print(f" VERDICT: Company is in overall strong financial health")
elif score>=4: 
    print(f" VERDICT: Company is in stable financial health, but has areas of concern")
else: print(f" VERDICT: Company shows significant financial risk")

print("=" *45)


from IPython.display import display
display(df_combined)

def calculate_fcf(df_input, capex_rate = 0.10):
    df_input = df_input.copy()
    df_input["CapEX"] = df_input["Revenue"] * capex_rate
    df_input["FCF"] = df_input["Profit"] - df_input["CapEX"]
    return df_input
def dcf_valuation(df_projected, discount_rate = 0.10, terminal_growth = 0.03, capex_rate = 0.10):

    df_fcf = calculate_fcf(df_projected, capex_rate)
    fcf_values = df_fcf["FCF"].tolist()
    years = df_fcf["Year"].tolist()

    print("=" *50)
    print(" Discounted Cash Flow Valuation")
    print("=" *50)

    print(f"/n Assumptions:")
    print(f" Discount Rate: { discount_rate *100:.1f}%")
    print(f" Terminal Growth: { terminal_growth *100:.1f}%")
    print(f" CapEx Rate: { capex_rate *100:.1f}%" )
    
    print(f"\n{'Year':<8} {'FCF' :>12} {'Discount Rate' :>16} {'Present Value':>14}")
    print("-" *50)


    total_pv = 0
    pv_values = [] 
    disc_factors = [] 


    for i, (year, fcf) in enumerate(
            zip(years, fcf_values), 1):
        discount_factor = 1/ (1 + discount_rate) **1
        pv = fcf * discount_factor
        total_pv += pv
        pv_values.append(pv)
        disc_factors.append(discount_factor)
        print(f" {int(year):<8} {fcf:>12,.2f}"
              f" {discount_factor: >16.4f}"
              f" {pv:>14,.2f}" )

    terminal_value = (fcf_values[-1] * (1 + terminal_growth)) / (discount_rate - terminal_growth)

    terminal_pv = terminal_value / (1 + discount_rate) ** len(fcf_values)

    intrinsic_value = total_pv + terminal_pv

    print("=" *50)
    print(f"/n {'PV of projected FCFs':<30}"
          f" {total_pv: >14,.2f}")
    print(f"{'Terminal value (Discounted)':<30}"
          f"{terminal_value: >14,.2f}")

    print(f"{'PV of Terminal value':<30}"
          f"{terminal_pv: >14,.2f}")

    print("=" *50)
    print(f" {'INTRINSIC VALUE':<30}"
          f"{intrinsic_value: >14,.2f}")
    print("=" *50)


    print(f"/n MARGIN OF SAFETY MARGIN")
    print("=" *50)
    for margin in [0.10,0.20,0.30]:
        safe_price = intrinsic_value * (1- margin)
        print(f" {int(margin*100)}% Margin of safety: "
              f" Buy below { safe_price: >10,.2f}")




    print(f"/n VALUE INTEPRETATION")
    print("=" *50)
    tv_pct = (terminal_pv / intrinsic_value) *100
    pv_pct = (total_pv / intrinsic_value) *100
    print(f" Projection value contributes:"
          f" {pv_pct:.1f}% of value")
    print(f" Terminal value contributes:"
          f" {tv_pct:.1f}% of value")

    if tv_pct >75:
        print(f" High Value Dependency -"
              f" Growth assumptions are critical")

    else: print(f" Balanced Valuation -"
                f" Near Term Cash Flows well represented")

    return {
        "intrinsic_value" : round(intrinsic_value, 2),
        "total_pv" : round(total_pv, 2),
        "terminal_value" : round(terminal_value, 2),
        "pv_values" : pv_values,
        "fcf_values" : fcf_values,
        "years" : years, 
        "disc_factors" : disc_factors
    }


dcf_results = dcf_valuation(
    df_proj,
    discount_rate = 0.10,
    terminal_growth = 0.03,
    capex_rate = 0.10
)
    


        
              
        

    
    
    




      




   


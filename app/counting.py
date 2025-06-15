import pandas as pd
import numpy as np

def load_salary_data():
    salaries = pd.read_excel("data/salaries.xlsx")
    salaries = salaries.rename(columns={"Unnamed: 0": "Sector"})
    salaries_melted = salaries.melt(id_vars="Sector", var_name="Year", value_name="Salary")
    salaries_melted = salaries_melted.dropna()
    salaries_melted["Year"] = salaries_melted["Year"].astype(int)
    return salaries_melted

def load_inflation_data():
    inflation = pd.read_excel("data/inflation.xlsx")
    inflation = inflation.dropna(subset=["Всего"])
    inflation["Год"] = inflation["Год"].astype(int)
    inflation = inflation.set_index("Год").sort_index()
    return inflation

def calculate_real_salaries(salaries_melted, inflation, base_year=2024):
    # inflation_dict = df_inflation.set_index("Year")["Inflation"].to_dict()
    # inflation_multipliers = {}

    # cumulative = 1.0
    # for year in sorted(inflation_dict.keys(), reverse=True):
    #     if year == base_year:
    #         inflation_multipliers[year] = 1.0
    #     else:
    #         cumulative *= 1 + inflation_dict[year] / 100
    #         inflation_multipliers[year] = cumulative

    # df_salaries["InflationFactor"] = df_salaries["Year"].map(lambda y: inflation_multipliers.get(y, 1.0))
    # df_salaries["RealSalary"] = df_salaries["Salary"] / df_salaries["InflationFactor"]

    # df_salaries.sort_values(["Sector", "Year"], inplace=True)
    # df_salaries["RealSalaryChange%"] = df_salaries.groupby("Sector")["RealSalary"].pct_change() * 100

    years = sorted(inflation.index.unique())

    # Множители инфляции для каждого года до base_year
    inflation_multipliers = {
        year: np.prod([1 + inflation.loc[y, "Всего"]/100 for y in range(year+1, base_year+1) if y in inflation.index])
        for year in years
    }

    salaries_melted["InflationMultiplier"] = salaries_melted["Year"].map(inflation_multipliers)
    salaries_melted["RealSalary"] = salaries_melted["Salary"] / salaries_melted["InflationMultiplier"]

    # === РАСЧЁТ РАЗНИЦЫ ПО ГОДАМ ===
    salaries_melted = salaries_melted.sort_values(["Sector", "Year"])
    salaries_melted["RealSalaryChange%"] = salaries_melted.groupby("Sector")["RealSalary"].pct_change() * 100

    return salaries_melted

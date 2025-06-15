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
    years = sorted(inflation.index.unique())
    inflation_multipliers = {
        year: np.prod([1 + inflation.loc[y, "Всего"]/100 for y in range(year+1, base_year+1) if y in inflation.index])
        for year in years
    }

    salaries_melted["InflationMultiplier"] = salaries_melted["Year"].map(inflation_multipliers)
    salaries_melted["RealSalary"] = salaries_melted["Salary"] / salaries_melted["InflationMultiplier"]

    salaries_melted = salaries_melted.sort_values(["Sector", "Year"])
    salaries_melted["RealSalaryChange%"] = salaries_melted.groupby("Sector")["RealSalary"].pct_change() * 100

    return salaries_melted

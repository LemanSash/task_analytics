import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

from counting import load_salary_data, load_inflation_data, calculate_real_salaries

def show_main_page():
    st.set_page_config(
        layout="wide",
        page_title="Анализ зарплат",
    )

    st.title("Анализ заработных плат по видам деятельности")
    st.markdown("""
    Это приложение позволяет анализировать изменение средних зарплат в секторах **Наука**, **Медицина**, **Культура** с учётом инфляции по годам.
    """)

def show_sidebar():
    st.sidebar.header("Настройки")
    sectors = st.sidebar.multiselect(
        "Выберите виды деятельности:",
        ["Science", "Medicine", "Culture"],
        default=["Science", "Medicine", "Culture"]
    )
    return sectors

def plot_salary_trends(df, sectors):
    st.subheader("Динамика средних зарплат (номинальные значения)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df[df["Sector"].isin(sectors)], x="Year", y="Salary", hue="Sector", marker="o", ax=ax)
    st.pyplot(fig)

def plot_real_salary_trends(df, sectors):
    st.subheader("Реальные зарплаты (с учетом инфляции)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df[df["Sector"].isin(sectors)], x="Year", y="RealSalary", hue="Sector", marker="o", ax=ax)
    st.pyplot(fig)

def plot_salary_changes(df, sectors):
    st.subheader("Годовое изменение реальных зарплат (%)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df[df["Sector"].isin(sectors)], x="Year", y="RealSalaryChange%", hue="Sector", marker="o", ax=ax)
    st.pyplot(fig)

def show_data_table(df, sectors):
    st.subheader("Данные по реальным зарплатам")
    st.dataframe(df[df["Sector"].isin(sectors)].sort_values(["Sector", "Year"]), use_container_width=True)

def main():
    show_main_page()

    sectors = show_sidebar()

    df_salary = load_salary_data()
    df_inflation = load_inflation_data()
    df_real = calculate_real_salaries(df_salary, df_inflation)

    plot_salary_trends(df_real, sectors)
    plot_real_salary_trends(df_real, sectors)
    plot_salary_changes(df_real, sectors)
    show_data_table(df_real, sectors)

if __name__ == "__main__":
    main()

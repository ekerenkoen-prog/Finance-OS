import streamlit as st
import pandas as pd
from datetime import date, timedelta

from database.cashflow import insert_cashflow_entry, get_all_cashflow_entries
from utils.calculations import (
    calculate_total_income,
    calculate_total_expenses,
    calculate_cashflow,
    calculate_savings_rate,
    calculate_investment_rate,
)


def render_cashflow_page():
    st.subheader("Weekly Cashflow")
    st.caption("Track income, spending and invested amount once per week.")

    today = date.today()
    default_start = today - timedelta(days=today.weekday())
    default_end = default_start + timedelta(days=6)

    with st.form("cashflow_form"):
        period_start = st.date_input("Period start", value=default_start)
        period_end = st.date_input("Period end", value=default_end)

        st.markdown("### Income")

        salary_income = st.number_input("Salary income", min_value=0.0, step=100.0)
        side_income = st.number_input("Side job income", min_value=0.0, step=100.0)
        business_income = st.number_input("Business income", min_value=0.0, step=100.0)
        dividend_income = st.number_input("Dividend income", min_value=0.0, step=10.0)
        other_income = st.number_input("Other income", min_value=0.0, step=50.0)

        st.markdown("### Expenses")

        housing_expense = st.number_input("Housing expense", min_value=0.0, step=100.0)
        groceries_expense = st.number_input("Groceries expense", min_value=0.0, step=50.0)
        eating_out_expense = st.number_input("Eating out expense", min_value=0.0, step=25.0)
        transport_expense = st.number_input("Transport expense", min_value=0.0, step=25.0)
        travel_expense = st.number_input("Travel expense", min_value=0.0, step=50.0)
        fun_expense = st.number_input("Fun expense", min_value=0.0, step=25.0)
        other_expense = st.number_input("Other expense", min_value=0.0, step=25.0)

        st.markdown("### Investing")

        invested_amount = st.number_input("Invested amount", min_value=0.0, step=50.0)

        notes = st.text_area("Notes")

        data = {
            "period_start": str(period_start),
            "period_end": str(period_end),
            "salary_income": salary_income,
            "side_income": side_income,
            "business_income": business_income,
            "dividend_income": dividend_income,
            "other_income": other_income,
            "housing_expense": housing_expense,
            "groceries_expense": groceries_expense,
            "eating_out_expense": eating_out_expense,
            "transport_expense": transport_expense,
            "travel_expense": travel_expense,
            "fun_expense": fun_expense,
            "other_expense": other_expense,
            "invested_amount": invested_amount,
            "notes": notes,
        }

        total_income = calculate_total_income(data)
        total_expenses = calculate_total_expenses(data)
        cashflow = calculate_cashflow(data)
        savings_rate = calculate_savings_rate(data)
        investment_rate = calculate_investment_rate(data)

        st.markdown("### Cashflow Preview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"€{total_income:,.2f}")
        col2.metric("Total Expenses", f"€{total_expenses:,.2f}")
        col3.metric("Cashflow", f"€{cashflow:,.2f}")

        col4, col5 = st.columns(2)
        col4.metric("Savings Rate", f"{savings_rate:.1%}")
        col5.metric("Investment Rate", f"{investment_rate:.1%}")

        submitted = st.form_submit_button("Save Cashflow Entry")

        if submitted:
            insert_cashflow_entry(data)
            st.success("Cashflow entry saved.")

    entries = get_all_cashflow_entries()

    if entries:
        st.markdown("---")
        st.subheader("Cashflow History")

        rows = []

        for entry in entries:
            total_income = calculate_total_income(entry)
            total_expenses = calculate_total_expenses(entry)
            cashflow = calculate_cashflow(entry)
            savings_rate = calculate_savings_rate(entry)
            investment_rate = calculate_investment_rate(entry)

            rows.append({
                "Start": entry["period_start"],
                "End": entry["period_end"],
                "Income": total_income,
                "Expenses": total_expenses,
                "Cashflow": cashflow,
                "Savings Rate": savings_rate,
                "Investment Rate": investment_rate,
                "Invested": entry.get("invested_amount", 0),
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        latest = df.iloc[-1]

        st.markdown("### Latest Cashflow Position")

        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Cashflow", f"€{latest['Cashflow']:,.2f}")
        col2.metric("Latest Savings Rate", f"{latest['Savings Rate']:.1%}")
        col3.metric("Latest Investment Rate", f"{latest['Investment Rate']:.1%}")

    else:
        st.info("No cashflow entries saved yet.")
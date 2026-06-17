import streamlit as st
from datetime import date

from database.net_worth import insert_net_worth_snapshot, get_latest_snapshot
from utils.calculations import (
    calculate_total_assets,
    calculate_total_liabilities,
    calculate_net_worth,
)


def render_net_worth_page():
    st.subheader("Weekly Net Worth Snapshot")
    st.caption("Update this once per week. Same day, same rhythm.")

    with st.form("net_worth_form"):
        snapshot_date = st.date_input("Snapshot date", value=date.today())

        st.markdown("### Assets")

        bank_balance = st.number_input("Bank balance", min_value=0.0, step=100.0)
        savings_balance = st.number_input("Savings balance", min_value=0.0, step=100.0)
        investments_value = st.number_input("Investments value", min_value=0.0, step=100.0)
        crypto_value = st.number_input("Crypto value", min_value=0.0, step=100.0)
        pension_value = st.number_input("Pension value", min_value=0.0, step=100.0)
        business_cash = st.number_input("Business cash", min_value=0.0, step=100.0)
        other_assets = st.number_input("Other assets", min_value=0.0, step=100.0)

        st.markdown("### Liabilities")

        student_debt = st.number_input("Student debt", min_value=0.0, step=100.0)
        credit_card_debt = st.number_input("Credit card debt", min_value=0.0, step=100.0)
        loans = st.number_input("Loans", min_value=0.0, step=100.0)
        tax_debt = st.number_input("Tax debt", min_value=0.0, step=100.0)
        other_debt = st.number_input("Other debt", min_value=0.0, step=100.0)

        notes = st.text_area("Notes")

        data = {
            "snapshot_date": str(snapshot_date),
            "bank_balance": bank_balance,
            "savings_balance": savings_balance,
            "investments_value": investments_value,
            "crypto_value": crypto_value,
            "pension_value": pension_value,
            "business_cash": business_cash,
            "other_assets": other_assets,
            "student_debt": student_debt,
            "credit_card_debt": credit_card_debt,
            "loans": loans,
            "tax_debt": tax_debt,
            "other_debt": other_debt,
            "notes": notes,
        }

        total_assets = calculate_total_assets(data)
        total_liabilities = calculate_total_liabilities(data)
        net_worth = calculate_net_worth(data)

        st.markdown("### Snapshot Preview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Assets", f"€{total_assets:,.2f}")
        col2.metric("Total Liabilities", f"€{total_liabilities:,.2f}")
        col3.metric("Net Worth", f"€{net_worth:,.2f}")

        submitted = st.form_submit_button("Save Snapshot")

        if submitted:
            insert_net_worth_snapshot(data)
            st.success("Net worth snapshot saved.")

    latest_snapshot = get_latest_snapshot()

    if latest_snapshot:
        st.markdown("---")
        st.subheader("Latest Saved Snapshot")
        st.write(latest_snapshot)
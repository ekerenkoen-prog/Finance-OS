import streamlit as st

from database.net_worth import get_latest_snapshot
from database.cashflow import get_latest_cashflow_entry
from database.goals import get_active_goals

from utils.calculations import (
    calculate_net_worth,
    calculate_cashflow,
    calculate_savings_rate,
    calculate_investment_rate,
    calculate_goal_progress,
)


def render_dashboard_page():
    st.title("Finance OS Dashboard")

    latest_snapshot = get_latest_snapshot()
    latest_cashflow = get_latest_cashflow_entry()
    active_goals = get_active_goals()

    net_worth = 0
    cashflow = 0
    savings_rate = 0
    investment_rate = 0

    if latest_snapshot:
        net_worth = calculate_net_worth(latest_snapshot)

    if latest_cashflow:
        cashflow = calculate_cashflow(latest_cashflow)
        savings_rate = calculate_savings_rate(latest_cashflow)
        investment_rate = calculate_investment_rate(latest_cashflow)

    avg_goal_progress = 0

    if active_goals:
        progresses = []

        for goal in active_goals:
            progress = calculate_goal_progress(
                float(goal["current_amount"]),
                float(goal["target_amount"])
            )

            progresses.append(progress)

        avg_goal_progress = sum(progresses) / len(progresses)

    st.subheader("Core Financial KPI's")

    col1, col2 = st.columns(2)

    col1.metric(
        "Net Worth",
        f"€{net_worth:,.2f}"
    )

    col2.metric(
        "Cashflow",
        f"€{cashflow:,.2f}"
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "Savings Rate",
        f"{savings_rate:.1%}"
    )

    col4.metric(
        "Investment Rate",
        f"{investment_rate:.1%}"
    )

    st.markdown("---")

    col5, col6 = st.columns(2)

    col5.metric(
        "Active Goals",
        len(active_goals)
    )

    col6.metric(
        "Average Goal Progress",
        f"{avg_goal_progress:.1%}"
    )
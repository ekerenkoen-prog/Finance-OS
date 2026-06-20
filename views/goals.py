import streamlit as st
import pandas as pd
from datetime import date

from database.goals import insert_goal, get_active_goals
from utils.calculations import calculate_goal_progress
from utils.constants import GOAL_CATEGORIES


def render_goals_page():
    st.subheader("Financial Goals")
    st.caption("Track only goals that genuinely increase financial strength.")

    with st.form("goal_form"):
        goal_name = st.text_input("Goal name")

        goal_category = st.selectbox(
            "Goal category",
            GOAL_CATEGORIES
        )

        target_amount = st.number_input(
            "Target amount",
            min_value=0.0,
            step=100.0
        )

        current_amount = st.number_input(
            "Current amount",
            min_value=0.0,
            step=100.0
        )

        deadline = st.date_input("Deadline", value=date.today())

        priority = st.slider(
            "Priority",
            min_value=1,
            max_value=5,
            value=3
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Goal")

        if submitted:
            data = {
                "goal_name": goal_name,
                "goal_category": goal_category,
                "target_amount": target_amount,
                "current_amount": current_amount,
                "deadline": str(deadline),
                "priority": priority,
                "status": "Active",
                "notes": notes,
            }

            insert_goal(data)
            st.success("Goal saved.")

    goals = get_active_goals()

    if goals:
        st.markdown("---")
        st.subheader("Active Goals")

        rows = []

        for goal in goals:
            progress = calculate_goal_progress(
                float(goal.get("current_amount", 0)),
                float(goal.get("target_amount", 0))
            )

            rows.append({
                "Goal": goal["goal_name"],
                "Category": goal["goal_category"],
                "Current": float(goal["current_amount"]),
                "Target": float(goal["target_amount"]),
                "Progress": progress,
                "Deadline": goal["deadline"],
                "Priority": goal["priority"],
            })

            st.markdown(f"### {goal['goal_name']}")
            st.progress(min(progress, 1.0))
            st.write(f"{progress:.1%} complete")

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No active financial goals yet.")
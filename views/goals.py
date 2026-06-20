import streamlit as st
import pandas as pd
from datetime import date

from database.goals import (
    insert_goal,
    get_all_goals,
    get_active_goals,
    get_completed_goals,
    update_goal,
)
from utils.calculations import calculate_goal_progress
from utils.constants import GOAL_CATEGORIES


def build_goals_dataframe(goals):
    rows = []

    for goal in goals:
        current_amount = float(goal.get("current_amount", 0))
        target_amount = float(goal.get("target_amount", 0))
        progress = calculate_goal_progress(current_amount, target_amount)

        rows.append({
            "Goal": goal["goal_name"],
            "Category": goal["goal_category"],
            "Current": current_amount,
            "Target": target_amount,
            "Progress": progress,
            "Deadline": goal["deadline"],
            "Priority": goal["priority"],
            "Status": goal["status"],
        })

    return pd.DataFrame(rows)


def render_goal_progress(goals):
    for goal in goals:
        current_amount = float(goal.get("current_amount", 0))
        target_amount = float(goal.get("target_amount", 0))
        progress = calculate_goal_progress(current_amount, target_amount)

        st.markdown(f"### {goal['goal_name']}")
        st.progress(min(progress, 1.0))
        st.write(f"{progress:.1%} complete")


def render_goals_page():
    st.subheader("Financial Goals")
    st.caption("Track only goals that genuinely increase financial strength.")

    with st.expander("➕ New Goal"):

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
                if not goal_name:
                    st.error("Goal name is required.")
                    return

                if target_amount <= 0:
                    st.error("Target amount must be higher than 0.")
                    return

                status = "Completed" if current_amount >= target_amount else "Active"

                data = {
                    "goal_name": goal_name,
                    "goal_category": goal_category,
                    "target_amount": target_amount,
                    "current_amount": current_amount,
                    "deadline": str(deadline),
                    "priority": priority,
                    "status": status,
                    "notes": notes,
                }

                insert_goal(data)
                st.success("Goal saved.")
                st.rerun()

    all_goals = get_all_goals()

    if all_goals:
    
        with st.expander("✏️ Update Existing Goal"):
            goal_options = {
                f"{goal['goal_name']} ({goal['status']})": goal
                for goal in all_goals
            }

            selected_goal_label = st.selectbox(
                "Select goal to update",
                list(goal_options.keys())
            )

            selected_goal = goal_options[selected_goal_label]

            with st.form("update_goal_form"):
                updated_current_amount = st.number_input(
                    "Updated current amount",
                    min_value=0.0,
                    value=float(selected_goal.get("current_amount", 0)),
                    step=100.0
                )

                updated_target_amount = st.number_input(
                    "Updated target amount",
                    min_value=0.0,
                    value=float(selected_goal.get("target_amount", 0)),
                    step=100.0
                )

                updated_deadline = st.date_input(
                    "Updated deadline",
                    value=pd.to_datetime(selected_goal["deadline"]).date()
                )

                updated_priority = st.slider(
                    "Updated priority",
                    min_value=1,
                    max_value=5,
                    value=int(selected_goal.get("priority", 3))
                )

                updated_notes = st.text_area(
                    "Updated notes",
                    value=selected_goal.get("notes") or ""
                )

                submitted_update = st.form_submit_button("Update Goal")

                if submitted_update:
                    updated_status = (
                        "Completed"
                        if updated_current_amount >= updated_target_amount
                        else "Active"
                    )

                    update_goal(
                        selected_goal["id"],
                        {
                            "current_amount": updated_current_amount,
                            "target_amount": updated_target_amount,
                            "deadline": str(updated_deadline),
                            "priority": updated_priority,
                            "status": updated_status,
                            "notes": updated_notes,
                        }
                    )

                    st.success("Goal updated.")
                    st.rerun()

    active_goals = get_active_goals()
    completed_goals = get_completed_goals()

    if active_goals:
        st.markdown("---")
        st.subheader("Active Goals")

        active_df = build_goals_dataframe(active_goals)

        total_current = active_df["Current"].sum()
        total_target = active_df["Target"].sum()
        average_progress = active_df["Progress"].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric("Current Total", f"€{total_current:,.2f}")
        col2.metric("Target Total", f"€{total_target:,.2f}")
        col3.metric("Average Progress", f"{average_progress:.1%}")

        render_goal_progress(active_goals)

        st.markdown("### Active Goals Table")

        st.dataframe(
            active_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No active financial goals yet.")

    if completed_goals:
        st.markdown("---")
        st.subheader("Completed Goals")

        completed_df = build_goals_dataframe(completed_goals)

        st.dataframe(
            completed_df,
            use_container_width=True,
            hide_index=True,
        )
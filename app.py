import streamlit as st
from database.supabase import get_supabase_client

st.set_page_config(
    page_title="Finance OS",
    page_icon="💰",
    layout="wide"
)

st.sidebar.title("Finance OS")
st.sidebar.caption("Building Financial Freedom")

try:
    supabase = get_supabase_client()
    st.sidebar.success("Supabase connected")
except Exception as e:
    st.sidebar.error(f"Supabase error: {e}")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Net Worth",
        "Cashflow",
        "Investments",
        "Goals",
        "FIRE",
    ]
)

st.title(page)

if page == "Dashboard":
    st.write("Overview of your financial system.")

elif page == "Net Worth":
    st.write("Track your total assets, liabilities, and net worth.")

elif page == "Cashflow":
    st.write("Track income, expenses, savings rate, and investment rate.")

elif page == "Investments":
    st.write("Track ETFs, stocks, crypto, and allocation.")

elif page == "Goals":
    st.write("Track financial goals and progress.")

elif page == "FIRE":
    st.write("Calculate financial independence scenarios.")
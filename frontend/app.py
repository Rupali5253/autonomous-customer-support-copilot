import streamlit as st


st.set_page_config(
    page_title="NovaCart",
    page_icon="🛍️",
    layout="wide"
)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


if st.session_state.authenticated:

    st.switch_page(
        "pages/customer_dashboard.py"
    )

else:

    st.switch_page(
        "pages/login.py"
    )
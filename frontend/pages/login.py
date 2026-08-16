import streamlit as st

import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from api_client import login_user, register_user


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NovaCart | Login",
    page_icon="🛍️",
    layout="centered"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f7f9fc;
    }

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-top: 35px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .brand {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 25px;
    }

    .info-box {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SESSION STATE
# ==========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


# ==========================================
# BRANDING
# ==========================================

st.markdown(
    '<div class="brand">🛍️ NovaCart</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Welcome back</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent customer support assistant'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# LOGIN / REGISTER TABS
# ==========================================

login_tab, register_tab = st.tabs(
    ["🔐 Login", "✨ Create Account"]
)


# ==========================================
# LOGIN
# ==========================================

with login_tab:

    st.markdown("### Sign in to your account")

    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )

    st.write("")

    if st.button(
        "Login",
        type="primary",
        use_container_width=True
    ):

        if not email or not password:

            st.warning(
                "Please enter your email and password."
            )

        else:

            try:

                response = login_user(
                    email,
                    password
                )

                if response.status_code == 200:

                    data = response.json()

                    # Save authentication details
                    st.session_state.access_token = (
                        data["access_token"]
                    )

                    st.session_state.authenticated = True

                    # Save user role
                    st.session_state.user_role = (
                        data.get("role")
                    )

                    role = data.get("role")

                    # ----------------------------------
                    # ROLE-BASED REDIRECTION
                    # ----------------------------------

                    if role == "customer":

                        st.switch_page(
                            "pages/customer_dashboard.py"
                        )

                    elif role == "agent":

                        st.switch_page(
                            "pages/agent_dashboard.py"
                        )

                    elif role == "manager":

                        st.switch_page(
                            "pages/manager_dashboard.py"
                        )

                    else:

                        st.session_state.authenticated = False

                        st.error(
                            "Unknown user role. "
                            "Please contact support."
                        )

                else:

                    try:

                        error = response.json().get(
                            "detail",
                            "Invalid email or password."
                        )

                    except Exception:

                        error = "Login failed."

                    st.error(error)

            except Exception:

                st.error(
                    "Unable to connect to the server. "
                    "Please make sure the FastAPI backend "
                    "is running."
                )

# ==========================================
# REGISTER
# ==========================================

with register_tab:

    st.markdown("### Create your NovaCart account")

    name = st.text_input(
        "Full name",
        placeholder="Enter your full name",
        key="register_name"
    )

    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Re-enter your password",
        key="register_confirm_password"
    )

    st.write("")

    if st.button(
        "Create Account",
        type="primary",
        use_container_width=True
    ):

        if not name or not email or not password:

            st.warning(
                "Please fill in all required fields."
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        elif len(password) < 6:

            st.warning(
                "Password should contain at least 6 characters."
            )

        else:

            try:

                response = register_user(
                    name,
                    email,
                    password
                )

                if response.status_code == 200:

                    st.success(
                        "Account created successfully! "
                        "You can now login."
                    )
                    st.write("DEBUG STATUS:", response.status_code)
                    st.write("DEBUG URL:", response.url)
                    st.write("DEBUG RESPONSE:", response.text)
                else:

                    try:
                        error = response.json().get(
                            "detail",
                            "Registration failed."
                        )
                    except Exception:
                        error = "Registration failed."

                    st.error(error)

            except Exception:

                st.error(
                    "Unable to connect to the server. "
                    "Please make sure the FastAPI backend is running."
                )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        padding: 10px 0 5px 0;
    ">
        NovaCart Autonomous Customer Support Copilot
    </div>
    """,
    unsafe_allow_html=True
)
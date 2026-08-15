import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

import streamlit as st

from api_client import (
    get_assigned_tickets,
    update_ticket_status,
    get_assigned_feedback
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NovaCart | Agent Dashboard",
    page_icon="🎧",
    layout="wide"
)


# ==========================================
# AUTH CHECK
# ==========================================

if not st.session_state.get("authenticated", False):
    st.warning("Please login to continue.")
    st.stop()


# Only agents can access this dashboard
if st.session_state.get("user_role") != "agent":
    st.error("Access denied. Agent access required.")
    st.stop()


token = st.session_state.get("access_token")


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f7f9fc;
    }

    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .stat-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🎧 NovaCart")

    st.caption("Support Agent Portal")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🎫 Assigned Tickets",
            "📊 Overview"
        ]
    )

    st.markdown("---")

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.authenticated = False
        st.session_state.access_token = None
        st.session_state.user_role = None

        st.switch_page(
            "pages/login.py"
        )


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="dashboard-title">'
    'Agent Dashboard 🎧'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Manage and resolve your assigned customer support tickets.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# LOAD ASSIGNED TICKETS
# ==========================================

try:

    response = get_assigned_tickets(token)

    if response.status_code == 200:

        data = response.json()

        tickets = data.get(
            "tickets",
            []
        )

    else:

        tickets = []

        st.error(
            "Unable to load assigned tickets."
        )

except Exception:

    tickets = []

    st.error(
        "Unable to connect to the ticket service."
    )

# ==========================================
# LOAD ASSIGNED FEEDBACK
# ==========================================

try:

    feedback_response = get_assigned_feedback(token)

    if feedback_response.status_code == 200:

        feedback_data = feedback_response.json()

        assigned_feedback = feedback_data.get(
            "feedback",
            []
        )

    else:

        assigned_feedback = []

except Exception:

    assigned_feedback = []

# ==========================================
# OVERVIEW
# ==========================================

if page == "📊 Overview":

    total_tickets = len(tickets)

    assigned_count = sum(
        1
        for ticket in tickets
        if ticket.get("status") == "assigned"
    )

    in_progress_count = sum(
        1
        for ticket in tickets
        if ticket.get("status") == "in_progress"
    )

    resolved_count = sum(
        1
        for ticket in tickets
        if ticket.get("status") == "resolved"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>🎫</h2>
                <b>{total_tickets}</b>
                <p>Total Assigned</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>📥</h2>
                <b>{assigned_count}</b>
                <p>Assigned</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>🔄</h2>
                <b>{in_progress_count}</b>
                <p>In Progress</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>✅</h2>
                <b>{resolved_count}</b>
                <p>Resolved</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# ASSIGNED TICKETS
# ==========================================

elif page == "🎫 Assigned Tickets":

    st.markdown("### 🎫 Assigned Tickets")

    if not tickets:

        st.info(
            "You currently have no assigned tickets."
        )

    else:

        for ticket in tickets:

            ticket_id = ticket.get("id")

            with st.container(border=True):

                # ==========================================
                # TICKET HEADER
                # ==========================================

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.markdown(
                        f"### 🎫 Ticket #{ticket_id}"
                    )

                    st.write(
                        f"**Subject:** "
                        f"{ticket.get('subject', 'No subject')}"
                    )

                    st.write(
                        f"**Customer ID:** "
                        f"{ticket.get('customer_id', 'N/A')}"
                    )

                    st.write(
                        f"**Description:** "
                        f"{ticket.get('description', '')}"
                    )

                with col2:

                    st.caption(
                        f"Priority: "
                        f"{ticket.get('priority', 'unknown')}"
                    )

                    st.caption(
                        f"Intent: "
                        f"{ticket.get('intent', 'unknown')}"
                    )


                # ==========================================
                # AI RESPONSE
                # ==========================================

                st.markdown("---")

                st.markdown(
                    "**🤖 AI Response:**"
                )

                st.info(
                    ticket.get(
                        "ai_response",
                        "No AI response available."
                    )
                )


                # ==========================================
                # TICKET STATUS
                # ==========================================

                st.markdown("---")

                current_status = ticket.get(
                    "status",
                    "assigned"
                )

                status_options = [
                    "assigned",
                    "in_progress",
                    "resolved",
                    "closed"
                ]

                new_status = st.selectbox(
                    "Ticket Status",
                    status_options,
                    index=(
                        status_options.index(current_status)
                        if current_status in status_options
                        else 0
                    ),
                    key=f"status_{ticket_id}"
                )


                # ==========================================
                # UPDATE STATUS
                # ==========================================

                if st.button(
                    "Update Status",
                    key=f"update_{ticket_id}",
                    type="primary"
                ):

                    try:

                        update_response = update_ticket_status(
                            ticket_id,
                            new_status,
                            token
                        )

                        if update_response.status_code == 200:

                            st.success(
                                "Ticket status updated successfully."
                            )

                            st.rerun()

                        else:

                            try:

                                error = (
                                    update_response
                                    .json()
                                    .get(
                                        "detail",
                                        "Unable to update ticket."
                                    )
                                )

                            except Exception:

                                error = (
                                    "Unable to update ticket."
                                )

                            st.error(error)

                    except Exception:

                        st.error(
                            "Unable to connect to the ticket service."
                        )


                # ==========================================
                # CUSTOMER FEEDBACK
                # ==========================================

                ticket_feedback = [
                    feedback
                    for feedback in assigned_feedback
                    if feedback.get("ticket_id") == ticket_id
                ]

                if ticket_feedback:

                    st.markdown("---")

                    st.markdown(
                        "### ⭐ Customer Feedback"
                    )

                    for feedback in ticket_feedback:

                        rating = feedback.get(
                            "rating",
                            "unknown"
                        )

                        comment = feedback.get(
                            "comment",
                            ""
                        )


                        # Helpful feedback

                        if rating == "helpful":

                            st.success(
                                "👍 Customer marked this response as Helpful."
                            )


                        # Not helpful feedback

                        elif rating == "not_helpful":

                            st.warning(
                                "👎 Customer marked this response as Not Helpful."
                            )


                        # Customer comment

                        if comment:

                            st.caption(
                                f"💬 Customer comment: {comment}"
                            )

                else:

                    st.caption(
                        "⭐ No customer feedback submitted yet."
                    )
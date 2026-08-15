import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)
import streamlit as st

from api_client import (
    send_chat,
    get_my_tickets,
    submit_feedback,
    get_my_feedback,
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NovaCart | Customer Dashboard",
    page_icon="🛍️",
    layout="wide"
)


# ==========================================
# AUTH CHECK
# ==========================================

if not st.session_state.get("authenticated", False):
    st.warning("Please login to continue.")
    st.stop()


token = st.session_state.get("access_token")

# ==========================================
# CHAT HISTORY
# ==========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

    .welcome-card {
        background: white;
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin-bottom: 24px;
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
# NAVIGATION STATE
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "💬 AI Support"


def navigate_to(page_name):

    st.session_state.page = page_name

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🛍️ NovaCart")

    st.markdown("---")

    st.markdown("### Customer Support")
    st.caption(
        "AI-powered support for your orders, "
        "payments and account issues."
    )

    st.markdown("---")

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.authenticated = False
        st.session_state.access_token = None

        st.switch_page("pages/login.py")

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="dashboard-title">'
    'Welcome back 👋'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'How can NovaCart help you today?'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# WELCOME CARD
# ==========================================

st.markdown(
    """
    <div class="welcome-card">
        <h3>Need help with something?</h3>
        <p>
            Our AI support assistant can help with
            payments, orders, account issues, delivery,
            refunds and more.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# QUICK ACCESS
# ==========================================

st.markdown("### Quick Access")

col1, col2, col3 = st.columns(3)

# ------------------------------------------
# AI SUPPORT CARD
# ------------------------------------------

with col1:

    with st.container(border=True):

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:10px 0 4px 0;
            ">
                <div style="font-size:42px;">💬</div>
                <div style="
                    font-size:18px;
                    font-weight:600;
                    margin-top:6px;
                ">
                    AI Support
                </div>
                <div style="
                    color:#6b7280;
                    font-size:14px;
                    margin-top:5px;
                ">
                    Get instant assistance
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open AI Support →",
            key="open_ai_support",
            use_container_width=True
        ):

            navigate_to("💬 AI Support")


# ------------------------------------------
# MY TICKETS CARD
# ------------------------------------------

with col2:

    with st.container(border=True):

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:10px 0 4px 0;
            ">
                <div style="font-size:42px;">🎫</div>
                <div style="
                    font-size:18px;
                    font-weight:600;
                    margin-top:6px;
                ">
                    My Tickets
                </div>
                <div style="
                    color:#6b7280;
                    font-size:14px;
                    margin-top:5px;
                ">
                    Track your support requests
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "View My Tickets →",
            key="open_my_tickets",
            use_container_width=True
        ):

            navigate_to("🎫 My Tickets")


# ------------------------------------------
# FEEDBACK CARD
# ------------------------------------------

with col3:

    with st.container(border=True):

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:10px 0 4px 0;
            ">
                <div style="font-size:42px;">⭐</div>
                <div style="
                    font-size:18px;
                    font-weight:600;
                    margin-top:6px;
                ">
                    Feedback
                </div>
                <div style="
                    color:#6b7280;
                    font-size:14px;
                    margin-top:5px;
                ">
                    Share your experience
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Give Feedback →",
            key="open_feedback",
            use_container_width=True
        ):

            navigate_to("⭐ Feedback")

# ==========================================
# AI SUPPORT
# ==========================================

page = st.session_state.page

if page == "💬 AI Support":

    st.markdown("### 💬 AI Support")

    st.markdown(
        """
        <div class="welcome-card">
            <h3>How can I help you today?</h3>
            <p>
                Ask me about payments, orders, refunds,
                delivery, account issues and more.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------
    # Display previous messages
    # --------------------------------------

    for chat in st.session_state.chat_history:

        with st.chat_message(chat["role"]):
            st.write(chat["content"])

            if (
                chat["role"] == "assistant"
                and chat.get("ticket_id")
            ):
                st.info(
                    f"🎫 Support ticket "
                    f"#{chat['ticket_id']} created."
                )

    # --------------------------------------
    # Chat input
    # --------------------------------------

    message = st.chat_input(
        "Ask NovaCart anything..."
    )

    if message:

        # Show user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": message
            }
        )

        with st.chat_message("user"):
            st.write(message)

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner(
                "NovaCart is thinking..."
            ):

                try:

                    response = send_chat(
                        message,
                        token
                    )

                    if response.status_code == 200:

                        data = response.json()

                        ai_message = data.get(
                            "message",
                            "I couldn't generate a response."
                        )

                        ticket_id = data.get(
                            "ticket_id"
                        )

                        st.write(ai_message)

                        # Save assistant response
                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": ai_message,
                                "ticket_id": ticket_id
                            }
                        )

                        # Ticket notification
                        if ticket_id:

                            st.info(
                                f"🎫 Support ticket "
                                f"#{ticket_id} has been created "
                                f"for this issue."
                            )

                    else:

                        error_message = (
                            "Unable to process your request."
                        )

                        st.error(error_message)

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": error_message
                            }
                        )

                except Exception as e:

                    error_message = (
                        "Unable to connect to NovaCart support."
                    )

                    st.error(error_message)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )
# ==========================================
# TICKETS
# ==========================================

elif page == "🎫 My Tickets":

    st.markdown("### 🎫 My Tickets")

    try:

        response = get_my_tickets(token)

        if response.status_code == 200:

            data = response.json()

            tickets = data.get(
                "tickets",
                []
            )

            if not tickets:

                st.info(
                    "You don't have any support tickets yet."
                )

            else:

                st.caption(
                    f"You have {len(tickets)} support ticket(s)."
                )

                for ticket in tickets:

                    ticket_id = ticket.get("id")
                    status = ticket.get(
                        "status",
                        "unknown"
                    )

                    with st.container(
                        border=True
                    ):

                        # Ticket heading
                        col1, col2 = st.columns(
                            [4, 1]
                        )

                        with col1:

                            st.markdown(
                                f"### 🎫 Ticket #{ticket_id}"
                            )

                        with col2:

                            st.caption(
                                f"Status: {status}"
                            )

                        # Issue
                        st.write(
                            ticket.get(
                                "description",
                                ""
                            )
                        )

                        # Ticket information
                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.caption(
                                f"Priority: "
                                f"{ticket.get('priority', 'unknown')}"
                            )

                        with col2:

                            st.caption(
                                f"Intent: "
                                f"{ticket.get('intent', 'unknown')}"
                            )

                        with col3:

                            st.caption(
                                f"Assigned to: "
                                f"{ticket.get('assigned_to', 'Not assigned')}"
                            )

                        # AI response
                        ai_response = ticket.get(
                            "ai_response"
                        )

                        if ai_response:

                            st.markdown(
                                "**🤖 NovaCart Response**"
                            )

                            st.info(
                                ai_response
                            )

                        # Escalation reason
                        escalation_reason = ticket.get(
                            "escalation_reason"
                        )

                        if escalation_reason:

                            st.warning(
                                f"Human Support: "
                                f"{escalation_reason}"
                            )

                        # Resolved / closed status
                        if status in [
                            "resolved",
                            "closed"
                        ]:

                            st.success(
                                "✅ This ticket has been resolved."
                            )
    except Exception:

        st.error(
            "Unable to connect to the ticket service."
        )
# ==========================================
# FEEDBACK
# ==========================================

elif page == "⭐ Feedback":

    st.markdown("### ⭐ Feedback")

    st.caption(
        "Share your experience for resolved support tickets."
    )

    try:

        response = get_my_tickets(token)

        feedback_response = get_my_feedback(token)

        if feedback_response.status_code == 200:
            feedback_data = feedback_response.json()
            my_feedback = feedback_data.get("feedback", [])
        else:
            my_feedback = []

        if response.status_code == 200:

            data = response.json()

            tickets = data.get(
                "tickets",
                []
            )

            submitted_ticket_ids = {
                feedback.get("ticket_id")
                for feedback in my_feedback
            }

            resolved_tickets = [
                ticket
                for ticket in tickets
                if ticket.get("status") in ["resolved", "closed"]
                and ticket.get("id") not in submitted_ticket_ids
            ]

            if not resolved_tickets:

                st.info(
                    "Feedback will be available "
                    "after a ticket is resolved."
                )

            else:

                for ticket in resolved_tickets:

                    ticket_id = ticket.get("id")

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### 🎫 Ticket #{ticket_id}"
                        )

                        st.write(
                            ticket.get(
                                "description",
                                ""
                            )
                        )

                        st.success(
                            f"Status: "
                            f"{ticket.get('status')}"
                        )

                        st.markdown(
                            "**How was your support experience?**"
                        )

                        rating = st.radio(
                            "Feedback",
                            [
                                "👍 Helpful",
                                "👎 Not Helpful"
                            ],
                            horizontal=True,
                            key=f"rating_{ticket_id}",
                            label_visibility="collapsed"
                        )

                        comment = st.text_area(
                            "Comment (optional)",
                            placeholder=(
                                "Tell us about your experience..."
                            ),
                            key=f"comment_{ticket_id}"
                        )

                        if st.button(
                            "Submit Feedback",
                            type="primary",
                            key=f"submit_feedback_{ticket_id}",
                            use_container_width=True
                        ):

                            if rating == "👍 Helpful":

                                feedback_rating = "helpful"

                            else:

                                feedback_rating = "not_helpful"

                            try:

                                feedback_response = (
                                    submit_feedback(
                                        ticket_id,
                                        feedback_rating,
                                        comment,
                                        token
                                    )
                                )

                                if feedback_response.status_code in [
                                    200,
                                    201
                                ]:

                                    st.success(
                                        "⭐ Thank you! "
                                        "Your feedback has been submitted successfully."
                                    )
                                   
                                else:

                                    try:

                                        error = (
                                            feedback_response
                                            .json()
                                            .get(
                                                "detail",
                                                "Unable to submit feedback."
                                            )
                                        )

                                    except Exception:

                                        error = (
                                            "Unable to submit feedback."
                                        )

                                    st.error(error)

                            except Exception:

                                st.error(
                                    "Unable to connect "
                                    "to the feedback service."
                                )

        else:

            st.error(
                "Unable to load your tickets."
            )

    except Exception:

        st.error(
            "Unable to connect to the ticket service."
        )
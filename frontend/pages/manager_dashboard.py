import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

import streamlit as st

from api_client import (
    get_all_feedback,
    get_feedback_analytics,
    get_feedback_reviews,
    update_feedback_review,
    get_feedback_improvements,
    get_improvements_by_intent,
    get_improvement_suggestions,
    create_agent,
    get_all_users,
    get_all_tickets,
    assign_ticket
)
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NovaCart | Manager Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# AUTH CHECK
# ==========================================

if not st.session_state.get(
    "authenticated",
    False
):
    st.warning(
        "Please login to continue."
    )
    st.stop()


# Only managers can access
if st.session_state.get(
    "user_role"
) != "manager":

    st.error(
        "Access denied. Manager access required."
    )

    st.stop()


token = st.session_state.get(
    "access_token"
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

    st.markdown("## 📊 NovaCart")

    st.caption(
        "Support Manager Portal"
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "📊 Overview",
            "⭐ Customer Feedback",
            "📝 Feedback Reviews",
            "💡 Improvements",
            "👥 Users & Agents",
            "🎫 Assign Tickets",
            "➕ Create Agent"
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
    'Manager Dashboard 📊'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Monitor customer feedback and support performance.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# LOAD FEEDBACK ANALYTICS
# ==========================================

analytics = {
    "total_feedback": 0,
    "helpful": 0,
    "not_helpful": 0,
    "satisfaction_rate": 0
}

try:

    analytics_response = (
        get_feedback_analytics(token)
    )

    if analytics_response.status_code == 200:

        analytics = (
            analytics_response.json()
        )

    else:

        st.error(
            "Unable to load feedback analytics."
        )

except Exception:

    st.error(
        "Unable to connect to the feedback service."
    )


# ==========================================
# LOAD ALL FEEDBACK
# ==========================================

all_feedback = []

try:

    feedback_response = (
        get_all_feedback(token)
    )

    if feedback_response.status_code == 200:

        feedback_data = (
            feedback_response.json()
        )

        all_feedback = feedback_data.get(
            "feedback",
            []
        )

    else:

        st.error(
            "Unable to load customer feedback."
        )

except Exception:

    st.error(
        "Unable to connect to the feedback service."
    )

# ==========================================
# LOAD ALL USERS
# ==========================================

all_users = []

try:

    users_response = get_all_users(token)

    if users_response.status_code == 200:

        users_data = users_response.json()

        all_users = users_data.get(
            "users",
            []
        )

    else:

        st.error(
            "Unable to load users."
        )

except Exception:

    st.error(
        "Unable to connect to user service."
    )

# ==========================================
# LOAD ALL TICKETS
# ==========================================

all_tickets = []

try:

    tickets_response = get_all_tickets(token)

    if tickets_response.status_code == 200:

        tickets_data = tickets_response.json()

        all_tickets = tickets_data.get(
            "tickets",
            []
        )

    else:

        st.error(
            "Unable to load tickets."
        )

except Exception:

    st.error(
        "Unable to connect to ticket service."
    )

# ==========================================
# OVERVIEW
# ==========================================

if page == "📊 Overview":

    st.markdown(
        "### 📊 Feedback Overview"
    )

    total_feedback = analytics.get(
        "total_feedback",
        0
    )

    helpful = analytics.get(
        "helpful",
        0
    )

    not_helpful = analytics.get(
        "not_helpful",
        0
    )

    satisfaction_rate = analytics.get(
        "satisfaction_rate",
        0
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>⭐</h2>
                <b>{total_feedback}</b>
                <p>Total Feedback</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>👍</h2>
                <b>{helpful}</b>
                <p>Helpful</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>👎</h2>
                <b>{not_helpful}</b>
                <p>Not Helpful</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="stat-card">
                <h2>📈</h2>
                <b>{satisfaction_rate}%</b>
                <p>Satisfaction Rate</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("---")

    st.markdown(
        "### ⭐ Recent Customer Feedback"
    )

    if not all_feedback:

        st.info(
            "No customer feedback available yet."
        )

    else:

        for feedback in all_feedback[:10]:

            ticket_id = feedback.get(
                "ticket_id",
                "N/A"
            )

            rating = feedback.get(
                "rating",
                "unknown"
            )

            comment = feedback.get(
                "comment",
                ""
            )

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"### 🎫 Ticket #{ticket_id}"
                    )

                    if comment:

                        st.write(
                            comment
                        )

                    else:

                        st.caption(
                            "No comment provided."
                        )

                with col2:

                    if rating == "helpful":

                        st.success(
                            "👍 Helpful"
                        )

                    elif rating == "not_helpful":

                        st.warning(
                            "👎 Not Helpful"
                        )

                    else:

                        st.info(
                            str(rating)
                        )


# ==========================================
# CUSTOMER FEEDBACK
# ==========================================

elif page == "⭐ Customer Feedback":

    st.markdown(
        "### ⭐ Customer Feedback"
    )

    st.caption(
        "View feedback submitted by customers."
    )


    if not all_feedback:

        st.info(
            "No customer feedback available."
        )

    else:

        for feedback in all_feedback:

            ticket_id = feedback.get(
                "ticket_id",
                "N/A"
            )

            rating = feedback.get(
                "rating",
                "unknown"
            )

            comment = feedback.get(
                "comment",
                ""
            )

            created_at = feedback.get(
                "created_at",
                ""
            )


            with st.container(
                border=True
            ):

                st.markdown(
                    f"### 🎫 Ticket #{ticket_id}"
                )


                if rating == "helpful":

                    st.success(
                        "👍 Helpful"
                    )

                elif rating == "not_helpful":

                    st.warning(
                        "👎 Not Helpful"
                    )

                else:

                    st.info(
                        f"Rating: {rating}"
                    )


                if comment:

                    st.write(
                        f"**Customer Comment:** {comment}"
                    )

                else:

                    st.caption(
                        "No comment provided."
                    )


                if created_at:

                    st.caption(
                        f"Submitted: {created_at}"
                    )

# ==========================================
# FEEDBACK REVIEWS
# ==========================================

elif page == "📝 Feedback Reviews":

    st.markdown("### 📝 Feedback Reviews")

    st.caption(
        "Review negative customer feedback and help improve AI responses."
    )

    try:

        response = get_feedback_reviews(token)

        if response.status_code == 200:

            data = response.json()

            reviews = data.get(
                "reviews",
                []
            )

            if not reviews:

                st.success(
                    "🎉 No pending feedback reviews."
                )

            else:

                st.info(
                    f"{len(reviews)} pending feedback review(s) found."
                )

                for review in reviews:

                    review_id = review.get("id")
                    ticket_id = review.get("ticket_id")
                    feedback_id = review.get("feedback_id")

                    with st.container(border=True):

                        st.markdown(
                            f"### 🎫 Ticket #{ticket_id}"
                        )

                        st.caption(
                            f"Review ID: {review_id} | "
                            f"Feedback ID: {feedback_id}"
                        )

                        st.markdown(
                            "**Review Status:**"
                        )

                        st.warning(
                            "⏳ Pending Review"
                        )

                        st.markdown("---")

                        review_comment = st.text_area(
                            "Manager Review / Comment",
                            placeholder=(
                                "Write what should be improved..."
                            ),
                            key=f"review_comment_{review_id}"
                        )

                        if st.button(
                            "✅ Mark as Reviewed",
                            key=f"review_{review_id}",
                            type="primary",
                            use_container_width=True
                        ):

                            try:

                                update_response = update_feedback_review(
                                    review_id,
                                    "reviewed",
                                    review_comment,
                                    token
                                )

                                if update_response.status_code == 200:

                                    st.success(
                                        "Feedback review completed successfully."
                                    )

                                    st.rerun()

                                else:

                                    try:

                                        error = (
                                            update_response
                                            .json()
                                            .get(
                                                "detail",
                                                "Unable to update review."
                                            )
                                        )

                                    except Exception:

                                        error = (
                                            "Unable to update review."
                                        )

                                    st.error(error)

                            except Exception:

                                st.error(
                                    "Unable to connect to feedback service."
                                )

        else:

            try:

                error = (
                    response.json()
                    .get(
                        "detail",
                        "Unable to load feedback reviews."
                    )
                )

            except Exception:

                error = "Unable to load feedback reviews."

            st.error(error)

    except Exception:

        st.error(
            "Unable to connect to feedback service."
        )

# ==========================================
# IMPROVEMENTS
# ==========================================

elif page == "💡 Improvements":

    st.markdown("### 💡 AI Improvement Insights")

    st.caption(
        "Analyze reviewed negative feedback and identify areas for improving AI responses."
    )

    # ======================================
    # REVIEWED IMPROVEMENTS
    # ======================================

    st.markdown("### 📝 Reviewed Feedback")

    try:

        response = get_feedback_improvements(token)

        if response.status_code == 200:

            data = response.json()

            improvements = data.get(
                "improvements",
                []
            )

            if not improvements:

                st.info(
                    "No reviewed improvements available yet."
                )

            else:

                for item in improvements:

                    with st.container(border=True):

                        st.markdown(
                            f"### 🎫 Ticket #{item.get('ticket_id')}"
                        )

                        st.write(
                            f"**Intent:** {item.get('intent', 'N/A')}"
                        )

                        st.write(
                            f"**Priority:** {item.get('priority', 'N/A')}"
                        )

                        st.markdown("**Customer Question:**")

                        st.write(
                            item.get(
                                "customer_question",
                                "N/A"
                            )
                        )

                        st.markdown("**AI Response:**")

                        st.write(
                            item.get(
                                "ai_response",
                                "N/A"
                            )
                        )

                        st.markdown("**Customer Feedback:**")

                        st.warning(
                            item.get(
                                "customer_feedback",
                                "No comment provided."
                            )
                        )

                        st.markdown("**Manager Review:**")

                        st.success(
                            item.get(
                                "review_comment",
                                "No manager comment."
                            )
                        )

                        st.caption(
                            f"Review Status: "
                            f"{item.get('review_status', 'N/A')}"
                        )

        else:

            st.error(
                "Unable to load improvement data."
            )

    except Exception:

        st.error(
            "Unable to connect to improvement service."
        )

    # ======================================
    # NEGATIVE FEEDBACK BY INTENT
    # ======================================

    st.markdown("---")

    st.markdown(
        "### 📊 Negative Feedback by Intent"
    )

    try:

        response = get_improvements_by_intent(token)

        if response.status_code == 200:

            data = response.json()

            intent_counts = data.get(
                "negative_feedback_by_intent",
                {}
            )

            if not intent_counts:

                st.info(
                    "No negative feedback data available."
                )

            else:

                for intent, count in intent_counts.items():

                    st.write(
                        f"**{intent}** — {count} negative feedback(s)"
                    )

        else:

            st.error(
                "Unable to load intent analytics."
            )

    except Exception:

        st.error(
            "Unable to connect to analytics service."
        )

    # ======================================
    # AI IMPROVEMENT SUGGESTIONS
    # ======================================

    st.markdown("---")

    st.markdown(
        "### 🤖 Improvement Suggestions"
    )

    try:

        response = get_improvement_suggestions(token)

        if response.status_code == 200:

            data = response.json()

            suggestions = data.get(
                "suggestions",
                []
            )

            if not suggestions:

                st.success(
                    "🎉 No repeated negative-feedback patterns detected."
                )

            else:

                for suggestion in suggestions:

                    with st.container(border=True):

                        st.markdown(
                            f"### 🔍 {suggestion.get('intent', 'Unknown Intent')}"
                        )

                        st.warning(
                            f"Negative feedback: "
                            f"{suggestion.get('negative_feedback_count', 0)}"
                        )

                        st.write(
                            suggestion.get(
                                "suggestion",
                                "No suggestion available."
                            )
                        )

        else:

            st.error(
                "Unable to load improvement suggestions."
            )

    except Exception:

        st.error(
            "Unable to connect to suggestion service."
        )

# ==========================================
# MANAGE AGENTS
# ==========================================

elif page == "➕ Create Agent":

    st.markdown("### ➕ Create Agent")

    st.caption(
        "Create new support agents who can access the Agent Dashboard."
    )

    st.markdown("---")

    st.markdown("### ➕ Create New Agent")

    with st.form("create_agent_form"):

        agent_name = st.text_input(
            "Agent Name",
            placeholder="Enter agent name"
        )

        agent_email = st.text_input(
            "Agent Email",
            placeholder="Enter agent email"
        )

        agent_password = st.text_input(
            "Agent Password",
            type="password",
            placeholder="Enter temporary password"
        )

        create_button = st.form_submit_button(
            "👤 Create Agent",
            use_container_width=True
        )

        if create_button:

            if not agent_name.strip():
                st.error("Please enter agent name.")

            elif not agent_email.strip():
                st.error("Please enter agent email.")

            elif not agent_password:
                st.error("Please enter agent password.")

            elif len(agent_password) < 6:
                st.error(
                    "Password must be at least 6 characters."
                )

            else:

                try:

                    response = create_agent(
                        agent_name.strip(),
                        agent_email.strip(),
                        agent_password,
                        token
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.success(
                            "✅ Agent created successfully!"
                        )

                        st.write(
                            f"**Agent Name:** "
                            f"{data.get('name')}"
                        )

                        st.write(
                            f"**Agent Email:** "
                            f"{data.get('email')}"
                        )

                        st.write(
                            f"**Role:** "
                            f"{data.get('role')}"
                        )

                    else:

                        try:

                            error = response.json().get(
                                "detail",
                                "Unable to create agent."
                            )

                        except Exception:

                            error = "Unable to create agent."

                        st.error(error)

                except Exception as e:

                    st.error(
                        "Unable to connect to authentication service."
                    )

# ==========================================
# USERS & AGENTS
# ==========================================

elif page == "👥 Users & Agents":

    st.markdown("### 👥 Users & Agents")

    st.caption(
        "View all customers, agents, and managers in the system."
    )

    if not all_users:

        st.info(
            "No users available."
        )

    else:

        # --------------------------------------
        # FILTER
        # --------------------------------------

        role_filter = st.selectbox(
            "Filter by Role",
            [
                "All",
                "Customer",
                "Agent",
                "Manager"
            ]
        )

        if role_filter == "All":

            filtered_users = all_users

        else:

            filtered_users = [
                user
                for user in all_users
                if user.get("role", "").lower()
                == role_filter.lower()
            ]

        # --------------------------------------
        # SUMMARY
        # --------------------------------------

        total_users = len(all_users)

        total_customers = sum(
            1
            for user in all_users
            if user.get("role") == "customer"
        )

        total_agents = sum(
            1
            for user in all_users
            if user.get("role") == "agent"
        )

        total_managers = sum(
            1
            for user in all_users
            if user.get("role") == "manager"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Total Users",
                total_users
            )

        with col2:
            st.metric(
                "🧑‍💻 Customers",
                total_customers
            )

        with col3:
            st.metric(
                "🛠️ Agents",
                total_agents
            )

        with col4:
            st.metric(
                "👔 Managers",
                total_managers
            )

        st.markdown("---")

        # --------------------------------------
        # USER TABLE
        # --------------------------------------

        st.markdown("### 📋 User Directory")

        if not filtered_users:

            st.info(
                "No users found for this role."
            )

        else:

            table_data = []

            for user in filtered_users:

                user_id = user.get("id")
                role = user.get("role")

                # Count active tickets assigned to this user
                active_ticket_count = 0

                if role == "agent":

                    active_ticket_count = sum(
                        1
                        for ticket in all_tickets
                        if ticket.get("assigned_to") == user_id
                        and ticket.get("status") in [
                            "assigned",
                            "in_progress"
                        ]
                    )

                table_data.append({
                    "ID": user_id,
                    "Name": user.get("name"),
                    "Email": user.get("email"),
                    "Role": role,
                    "Active Tickets": (
                        active_ticket_count
                        if role == "agent"
                        else "-"
                    ),
                    "Created At": user.get("created_at")
                })

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )

# ==========================================
# ASSIGN TICKETS
# ==========================================

elif page == "🎫 Assign Tickets":

    st.markdown("### 🎫 Assign Tickets")

    st.caption(
        "Assign customer tickets to available support agents."
    )

    # --------------------------------------
    # GET AGENTS
    # --------------------------------------

    agents = [
        user
        for user in all_users
        if user.get("role") == "agent"
    ]

    # --------------------------------------
    # CHECK AGENTS
    # --------------------------------------

    if not agents:

        st.warning(
            "No support agents available. "
            "Create an agent first."
        )

    elif not all_tickets:

        st.info(
            "No tickets available."
        )

    else:

        # ----------------------------------
        # SHOW TICKETS
        # ----------------------------------

        for ticket in all_tickets:

            ticket_id = ticket.get("id")
            subject = ticket.get(
                "subject",
                "No subject"
            )

            description = ticket.get(
                "description",
                ""
            )

            status = ticket.get(
                "status",
                "unknown"
            )

            assigned_to = ticket.get(
                "assigned_to"
            )

            with st.container(border=True):

                st.markdown(
                    f"### 🎫 Ticket #{ticket_id}"
                )

                st.write(
                    f"**Subject:** {subject}"
                )

                st.write(
                    f"**Description:** {description}"
                )

                st.write(
                    f"**Status:** {status}"
                )

                # ------------------------------
                # CURRENT ASSIGNMENT
                # ------------------------------

                if assigned_to:

                    current_agent = next(
                        (
                            agent
                            for agent in agents
                            if agent.get("id") == assigned_to
                        ),
                        None
                    )

                    if current_agent:

                        st.info(
                            f"Currently assigned to: "
                            f"{current_agent.get('name')}"
                        )

                # ------------------------------
                # AGENT SELECT
                # ------------------------------

                agent_options = {
                    f"{agent.get('name')} "
                    f"({agent.get('email')})":
                    agent.get("id")
                    for agent in agents
                }

                selected_agent = st.selectbox(
                    "Assign to Agent",
                    options=list(
                        agent_options.keys()
                    ),
                    key=f"agent_select_{ticket_id}"
                )

                selected_agent_id = agent_options[
                    selected_agent
                ]

                # ------------------------------
                # ASSIGN BUTTON
                # ------------------------------

                if st.button(
                    "🎯 Assign Ticket",
                    key=f"assign_ticket_{ticket_id}",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        response = assign_ticket(
                            ticket_id,
                            selected_agent_id,
                            token
                        )

                        if response.status_code == 200:

                            result = response.json()

                            st.success(
                                f"✅ Ticket #{ticket_id} "
                                f"assigned to "
                                f"{result.get('assigned_agent')}"
                            )

                            st.rerun()

                        else:

                            try:

                                error = (
                                    response
                                    .json()
                                    .get(
                                        "detail",
                                        "Unable to assign ticket."
                                    )
                                )

                            except Exception:

                                error = (
                                    "Unable to assign ticket."
                                )

                            st.error(error)

                    except Exception:

                        st.error(
                            "Unable to connect "
                            "to ticket service."
                        )
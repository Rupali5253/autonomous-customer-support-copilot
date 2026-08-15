import requests

from config import (
    BACKEND_URL,
    CHAT_ENDPOINT,
    TICKETS_ENDPOINT,
    FEEDBACK_ENDPOINT,
)


# ==========================================
# AUTHENTICATION
# ==========================================

def register_user(
    name: str,
    email: str,
    password: str
):
    response = requests.post(
        f"{BACKEND_URL}/auth/register",
        params={
            "name": name,
            "email": email,
            "password": password,
        }
    )

    return response


def login_user(
    email: str,
    password: str
):
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        params={
            "email": email,
            "password": password,
        }
    )

    return response

# ==========================================
# MANAGER - USERS
# ==========================================

def get_all_users(token: str):

    response = requests.get(
        f"{BACKEND_URL}/auth/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

# ==========================================
# CHAT
# ==========================================

def send_chat(
    message: str,
    token: str
):
    response = requests.post(
        CHAT_ENDPOINT,
        json={
            "message": message
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


# ==========================================
# TICKETS
# ==========================================

def get_my_tickets(token: str):

    response = requests.get(
        f"{TICKETS_ENDPOINT}/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def get_assigned_tickets(token: str):

    response = requests.get(
        f"{TICKETS_ENDPOINT}/assigned",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def update_ticket_status(
    ticket_id: int,
    new_status: str,
    token: str
):

    response = requests.put(
        f"{TICKETS_ENDPOINT}/{ticket_id}/status",
        params={
            "new_status": new_status
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

def get_all_tickets(token: str):

    response = requests.get(
        f"{TICKETS_ENDPOINT}/all",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def assign_ticket(
    ticket_id: int,
    agent_id: int,
    token: str
):

    response = requests.put(
        f"{TICKETS_ENDPOINT}/{ticket_id}/assign",
        params={
            "agent_id": agent_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


# ==========================================
# FEEDBACK
# ==========================================

def get_assigned_feedback(token: str):
    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/assigned",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

def get_my_feedback(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/my",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

# Manager Dashboard API Client Functions
def get_all_feedback(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/all",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def get_feedback_analytics(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/analytics",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

def submit_feedback(
    ticket_id: int,
    rating: str,
    comment: str,
    token: str
):
    response = requests.post(
        FEEDBACK_ENDPOINT,
        json={
            "ticket_id": ticket_id,
            "rating": rating,
            "comment": comment,
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

# ==========================================
# FEEDBACK REVIEWS
# ==========================================

def get_feedback_reviews(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/reviews",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def update_feedback_review(
    review_id: int,
    review_status: str,
    review_comment: str,
    token: str
):

    response = requests.put(
        f"{FEEDBACK_ENDPOINT}/reviews/{review_id}",
        json={
            "review_status": review_status,
            "review_comment": review_comment
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


# ==========================================
# FEEDBACK IMPROVEMENTS
# ==========================================

def get_feedback_improvements(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/improvements",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def get_improvements_by_intent(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/improvements/by-intent",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def get_improvement_suggestions(token: str):

    response = requests.get(
        f"{FEEDBACK_ENDPOINT}/improvements/suggestions",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response

def create_agent(
    name,
    email,
    password,
    token
):
    response = requests.post(
        f"{BACKEND_URL}/auth/create-agent",
        params={
            "name": name,
            "email": email,
            "password": password
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response
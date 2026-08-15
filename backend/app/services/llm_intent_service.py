import json

from app.services.llm_service import (
    generate_gemini_response,
    generate_groq_response
)


def detect_intent_with_llm(message: str) -> dict:
    """
    LLM fallback for intent classification.
    """

    prompt = f"""
You are an intent classification system for a customer support application.

Classify the customer message into exactly ONE of these intents:

payment_issue
account_security
account_guidance
account_issue
technical_issue
general_chat

Also determine:
- ticket_required: true or false
- priority: low, medium, high, or critical

Classification rules:

payment_issue:
Payment, transaction, charged, deducted, refund,
payment failure, or payment/order mismatch.

account_security:
Hacked account, unauthorized access, fraud,
suspicious activity, or an order/action the customer
did not perform.

account_guidance:
Customer is asking how to reset/change password,
update email, login, or perform a normal account action.

account_issue:
Customer cannot login/access account, password reset
does not work, or account is locked.

technical_issue:
Website, app, dashboard, page, system, or software
is broken, crashing, loading incorrectly, or showing an error.

general_chat:
Normal conversation that is not a customer support issue.

Priority rules:
- critical = security/fraud
- high = payment issue
- medium = account or technical problem
- low = simple guidance
- none = general chat

Return ONLY valid JSON in exactly this format:

{{
    "intent": "one_intent_here",
    "ticket_required": true,
    "priority": "medium"
}}

Customer message:
{message}
"""

    try:
        # Gemini first
        response = generate_gemini_response(prompt)

    except Exception as gemini_error:

        print("Gemini intent classification failed.")
        print("Gemini error:", gemini_error)

        try:
            # Groq fallback
            response = generate_groq_response(prompt)

        except Exception as groq_error:

            print("Groq intent classification failed.")
            print("Groq error:", groq_error)

            return {
                "intent": "general_chat",
                "ticket_required": False,
                "priority": "none"
            }

    try:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.replace(
                "```json", ""
            )
            cleaned_response = cleaned_response.replace(
                "```", ""
            )
            cleaned_response = cleaned_response.strip()

        result = json.loads(cleaned_response)

        intent = result.get(
            "intent",
            "general_chat"
        )

        ticket_required = result.get(
            "ticket_required",
            False
        )

        priority = result.get(
            "priority",
            "none"
        )

        # General chat should not create a ticket
        if intent == "general_chat":
            ticket_required = False
            priority = "none"

        return {
            "intent": intent,
            "ticket_required": ticket_required,
            "priority": priority
        }

    except (json.JSONDecodeError, TypeError):

        print("LLM returned invalid intent JSON.")
        print("RAW LLM RESPONSE:", response)

        return {
            "intent": "general_chat",
            "ticket_required": False,
            "priority": "none"
        }
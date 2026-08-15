def check_escalation(
    user_message: str,
    intent: str,
    priority: str
) -> dict:
    """
    Decide whether a customer issue requires
    human support escalation.
    """

    message = user_message.lower()

    # Critical account-security situations
    critical_keywords = [
        "account hacked",
        "account compromised",
        "someone accessed my account",
        "someone has access to my account",
        "unauthorized order",
        "order i didn't place",
        "order i did not place",
        "fraud",
        "stolen account"
    ]

    # Payment investigation situations
    payment_keywords = [
        "charged twice",
        "charged two times",
        "payment deducted twice",
        "money deducted but",
        "payment deducted but order",
        "payment deducted and order",
        "payment failed but money",
        "money was deducted",
        "amount deducted"
    ]

    # Account recovery situations
    account_keywords = [
        "cannot reset password",
        "can't reset password",
        "unable to reset password",
        "cannot access my account",
        "can't access my account",
        "locked account",
        "account locked",
        "cannot recover account"
    ]

    # Check critical security issues
    if any(keyword in message for keyword in critical_keywords):
        return {
            "escalation_required": True,
            "escalation_reason": (
                "Potential account security or "
                "unauthorized activity requires human investigation."
            )
        }

    # Check payment investigation
    if any(keyword in message for keyword in payment_keywords):
        return {
            "escalation_required": True,
            "escalation_reason": (
                "Payment verification or transaction "
                "investigation may be required."
            )
        }

    # Check account recovery
    if any(keyword in message for keyword in account_keywords):
        return {
            "escalation_required": True,
            "escalation_reason": (
                "Account recovery requires additional "
                "verification or human assistance."
            )
        }

    # Critical/high priority can require escalation
    if priority.lower() in ["critical", "high"]:
        return {
            "escalation_required": True,
            "escalation_reason": (
                "High-priority issue requires human review."
            )
        }

    # Otherwise AI can handle the request
    return {
        "escalation_required": False,
        "escalation_reason": None
    }

if __name__ == "__main__":

    test_cases = [
        {
            "message": "How can I reset my password?",
            "intent": "account_support",
            "priority": "low"
        },
        {
            "message": "My payment was deducted but my order was not confirmed.",
            "intent": "payment_issue",
            "priority": "high"
        },
        {
            "message": "Someone placed an order from my account that I did not place.",
            "intent": "account_security",
            "priority": "high"
        },
        {
            "message": "My account has been hacked.",
            "intent": "account_security",
            "priority": "critical"
        }
    ]

    for test in test_cases:

        result = check_escalation(
            test["message"],
            test["intent"],
            test["priority"]
        )

        print("\nQuestion:", test["message"])
        print("Result:", result)
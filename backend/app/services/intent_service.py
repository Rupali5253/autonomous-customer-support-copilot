from app.services.llm_intent_service import detect_intent_with_llm
def detect_intent(message: str) -> dict:
    """
    Detect customer intent and decide whether a support ticket
    should be created.
    """

    text = message.lower()

   # ==========================================
    # SMART PAYMENT CONTEXT DETECTION
    # ==========================================

    payment_words = [
        "payment",
        "paid",
        "pay",
        "charged",
        "debited",
        "deducted",
        "transaction",
        "money",
        "amount"
    ]

    order_words = [
        "order",
        "purchase",
        "checkout"
    ]

    problem_words = [
        "failed",
        "failure",
        "not confirmed",
        "not received",
        "didn't receive",
        "did not receive",
        "not showing",
        "not created",
        "didn't go through",
        "did not go through",
        "missing",
        "pending",
        "error",
        "declined",
        "rejected",
        "deducted",
        "debited"
    ]

    duplicate_words = [
        "twice",
        "two times",
        "duplicate",
        "duplicated"
    ]

    has_payment_context = any(
        word in text
        for word in payment_words
    )

    has_order_context = any(
        word in text
        for word in order_words
    )

    has_problem_context = any(
        word in text
        for word in problem_words
    )

    has_duplicate_context = any(
        word in text
        for word in duplicate_words
    )

    # Payment + order + problem
    if (
        has_payment_context
        and has_order_context
        and has_problem_context
    ):
        return {
            "intent": "payment_issue",
            "ticket_required": True,
            "priority": "high"
        }

    # Payment + problem
    if (
        has_payment_context
        and has_problem_context
    ):
        return {
            "intent": "payment_issue",
            "ticket_required": True,
            "priority": "high"
        }

    # Payment charged/deducted multiple times
    if (
        has_payment_context
        and has_duplicate_context
    ):
        return {
            "intent": "payment_issue",
            "ticket_required": True,
            "priority": "high"
        }
  

    # ==========================================
    # SMART ACCOUNT SECURITY DETECTION
    # ==========================================

    security_account_words = [
        "account",
        "profile",
        "login"
    ]

    security_action_words = [
        "hacked",
        "compromised",
        "stolen",
        "accessed",
        "access",
        "logged in",
        "login",
        "used",
        "taken over"
    ]

    unauthorized_words = [
        "someone",
        "unknown",
        "unauthorized",
        "unauthorised",
        "not mine",
        "not me",
        "didn't place",
        "did not place",
        "don't recognize",
        "do not recognize",
        "unrecognized",
        "unknown order",
        "fraud"
    ]

    has_security_account = any(
        word in text
        for word in security_account_words
    )

    has_security_action = any(
        word in text
        for word in security_action_words
    )

    has_unauthorized_context = any(
        phrase in text
        for phrase in unauthorized_words
    )

    # Account compromised / accessed
    if (
        has_security_account
        and has_security_action
    ):
        return {
            "intent": "account_security",
            "ticket_required": True,
            "priority": "critical"
        }

    # Unauthorized activity
    if has_unauthorized_context and (
        "order" in text
        or "account" in text
        or "purchase" in text
    ):
        return {
            "intent": "account_security",
            "ticket_required": True,
            "priority": "critical"
        }

    # ==========================================
    # ACCOUNT PROBLEM HAS PRIORITY OVER GUIDANCE
    # ==========================================

    problem_action_words = [
        "not working",
        "isn't working",
        "is not working",
        "cannot",
        "can't",
        "unable",
        "won't",
        "doesn't work",
        "not able",
        "blocked",
        "locked out"
    ]

    has_problem_action = any(
        phrase in text
        for phrase in problem_action_words
    )

    if has_problem_action and (
        "password" in text
        or "account" in text
        or "login" in text
        or "log in" in text
        or "sign in" in text
        or "access" in text
    ):
        return {
            "intent": "account_issue",
            "ticket_required": True,
            "priority": "medium"
        }

    # ==========================================
    # SMART ACCOUNT GUIDANCE DETECTION
    # ==========================================

    account_guidance_words = [
        "password",
        "login",
        "log in",
        "sign in",
        "email"
    ]

    guidance_action_words = [
        "reset",
        "change",
        "update",
        "forgot",
        "recover",
        "how",
        "want to"
    ]

    has_account_guidance_context = any(
        word in text
        for word in account_guidance_words
    )

    has_guidance_action = any(
        word in text
        for word in guidance_action_words
    )

    if (
        has_account_guidance_context
        and has_guidance_action
    ):
        return {
            "intent": "account_guidance",
            "ticket_required": False,
            "priority": "low"
        }
   
    # ==========================================
    # SMART TECHNICAL ISSUE DETECTION
    # ==========================================

    technical_context_words = [
        "website",
        "app",
        "application",
        "page",
        "screen",
        "button",
        "system",
        "server",
        "software",
        "dashboard",
        "platform"
    ]

    technical_problem_words = [
        "not working",
        "isn't working",
        "is not working",
        "doesn't work",
        "not loading",
        "won't load",
        "cannot open",
        "can't open",
        "unable to open",
        "crash",
        "crashed",
        "error",
        "bug",
        "broken",
        "down",
        "slow",
        "freezing",
        "frozen",
        "stuck"
    ]

    has_technical_context = any(
        word in text
        for word in technical_context_words
    )

    has_technical_problem = any(
        phrase in text
        for phrase in technical_problem_words
    )

    if (
        has_technical_context
        and has_technical_problem
    ):
        return {
            "intent": "technical_issue",
            "ticket_required": True,
            "priority": "medium"
        }

    
    # ==========================================
    # LLM FALLBACK
    # ==========================================

    return detect_intent_with_llm(message)
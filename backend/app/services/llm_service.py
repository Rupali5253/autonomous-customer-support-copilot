import os

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()


# ==============================
# Gemini Configuration
# ==============================

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ==============================
# Groq Configuration
# ==============================

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==============================
# Gemini Response
# ==============================

def generate_gemini_response(message: str) -> str:

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            "You are a helpful customer support assistant. "
            "Give a clear, concise and professional response.\n\n"
            f"Customer message: {message}"
        )
    )

    return response.text


# ==============================
# Groq Response
# ==============================

def generate_groq_response(message: str) -> str:

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful customer support assistant. "
                    "Give a clear, concise and professional response."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content


# ==============================
# Main LLM Function
# ==============================

def generate_llm_response(message: str) -> str:

    try:

        # Try Gemini first
        return generate_gemini_response(message)

    except Exception as gemini_error:

        print("Gemini failed. Switching to Groq...")
        print("Gemini error:", gemini_error)

        try:

            # Fallback to Groq
            return generate_groq_response(message)

        except Exception as groq_error:

            print("Groq failed.")
            print("Groq error:", groq_error)

            return (
                "I'm sorry, but I'm currently unable to process "
                "your request. Please try again later."
            )
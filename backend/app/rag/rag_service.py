import os

from dotenv import load_dotenv
from groq import Groq

from app.rag.retriever import retrieve_relevant_chunks


load_dotenv()


# Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)


def generate_rag_response(
    user_query: str,
    top_k: int = 3
) -> str:
    """
    Generate an answer using retrieved
    NovaCart knowledge-base context.
    """

    # Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(
        user_query,
        top_k=top_k
    )

    # If no relevant information is found
    if not relevant_chunks:
        return (
            "I'm sorry, but I couldn't find "
            "relevant information in the NovaCart "
            "knowledge base."
        )

    # Build knowledge-base context
    context_parts = []

    for chunk in relevant_chunks:

        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"Content:\n{chunk['text']}"
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    # System instructions
    system_prompt = """
You are NovaCart's Autonomous Customer Support Copilot.

Your job is to answer customer questions using
ONLY the information provided in the NovaCart
knowledge-base context.

IMPORTANT RULES:

1. Do not invent policies, prices, timelines,
   refunds, delivery dates, or procedures.

2. Use the provided knowledge base as the
   authoritative source.

3. If the required information is not available
   in the context, clearly say that you do not
   have enough information.

4. Give clear, professional and customer-friendly
   responses.

5. Never ask for passwords, OTPs, PINs,
   authentication codes, or confidential credentials.

6. Never request complete payment-card details.

7. Do not promise a refund or order confirmation
   before the required verification.

8. If the customer's issue requires investigation,
   explain the appropriate next step.

9. If a ticket or human investigation is appropriate,
   clearly explain that the case may need support
   investigation.

10. Do not mention that you are using a RAG system,
    embeddings, chunks, or internal implementation.

11. Answer the customer's actual question directly.

12. Keep the answer concise but helpful.
"""

    # User prompt
    user_prompt = f"""
KNOWLEDGE BASE CONTEXT:

{context}


CUSTOMER QUESTION:

{user_query}


Using only the knowledge-base context above,
provide the best possible customer-support response.
"""

    # Generate response using Llama
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=500
    )

    return response.choices[0].message.content


# Test the RAG service directly
if __name__ == "__main__":

    question = input(
        "\nAsk a customer-support question: "
    )

    answer = generate_rag_response(
        question
    )

    print("\n==============================")
    print("RAG RESPONSE")
    print("==============================")

    print(answer)
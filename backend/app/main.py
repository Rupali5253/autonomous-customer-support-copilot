from fastapi import FastAPI, Depends
from app.api import auth, tickets, chat, feedback

app = FastAPI(
    title="Autonomous Customer Support Copilot API",
    description="Backend API for AI-powered customer support system",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(chat.router)
app.include_router(feedback.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Autonomous Customer Support Copilot 🚀"
    }

from fastapi import FastAPI
from models.schemas import QuestionRequest, ChatResponse
from services.rag_service import ask_question
from services.database_service import initialize_database
from services.ticket_service import TicketService

app = FastAPI(title="AI Customer Support Agent")


initialize_database()
TicketService.initialize()

@app.get("/")
def home():
    return {
        "message": "AI Customer Support Agent is running 🚀"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: QuestionRequest):

    result = ask_question(
        session_id=request.session_id,
        question=request.question
    )

    return ChatResponse(
        question=request.question,
        answer=result["answer"],
        sources=result["sources"],
        ticket_created=result["ticket_created"],
        ticket_id=result["ticket_id"],
    )

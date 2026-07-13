from pydantic import BaseModel


class QuestionRequest(BaseModel):
    session_id: str
    question: str


class SourceReference(BaseModel):
    document: str
    page: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceReference]
    ticket_created: bool = False
    ticket_id: int | None = None
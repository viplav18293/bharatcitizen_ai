from pydantic import BaseModel
from typing import List, Optional, Dict

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    language: str = "en"
    session_id: Optional[str] = None

class Source(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    confidence_score: float
    official_portal_link: Optional[str] = None
    suggested_questions: List[str] = []

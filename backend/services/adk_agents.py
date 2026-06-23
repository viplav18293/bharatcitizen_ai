from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from loguru import logger

from core.config import settings
from schemas.chat import ChatResponse, Message
from services import adk_tools
from services.rag_service import rag_service

GoogleAdkAgent = None
if settings.GOOGLE_ADK_ENABLED:
    try:
        from google.adk import Agent as GoogleAdkAgent
    except Exception as exc:
        ADK_IMPORT_ERROR = str(exc)
    else:
        ADK_IMPORT_ERROR = None
else:
    ADK_IMPORT_ERROR = None


@dataclass
class SpecializedAgent:
    name: str
    description: str
    keywords: List[str]

    def matches(self, message: str) -> bool:
        lowered = message.lower()
        return any(keyword in lowered for keyword in self.keywords)


class ConversationMemory:
    def __init__(self) -> None:
        self._store: Dict[str, List[Message]] = {}

    def append(self, session_id: str, user_message: str, assistant_message: str) -> None:
        messages = self._store.setdefault(session_id, [])
        messages.append(Message(role="user", content=user_message))
        messages.append(Message(role="assistant", content=assistant_message))
        self._store[session_id] = messages[-12:]

    def get(self, session_id: str) -> List[Message]:
        return self._store.get(session_id, [])

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": True,
            "type": "in_memory",
            "sessions": len(self._store),
        }


class CitizenAssistantAgent:
    def __init__(self) -> None:
        self.memory = ConversationMemory()
        self.specialized_agents = [
            SpecializedAgent(
                name="Aadhaar Agent",
                description="Aadhaar enrollment, address update, mobile update, and UIDAI procedures.",
                keywords=["aadhaar", "uidai", "enrollment", "address update", "mobile update"],
            ),
            SpecializedAgent(
                name="PAN Agent",
                description="PAN application, corrections, and reprint.",
                keywords=["pan", "incometax", "income tax", "reprint"],
            ),
            SpecializedAgent(
                name="Exam Agent",
                description="NEET, JEE, UPSC and other official exam procedures.",
                keywords=["neet", "jee", "upsc", "exam", "nta"],
            ),
            SpecializedAgent(
                name="Government Schemes Agent",
                description="PM Kisan, Ayushman Bharat, PMAY, Jan Dhan, e-Shram, APY, PM SVANidhi.",
                keywords=[
                    "pm kisan", "ayushman", "pmay", "jan dhan", "e-shram",
                    "apy", "atal pension", "svanidhi", "scheme",
                ],
            ),
            SpecializedAgent(
                name="Rights & Law Agent",
                description="RTI, consumer rights, and labour rights.",
                keywords=["rti", "consumer", "labour", "labor", "rights", "law"],
            ),
            SpecializedAgent(
                name="Retrieval Agent",
                description="Vector search, source retrieval, and citation verification.",
                keywords=["source", "citation", "official", "document", "portal"],
            ),
        ]
        self.adk_agent = self._build_google_adk_agent()

    def _build_google_adk_agent(self) -> Optional[Any]:
        if GoogleAdkAgent is None:
            if ADK_IMPORT_ERROR:
                logger.warning(f"Google ADK unavailable; using compatibility orchestrator: {ADK_IMPORT_ERROR}")
            else:
                logger.warning("Google ADK disabled; using compatibility orchestrator")
            return None
        try:
            return GoogleAdkAgent(
                name="CitizenAssistantAgent",
                model="gemini-flash-latest",
                instruction=(
                    "Route Indian citizen-service questions to specialized tools. "
                    "Use only verified official government sources and preserve citations."
                ),
                tools=[
                    adk_tools.retrieve_documents,
                    adk_tools.search_sources,
                    adk_tools.get_scheme_information,
                    adk_tools.get_exam_information,
                    adk_tools.get_citizen_rights,
                    adk_tools.portal_lookup,
                    adk_tools.citation_validator,
                ],
            )
        except Exception as exc:
            logger.warning(f"Google ADK agent construction failed; compatibility mode active: {exc}")
            return None

    def route(self, message: str) -> SpecializedAgent:
        for agent in self.specialized_agents:
            if agent.matches(message):
                return agent
        return self.specialized_agents[-1]

    def _contextualize(self, message: str, history: List[Message], session_id: str) -> str:
        combined_history = history or self.memory.get(session_id)
        if not combined_history:
            return message
        last_user_turns = [item.content for item in combined_history if item.role == "user"]
        if not last_user_turns:
            return message
        short_follow_up = len(message.split()) <= 7
        if short_follow_up:
            return f"Previous topic: {last_user_turns[-1]}\nFollow-up question: {message}"
        return message

    async def query(
        self,
        message: str,
        history: List[Message],
        language: str = "en",
        session_id: Optional[str] = None,
    ) -> ChatResponse:
        session = session_id or "default"
        routed_agent = self.route(message)
        contextual_message = self._contextualize(message, history, session)
        logger.info(f"CitizenAssistantAgent routed request to {routed_agent.name}")

        response = await rag_service.query(contextual_message, history, language)
        response.sources = adk_tools.validate_response_sources(response.sources)
        if not response.sources:
            response.answer = "No verified information was found from official sources."
            response.confidence_score = 0.0
            response.official_portal_link = adk_tools.portal_lookup(message)

        self.memory.append(session, message, response.answer)
        return response

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "online" if self.adk_agent is not None else "compatibility_mode",
            "framework": "google-adk" if self.adk_agent is not None else "adk-compatible",
            "google_adk_enabled": settings.GOOGLE_ADK_ENABLED,
            "import_error": ADK_IMPORT_ERROR,
            "agent_count": len(self.specialized_agents) + 1,
            "agents": [agent.name for agent in self.specialized_agents] + ["CitizenAssistantAgent"],
            "memory_status": self.memory.status(),
            "tools": [
                "retrieve_documents",
                "search_sources",
                "get_scheme_information",
                "get_exam_information",
                "get_citizen_rights",
                "portal_lookup",
                "citation_validator",
            ],
        }


citizen_assistant_agent = CitizenAssistantAgent()

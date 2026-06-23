import os
import sys
import asyncio

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from schemas.chat import ChatResponse, Source
from services.adk_agents import citizen_assistant_agent


def _official_response(url: str = "https://uidai.gov.in") -> ChatResponse:
    return ChatResponse(
        answer="Official answer with verified citation.",
        sources=[Source(title="Official Source", url=url)],
        confidence_score=0.8,
        official_portal_link=url,
        suggested_questions=[],
    )


@pytest.mark.parametrize(
    ("message", "agent_name"),
    [
        ("How do I update Aadhaar address?", "Aadhaar Agent"),
        ("How do I correct my PAN?", "PAN Agent"),
        ("What is the NEET application process?", "Exam Agent"),
        ("Tell me PM Kisan eligibility", "Government Schemes Agent"),
        ("How do I file RTI?", "Rights & Law Agent"),
    ],
)
def test_specialized_agents_route_and_preserve_official_citations(monkeypatch, message, agent_name):
    async def fake_query(query, history, language):
        return _official_response()

    monkeypatch.setattr("services.adk_agents.rag_service.query", fake_query)

    assert citizen_assistant_agent.route(message).name == agent_name
    response = asyncio.run(
        citizen_assistant_agent.query(message, [], "en", session_id=f"test-{agent_name}")
    )

    assert response.answer == "Official answer with verified citation."
    assert response.sources
    assert response.sources[0].url == "https://uidai.gov.in"


def test_agent_rejects_unofficial_citations_and_avoids_hallucination(monkeypatch):
    async def fake_query(query, history, language):
        return _official_response("https://example.com/aadhaar")

    monkeypatch.setattr("services.adk_agents.rag_service.query", fake_query)

    response = asyncio.run(
        citizen_assistant_agent.query(
            "How do I apply for Aadhaar?",
            [],
            "en",
            session_id="test-unofficial",
        )
    )

    assert response.answer == "No verified information was found from official sources."
    assert response.sources == []
    assert response.confidence_score == 0.0


def test_agent_memory_contextualizes_follow_up(monkeypatch):
    seen_queries = []

    async def fake_query(query, history, language):
        seen_queries.append(query)
        return _official_response()

    monkeypatch.setattr("services.adk_agents.rag_service.query", fake_query)

    asyncio.run(
        citizen_assistant_agent.query(
            "How do I apply for Aadhaar?", [], "en", session_id="test-memory"
        )
    )
    asyncio.run(
        citizen_assistant_agent.query("What documents?", [], "en", session_id="test-memory")
    )

    assert "Previous topic: How do I apply for Aadhaar?" in seen_queries[-1]
    assert "Follow-up question: What documents?" in seen_queries[-1]

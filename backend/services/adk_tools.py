from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from loguru import logger

from schemas.chat import Source
from services.rag_service import OFFICIAL_DOMAINS, rag_service


PORTAL_REGISTRY = {
    "aadhaar": "https://uidai.gov.in",
    "uidai": "https://uidai.gov.in",
    "pan": "https://www.incometax.gov.in",
    "voter": "https://eci.gov.in",
    "passport": "https://passportindia.gov.in",
    "driving license": "https://parivahan.gov.in",
    "digilocker": "https://digilocker.gov.in",
    "neet": "https://nta.ac.in",
    "jee": "https://nta.ac.in",
    "nta": "https://nta.ac.in",
    "upsc": "https://upsc.gov.in",
    "pm kisan": "https://pmkisan.gov.in",
    "ayushman bharat": "https://nha.gov.in",
    "pmay": "https://pmaymis.gov.in",
    "rti": "https://rtionline.gov.in",
    "india code": "https://indiacode.nic.in",
    "labour rights": "https://labour.gov.in",
}


def _is_allowed_url(url: Optional[str]) -> bool:
    if not url:
        return False
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.netloc.lower()
    return any(host == domain or host.endswith(f".{domain}") for domain in OFFICIAL_DOMAINS)


def citation_validator(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only citations from the official source registry."""
    validated = []
    for source in sources:
        url = source.get("url")
        if _is_allowed_url(url):
            validated.append(source)
        else:
            logger.warning(f"ADK citation validator rejected source: {url}")
    return validated


def retrieve_documents(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Use the existing LangChain/vector DB RAG service for retrieval."""
    documents = rag_service.retrieve_documents(query, k=k)
    return citation_validator([
        {
            "title": item["title"],
            "url": item["url"],
            "snippet": item["snippet"],
            "score": item["score"],
        }
        for item in documents
    ])


def search_sources(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Search official source chunks through the existing vector store."""
    return retrieve_documents(query, k=k)


def portal_lookup(topic: str) -> Optional[str]:
    topic_lower = topic.lower()
    for key, url in PORTAL_REGISTRY.items():
        if key in topic_lower and _is_allowed_url(url):
            return url
    return None


def get_scheme_information(scheme_name: str) -> Dict[str, Any]:
    query = f"government scheme {scheme_name} eligibility application benefits official portal"
    return {
        "portal": portal_lookup(scheme_name),
        "documents": retrieve_documents(query),
    }


def get_exam_information(exam_name: str) -> Dict[str, Any]:
    query = f"{exam_name} exam official notification eligibility application dates"
    return {
        "portal": portal_lookup(exam_name),
        "documents": retrieve_documents(query),
    }


def get_citizen_rights(topic: str) -> Dict[str, Any]:
    query = f"{topic} rights law official government procedure"
    return {
        "portal": portal_lookup(topic),
        "documents": retrieve_documents(query),
    }


def validate_response_sources(sources: List[Source]) -> List[Source]:
    return [
        source
        for source in sources
        if _is_allowed_url(source.url)
    ]

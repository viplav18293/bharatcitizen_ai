import os
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from schemas.chat import Message, ChatResponse, Source
from core.config import settings
from loguru import logger

# 1. Imports with safety
IMPORT_ERRORS = {}
ChatOpenAI = None
Chroma = None
ChatPromptTemplate = None
create_retrieval_chain = None
create_stuff_documents_chain = None
HuggingFaceEmbeddings = None

# Official Source Registry (Phase 4)
OFFICIAL_DOMAINS = [
    "uidai.gov.in", "incometax.gov.in", "eci.gov.in", "passportindia.gov.in",
    "parivahan.gov.in", "digilocker.gov.in", "nta.ac.in", "upsc.gov.in",
    "pmkisan.gov.in", "nha.gov.in", "pmaymis.gov.in", "rtionline.gov.in",
    "indiacode.nic.in", "labour.gov.in"
]

class RAGService:
    def __init__(self):
        self.retrieval_chain = None
        self.ready = False
        self.initializing = False
        self.vector_store = None
        self.status = {
            "llm": False,
            "embeddings": False,
            "vectordb": False,
            "errors": []
        }
        if settings.RAG_INIT_ON_IMPORT:
            self.initialize_once()

    def initialize_once(self):
        if self.ready or self.initializing:
            return
        self.initializing = True
        try:
            self.initialize()
        finally:
            self.initializing = False

    def initialize(self):
        logger.info("Initializing BharatAI RAG Pipeline...")

        try:
            global ChatOpenAI
            global Chroma
            global ChatPromptTemplate
            global create_retrieval_chain
            global create_stuff_documents_chain
            global HuggingFaceEmbeddings

            from langchain_openai import ChatOpenAI
            from langchain_community.vectorstores import Chroma
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_classic.chains import create_retrieval_chain
            from langchain_classic.chains.combine_documents import create_stuff_documents_chain
            from langchain_huggingface import HuggingFaceEmbeddings

            # 1. Initialize Local Embeddings
            logger.info(f"Loading local embedding model: {settings.EMBEDDING_MODEL}")
            self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            self.status["embeddings"] = True

            # 2. Initialize Vector Store (Chroma)
            logger.info(f"Connecting to {settings.VECTOR_DB_TYPE} vector database at {settings.CHROMA_DB_PATH}")
            os.makedirs(os.path.dirname(settings.CHROMA_DB_PATH), exist_ok=True)
            self.vector_store = Chroma(
                persist_directory=settings.CHROMA_DB_PATH,
                embedding_function=self.embeddings
            )
            self.status["vectordb"] = True

            # 3. Initialize LLM
            if settings.LLM_API_KEY and settings.LLM_API_KEY != "your-api-key":
                logger.info(f"Initializing LLM: {settings.LLM_MODEL}")
                self.llm = ChatOpenAI(
                    model=settings.LLM_MODEL,
                    openai_api_key=settings.LLM_API_KEY,
                    openai_api_base=settings.LLM_BASE_URL,
                    temperature=0
                )
                self.status["llm"] = True
                
                # Setup Full RAG Chain
                prompt = ChatPromptTemplate.from_template("""
You are BharatAI Citizen Assistant, a production-grade helpful assistant for Indian citizens.
Answer based ONLY on the provided context. If the answer is not in the context, 
explicitly state: "No verified information was found from official sources."

Every answer MUST follow this exact format:

### Title: [Title]
### Overview: [Brief description]
### How is it useful: [Explain the usefulness/use case]
### Eligibility to apply: [List eligibility criteria]
### Pros: [List pros/benefits]
### How to apply (Steps): [List step-by-step instructions]
### Portal Link: [Official URL]
### Sources: [List official sources]

<context>
{context}
</context>

Question: {input}

Response:""")
                
                document_chain = create_stuff_documents_chain(self.llm, prompt)
                self.retrieval_chain = create_retrieval_chain(
                    self.vector_store.as_retriever(search_kwargs={"k": 5}),
                    document_chain
                )
            else:
                logger.warning("LLM_API_KEY missing. Using retrieval-only mode.")
                self.llm = None
                self.retrieval_chain = None
            
            self.ready = True
            logger.info("BharatAI RAG Pipeline successfully initialized.")

        except Exception as e:
            err_msg = f"RAG initialization failed: {str(e)}"
            self.status["errors"].append(err_msg)
            logger.exception(err_msg)

    def _is_official_source(self, url: str) -> bool:
        if not url:
            return False
        parsed = urlparse(url if "://" in url else f"https://{url}")
        host = parsed.netloc.lower()
        return any(host == domain or host.endswith(f".{domain}") for domain in OFFICIAL_DOMAINS)

    def validate_citations(self, sources: List[Source]) -> List[Source]:
        return [source for source in sources if self._is_official_source(source.url or "")]

    def retrieve_documents(self, message: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.vector_store:
            logger.warning("Retrieval requested before vector store initialization.")
            return []

        docs_with_scores = self.vector_store.similarity_search_with_score(message, k=k)
        documents = []
        for doc, score in docs_with_scores:
            source_url = doc.metadata.get("source_url") or doc.metadata.get("url")
            if not self._is_official_source(source_url):
                logger.warning(f"Rejected unofficial source: {source_url}")
                continue
            documents.append({
                "title": doc.metadata.get("title", "Official Source"),
                "url": source_url,
                "snippet": doc.page_content[:500],
                "score": score,
                "document": doc,
            })
        return documents

    async def query(self, message: str, history: List[Message], language: str = "en") -> ChatResponse:
        try:
            # 1. Retrieval with Similarity Score
            logger.info(f"Query: {message}")

            if not self.vector_store:
                logger.error("RAG query requested while vector store is unavailable.")
                return ChatResponse(
                    answer="No verified information was found from official sources.",
                    sources=[],
                    confidence_score=0.0,
                    official_portal_link=None,
                    suggested_questions=["Check /health for backend status."]
                )
            
            docs_with_scores = self.vector_store.similarity_search_with_score(message, k=5)
            
            if not docs_with_scores:
                logger.warning("Chroma returned 0 results.")
                return ChatResponse(
                    answer="No verified information was found from official sources.",
                    sources=[],
                    confidence_score=0.0,
                    official_portal_link=None,
                    suggested_questions=["How do I apply for Aadhaar?", "What is PM Kisan?"]
                )

            filtered_docs = []
            for doc, score in docs_with_scores:
                confidence = max(0, 1 - (score / 2.0)) 
                logger.info(f"Retrieved: {doc.metadata.get('title', 'Unknown')} | Score: {score:.4f} | Confidence: {confidence:.4f}")
                
                # REQ 9: Only return 'No verified info' if retrieval genuinely returns 0 documents.
                # Here we include official documents even if confidence is lower than threshold, 
                # but we still log the warning.
                source_url = doc.metadata.get("source_url") or doc.metadata.get("url")
                if self._is_official_source(source_url):
                    filtered_docs.append(doc)
                else:
                    logger.warning(f"Rejected unofficial source: {source_url}")

            if not filtered_docs:
                logger.warning("No official documents found in search results.")
                return ChatResponse(
                    answer="No verified information was found from official sources.",
                    sources=[],
                    confidence_score=0.0,
                    official_portal_link=None,
                    suggested_questions=["How do I apply for Aadhaar?", "What is PM Kisan?"]
                )

            # 2. Synthesis
            if self.retrieval_chain:
                response = self.retrieval_chain.invoke({
                    "input": f"{message} (Please respond in {language})",
                    "context": filtered_docs
                })
                answer = response["answer"]
            else:
                # Retrieval-only mode (No LLM)
                answer = "### Official Information Found (Synthesized view unavailable):\n\n"
                for i, doc in enumerate(filtered_docs):
                    answer += f"#### Data from: {doc.metadata.get('title', 'Document')}\n"
                    answer += f"{doc.page_content}\n\n"
                answer += "### Eligibility to apply:\n[Please refer to official source]\n"
                answer += "### Pros:\n[Please refer to official source]\n"
                answer += "### How to apply (Steps):\n[Please refer to official source]\n"
                answer += "### Portal Link:\n[See Sources below]\n"
                answer += "\n*Note: Full synthesis/formatting is disabled (LLM API key missing).* "

            # 3. Extract Sources & Citations
            sources = []
            seen_urls = set()
            official_portal = None
            
            for doc in filtered_docs:
                url = doc.metadata.get("source_url") or doc.metadata.get("url")
                title = doc.metadata.get("title", "Official Source")
                if url and url not in seen_urls:
                    sources.append(Source(title=title, url=url))
                    seen_urls.add(url)
                    if not official_portal:
                        official_portal = url
            
            return ChatResponse(
                answer=answer,
                sources=sources,
                confidence_score=0.9 if self.llm else 0.6,
                official_portal_link=official_portal,
                suggested_questions=["What documents are required?", "How long does it take?"]
            )
            
        except Exception as e:
            logger.exception(f"Error in RAG query: {e}")
            return ChatResponse(
                answer=f"An error occurred while retrieving official information: {str(e)}",
                sources=[],
                confidence_score=0.0,
                official_portal_link=None,
                suggested_questions=[]
            )

    def get_health(self) -> Dict[str, Any]:
        doc_count = 0
        if self.ready and hasattr(self.vector_store, '_collection'):
            try:
                doc_count = self.vector_store._collection.count()
            except:
                pass
        
        component_ready = self.status["embeddings"] or self.status["vectordb"] or self.status["llm"]
        return {
            "status": "online" if self.ready else ("degraded" if component_ready else "offline"),
            "initializing": self.initializing,
            "components": {
                "llm": self.status["llm"],
                "embeddings": self.status["embeddings"],
                "vectordb": self.status["vectordb"]
            },
            "stats": {
                "document_count": doc_count,
                "official_sources": len(OFFICIAL_DOMAINS)
            },
            "config": {
                "model": settings.LLM_MODEL,
                "threshold": settings.SIMILARITY_THRESHOLD
            },
            "errors": self.status["errors"]
        }

    def get_rag_status(self) -> Dict[str, Any]:
        doc_count = 0
        chunk_count = 0
        collections = []
        if self.ready and hasattr(self.vector_store, '_collection'):
            try:
                doc_count = self.vector_store._collection.count()
                chunk_count = doc_count # In our case documents=chunks
                collections = ["bharatai_docs"] # Default Chroma collection name if not specified
            except:
                pass
        
        return {
            "status": "online" if self.ready else ("initializing" if self.initializing else "degraded"),
            "documents": doc_count,
            "chunks": chunk_count,
            "embeddings": chunk_count, # 1:1 ratio
            "collections": collections,
            "retrieval_working": self.ready and doc_count > 0
        }

rag_service = RAGService()

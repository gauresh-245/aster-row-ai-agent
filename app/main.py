from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.document_loader import load_documents
from app.chunker import create_all_chunks
from app.vector_store import VectorStore
from app.agent import ask_agent
from app.memory import ConversationMemory


app = FastAPI(
    title="Aster & Row AI Customer Service",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# LOAD KNOWLEDGE BASE ON STARTUP
# --------------------------------------------------

documents = load_documents("knowledge-base")

chunks = create_all_chunks(documents)

store = VectorStore()
store.build(chunks)


# --------------------------------------------------
# SESSION-SCOPED MEMORY
# --------------------------------------------------
# Each session_id gets its own isolated ConversationMemory.
# This is in-memory only (process-lifetime), which is acceptable
# for this assignment's scope, but must not be a single shared
# instance — otherwise unrelated conversations bleed into each
# other's context.

session_memories: dict[str, ConversationMemory] = {}


def get_memory(session_id: str) -> ConversationMemory:
    if session_id not in session_memories:
        session_memories[session_id] = ConversationMemory()
    return session_memories[session_id]


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Aster & Row AI Customer Service",
    }


# --------------------------------------------------
# CHAT
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    memory = get_memory(request.session_id)

    answer = ask_agent(
        question=request.message,
        store=store,
        memory=memory,
    )

    return {
        "answer": answer,
    }
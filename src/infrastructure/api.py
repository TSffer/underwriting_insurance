from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add src to path if needed, though usually python path logic handles this better.
# Assuming this is run from project root, importing from src.infrastructure should work.
# Relative import since we are in the same package:
from infrastructure.advanced_broker_vehicular import (
    clasificar_intencion,
    preparar_rag,
    manejar_saludo,
    manejar_emergencia,
)

from contextlib import asynccontextmanager

# Prepare RAG chain on startup to avoid reloading it on every request
# Note: This might take a moment on startup.
check_rag_chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global check_rag_chain
    try:
        check_rag_chain = preparar_rag()
    except Exception as e:
        print(f"Warning: Failed to initialize RAG chain: {e}")
    yield
    # Clean up resources if needed

app = FastAPI(
    title="Insurance Broker API",
    description="API for the AI-powered Insurance Broker Assistant. Supports intention classification and RAG-based policy queries.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    intention: str
    response: str

@app.post("/chat", response_model=ChatResponse, tags=["Chat"], summary="Process user query")
async def chat_endpoint(request: ChatRequest):
    query = request.query
    
    try:
        # Step 1: Detect Intention
        # Note: calling OpenAI here might fail due to quota, handled by try-except
        intencion = clasificar_intencion(query)
    except Exception as e:
        # Fallback or error reporting
        # If rate limited, we might not assume intencion
        raise HTTPException(status_code=503, detail=f"Error classifying intention (likely upstream API error): {str(e)}")

    response_text = ""
    
    # Step 2: Route logic
    if intencion == "SALUDO":
        response_text = manejar_saludo()
    elif intencion == "EMERGENCIA":
        response_text = manejar_emergencia()
    elif intencion == "CONSULTA":
        if check_rag_chain:
            try:
                res = check_rag_chain.invoke({"query": query})
                response_text = res['result']
            except Exception as e:
                raise HTTPException(status_code=503, detail=f"RAG Error: {str(e)}")
        else:
            response_text = "Error: Políticas no cargadas o error en inicialización."
    else:
        response_text = "No estoy seguro de cómo ayudarte con eso. Intenta preguntar sobre seguros."

    return ChatResponse(intention=intencion, response=response_text)

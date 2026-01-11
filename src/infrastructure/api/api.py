from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
import sys

import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.agent import get_agent_executor
from src.core.auth import create_user, DB_PATH

app = FastAPI(
    title="Insurance Copilot API",
    description="API for the AI-powered Insurance Copilot. Supports complex comparisons and RAG.",
    version="0.2.0"
)



class ChatRequest(BaseModel):
    query: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str = "ejecutivo"


class ChatResponse(BaseModel):
    response: str
    data: dict = {}


@app.post("/users", status_code=status.HTTP_201_CREATED, summary="Crear un nuevo usuario")
async def create_user_endpoint(request: CreateUserRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT 1 FROM users WHERE username = ?", (request.username,))
        if c.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="Username already exists")
            
        create_user(c, request.username, request.password, request.role)
        conn.commit()
        conn.close()
        
        return {"message": f"User '{request.username}' created successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse, summary="Procesar consulta del usuario con el Agente")
async def chat_endpoint(request: ChatRequest):
    try:
        agent = get_agent_executor()
        result = agent.invoke({"messages": [{"role": "user", "content": request.query}]})
        output = result["messages"][-1].content

        data = {}
        if isinstance(output, dict):
            data = output
            response_text = "Comparativo generado exitosamente."
        else:
            response_text = str(output)

        return ChatResponse(response=response_text, data=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

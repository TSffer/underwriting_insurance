from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.core.database import get_vectorstore
import json


class ComparisonInput(BaseModel):
    feature: str = Field(description="La característica a comparar (ej: 'Cobertura de robo', 'Deducible').")
    insurers: List[str] = Field(description="Lista de aseguradoras a comparar (ej: ['RIMAC', 'MAPFRE']).")


@tool("compare_policies", args_schema=ComparisonInput)
def compare_policies(feature: str, insurers: List[str]):
    """
    Compara una característica específica entre varias aseguradoras.
    Devuelve un JSON con la comparación detallada.
    """
    vectorstore = get_vectorstore()
    results = {}

    # 1. Búsqueda por cada aseguradora
    for insurer in insurers:
        insurer_key = insurer.upper()

        docs = vectorstore.similarity_search(
            feature,
            k=5,
            filter={"insurer": insurer_key}
        )

        context = "\n".join([d.page_content for d in docs])
        results[insurer_key] = context

    # 2. Generación del comparativo con LLM
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    prompt_template = """
    Eres un experto en seguros. Tu tarea es extraer y comparar la característica '{feature}' para las siguientes aseguradoras basándote en su contexto.

    {context_json}

    Devuelve un JSON con este formato exacto:
    {{
        "feature": "{feature}",
        "comparison": [
            {{
                "insurer": "NOMBRE_ASEGURADORA",
                "value": "Resumen del valor/condición (max 20 palabras)",
                "details": "Detalle técnico o cláusula completa",
                "source": "Referencia de página o documento"
            }},
            ...
        ]
    }}

    Si no encuentras información para una aseguradora, pon "No especificado" en value.
    """

    # Preparar contexto para el prompt
    context_str = ""
    for ins, txt in results.items():
        context_str += f"--- CONTEXTO {ins} ---\n{txt}\n\n"

    prompt = PromptTemplate(template=prompt_template, input_variables=["feature", "context_json"])
    chain = prompt | llm | JsonOutputParser()

    try:
        response = chain.invoke({"feature": feature, "context_json": context_str})
        return response
    except Exception as e:
        return {"error": str(e)}

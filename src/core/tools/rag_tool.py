from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.core.database import get_vectorstore


def format_docs(docs):
    formatted = []
    for doc in docs:
        source = doc.metadata.get("insurer", "Desconocido")
        page = doc.metadata.get("page", "?")
        formatted.append(f"--- FUENTE: {source} (Pág {page}) ---\n{doc.page_content}")
    return "\n\n".join(formatted)


@tool("consult_policy")
def consult_policy(query: str):
    """
    Responde consultas generales sobre pólizas de seguros buscando en toda la base de conocimiento.
    Úsalo para preguntas como '¿Qué es el deducible?', '¿Cubre daños por lluvia?', etc.
    """
    vectorstore = get_vectorstore()
    
    # 1. Recuperación inicial
    initial_docs = vectorstore.similarity_search(query, k=15)
    
    if not initial_docs:
        return "No se ha encontrado información relevante sobre tu consulta en la documentación disponible."
    
    # 2. Reranking Estrategia
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    rerank_template = """
    Como experto en seguros, evalúa la relevancia de los siguientes fragmentos para responder a la pregunta: "{question}"
    
    Devuelve ÚNICAMENTE los índices de los 5 fragmentos más útiles, separados por comas (ej: 0,3,4,1,2).
    
    Fragmentos:
    {fragments}
    """
    
    fragments_str = "\n".join([f"[{i}] {d.page_content[:200]}..." for i, d in enumerate(initial_docs)])
    rerank_prompt = rerank_template.format(question=query, fragments=fragments_str)
    
    try:
        rerank_response = llm.invoke(rerank_prompt).content
        indices = [int(i.strip()) for i in rerank_response.split(",") if i.strip().isdigit()]
        reranked_docs = [initial_docs[i] for i in indices if i < len(initial_docs)][:5]
    except:
        reranked_docs = initial_docs[:5]

    template = """Eres un asistente experto en seguros. Genera una respuesta estructurada basándote ÚNICAMENTE en el contexto proporcionado.

    Usa el siguiente formato Markdown para tu respuesta:

    ### 📋 Resumen
    (Una síntesis directa de la respuesta en 2-4 frases)

    ### 📝 Detalles
    (Explicación completa utilizando viñetas para coberturas, condiciones o exclusiones)

    ### 📂 Fuentes Referenciadas
    (Lista explícita de los documentos y páginas citados, ej: 'Rimac Vehicular (Pág 12)')

    ---
    Contexto:
    {context}

    Pregunta: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    context_text = format_docs(reranked_docs)
    
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"context": context_text, "question": query})
    
    return result

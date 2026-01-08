import os
import sys
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 1. CONFIGURACIÓN ---
load_dotenv()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    # Remove surrounding quotes and whitespace (fixes common Docker --env-file issues)
    api_key = api_key.strip().strip("'").strip('"')
    os.environ["OPENAI_API_KEY"] = api_key
else:
    # Warning instead of exit to allow imports in CI/CD or tests
    print("⚠️  Advertencia: OPENAI_API_KEY no encontrada. Algunas funciones fallarán.")



# --- 2. PREPARACIÓN DE LA BASE DE CONOCIMIENTO (RAG) ---
# Esta parte es igual, carga los PDFs de seguros para cuando sea necesario comparar
def preparar_rag():
    # Define base path relative to this file or project root
    # Assuming 'data' needs to be found relative to the project root
    # We will try to locate the 'data' directory
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/infrastructure
    project_root = os.path.dirname(os.path.dirname(current_dir)) # underwriting_insurance
    data_dir = os.path.join(project_root, "data")
    
    if not os.path.exists(data_dir):
         # Fallback for docker or other structures if needed
         data_dir = "data"

    archivos_polizas = [
        os.path.join(data_dir, "Interseguro Vehicular.pdf"),
        os.path.join(data_dir, "La Positiva Vehicular.pdf"),
        os.path.join(data_dir, "Mapfre Vehicular.pdf"),
        os.path.join(data_dir, "Pacifico Vehicular.pdf"),
        os.path.join(data_dir, "Rimac Vehicular.pdf"),
    ]

    docs = []
    print("\n⚙️  Inicializando sistema: Cargando pólizas...")
    for archivo in archivos_polizas:
        if os.path.exists(archivo):
            loader = PyPDFLoader(archivo)
            d = loader.load()
            for doc in d:
                doc.metadata["source"] = os.path.basename(archivo).replace(".pdf", "")
            docs.extend(d)

    if not docs:
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Prompt específico para cuando el experto es el "Comparador"
    template_rag = """
    Eres un analista experto en seguros. Comparas condiciones basándote SOLO en el contexto:
    {context}
    
    Pregunta: {question}
    
    Si comparas, usa una tabla Markdown. Sé breve y directo.
    """
    prompt_rag = PromptTemplate(
        template=template_rag, input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": prompt_rag},
    )


# --- 3. EL CLASIFICADOR DE INTENCIONES (ROUTER) ---
def clasificar_intencion(pregunta):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    template_router = """
    Tu única tarea es clasificar la intención del usuario en una de estas categorías:
    
    1. SALUDO: Si el usuario saluda, se despide o agradece.
    2. EMERGENCIA: Si el usuario menciona un choque, robo, accidente, auxilio mecánico o siniestro en curso.
    3. CONSULTA: Si el usuario pregunta sobre coberturas, precios, deducibles, comparaciones o cláusulas de las pólizas.
    
    Pregunta del usuario: "{question}"
    
    Responde SOLO con una palabra: SALUDO, EMERGENCIA o CONSULTA.
    """

    prompt = PromptTemplate(template=template_router, input_variables=["question"])
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"question": pregunta}).strip().upper()


# --- 4. MANEJADORES DE INTENCIÓN (HANDLERS) ---


def manejar_emergencia():
    return """
    🚨 **MODO EMERGENCIA ACTIVADO** 🚨
    
    Si estás en un lugar seguro, comunícate inmediatamente con la central de emergencias de tu aseguradora:
    
    - **Rimac:** (01) 411-1111
    - **Pacífico:** (01) 415-1515
    - **Mapfre:** (01) 213-3333
    - **La Positiva:** (01) 211-0212
    - **Interseguro:** (01) 500-0000
    
    ⚠️ No abandones el vehículo ni aceptes responsabilidad hasta que llegue el procurador.
    """


def manejar_saludo():
    return "¡Hola! Soy tu Copiloto de Seguros. Puedo ayudarte a **comparar pólizas**, revisar **coberturas** o guiarte en caso de **emergencia**. ¿En qué te ayudo hoy?"


# --- 5. BUCLE PRINCIPAL ---

if __name__ == "__main__":
    rag_chain = preparar_rag()
    print("\n" + "=" * 50)
    print("🤖 BROKER INTELIGENTE (Con Detección de Intenciones)")
    print("Intenta decir: 'Hola', 'Choqué mi auto' o 'Compara Rimac y Pacífico'")
    print("=" * 50 + "\n")

    while True:
        query = input("Usuario: ")
        if query.lower() in ["salir", "exit"]:
            break

        # PASO 1: Detectar Intención
        intencion = clasificar_intencion(query)
        print(f"   [🧠 Intención detectada: {intencion}]")

        # PASO 2: Enrutar a la función correcta
        if intencion == "SALUDO":
            print(f"Bot: {manejar_saludo()}\n")

        elif intencion == "EMERGENCIA":
            # Aquí aplicamos una "regla" hardcoded, no gastamos tokens de RAG
            print(f"Bot: {manejar_emergencia()}\n")

        elif intencion == "CONSULTA":
            # Aquí sí usamos el sistema pesado de IA (RAG)
            if rag_chain:
                print("Bot: Analizando documentos...", end="\r")
                try:
                    res = rag_chain.invoke({"query": query})
                    print(f"Bot:\n{res['result']}\n")
                except Exception as e:
                    print(f"Error en RAG: {e}")
            else:
                print("Error: No se cargaron las pólizas para responder consultas.")

        else:
            print(
                "Bot: No estoy seguro de cómo ayudarte con eso. Intenta preguntar sobre seguros.\n"
            )

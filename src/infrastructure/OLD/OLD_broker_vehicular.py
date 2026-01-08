import os
import sys
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- CONFIGURACIÓN ---
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: Configura tu OPENAI_API_KEY en el archivo .env")
    sys.exit(1)


# --- CARGA DE PÓLIZAS VEHICULARES ---
def cargar_documentos():
    # Lista exacta de los archivos que subiste
    archivos_polizas = [
        "Interseguro Vehicular.pdf",
        "La Positiva Vehicular.pdf",
        "Mapfre Vehicular.pdf",
        "Pacifico Vehicular.pdf",
        "Rimac Vehicular.pdf",
    ]

    todos_los_docs = []

    print("\n1️⃣  Leyendo pólizas vehiculares del mercado...")
    for archivo in archivos_polizas:
        if os.path.exists(archivo):
            print(f"   -> Procesando: {archivo}...")
            loader = PyPDFLoader(archivo)
            docs = loader.load()
            # Añadimos metadata para que el bot sepa de qué aseguradora habla
            for d in docs:
                d.metadata["source"] = archivo.replace(".pdf", "")
            todos_los_docs.extend(docs)
        else:
            print(f"   ⚠️ Advertencia: No encontré '{archivo}'. Saltando...")

    if not todos_los_docs:
        print(
            "❌ Error: No se cargó ninguna póliza. Verifica que los PDFs estén en la carpeta."
        )
        sys.exit(1)

    return todos_los_docs


# --- PROCESAMIENTO ---
docs = cargar_documentos()

# Chunking: Usamos un tamaño un poco mayor para capturar tablas de cobertura completas
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

print(f"2️⃣  Indexando {len(chunks)} fragmentos de condiciones vehiculares...")
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# --- EL CEREBRO DEL BROKER (PROMPT VEHICULAR) ---
template_broker = """
Eres un Asistente Broker de Seguros Vehiculares experto.
Tu objetivo es ayudar a comparar las condiciones de diferentes aseguradoras (Interseguro, Rimac, Pacifico, Mapfre, La Positiva).

Usa el siguiente contexto recuperado de las pólizas reales para responder.
SI EL USUARIO PIDE UNA COMPARACIÓN: Genera una tabla Markdown clara.
Si la información no está explícita en el texto, indica "No especificado en el documento".

Contexto recuperado:
{context}

Pregunta del Cliente: {question}

Instrucciones de formato:
- Si comparas costos o coberturas, usa una tabla.
- Sé conciso con los deducibles (copagos).
- Identifica siempre la aseguradora.

Respuesta del Broker:
"""

PROMPT = PromptTemplate(
    template=template_broker, input_variables=["context", "question"]
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 6}
    ),  # Buscamos más fragmentos para cubrir las 5 marcas
    chain_type_kwargs={"prompt": PROMPT},
)

# --- INTERFAZ ---
print("\n" + "=" * 60)
print("🚗 BROKER COPILOT - MÓDULO VEHICULAR")
print("Pólizas activas: Interseguro, La Positiva, Mapfre, Pacífico, Rimac")
print("=" * 60 + "\n")

while True:
    query = input("\nConsulta del Cliente: ")
    if query.lower() in ["salir", "exit"]:
        break

    print("🔍 Analizando condicionados...", end="\r")
    try:
        res = qa_chain.invoke({"query": query})
        print(f"\nResultados:\n{res['result']}\n")
        print("-" * 60)
    except Exception as e:
        print(f"Error: {e}")

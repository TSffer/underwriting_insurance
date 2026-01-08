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

# --- 1. CONFIGURACIÓN ---
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: Configura tu OPENAI_API_KEY en el archivo .env")
    sys.exit(1)


# --- 2. CARGA DE MÚLTIPLES PÓLIZAS ---
def cargar_documentos():
    archivos = ["poliza_basica.pdf", "poliza_premium.pdf"]
    todos_los_docs = []

    print("\n1️⃣  Leyendo pólizas de las aseguradoras...")
    for archivo in archivos:
        if os.path.exists(archivo):
            loader = PyPDFLoader(archivo)
            docs = loader.load()
            # Agregamos metadata para saber de qué póliza viene cada texto
            for d in docs:
                d.metadata["source"] = archivo
            todos_los_docs.extend(docs)
            print(f"   -> Cargada: {archivo}")
        else:
            print(
                f"   ⚠️ Falta el archivo {archivo}. Ejecuta generar_polizas.py primero."
            )
            sys.exit(1)
    return todos_los_docs


# --- 3. PROCESAMIENTO E INDEXACIÓN ---
docs = cargar_documentos()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)

print(f"2️⃣  Indexando {len(chunks)} fragmentos de información en la Base de Datos...")
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# --- 4. EL CEREBRO DEL BROKER (PROMPT ENGINEERING) ---
# Aquí definimos la personalidad del bot para que haga tablas comparativas
template_broker = """
Eres un Asistente Broker de Seguros experto. Tu trabajo es ayudar a los clientes a comparar pólizas.

Usa los siguientes fragmentos de contexto (que provienen de diferentes pólizas) para responder la consulta.
Si el usuario pide comparar, DEBES generar una tabla comparativa o una lista estructurada clara.
Identifica siempre de qué compañía (archivo) proviene la información.

Contexto:
{context}

Pregunta del Usuario: {question}

Respuesta (formato Broker):
"""

PROMPT = PromptTemplate(
    template=template_broker, input_variables=["context", "question"]
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 5}
    ),  # Traemos más contexto (k=5) para poder comparar
    chain_type_kwargs={"prompt": PROMPT},
)

# --- 5. INTERFAZ DE CHAT ---
print("\n" + "=" * 50)
print("👔 ASISTENTE BROKER ACTIVO")
print("Tengo las pólizas de 'Seguros El Ahorro' y 'Elite Global' cargadas.")
print("Pídeme que las compare según tus necesidades.")
print("=" * 50 + "\n")

while True:
    query = input("Cliente: ")
    if query.lower() in ["salir", "exit"]:
        break

    print("Broker IA: Analizando pólizas...", end="\r")
    try:
        res = qa_chain.invoke({"query": query})
        print(f"\nBroker IA:\n{res['result']}\n")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")

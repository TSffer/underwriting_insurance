import os
import sys
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.core.database import get_vectorstore, PERSIST_DIRECTORY

load_dotenv()

def ingest_documents(reprocess=False):
    """
    Escanea la carpeta data/ buscando PDFs en subcarpetas, los fragmenta y los guarda en ChromaDB.
    """
    # Configuración de rutas
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data"
    
    # Obtener vectorstore
    vectorstore = get_vectorstore()
    
    # Verificar si ya hay documentos (evitar duplicados)
    if not reprocess:
        existing_count = len(vectorstore.get()['ids'])
        if existing_count > 0:
            print(f"ℹ️  La base de datos ya contiene {existing_count} fragmentos. Saltando ingesta.")
            return vectorstore

    if reprocess:
        print("⚠️  Reprocesando: Limpiando base de datos vectorial...")
        # Si PERSIST_DIRECTORY existe, borramos los archivos
        if os.path.exists(PERSIST_DIRECTORY):
            print(f"🗑️  Borrando persistencia en {PERSIST_DIRECTORY}")
            import shutil
            shutil.rmtree(PERSIST_DIRECTORY)
            os.makedirs(PERSIST_DIRECTORY)
        # Re-instanciar después de borrar
        vectorstore = get_vectorstore()

    # Escaneo recursivo
    all_docs = []
    print(f"📂 Escaneando documentos en {data_dir}...")
    
    # Extensiones a buscar
    for pdf_path in data_dir.rglob("*.pdf"):
        # Ignorar si está en chroma_db
        if "chroma_db" in str(pdf_path):
            continue
            
        insurer_name = pdf_path.parent.name.upper()
        print(f"📄 Cargando: {pdf_path.name} (Aseguradora: {insurer_name})")
        
        try:
            loader = PyPDFLoader(str(pdf_path))
            docs = loader.load()
            
            for doc in docs:
                doc.metadata["insurer"] = insurer_name
                doc.metadata["source"] = pdf_path.name
                
            all_docs.extend(docs)
        except Exception as e:
            print(f"❌ Error cargando {pdf_path.name}: {e}")

    if not all_docs:
        print("⚠️  No se encontraron nuevos documentos para indexar.")
        return vectorstore

    # Fragmentación
    print(f"✂️  Fragmentando {len(all_docs)} páginas...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_docs)

    # Almacenamiento
    print(f"💾 Guardando {len(chunks)} fragmentos en ChromaDB...")
    vectorstore.add_documents(chunks)
    
    print("✅ Ingesta completada exitosamente.")
    return vectorstore

if __name__ == "__main__":
    # Reprocesar enviar --reprocess
    force_reprocess = "--reprocess" in sys.argv
    ingest_documents(reprocess=force_reprocess)

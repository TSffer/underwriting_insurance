import streamlit as st
import os
import sys

# Ensure src/infrastructure is in sys.path to allow imports if running from root
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from advanced_broker_vehicular import preparar_rag, clasificar_intencion, manejar_saludo, manejar_emergencia

# Page configuration
st.set_page_config(page_title="Copiloto de Seguros", page_icon="🚗", layout="centered")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    with st.spinner("Inicializando sistema de seguros..."):
        st.session_state.rag_chain = preparar_rag()

# Sidebar
st.sidebar.title("🚗 Copiloto de Seguros")
st.sidebar.markdown("""
Asistente inteligente para consultas sobre seguros vehiculares.
- **Consultas**: Pregunta por coberturas, precios, etc.
- **Emergencias**: Reporta siniestros.
- **Comparaciones**: Compara aseguradoras.
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 1. Classify intention
        intencion = clasificar_intencion(prompt)
        
        response_text = ""
        
        if intencion == "SALUDO":
            response_text = manejar_saludo()
        
        elif intencion == "EMERGENCIA":
            response_text = manejar_emergencia()
            
        elif intencion == "CONSULTA":
            if st.session_state.rag_chain:
                message_placeholder.markdown("🔍 Analizando pólizas...")
                try:
                    res = st.session_state.rag_chain.invoke({"query": prompt})
                    response_text = res['result']
                except Exception as e:
                    response_text = f"Error al consultar la base de conocimiento: {str(e)}"
            else:
                response_text = "⚠️ El sistema de consultas no está disponible (PDFs no cargados)."
        
        else:
            response_text = "No estoy seguro de cómo ayudarte con eso. Intenta preguntar sobre seguros, emergencias o salúdame."

        message_placeholder.markdown(response_text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})

import streamlit as st
import sys
import os
import json
import pandas as pd
from dotenv import load_dotenv
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.auth import verify_user, init_db, create_user
from src.core.agent import get_agent_executor
from src.core.prompts import INSURANCE_COPILOT_PROMPT
from src.core.security import check_input, check_output, get_random_response, SemanticSecurity
from src.core.chitchat import SemanticRouter

load_dotenv()

# Inicializar DB
if "db_init" not in st.session_state:
    init_db()
    st.session_state.db_init = True

st.set_page_config(page_title="Copiloto de Seguros Vehiculares", page_icon="🛡️", layout="wide")

# --- ESTILOS ---
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* --- VARIABLES --- */
        :root {
            --primary: #2563EB;
            --bg-body: #F8FAFC;
            --text-main: #0F172A;
            --input-border: #94A3B8; 
        }

        /* --- GLOBAL --- */
        html, body, .stApp {
            background-color: var(--bg-body);
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }

        /* --- HEADER Y SIDEBAR --- */
        header[data-testid="stHeader"] {
            background-color: transparent;
        }
        
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        /* --- INPUTS GENERALES (Login y Textos) --- */
        .stTextInput input, .stPasswordInput input {
            background-color: #FFFFFF !important; 
            border: 1px solid var(--input-border) !important; 
            border-radius: 8px !important;
            color: #1E293B !important;
            padding: 10px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        /* Efecto al hacer clic en el input */
        .stTextInput input:focus, .stPasswordInput input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
        }

        /* --- CHAT INPUT (La barra de abajo) --- */
        .stChatInput {
            padding-bottom: 2rem;
        }
        
        /* Caja del input del chat */
        div[data-testid="stChatInput"] {
            background-color: #FFFFFF !important; 
            border: 2px solid #CBD5E1 !important; 
            border-radius: 30px !important; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important; 
            padding: 5px !important;
        }

        /* Efecto focus en el chat */
        div[data-testid="stChatInput"]:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
        }

        /* --- CHAT MESSAGES --- */
        [data-testid="stChatMessage"] {
            padding: 1.5rem;
            border-radius: 12px;
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }

        /* Mensaje Usuario */
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
            background-color: #EFF6FF; 
            border: 1px solid #BFDBFE;
        }
        
        /* Avatares */
        [data-testid="chatAvatarIcon-user"] { background-color: var(--primary); color: white; }
        [data-testid="chatAvatarIcon-assistant"] { background-color: #10B981; color: white; }

        /* --- LOGIN CARD --- */
        .login-card {
            background: white;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            border: 1px solid #E2E8F0;
            text-align: center;
        }
        
        /* Botones */
        .stButton button {
            background-color: var(--primary);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        .stButton button:hover {
            background-color: #1D4ED8; 
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
        }

        /* Ocultar elementos extra */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
def login_page():
    load_css()

    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h1>🛡️</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-bottom: 0.5rem;'>Bienvenido</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; margin-bottom: 2rem;'>Accede al Copiloto de Seguros Vehiculares</p>", unsafe_allow_html=True)

        username = st.text_input("Usuario", placeholder="admin", label_visibility="collapsed")
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        password = st.text_input("Contraseña", type="password", placeholder="••••••••", label_visibility="collapsed")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        
        if st.button("Ingresar al Sistema"):
            valid, role = verify_user(username, password)
            if valid:
                st.session_state.user = username
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Credenciales inválidas")

        st.markdown("<p style='margin-top: 1rem; font-weight: bold; font-size: 1rem; color: #94A3B8;'>Demo: admin / admin123</p>", unsafe_allow_html=True)

# --- DASHBOARD ---
def main_page():
    load_css()
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; padding: 1rem 0;">
            <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);">
                {st.session_state.user[0].upper()}
            </div>
            <div style="font-weight: 600; font-size: 1.1rem; color: #0F172A;">{st.session_state.user}</div>
            <div style="font-size: 0.8rem; color: #64748B; background: #F1F5F9; padding: 2px 8px; border-radius: 4px; margin-top: 4px;">{st.session_state.role}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🧭 Navegación")
        st.info("Estas conversando con el **Agente Técnico** de pólizas vehiculares.")
        st.info("""
        Este asistente tiene acceso a:
        - 📄 Pólizas Vehiculares
        - ⚖️ Comparador de caracteristicas
        """)
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            del st.session_state.user
            st.rerun()

    # HEADER PRINCIPAL
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin-bottom: 0;">🚗 Copiloto de <span style="color: #2563EB;">Seguros Vehiculares</span></h1>
        <p style="color: #64748B; font-size: 1.1rem; margin-top: 0.5rem;">
            Asistente inteligente para análisis y comparación de pólizas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # HISTORIAL DE CHAT
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome_msg = "Hola. Soy tu copiloto. ¿Necesitas comparar cotizaciones o buscar una cláusula específica?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], dict) and "comparison" in msg["content"]:
                render_comparison(msg["content"])
            else:
                st.markdown(msg["content"])

    # LOGICA DEL CHAT
    if prompt := st.chat_input("Escribe tu consulta sobre seguros aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            prompt_lower = prompt.lower().strip()
            saludos = ["hola", "buenos dias", "buenas"]

            if any(prompt_lower.startswith(s) for s in saludos) and len(prompt_lower.split()) < 4:
                response_text = "¡Hola! Estoy listo para ayudarte. ¿Qué póliza revisamos hoy?"
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            else:
                # --- SEGURIDAD INPUT ---
                # Validacion por palabras clave
                is_blocked, phrase = check_input(prompt)
                
                # Validacion semantica
                if not is_blocked:
                    if "semantic_security" not in st.session_state:
                         with st.spinner("Inicializando seguridad..."):
                            st.session_state.semantic_security = SemanticSecurity()
                    
                    is_blocked, phrase, score = st.session_state.semantic_security.check_semantic_similarity(prompt)
                
                #Interacciones comunes
                chitchat_response = None
                if not is_blocked:
                    if "semantic_chitchat" not in st.session_state:
                        st.session_state.semantic_chitchat = SemanticRouter()
                    
                    intent, score = st.session_state.semantic_chitchat.detect_intent(prompt)
                    if intent:
                        chitchat_response = st.session_state.semantic_chitchat.get_response(intent)

                if is_blocked:
                     response_text = get_random_response()
                     st.warning(f"Consulta bloqueada por seguridad. Tema detectado: {phrase}")
                     st.session_state.messages.append({"role": "assistant", "content": response_text})
                     st.markdown(response_text)
                
                elif chitchat_response:
                    st.session_state.messages.append({"role": "assistant", "content": chitchat_response})
                    st.markdown(chitchat_response)

                else:
                    with st.spinner("Analizando..."):
                        try:
                            agent = get_agent_executor()
                            system_prompt = INSURANCE_COPILOT_PROMPT
                            langchain_messages = [system_prompt]
                            
                            for m in st.session_state.messages[-4:]:
                                content = json.dumps(m["content"]) if isinstance(m["content"], dict) else m["content"]
                                langchain_messages.append((m["role"], content))

                            response = agent.invoke({"messages": langchain_messages})
                            output = response['messages'][-1].content
                            
                            # --- SEGURIDAD OUTPUT ---
                            is_blocked_out, phrase_out = check_output(output)
                            if is_blocked_out:
                                final_output = get_random_response()
                                st.warning(f"Respuesta bloqueada. Contenido no permitido detectado.")
                            else:
                                final_output = output

                            is_json = False
                            if not is_blocked_out:
                                try:
                                    json_match = re.search(r'\{[\s\S]*\}', final_output)
                                    if json_match:
                                        parsed = json.loads(json_match.group(0))
                                        if "comparison" in parsed:
                                            final_output = parsed
                                            is_json = True
                                except: pass

                            if is_json:
                                render_comparison(final_output)
                            else:
                                st.markdown(str(final_output))

                            st.session_state.messages.append({"role": "assistant", "content": final_output})

                        except Exception as e:
                            st.error(f"Error: {e}")

def render_comparison(data):
    feature = data.get("feature", "Comparativo")
    st.markdown(f"""
    <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; margin-top: 10px;">
        <h4 style="color: #1E3A8A; margin-top: 0;">📊 {feature}</h4>
    """, unsafe_allow_html=True)

    items = data.get("comparison", [])
    df_data = [{
        "Aseguradora": i.get("insurer"), 
        "Detalle": i.get("value"), 
        "Fuente": i.get("source")
    } for i in items]

    st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)

    with st.expander("Ver Cláusulas Completas"):
        for item in items:
            st.markdown(f"**{item.get('insurer')}**: {item.get('details')}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- APP START ---
if "user" not in st.session_state:
    login_page()
else:
    main_page()
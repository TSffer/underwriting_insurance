import random
import numpy as np
import os
import pickle
from langchain_openai import OpenAIEmbeddings

# --- CONFIGURACIÓN DE INTENCIONES ---
INTENT_COMMONS = {
    "greeting": [
        "hola", "buenos dias", "buenas tardes", "buenas noches", 
        "que tal", "como estas", "hl", "hi", "hello", "buen dia",
    ],
    "farewell": [
        "adios", "chau", "hasta luego", "nos vemos", 
        "bye", "hasta pronto", "cerrar", "me voy"
    ],
    "thanks": [
        "gracias", "muchas gracias", "te agradezco", 
        "ok gracias", "vale gracias", "thx"
    ],
    "capabilities": [
        "que puedes hacer", "para que sirves", "quien eres",
        "ayuda", "que sabes hacer", "cuales son tus funciones"
    ]
}

# Respuestas aleatorias
INTENT_RESPONSES = {
    "greeting": [
        "¡Hola! Soy tu Copiloto de Seguros. ¿En qué puedo ayudarte hoy?",
        "¡Buenos días! Estoy listo para revisar pólizas contigo.",
        "¡Hola! ¿Necesitas comparar alguna cotización o revisar coberturas?",
        "Bienvenido. Soy el asistente experto en seguros. Cuéntame qué necesitas."
    ],
    "farewell": [
        "¡Hasta luego! Si tienes más dudas sobre seguros, aquí estaré.",
        "Nos vemos. ¡Que tengas un excelente día!",
        "Adiós. Recuerda revisar bien las cláusulas importantes.",
        "¡Hasta pronto! Cierra sesión si estás en un equipo compartido."
    ],
    "thanks": [
        "¡De nada! Es un placer ayudarte.",
        "Para eso estamos. ¿Alguna otra consulta?",
        "Con gusto. Avisame si necesitas algo más.",
        "No hay de qué."
    ],
    "capabilities": [
        "Soy un agente experto en seguros vehiculares. Puedo:\n1. 🔍 Buscar información en tus pólizas.\n2. ⚖️ Comparar cotizaciones de diferentes aseguradoras.\n3. 🛡️ Explicarte coberturas y exclusiones.",
        "Estoy entrenado para asistir a suscriptores. Mi especialidad es analizar documentos de seguros y darte respuestas precisas y comparativas.",
        "Puedo leer tus PDFs de pólizas, extraer datos clave y generar tablas comparativas para que tomes mejores decisiones."
    ]
}


class SemanticRouter:
    def __init__(self, threshold: float = 0.85, cache_file: str = "chitchat_embeddings.pkl"):
        """
        Enrutador semántico para conversaciones casuales.
        """
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.threshold = threshold
        self.cache_path = os.path.join(os.path.dirname(__file__), cache_file)
        
        self.intent_map = []
        self.corpus_texts = []
        
        for intent, examples in INTENT_COMMONS.items():
            for text in examples:
                self.corpus_texts.append(text)
                self.intent_map.append(intent)
        
        self.intent_vectors = self._load_or_generate_embeddings()

    def _embed_list(self, texts: list[str]) -> list[list[float]]:
        if not texts: return []
        return self.embeddings.embed_documents(texts)

    def _load_or_generate_embeddings(self) -> list[list[float]]:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error cargando cache chitchat: {e}")
        
        print("Generando embeddings de Chitchat...")
        vectors = self._embed_list(self.corpus_texts)
        
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(vectors, f)
        except: pass
            
        return vectors

    def detect_intent(self, text: str) -> tuple[str | None, float]:
        """
        Detecta la intención del texto. 
        Retorna (intent_name, score) o (None, 0.0) si no supera el umbral.
        """
        query_vec = self.embeddings.embed_query(text)
        
        vec_a = np.array(query_vec)
        norm_a = np.linalg.norm(vec_a)
        if norm_a == 0: return None, 0.0
        
        best_score = -1.0
        best_intent = None
        
        for i, target_vec in enumerate(self.intent_vectors):
            vec_b = np.array(target_vec)
            norm_b = np.linalg.norm(vec_b)
            if norm_b == 0: continue
            
            cosine_sim = np.dot(vec_a, vec_b) / (norm_a * norm_b)
            
            if cosine_sim > best_score:
                best_score = cosine_sim
                best_intent = self.intent_map[i]
        
        if best_score >= self.threshold:
            return best_intent, float(best_score)
            
        return None, 0.0

    def get_response(self, intent: str) -> str:
        """Retorna una respuesta aleatoria para la intención dada."""
        return random.choice(INTENT_RESPONSES.get(intent, ["Hola."]))

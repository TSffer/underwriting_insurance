# Proyecto: Asistente de Seguros (Underwriting Insurance App)

## Planteamiento del Problema

### Negocio
El sector de seguros enfrenta desafíos operativos relacionados con la gestión eficiente de la información y la atención al cliente, específicamente en la oferta corporativa y la consulta de pólizas.

### Objetivos
1.  **Gestionar oferta corporativa:** Administrar eficientemente planes, coberturas y pricing.
2.  **Automatizar consultas:** Facilitar la consulta automatizada de información de pólizas de seguros para reducir tiempos de respuesta.
3.  **Mejorar acceso a información:** Solucionar la dificultad y el tiempo excesivo que toma recuperar y juntar información relevante atrapada en documentos no estructurados (PDFs).

### Hipótesis
La implementación de un asistente virtual inteligente (Chatbot), capaz de clasificar intenciones de usuario y extraer información de fuentes estructuradas y no estructuradas, optimizará la recuperación de datos, reduciendo el tiempo de atención al cliente y mejorando la precisión en la gestión de ofertas corporativas.

### Acciones con Entregables
*   Implementación de módulos para consulta de reglas de negocio.
*   Creación de una interfaz o API para interactuar con el asistente.
*   Documentación de análisis y reporte de resultados.

---

## Acceso a Datos

### Tipo de Datos
*   **Estructurados:**
    *   Información transaccional simulada (bases de datos de clientes, estados de pólizas).
*   **No Estructurados:**
    *   Documentos de pólizas y condiciones generales en formato PDF (fuente de información para consultas complejas).

---

## Tipo de Solución a Elaborar

Se desarrollará una solución basada en **Inteligencia Artificial y Automatización** que consiste en:

1.  **Chatbot de Asistencia (Agente Inteligente):**
    *   **Arquitectura RAG (Retrieval-Augmented Generation):** Integración con **ChromaDB** para la búsqueda vectorial de documentos (pólizas en PDF) y recuperación de información precisa.
    *   **Motor de Reranking:** Estrategia avanzada para filtrar y ordenar los fragmentos de documentos más relevantes antes de generar la respuesta.
    *   **Lógica de Negocio:** Agente Orquestador (`agent.py`) que decide cuándo consultar la base de conocimientos o utilizar herramientas de comparación.

2.  **Infraestructura de Datos:**
    *   **Base de Datos Vectorial:** Almacenamiento persistente de embeddings en ChromaDB, con ingesta automática y recursiva de documentos.
    *   **Base de Datos Relacional:** Gestión de usuarios y roles mediante SQLite.

---

## Cronograma de Trabajo

| Fase | Actividad | Descripción |
| :--- | :--- | :--- |
| **1** | **Planteamiento y Diseño** | Definición del alcance, objetivos y arquitectura de la solución. (Completado) |
| **2** | **Acceso y Preparación de Datos** | Generación de datasets sintéticos y configuración de acceso a documentos. |
| **3** | **Desarrollo de Modelos** | Entrenamiento del modelo de clasificación de intenciones y ajuste de reglas. |
| **4** | **Implementación de Lógica** | Desarrollo del `core` del chatbot y funciones de `infrastructure` (pagos, cotizaciones, etc.). |
| **5** | **Integración y Pruebas** | Unificación de componentes en el flujo principal (`main.py`) y validación de casos de uso. |
| **6** |
### 6. Documentación y Entrega
Finalización del README y reporte de resultados.

---

## 🚀 Guía de Inicio Rápido

Sigue estos pasos para levantar el proyecto desde cero.

### 1. Preparar el Entorno
Asegúrate de tener Python 3.12+ y `uv` instalado.

```bash
# 1. Clonar repositorio
git clone <url-del-repo>
cd underwriting_insurance

# 2. Instalar dependencias
uv sync
```

### 2. Configuración
Crea un archivo `.env` en la raíz (puedes copiar el ejemplo si existe) con tu clave de OpenAI:

```ini
OPENAI_API_KEY=sk-tu-clave-aqui
```

### 3. Ingesta de Documentos (Solo la primera vez)
Carga y vectoriza los PDFs de las aseguradoras en la base de datos ChromaDB.

```bash
# Ejecutar ingesta inicial
uv run python src/infrastructure/ingest.py

# Recargar todo desde cero:
uv run python src/infrastructure/ingest.py --reprocess
```

### 4. Ejecutar la Aplicación Web (Streamlit)
```bash
uv run streamlit run src/interface/app.py
```
Accede a `http://localhost:8501`. Usuario por defecto: `admin` / `admin123`.

---

## 🔌 Documentación de API

El sistema expone una API REST para integraciones.

**Ejecutar Servidor API:**
```bash
uv run uvicorn src.infrastructure.api.api:app --reload
```

### Endpoints Principales

#### 1. Crear Usuario (`POST /users`)
Registra nuevos usuarios ejecutivos en el sistema.

**Request (HTTP):**
```http
POST /users HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "username": "nuevo_usuario",
    "password": "mi_password_seguro",
    "role": "ejecutivo"
}
```

**Comando cURL:**
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"username": "jdoe", "password": "secretops", "role": "analista"}'
```

#### 2. Chat con Agente (`POST /chat`)
Envía consultas al copiloto de seguros.

**Request (HTTP):**
```http
POST /chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "query": "¿Qué cubre el seguro Rimac Vehicular?"
}
```

**Comando cURL:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "Compara el deducible de Rimac y Pacífico"}'
```
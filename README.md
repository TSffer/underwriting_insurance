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
*   Desarrollo de un pipeline de clasificación de intenciones (NLP).
*   Implementación de módulos para consulta de reglas de negocio y precios.
*   Creación de una interfaz o API para interactuar con el asistente.
*   Documentó de análisis y reporte de resultados.

---

## Acceso a Datos

### Tipo de Datos
*   **Estructurados:**
    *   Información transaccional simulada (bases de datos de clientes, estados de pólizas, historial de pagos).
    *   Reglas de negocio definidas en código (pricing, coberturas).
    *   Datasets sintéticos para entrenamiento del modelo de clasificación (`crear_dataset_rules`).
*   **No Estructurados:**
    *   Documentos de pólizas y condiciones generales en formato PDF (fuente de información para consultas complejas).

---

## Tipo de Solución a Elaborar

Se desarrollará una solución basada en **Inteligencia Artificial y Automatización** que consiste en:

1.  **Chatbot de Asistencia:**
    *   Modelo de Machine Learning (Pipeline `TfidfVectorizer` + `RandomForestClassifier`) para entender la intención del usuario (ej. cotizar, consultar pagos, reportar emergencias).
    *   Lógica de negocio (`core.py` e `infrastructure`) para ejecutar acciones específicas basadas en la intención detectada.

2.  **Infraestructura de Datos:**
    *   Integración de reglas de negocio para validar coberturas y calcular precios.
    *   Simulación de consultas a sistemas externos (bancos, bases de datos de pólizas).

---

## Cronograma de Trabajo

| Fase | Actividad | Descripción |
| :--- | :--- | :--- |
| **1** | **Planteamiento y Diseño** | Definición del alcance, objetivos y arquitectura de la solución. (Completado) |
| **2** | **Acceso y Preparación de Datos** | Generación de datasets sintéticos y configuración de acceso a documentos. |
| **3** | **Desarrollo de Modelos** | Entrenamiento del modelo de clasificación de intenciones y ajuste de reglas. |
| **4** | **Implementación de Lógica** | Desarrollo del `core` del chatbot y funciones de `infrastructure` (pagos, cotizaciones, etc.). |
| **5** | **Integración y Pruebas** | Unificación de componentes en el flujo principal (`main.py`) y validación de casos de uso. |
| **6** | **Documentación y Entrega** | Finalización del README y reporte de resultados. |
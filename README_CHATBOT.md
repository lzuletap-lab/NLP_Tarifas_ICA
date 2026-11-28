# 🤖 Chatbot RAG para Consulta de Tarifas del Impuesto ICA

Este Chatbot es un asistente conversacional basado en **RAG (Retrieval-Augmented Generation)** y un **workflow híbrido** para consultar en tiempo real las tarifas del Impuesto de Industria y Comercio (ICA) en Colombia a partir de tablas estructuradas extraídas de estatutos tributarios municipales.

Este repositorio corresponde al módulo independiente de consulta (`Chatbot_ICA_RAG.ipynb`), desacoplado del pipeline de extracción de PDFs (`Proyecto tarifas del impuesto ICA.ipynb`).

---

## 🗺️ Arquitectura del Sistema

1. **Ingesta de datos:** Carga un archivo `tarifas_ica.csv` con las columnas `Municipio`, `CIIU`, `Actividad` y `Tarifa` (incluye un dataset de prueba de San Vicente Ferrer y Bogotá si no se carga un archivo propio) y exporta la base normalizada en formato `.csv`.
2. **Embeddings y Vector Store:** Convierte cada registro en texto descriptivo con metadatos utilizando `sentence-transformers/all-MiniLM-L6-v2` y los indexa en memoria con **FAISS** (`k=4`).
3. **Workflow Híbrido (Determinista + Semántico):**
   - **Ruta 1 (Filtro exacto):** Detecta códigos CIIU de 4 dígitos mediante expresiones regulares y filtra por municipio si se menciona en la consulta.
   - **Ruta 2 (Búsqueda semántica RAG):** Si no hay código CIIU explícito, recupera los documentos más similares desde FAISS.
4. **Generación (LLM local):** Utiliza `TinyLlama/TinyLlama-1.1B-Chat-v1.0` a través de `transformers` y `langchain-huggingface` (`temperature=0.2`, `max_new_tokens=200`).
5. **Interfaz Web:** Despliega un chat interactivo mediante **Gradio** (`gr.ChatInterface`).

---

## ⚙️ Requisitos

- **Python:** `>=3.10, <3.13`
- **Hardware recomendado:** GPU NVIDIA (en Google Colab, activar **GPU T4** en *Entorno de ejecución → Cambiar tipo de entorno de ejecución*). En CPU funciona automáticamente en `float32`, aunque con mayor latencia.

---

## 🚀 Instalación y Ejecución

### Opción A: Google Colab (Recomendada)
1. Abre `Chatbot_ICA_RAG.ipynb` en Google Colab.
2. Activa la aceleración por hardware **GPU T4**.
3. En la celda de carga de datos, ajusta `SUBIR_CSV_PROPIO = True` si deseas subir tu propio `tarifas_ica.csv` (o déjalo en `False` para usar los datos de prueba).
4. Ejecuta todas las celdas en orden (`Entorno de ejecución → Ejecutar todas`).

### Opción B: Entorno local con Poetry
1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/chatbot-ica-rag.git](https://github.com/tu-usuario/chatbot-ica-rag.git)
   cd chatbot-ica-rag

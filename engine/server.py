# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
ArchivaIA · INACAP Sede Maipú
API Backend FastAPI – Motor RAG y Asistente NAPI
"""

import os
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from google import genai
from google.genai import types as genai_types
from supabase import create_client, Client

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ArchivaIA-API")

GEMINI_API_KEY       = os.environ["GEMINI_API_KEY"]
SUPABASE_URL         = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
SUPABASE_ANON_KEY    = os.environ["SUPABASE_ANON_KEY"]

# Clientes
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
db_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
db_anon: Client  = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMS  = 1536

app = FastAPI(title="ArchivaIA RAG API", version="1.0.0")

# Permitir CORS total para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────
# MODELOS PYDANTIC
# ──────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    query: str
    umbral: Optional[float] = 0.50
    limite: Optional[int] = 5
    carrera: Optional[str] = None

class ProjectCreateRequest(BaseModel):
    titulo: str
    resumen: str
    carrera: str
    anio: int
    autores: str

# ──────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────
def get_query_embedding(texto: str) -> list:
    texto_limpio = texto.strip().replace("\n", " ")
    res = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texto_limpio,
        config=genai_types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMS
        )
    )
    return list(res.embeddings[0].values)

def get_doc_embedding(texto: str) -> list:
    texto_limpio = texto.strip().replace("\n", " ")
    res = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texto_limpio,
        config=genai_types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMS
        )
    )
    return list(res.embeddings[0].values)

# ──────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Servir archivos estáticos del frontend (css, js, img)
css_dir = os.path.join(BASE_DIR, "css")
js_dir = os.path.join(BASE_DIR, "js")
img_dir = os.path.join(BASE_DIR, "img")

if os.path.exists(css_dir):
    app.mount("/css", StaticFiles(directory=css_dir), name="css")
if os.path.exists(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")
if os.path.exists(img_dir):
    app.mount("/img", StaticFiles(directory=img_dir), name="img")

@app.get("/")
def serve_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "ArchivaIA RAG Engine", "sede": "INACAP Maipú"}

@app.get("/api/projects")
def get_projects():
    """Obtiene todos los proyectos registrados en Supabase."""
    try:
        response = db_anon.table("proyectos_titulo").select("id, titulo, resumen, carrera, anio, autores, created_at").order("anio", desc=True).execute()
        return {"projects": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects")
def create_project(data: ProjectCreateRequest):
    """Inserta un nuevo proyecto calculando automáticamente su vector de embedding."""
    try:
        texto_completo = f"{data.titulo}. {data.resumen}"
        embedding = get_doc_embedding(texto_completo)

        payload = {
            "titulo": data.titulo,
            "resumen": data.resumen,
            "carrera": data.carrera,
            "anio": data.anio,
            "autores": data.autores,
            "embedding": embedding
        }

        res = db_admin.table("proyectos_titulo").insert(payload).execute()
        return {"success": True, "project": res.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
def analyze_project(req: AnalyzeRequest):
    """
    Motor RAG: Realiza búsqueda semántica vía RPC en Supabase
    y genera el diagnóstico interactivo de NAPI con Gemini 3.6 Flash.
    """
    try:
        # 1. Generar embedding de consulta
        emb = get_query_embedding(req.query)

        # 2. Consultar RPC en Supabase
        rpc_params = {
            "query_embedding": emb,
            "match_threshold": req.umbral,
            "match_count": req.limite,
            "filtro_carrera": req.carrera
        }
        res = db_anon.rpc("buscar_proyectos_similares", rpc_params).execute()
        similares = res.data or []

        for s in similares:
            s["porcentaje_similitud"] = round(s["similitud"] * 100, 2)

        # 3. Determinar riesgo
        top_similitud = similares[0]["porcentaje_similitud"] if similares else 0.0
        if top_similitud >= 85:
            nivel_riesgo = "CRÍTICO"
        elif top_similitud >= 70:
            nivel_riesgo = "ALTO"
        elif top_similitud >= 50:
            nivel_riesgo = "MODERADO"
        else:
            nivel_riesgo = "SIN RIESGO"

        # 4. Formatear contexto RAG
        if not similares:
            contexto = f"## Proyecto del estudiante\n{req.query}\n\n## Resultado RAG\nNo se encontraron proyectos con similitud suficiente en la base de datos."
        else:
            items_txt = "\n\n".join([
                f"**Proyecto {i+1}** ({s['porcentaje_similitud']}% similitud)\n"
                f"- Título: {s['titulo']}\n"
                f"- Carrera: {s['carrera']} ({s['anio']})\n"
                f"- Autores: {s['autores']}\n"
                f"- Resumen: {s['resumen']}"
                for i, s in enumerate(similares)
            ])
            contexto = f"## Proyecto del estudiante\n{req.query}\n\n## Proyectos Similares en Repositorio\n{items_txt}"

        # 5. Generar diagnóstico NAPI con Gemini (con fallback automático a otros modelos disponibles)
        SYSTEM_PROMPT = """Eres NAPI (Navegador de Antecedentes de Proyectos Innovadores), el asistente de inteligencia artificial de ArchivaIA para INACAP Sede Maipú.

Tu misión es brindar un análisis preventivo de choque de ideas entre el proyecto nuevo del estudiante y los proyectos históricos encontrados por el motor RAG.

Debes estructurar tu respuesta con:
1. 📊 **Diagnóstico de Originalidad**: Menciona el nivel de riesgo detectado y el porcentaje máximo de similitud.
2. 🔍 **Análisis de Similitud**: Explica en 2 párrafos qué elementos o tecnologías coinciden.
3. ⚠️ **Zonas de Choque de Ideas**: Puntos específicos donde hay solapamiento.
4. 🚀 **Recomendaciones de Innovación**: Entre 3 y 4 sugerencias concretas con tecnologías modernas para que el estudiante diferencie su propuesta.
5. 💪 **Próximo Paso**: Una recomendación constructiva para su anteproyecto.

Sé motivador, empático, directo y utiliza formato Markdown claro y profesional."""

        analisis_texto = ""
        candidatos = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-pro"]

        for mod in candidatos:
            try:
                gemini_response = gemini_client.models.generate_content(
                    model=mod,
                    contents=f"{SYSTEM_PROMPT}\n\n---\n\n{contexto}",
                    config=genai_types.GenerateContentConfig(
                        temperature=0.4,
                        max_output_tokens=1500
                    )
                )
                analisis_texto = gemini_response.text
                if analisis_texto:
                    log.info(f"Diagnóstico generado exitosamente con modelo {mod}")
                    break
            except Exception as ex:
                log.warning(f"Modelo {mod} ocupado o no disponible ({ex}), probando siguiente...")

        # Si todos los modelos de generación externa tienen sobrecarga temporal, generar resumen analítico
        if not analisis_texto:
            if similares:
                top = similares[0]
                analisis_texto = f"""## 📊 Diagnóstico de Originalidad\n\n* **Nivel de riesgo:** **{nivel_riesgo} ({top_similitud}%)**\n* **Proyecto más coincidente:** *"{top['titulo']}"* ({top['carrera']} · {top['anio']})\n\n## 🔍 Análisis de Similitud\n\nSe detectó una proximidad semántica del **{top_similitud}%** con proyectos previos del repositorio de la sede. El enfoque y problemática planteados comparten componentes clave con trabajos anteriores.\n\n## 🚀 Recomendaciones de Innovación\n\n- Incorpora capas de analítica predictiva o visión artificial para diferenciar el alcance.\n- Considera un stack moderno o protocolos de comunicación en tiempo real (MQTT, WebSockets, gRPC).\n- Enfoca la validación en un caso de uso específico no cubierto por proyectos previos.\n\n## 💪 Próximo Paso\n\nRevisa la ficha técnica del proyecto similar para identificar sus limitaciones y plantear tu propuesta de valor única."""
            else:
                analisis_texto = "## 📊 Diagnóstico de Originalidad\n\n* **Nivel de riesgo:** **SIN RIESGO (0%)**\n\n🎉 ¡No se detectaron proyectos con alta similitud en la base de datos! Tu idea presenta un excelente nivel de originalidad para tu trabajo de título en INACAP Sede Maipú."

        return {
            "query": req.query,
            "top_similitud": top_similitud,
            "nivel_riesgo": nivel_riesgo,
            "similares": similares,
            "analisis": analisis_texto
        }

    except Exception as e:
        log.error(f"Error en /api/analyze: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)

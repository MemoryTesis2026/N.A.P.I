# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
ArchivaIA - INACAP Sede Maipu
Motor RAG - Fase 1 v3: Google Gemini SDK nuevo (google-genai)
=============================================================
Dependencias:
    pip install google-genai supabase python-dotenv openai

Variables de entorno (.env):
    GEMINI_API_KEY=AQ...          <- Google AI Studio (gratis)
    OPENAI_API_KEY=sk-...         <- Solo para NAPI chat (fallback a Gemini si no hay creditos)
    SUPABASE_URL=https://xxx.supabase.co
    SUPABASE_SERVICE_KEY=eyJ...
    SUPABASE_ANON_KEY=eyJ...
"""

import os
import logging
import time
from typing import Optional
from dotenv import load_dotenv

# Nuevo SDK de Google Gemini (reemplaza google-generativeai)
from google import genai
from google.genai import types as genai_types

from openai import OpenAI
from supabase import create_client, Client

# ─────────────────────────────────────────────────────────────
# Configuracion
# ─────────────────────────────────────────────────────────────
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("ArchivaIA")

GEMINI_API_KEY       = os.environ["GEMINI_API_KEY"]
OPENAI_API_KEY       = os.environ["OPENAI_API_KEY"]
SUPABASE_URL         = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
SUPABASE_ANON_KEY    = os.environ["SUPABASE_ANON_KEY"]

# Inicializar cliente Gemini (nuevo SDK)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

EMBEDDING_MODEL = "gemini-embedding-2"   # truncado a 1536 dims (max HNSW = 2000)
EMBEDDING_DIMS  = 1536


class ArchivaIAEngine:
    """Motor RAG para busqueda semantica de proyectos de titulo INACAP."""

    def __init__(self):
        self.openai: OpenAI   = OpenAI(api_key=OPENAI_API_KEY)
        self.db_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        self.db: Client       = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        log.info("ArchivaIA Engine v3 (Gemini google-genai) inicializado.")

    # ─────────────────────────────────────────
    # A. Embedding con nuevo SDK google-genai
    # ─────────────────────────────────────────
    def generar_embedding(self, texto: str) -> list:
        """Genera vector de 768 dims con Google text-embedding-004 (gratis)."""
        texto_limpio = texto.strip().replace("\n", " ")
        log.info(f"Generando embedding para: '{texto_limpio[:60]}...'")

        result = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texto_limpio,
            config=genai_types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=EMBEDDING_DIMS   # truncar a 1536 (bajo el limite HNSW)
            )
        )

        embedding = result.embeddings[0].values
        log.info(f"Embedding generado: {len(embedding)} dimensiones [OK]")
        return list(embedding)

    def generar_embedding_consulta(self, texto: str) -> list:
        """Genera embedding para texto de consulta (RETRIEVAL_QUERY)."""
        texto_limpio = texto.strip().replace("\n", " ")
        log.info(f"Generando embedding de consulta: '{texto_limpio[:60]}...'")

        result = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texto_limpio,
            config=genai_types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=EMBEDDING_DIMS   # truncar a 1536
            )
        )

        embedding = result.embeddings[0].values
        log.info(f"Embedding consulta: {len(embedding)} dims [OK]")
        return list(embedding)

    # ─────────────────────────────────────────
    # B. Guardar proyecto con embedding
    # ─────────────────────────────────────────
    def ingresar_proyecto(self, titulo, resumen, carrera, anio, autores) -> dict:
        texto_completo = f"{titulo}. {resumen}"
        embedding = self.generar_embedding(texto_completo)
        payload = {
            "titulo":    titulo,
            "resumen":   resumen,
            "carrera":   carrera,
            "anio":      anio,
            "autores":   autores,
            "embedding": embedding
        }
        resultado = self.db_admin.table("proyectos_titulo").insert(payload).execute()
        registro = resultado.data[0]
        log.info(f"Proyecto guardado con ID: {registro['id']}")
        return registro

    # ─────────────────────────────────────────
    # C. Generar embeddings para seed data
    # ─────────────────────────────────────────
    def actualizar_embeddings_faltantes(self) -> int:
        """Busca proyectos sin embedding y genera con Gemini."""
        log.info("Buscando proyectos sin embedding...")
        sin_embedding = (
            self.db_admin
            .table("proyectos_titulo")
            .select("id, titulo, resumen")
            .is_("embedding", "null")
            .execute()
        )
        registros = sin_embedding.data
        log.info(f"Encontrados {len(registros)} proyectos sin embedding.")

        for i, r in enumerate(registros, 1):
            log.info(f"  [{i}/{len(registros)}] Procesando: {r['titulo'][:50]}")
            texto = f"{r['titulo']}. {r['resumen']}"
            embedding = self.generar_embedding(texto)
            self.db_admin.table("proyectos_titulo").update(
                {"embedding": embedding}
            ).eq("id", r["id"]).execute()
            log.info(f"  [OK] Guardado para ID: {r['id']}")
            if i < len(registros):
                time.sleep(0.3)

        return len(registros)

    # ─────────────────────────────────────────
    # D. Busqueda semantica
    # ─────────────────────────────────────────
    def buscar_similares(
        self,
        texto_consulta: str,
        umbral: float = 0.50,
        limite: int   = 5,
        carrera: Optional[str] = None
    ) -> list:
        log.info("Iniciando busqueda semantica...")
        embedding_consulta = self.generar_embedding_consulta(texto_consulta)

        params = {
            "query_embedding": embedding_consulta,
            "match_threshold": umbral,
            "match_count":     limite,
            "filtro_carrera":  carrera
        }

        response = self.db.rpc("buscar_proyectos_similares", params).execute()
        resultados = response.data

        if not resultados:
            log.info("No se encontraron proyectos con similitud suficiente.")
            return []

        for r in resultados:
            r["porcentaje_similitud"] = round(r["similitud"] * 100, 2)

        log.info(f"Se encontraron {len(resultados)} proyectos similares.")
        return resultados


# ─────────────────────────────────────────────────────────────
# Analisis NAPI (GPT-4o con fallback a Gemini Flash gratis)
# ─────────────────────────────────────────────────────────────
def analizar_con_napi(texto_nuevo: str, similares: list, engine: ArchivaIAEngine) -> str:
    SYSTEM_PROMPT = """Eres NAPI (Navegador de Antecedentes de Proyectos Innovadores), el asistente de ArchivaIA de INACAP Sede Maipu.

Tu mision: analizar si el proyecto de un estudiante se parece a proyectos anteriores y dar recomendaciones de innovacion.

Estructura tu respuesta en:
1. DIAGNOSTICO DE ORIGINALIDAD (nivel de riesgo: CRITICO/ALTO/MODERADO/SIN RIESGO con porcentajes)
2. ANALISIS DE PROYECTOS SIMILARES (que elementos comparten)
3. ZONAS DE CHOQUE DE IDEAS (que partes estan en riesgo de duplicacion)
4. RECOMENDACIONES DE INNOVACION (3-5 concretas con tecnologias especificas)
5. MENSAJE DE CIERRE (motivador + proximo paso concreto)

Escala de riesgo: 85-100%=CRITICO, 70-84%=ALTO, 50-69%=MODERADO, 0-49%=SIN RIESGO
Usa markdown. Responde en espanol, tono profesional y cercano."""

    if not similares:
        contexto = (
            f"## Proyecto del estudiante\n{texto_nuevo}\n\n"
            "## Resultado RAG\nNo se encontraron proyectos similares. La idea parece original."
        )
    else:
        similares_txt = "\n\n".join([
            f"**Proyecto {i+1}** ({r['porcentaje_similitud']}% similitud)\n"
            f"- Titulo: {r['titulo']}\n"
            f"- Carrera: {r['carrera']} ({r['anio']})\n"
            f"- Autores: {r['autores']}\n"
            f"- Resumen: {r['resumen']}"
            for i, r in enumerate(similares)
        ])
        contexto = (
            f"## Proyecto del estudiante (nuevo)\n{texto_nuevo}\n\n"
            f"## Proyectos similares encontrados por RAG\n{similares_txt}"
        )

    # Generación con Gemini 3.6 Flash (100% gratuito)
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"{SYSTEM_PROMPT}\n\n---\n\n{contexto}",
            config=genai_types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=1500
            )
        )
        log.info("Analisis generado con Gemini 3.6 Flash (gratuito).")
        return response.text
    except Exception as e:
        log.error(f"Error generando con Gemini: {e}")
        return f"Error al generar analisis: {e}"


# ─────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  ArchivaIA - Motor RAG v3 (Google Gemini GRATIS)")
    print("  INACAP Sede Maipu")
    print("=" * 60)

    motor = ArchivaIAEngine()

    print("\n[*] Paso 1: Generando embeddings con Gemini para proyectos seed...")
    actualizados = motor.actualizar_embeddings_faltantes()
    print(f"   -> {actualizados} proyectos actualizados.")

    tesis_estudiante = (
        "Sistema IoT para monitoreo remoto de cultivos hidroponicos con alertas "
        "automaticas y panel de control en tiempo real. El sistema usara sensores "
        "de temperatura, pH y nutrientes conectados por WiFi a una Raspberry Pi, "
        "enviando datos a un servidor en la nube con notificaciones SMS y email "
        "cuando los valores esten fuera de rango."
    )

    print(f"\n[*] Paso 2: Buscando proyectos similares...")
    print(f"    Idea: {tesis_estudiante[:80]}...")
    similares = motor.buscar_similares(texto_consulta=tesis_estudiante, umbral=0.50, limite=5)

    if similares:
        print(f"\n[OK] Se encontraron {len(similares)} proyectos similares:\n")
        for i, p in enumerate(similares, 1):
            print(f"  {i}. [{p['porcentaje_similitud']}%] {p['titulo']}")
            print(f"     {p['carrera']} - {p['anio']}")
    else:
        print("\n[OK] No se encontraron proyectos similares. Idea original!")

    print("\n[*] Paso 3: Generando analisis preventivo con NAPI...")
    analisis = analizar_con_napi(tesis_estudiante, similares, motor)

    print("\n" + "-" * 60)
    print("ANALISIS DE NAPI:")
    print("-" * 60)
    print(analisis)
    print("-" * 60)
    print("\n[OK] Demo completada exitosamente.")

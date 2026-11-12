# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
ArchivaIA - INACAP Sede Maipu
Motor RAG - Fase 1 v3.1: Directrices centralizadas en Supabase + google-genai
"""

import os
import logging
import time
from typing import Optional, Tuple
from dotenv import load_dotenv

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

GEMINI_API_KEY       = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY       = os.environ.get("OPENAI_API_KEY", "")
DEEPSEEK_API_KEY     = os.environ.get("DEEPSEEK_API_KEY", "")
SUPABASE_URL         = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_ANON_KEY    = os.environ.get("SUPABASE_ANON_KEY", "")

# Inicializar clientes
gemini_client   = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com") if DEEPSEEK_API_KEY else None

EMBEDDING_MODEL = "gemini-embedding-2"   # truncado a 1536 dims (max HNSW = 2000)
EMBEDDING_DIMS  = 1536

# Cache en memoria para directrices de Supabase (TTL: 5 minutos)
_GUIDELINES_CACHE: dict[str, Tuple[str, float, float]] = {}
CACHE_TTL_SECONDS = 300

FALLBACK_SYSTEM_PROMPT = """Eres NAPI (Navegador de Antecedentes de Proyectos Innovadores), el asistente de ArchivaIA de INACAP Sede Maipu.
Analiza la similitud del proyecto del estudiante frente a proyectos anteriores y entrega recomendaciones concretas de innovacion en espanol."""


class ArchivaIAEngine:
    """Motor RAG para busqueda semantica de proyectos de titulo INACAP."""

    def __init__(self):
        self.openai: OpenAI   = OpenAI(api_key=OPENAI_API_KEY, timeout=30.0)
        self.db_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        self.db: Client       = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        log.info("ArchivaIA Engine v3.1 (Directrices en nube) inicializado.")

    # ─────────────────────────────────────────
    # Obtener directrices desde Supabase (con cache)
    # ─────────────────────────────────────────
    def obtener_directriz(self, slug: str = "analisis_originalidad") -> Tuple[str, float]:
        ahora = time.time()
        if slug in _GUIDELINES_CACHE:
            prompt_cache, temp_cache, timestamp = _GUIDELINES_CACHE[slug]
            if (ahora - timestamp) < CACHE_TTL_SECONDS:
                return prompt_cache, temp_cache

        try:
            resp = (
                self.db.table("ai_guidelines")
                .select("system_prompt, temperature")
                .eq("slug", slug)
                .eq("is_active", True)
                .single()
                .execute()
            )
            if resp.data:
                prompt = resp.data["system_prompt"]
                temp = float(resp.data.get("temperature") or 0.4)
                _GUIDELINES_CACHE[slug] = (prompt, temp, ahora)
                log.info(f"Directriz '{slug}' cargada desde Supabase [OK]")
                return prompt, temp
        except Exception as e:
            log.warning(f"No se pudo leer directriz '{slug}' de Supabase ({e}). Usando respaldo.")

        if slug in _GUIDELINES_CACHE:
            return _GUIDELINES_CACHE[slug][0], _GUIDELINES_CACHE[slug][1]
        return FALLBACK_SYSTEM_PROMPT, 0.4

    # ─────────────────────────────────────────
    # A. Embedding con nuevo SDK google-genai
    # ─────────────────────────────────────────
    def generar_embedding(self, texto: str) -> list:
        texto_limpio = texto.strip().replace("\n", " ")
        log.info(f"Generando embedding para: '{texto_limpio[:60]}...'")

        result = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texto_limpio,
            config=genai_types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=EMBEDDING_DIMS
            )
        )

        embedding = result.embeddings[0].values
        log.info(f"Embedding generado: {len(embedding)} dimensiones [OK]")
        return list(embedding)

    def generar_embedding_consulta(self, texto: str) -> list:
        texto_limpio = texto.strip().replace("\n", " ")
        log.info(f"Generando embedding de consulta: '{texto_limpio[:60]}...'")

        result = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texto_limpio,
            config=genai_types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=EMBEDDING_DIMS
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
# Analisis NAPI (DeepSeek con fallback a Gemini Flash)
# ─────────────────────────────────────────────────────────────
def analizar_con_napi(
    texto_nuevo: str,
    similares: list,
    engine: ArchivaIAEngine,
    slug_directriz: str = "analisis_originalidad"
) -> str:
    # Obtener directriz y temperatura dinamicamente desde Supabase
    system_prompt, temp_config = engine.obtener_directriz(slug_directriz)

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

    # 1. Generacion con DeepSeek (si esta configurada DEEPSEEK_API_KEY)
    if deepseek_client:
        try:
            resp_ds = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": contexto}
                ],
                temperature=temp_config,
                max_tokens=1500
            )
            if resp_ds.choices and resp_ds.choices[0].message.content:
                log.info("Analisis generado con DeepSeek (deepseek-chat).")
                return resp_ds.choices[0].message.content.strip()
        except Exception as e_ds:
            log.warning(f"Error generando con DeepSeek ({e_ds}), pasando a Gemini...")

    # 2. Generacion con Gemini (max 10s, salto inmediato si hay 503)
    if gemini_client:
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contexto,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temp_config,
                    max_output_tokens=1500
                )
            )
            log.info("Analisis generado con Gemini (gemini-3.8-flash).")
            return response.text
        except Exception as e:
            log.warning(f"Gemini no disponible ({e}), pasando a OpenAI...")

    # 3. Generacion con OpenAI como ultimo respaldo (si esta configurada OPENAI_API_KEY)
    if OPENAI_API_KEY and engine.openai:
        try:
            resp_oai = engine.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": contexto}
                ],
                temperature=temp_config,
                max_tokens=1500
            )
            if resp_oai.choices and resp_oai.choices[0].message.content:
                log.info("Analisis generado con OpenAI (gpt-4o-mini).")
                return resp_oai.choices[0].message.content.strip()
        except Exception as e_oai:
            log.error(f"Error generando con OpenAI: {e_oai}")

    return "Error: No se pudo generar respuesta con los proveedores LLM disponibles."

# ─────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  ArchivaIA - Motor RAG v3.1 (Directrices en Supabase)")
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

    print("\n[*] Paso 2: Buscando proyectos similares...")
    print(f"    Idea: {tesis_estudiante[:80]}...")
    similares = motor.buscar_similares(texto_consulta=tesis_estudiante, umbral=0.50, limite=5)

    if similares:
        print(f"\n[OK] Se encontraron {len(similares)} proyectos similares:\n")
        for i, p in enumerate(similares, 1):
            print(f"  {i}. [{p['porcentaje_similitud']}%] {p['titulo']}")
            print(f"     {p['carrera']} ({p['anio']})")
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
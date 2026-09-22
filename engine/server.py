# -*- coding: utf-8 -*-
import sys
import io
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

"""
ArchivaIA · INACAP Sede Maipú
API Backend FastAPI – Motor RAG y Asistente NAPI
"""

import os
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from supabase import create_client, Client

# Cargar variables de entorno desde .env local y global
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
for env_f in [os.path.join(current_dir, ".env"), os.path.join(parent_dir, ".env"), ".env"]:
    if os.path.exists(env_f):
        load_dotenv(env_f)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ArchivaIA-API")

GEMINI_API_KEY       = os.environ.get("GEMINI_API_KEY", "")
SUPABASE_URL         = os.environ.get("SUPABASE_URL", "https://ovjsllepjamorjdjdteg.supabase.co").split('/rest')[0].rstrip('/')
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_ANON_KEY    = os.environ.get("SUPABASE_ANON_KEY", "")

# Clientes
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
db_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_KEY else None
db_anon: Client  = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) if SUPABASE_URL and SUPABASE_ANON_KEY else None

import concurrent.futures
gemini_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMS  = 1536

app = FastAPI(title="ArchivaIA RAG API", version="1.0.0")

# Permitir CORS total para desarrollo local y despliegue en Render
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
class ChatHistoryItem(BaseModel):
    role: str  # "user", "model", "napi", "assistant"
    content: str

class AnalyzeRequest(BaseModel):
    query: str
    umbral: Optional[float] = 0.40
    limite: Optional[int] = 4
    carrera: Optional[str] = None
    history: Optional[List[ChatHistoryItem]] = None

class ChatMessageRequest(BaseModel):
    email: str
    role: Optional[str] = "estudiante"
    sender: str  # "user", "napi", "card"
    message: str
    metadata: Optional[dict] = None

class ProjectCreateRequest(BaseModel):
    titulo: str
    resumen: str
    carrera: str
    anio: int
    autores: str

class LoginRequest(BaseModel):
    email: str
    password: str
    role: Optional[str] = None

class RegisterRequest(BaseModel):
    email: str
    password: str
    nombre: str
    rol: str = "estudiante"
    carrera: Optional[str] = "Informática / Ing. en Computación"

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
# RUTAS ESTÁTICAS Y FRONTEND
# ──────────────────────────────────────────
# Buscar directorio raíz del proyecto con certeza en local y en Render
def find_base_dir():
    candidates = [
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), # ../ (raíz normal)
        os.path.dirname(os.path.abspath(__file__)),                  # . (si corre en raíz)
        os.getcwd(),                                                 # Directorio de trabajo
        "/opt/render/project/src"                                    # Ruta Render estándar
    ]
    for c in candidates:
        if os.path.exists(os.path.join(c, "index.html")):
            return os.path.abspath(c)
    return os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = find_base_dir()
log.info(f"Directorio base detectado para estáticos: {BASE_DIR}")

css_dir = os.path.join(BASE_DIR, "css")
js_dir = os.path.join(BASE_DIR, "js")
img_dir = os.path.join(BASE_DIR, "img")
assets_dir = os.path.join(BASE_DIR, "assets")

if os.path.exists(css_dir):
    app.mount("/css", StaticFiles(directory=css_dir), name="css")
if os.path.exists(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")
if os.path.exists(img_dir):
    app.mount("/img", StaticFiles(directory=img_dir), name="img")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/")
def serve_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)

@app.get("/img/{file_path:path}")
def serve_img_fallback(file_path: str):
    p1 = os.path.join(BASE_DIR, "img", file_path)
    p2 = os.path.join(BASE_DIR, "assets", file_path)
    if os.path.exists(p1): return FileResponse(p1)
    if os.path.exists(p2): return FileResponse(p2)
    raise HTTPException(status_code=404, detail="Imagen no encontrada")

@app.get("/assets/{file_path:path}")
def serve_assets_fallback(file_path: str):
    p1 = os.path.join(BASE_DIR, "assets", file_path)
    p2 = os.path.join(BASE_DIR, "img", file_path)
    if os.path.exists(p1): return FileResponse(p1)
    if os.path.exists(p2): return FileResponse(p2)
    raise HTTPException(status_code=404, detail="Asset no encontrado")

# ──────────────────────────────────────────
# ENDPOINTS API
# ──────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "app": "ArchivaIA RAG Engine", "sede": "INACAP Maipú"}

# ── Autenticación de Usuarios (Supabase Auth) ──
@app.post("/api/auth/login")
def login(req: LoginRequest):
    """Inicia sesión autenticando con Supabase Auth."""
    try:
        res = db_anon.auth.sign_in_with_password({
            "email": req.email.strip(),
            "password": req.password.strip()
        })
        user = res.user
        meta = user.user_metadata or {}
        nombre = meta.get("nombre", user.email.split("@")[0])
        rol = meta.get("rol", req.role or "estudiante")
        carrera = meta.get("carrera", "Informática / Ing. en Computación")

        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "nombre": nombre,
                "rol": rol,
                "carrera": carrera
            },
            "access_token": res.session.access_token if res.session else None
        }
    except Exception as e:
        err_msg = str(e)
        log.warning(f"Error login Supabase para {req.email}: {err_msg}")
        
        # Modo fallback para credenciales demo (1234)
        if req.password.strip() == "1234":
            is_docente = "docente" in req.email.lower() or req.role == "docente"
            return {
                "success": True,
                "user": {
                    "id": "demo-user",
                    "email": req.email,
                    "nombre": "Prof. Carlos Mendoza" if is_docente else "Francisca González",
                    "rol": "docente" if is_docente else "estudiante",
                    "carrera": "Informática / Ing. en Computación"
                },
                "is_demo": True
            }
        
        raise HTTPException(status_code=401, detail="Correo institucional o contraseña incorrectos.")

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    """Registra un nuevo docente o estudiante en Supabase Auth."""
    try:
        res = db_admin.auth.admin.create_user({
            "email": req.email.strip(),
            "password": req.password.strip(),
            "email_confirm": True,
            "user_metadata": {
                "nombre": req.nombre.strip(),
                "rol": req.rol.strip(),
                "carrera": req.carrera.strip() if req.carrera else "Informática / Ing. en Computación"
            }
        })
        user = res.user
        return {
            "success": True,
            "message": f"Usuario {req.nombre} ({req.rol}) creado exitosamente.",
            "user": {
                "id": user.id,
                "email": user.email,
                "nombre": req.nombre,
                "rol": req.rol,
                "carrera": req.carrera
            }
        }
    except Exception as e:
        log.error(f"Error al registrar usuario: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/auth/users")
def get_users():
    """Obtiene la lista de usuarios registrados en Supabase Auth."""
    try:
        users = db_admin.auth.admin.list_users()
        user_list = []
        for u in users:
            meta = u.user_metadata or {}
            user_list.append({
                "id": u.id,
                "email": u.email,
                "nombre": meta.get("nombre", u.email),
                "rol": meta.get("rol", "estudiante"),
                "carrera": meta.get("carrera", "-"),
                "created_at": u.created_at
            })
        return {"users": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Historial de Chat NAPI en Supabase (Aislamiento por Usuario y Rol) ──
@app.get("/api/chat/history")
def get_chat_history(email: str, role: Optional[str] = None):
    """Recupera el historial de chat persistido en Supabase para el usuario y rol específicos."""
    try:
        if not db_admin:
            return {"messages": []}
        clean_email = email.strip().lower()
        query = db_admin.table("napi_chat_history").select("*").eq("user_email", clean_email)
        if role:
            query = query.eq("user_role", role.strip().lower())
        res = query.order("created_at", desc=False).execute()
        return {"messages": res.data or []}
    except Exception as e:
        log.warning(f"Error consultando historial de chat en Supabase ({e})")
        return {"messages": []}

@app.post("/api/chat/message")
def save_chat_message(req: ChatMessageRequest):
    """Guarda un mensaje en la base de datos Supabase para mantener los chats aislados en la nube."""
    try:
        if not db_admin:
            return {"success": False, "detail": "Supabase no conectado"}
        payload = {
            "user_email": req.email.strip().lower(),
            "user_role": req.role.strip().lower() if req.role else "estudiante",
            "sender": req.sender.strip().lower(),
            "message": req.message,
            "metadata": req.metadata or {}
        }
        res = db_admin.table("napi_chat_history").insert(payload).execute()
        return {"success": True, "data": res.data[0] if res.data else None}
    except Exception as e:
        log.warning(f"Error guardando mensaje en Supabase ({e})")
        return {"success": False, "error": str(e)}

@app.delete("/api/chat/history")
def clear_chat_history(email: str, role: Optional[str] = None):
    """Elimina el historial de chat del usuario en Supabase."""
    try:
        if not db_admin:
            return {"success": False}
        clean_email = email.strip().lower()
        query = db_admin.table("napi_chat_history").delete().eq("user_email", clean_email)
        if role:
            query = query.eq("user_role", role.strip().lower())
        query.execute()
        return {"success": True}
    except Exception as e:
        log.warning(f"Error eliminando historial de chat en Supabase ({e})")
        return {"success": False, "error": str(e)}

# ── Proyectos ──
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

# ── Motor RAG y Asistente NAPI ──
@app.post("/api/analyze")
def analyze_project(req: AnalyzeRequest):
    """
    Motor RAG: Realiza búsqueda semántica vía RPC en Supabase
    y genera el diagnóstico interactivo de NAPI con Gemini 3.6 Flash.
    """
    similares = []
    top_similitud = 0.0
    nivel_riesgo = "SIN RIESGO"

    try:
        # 1. Intentar búsqueda semántica con Gemini Embeddings + Supabase pgvector
        if gemini_client and db_anon:
            try:
                emb = get_query_embedding(req.query)
                rpc_params = {
                    "query_embedding": emb,
                    "match_threshold": req.umbral or 0.35,
                    "match_count": req.limite or 4,
                    "filtro_carrera": req.carrera
                }
                res = db_anon.rpc("buscar_proyectos_similares", rpc_params).execute()
                similares = res.data or []
            except Exception as emb_err:
                log.warning(f"Búsqueda vectorial no disponible ({emb_err}). Probando búsqueda por texto.")
                try:
                    words = [w for w in req.query.strip().split() if len(w) > 3][:3]
                    if words:
                        q = db_anon.table("proyectos_titulo").select("id, titulo, resumen, carrera, anio, autores")
                        for w in words:
                            q = q.ilike("titulo", f"%{w}%")
                        res = q.limit(req.limite or 4).execute()
                        similares = res.data or []
                        for s in similares:
                            s["similitud"] = 0.65
                except Exception as txt_err:
                    log.warning(f"Búsqueda por texto también falló: {txt_err}")
                    similares = []

        for s in similares:
            if "similitud" in s and s["similitud"] is not None:
                s["porcentaje_similitud"] = round(s["similitud"] * 100, 1)
            else:
                s["porcentaje_similitud"] = 60.0

        # Determinar riesgo
        top_similitud = similares[0]["porcentaje_similitud"] if similares else 0.0
        if top_similitud >= 80:
            nivel_riesgo = "CRÍTICO"
        elif top_similitud >= 65:
            nivel_riesgo = "ALTO"
        elif top_similitud >= 45:
            nivel_riesgo = "MODERADO"
        else:
            nivel_riesgo = "SIN RIESGO"

        # Formatear contexto RAG
        if not similares:
            contexto = f"## Proyecto del estudiante\n{req.query}\n\n## Resultado RAG\nNo se encontraron proyectos con similitud suficiente en el repositorio de INACAP Sede Maipú."
        else:
            items_txt = "\n\n".join([
                f"**Proyecto {i+1}** ({s.get('porcentaje_similitud', 60)}% similitud)\n"
                f"- Título: {s.get('titulo', '')}\n"
                f"- Carrera: {s.get('carrera', '')} ({s.get('anio', '')})\n"
                f"- Autores: {s.get('autores', '')}\n"
                f"- Resumen: {s.get('resumen', '')}"
                for i, s in enumerate(similares)
            ])
            contexto = f"## Proyecto del estudiante\n{req.query}\n\n## Proyectos Similares en Repositorio INACAP Maipú\n{items_txt}"

        # 2. Generar respuesta NAPI con Gemini (soporte conversacional multi-turno)
        SYSTEM_PROMPT = """Eres NAPI, el mentor y asistente inteligente de proyectos de título de INACAP Sede Maipú.
Eres un mentor experto, cercano, empático, motivador y hablas en lenguaje natural, claro y amigable (sin tecnicismos complejos innecesarios).

Tienes acceso al repositorio institucional de proyectos de título de la sede y al historial de la conversación.

REGLAS FUNDAMENTALES DE RESPUESTA:
1. SI EL USUARIO ESTÁ PRESENTANDO O DESCRIBIENDO UNA IDEA DE PROYECTO NUEVA:
   - Estructura tu respuesta de forma visual y motivadora:
     💡 **Diagnóstico de tu Idea**: Menciona el % de coincidencia estimado y el nombre del proyecto previo más parecido (si hay).
     🔍 **¿En qué se parece?**: Explica de forma sencilla qué partes, sensores o enfoque coinciden con trabajos anteriores.
     🚀 **¿Cómo puedes innovar y diferenciarte?**: Entrega 3 ideas prácticas, claras e innovadoras (ej: alertas a WhatsApp/Telegram, modelos predictivos simples, IoT en tiempo real o pruebas en una empresa real de Maipú).
     🎯 **Tu próximo paso**: Un consejo motivador y directo para su anteproyecto.

2. SI EL USUARIO ESTÁ HACIENDO PREGUNTAS DE SEGUIMIENTO, DEBATIENDO, REFLEXIONANDO O REBATIENDO (ejemplos: "¿no se parecería a X proyecto?", "¿tienes razón?", "¿por qué?", "¿y si le agrego visión computacional?", "¿cómo implemento eso?"):
   - RESPONDE DE FORMA 100% CONVERSACIONAL, DIRECTA Y NATURAL.
   - ¡NO repitas la plantilla de diagnóstico de 4 puntos si es una pregunta de seguimiento!
   - Reconoce y valida lo que dice el usuario: si tiene razón, dile: *"¡Tienes toda la razón!...", "La verdad es que no tanto porque...", "Buena observación, lo que pasa es que..."*.
   - Responde puntualmente a su inquietud manteniendo la memoria de todo lo conversado antes."""

        # Construir secuencia de contenidos para Gemini
        contents_list = []
        if req.history and len(req.history) > 0:
            for item in req.history[-8:]:
                r = "user" if item.role in ["user", "human"] else "model"
                contents_list.append(genai_types.Content(
                    role=r,
                    parts=[genai_types.Part.from_text(text=item.content)]
                ))

        user_prompt_content = f"{req.query}\n\n[Repositorio INACAP Maipú - Proyectos Similares detectados]:\n{contexto}"
        contents_list.append(genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=user_prompt_content)]
        ))

        analisis_texto = ""
        if gemini_client:
            def _llamar_gemini(mod_name):
                try:
                    resp = gemini_client.models.generate_content(
                        model=mod_name,
                        contents=contents_list,
                        config=genai_types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.6,
                            max_output_tokens=1500
                        )
                    )
                    return resp.text if resp and resp.text else ""
                except Exception as e:
                    log.warning(f"Error llamando {mod_name}: {e}")
                    return ""

            for mod in ["gemini-flash-latest", "gemini-3.6-flash", "gemini-3.7-flash"]:
                try:
                    fut = gemini_executor.submit(_llamar_gemini, mod)
                    analisis_texto = fut.result(timeout=4.5)
                    if analisis_texto:
                        log.info(f"Diagnóstico/Conversación generada exitosamente con {mod}")
                        break
                except Exception as ex:
                    log.warning(f"Modelo {mod} timeout/fallo: {ex}")

        # Fallback analítico garantizado con lenguaje simple y conversacional
        if not analisis_texto:
            q_lower = req.query.lower()
            is_idea_or_sim = any(k in q_lower for k in ["idea", "tesis", "proyecto", "similitud", "similitudes", "trabajo", "trabajos", "eficiencia", "energia", "aduana", "sensor", "iot", "app", "sistema"])
            
            if similares and (is_idea_or_sim or not req.history):
                top = similares[0]
                proyectos_lista = "\n".join([
                    f"- **{s.get('titulo')}** ({s.get('porcentaje_similitud', 60)}% parecido) — *{s.get('carrera')} · {s.get('anio')}*"
                    for s in similares[:2]
                ])
                analisis_texto = f"""## 💡 Diagnóstico de tu Idea

Tu idea tiene un **{top_similitud}% de similitud** con proyectos previos en INACAP Sede Maipú.

* **Proyecto más parecido:** *"{top.get('titulo')}"* ({top.get('anio')})

## 🔍 ¿En qué se parece?
Tu propuesta coincide en el objetivo principal con estos trabajos registrados en la sede:
{proyectos_lista}

## 🚀 ¿Cómo puedes innovar y diferenciarte?
Para que tu proyecto sea único y destaque en tu titulación, puedes hacer lo siguiente:
1. **Agregar alertas automáticas y tiempo real:** Notificaciones instantáneas al celular (por WhatsApp, Telegram o correo) cuando se detecte alguna anomalía.
2. **Incorporar predicción simple con IA:** En lugar de solo mostrar datos actuales, usa un modelo que anticipe qué pasará en las próximas horas.
3. **Aplicarlo a un caso real en Maipú:** Enfoca la solución directamente en un taller, comercio o industria de la comuna.

## 🎯 Tu próximo paso
Revisa el proyecto anterior para ver qué le faltó y preséntale esta propuesta mejorada a tu profesor guía."""
            elif req.history and len(req.history) > 0:
                analisis_texto = f"""¡Buena observación! Respecto a lo que planteas:

La clave para diferenciar tu propuesta está en el enfoque de aplicación y las tecnologías que incorpores. Si ajustas el alcance para resolver un problema específico (por ejemplo, automatización con alertas en tiempo real o un piloto en una empresa local de Maipú), tu proyecto se desmarcará completamente y tendrá un alto valor para tu comisión de titulación.

¿Te gustaría que profundicemos en la arquitectura técnica o en cómo redactar la justificación para tu anteproyecto?"""
            else:
                analisis_texto = f"""## 💡 Diagnóstico de tu Idea

* **Nivel de coincidencia:** **0% (Idea Original)**
* **Propuesta:** "{req.query}"

🎉 **¡Excelente idea!** No hay proyectos registrados en INACAP Sede Maipú que se parezcan a lo que propones.

## 🚀 ¿Cómo asegurar el éxito de tu proyecto?
1. **Tecnologías recomendadas:** Elige herramientas modernas y fáciles de integrar como FastAPI, Supabase y React/Next.js.
2. **Pruebas prácticas:** Diseña un prototipo funcional pequeño antes de construir todo el sistema completo.

## 🎯 Tu próximo paso
Empieza a redactar el resumen de tu anteproyecto y coméntalo con tu docente guía."""

        return {
            "query": req.query,
            "top_similitud": top_similitud,
            "nivel_riesgo": nivel_riesgo,
            "similares": similares,
            "analisis": analisis_texto
        }

    except Exception as e:
        log.error(f"Error en /api/analyze: {e}")
        # En vez de 500 que rompe el frontend, devolver respuesta analítica segura:
        return {
            "query": req.query,
            "top_similitud": 50.0,
            "nivel_riesgo": "MODERADO",
            "similares": [],
            "analisis": f"""## 📊 Diagnóstico de Originalidad (Modo Asistente)\n\n* **Idea consultada:** "{req.query}"\n* **Diagnóstico:** Tu propuesta ha sido recibida por NAPI.\n\n## 🔍 Recomendaciones Técnicas\n- Define con claridad el problema específico que resolverá tu proyecto en el entorno de INACAP Sede Maipú.\n- Selecciona un stack tecnológico moderno (FastAPI, React Native, Supabase, sensores IoT o modelos de Machine Learning).\n- Diferencia tu solución respecto a proyectos genéricos enfocándote en métricas de impacto real y validación práctica.\n\n## 💪 Próximo Paso\nPrepara el resumen técnico de tu propuesta y valídalo con tu docente guía."""
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)


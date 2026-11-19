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
import uuid
import time
import random
import logging
from typing import Optional, List, Literal
from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from openai import OpenAI
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
OPENAI_API_KEY       = os.environ.get("OPENAI_API_KEY", "")
DEEPSEEK_API_KEY     = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL       = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
GROQ_API_KEY         = os.environ.get("GROQ_API_KEY", "")
GROQ_MODELS          = [m.strip() for m in (os.environ.get("GROQ_MODEL") or "openai/gpt-oss-120b,qwen/qwen3.6-27b").split(",") if m.strip()]
SUPABASE_URL         = os.environ.get("SUPABASE_URL", "https://ovjsllepjamorjdjdteg.supabase.co").split('/rest')[0].rstrip('/')
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_ANON_KEY    = os.environ.get("SUPABASE_ANON_KEY", "")

# Banderas globales para desactivar proveedores con fallos permanentes durante el ciclo de vida
DEEPSEEK_DISABLED = False
OPENAI_DISABLED   = False

# Clientes
gemini_client   = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
openai_client   = OpenAI(api_key=OPENAI_API_KEY, max_retries=0) if OPENAI_API_KEY else None
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", max_retries=0) if DEEPSEEK_API_KEY else None
groq_client     = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1", max_retries=0) if GROQ_API_KEY else None
db_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_KEY else None
db_anon: Client  = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) if SUPABASE_URL and SUPABASE_ANON_KEY else None

# Seguridad: validación de sesiones (JWT de Supabase Auth) y control de acceso por rol
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
import security  # noqa: E402
from security import AuthUser  # noqa: E402
security.init(auth_client=db_anon or db_admin, profile_client=db_admin)

import concurrent.futures
gemini_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMS  = 1536

app = FastAPI(title="ArchivaIA RAG API", version="1.0.0")

# Configuración de CORS segura (orígenes permitidos vía variable de entorno o localhost por defecto)
ALLOWED_ORIGINS_ENV = os.environ.get("ALLOWED_ORIGINS", "")
if ALLOWED_ORIGINS_ENV.strip():
    allowed_origins = [orig.strip() for orig in ALLOWED_ORIGINS_ENV.split(",") if orig.strip()]
else:
    allowed_origins = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://n-a-p-i.onrender.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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
    file_name: Optional[str] = None
    file_content: Optional[str] = None

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
    nota: Optional[float] = 6.5
    area: Optional[str] = "Informática, Ciberseguridad y Telecomunicaciones"
    stack: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str
    role: Optional[str] = None

class RegisterRequest(BaseModel):
    email: str
    password: str
    nombre: str
    rol: str = "student"
    area: Optional[str] = "Informática, Ciberseguridad y Telecomunicaciones"
    carrera: Optional[str] = "Ingeniería en Informática"
    cargo: Optional[str] = None
    admin_code: Optional[str] = None

def normalize_role(raw_role: Optional[str]) -> str:
    r = (raw_role or "student").strip().lower()
    if r in ("admin", "administrador", "crai"):
        return "admin"
    if r in ("teacher", "docente", "profesor"):
        return "teacher"
    if r in ("student", "estudiante", "alumno"):
        return "student"
    return r

# ──────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────
# ──────────────────────────────────────────
# VALIDACIÓN DE ARCHIVOS SUBIDOS
# ──────────────────────────────────────────
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

def validar_documento_subido(filename: str, file_bytes: bytes) -> tuple[str, str]:
    if not filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo no proporcionado.")
    
    clean_fn = filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
    _, ext = os.path.splitext(clean_fn)
    ext = ext.lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Extensión no permitida: {ext}. Solo se admiten PDF y DOCX.")
    
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="El archivo excede el límite permitido de 100 MB.")
    
    # Validar firma binaria (Magic bytes)
    content_type = "application/octet-stream"
    if ext == ".pdf":
        if not file_bytes.startswith(b"%PDF"):
            raise HTTPException(status_code=400, detail="Archivo PDF inválido o corrupto.")
        content_type = "application/pdf"
    elif ext in (".docx", ".doc"):
        # ZIP magic bytes para .docx o compound file binary para .doc antiguo
        if not (file_bytes.startswith(b"PK\x03\x04") or file_bytes.startswith(b"\xd0\xcf\x11\xe0")):
            raise HTTPException(status_code=400, detail="Archivo Word inválido o corrupto.")
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if ext == ".docx" else "application/msword"
        
    return clean_fn, content_type

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
# DIRECTRICES EN LA NUBE (SUPABASE + CACHÉ)
# ──────────────────────────────────────────
_GUIDELINES_CACHE = {}
CACHE_TTL_SECONDS = 300  # 5 minutos

FALLBACK_NAPI_PROMPT = """Eres NAPI, el asistente virtual de Inacap Sede Maipú que ayuda a estudiantes a validar y orientar ideas de proyecto de título. Conversas como un docente guía cercano, empático y constructivo (español de Chile, trato de "tú").
Responde de forma concisa, sin tablas ni encabezados markdown, indicando proyectos similares si existen y 2 recomendaciones concretas para diferenciarse."""

def get_cloud_guideline(slug: str = "napi_chat_principal") -> tuple[str, float]:
    now = time.time()
    if slug in _GUIDELINES_CACHE:
        prompt, temp, ts = _GUIDELINES_CACHE[slug]
        if (now - ts) < CACHE_TTL_SECONDS:
            return prompt, temp

    client_sb = db_anon or db_admin
    if client_sb:
        try:
            res = (
                client_sb.table("ai_guidelines")
                .select("system_prompt, temperature")
                .eq("slug", slug)
                .eq("is_active", True)
                .single()
                .execute()
            )
            if res.data:
                prompt = res.data["system_prompt"]
                temp = float(res.data.get("temperature") or 0.7)
                _GUIDELINES_CACHE[slug] = (prompt, temp, now)
                log.info(f"Directriz '{slug}' cargada desde Supabase [OK]")
                return prompt, temp
        except Exception as e:
            log.warning(f"No se pudo leer directriz '{slug}' desde Supabase ({e}). Usando respaldo.")

    if slug in _GUIDELINES_CACHE:
        return _GUIDELINES_CACHE[slug][0], _GUIDELINES_CACHE[slug][1]
    return FALLBACK_NAPI_PROMPT, 0.7

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
    if not db_anon:
        raise HTTPException(status_code=503, detail="Servicio de autenticación Supabase no configurado.")
    try:
        clean_email = req.email.strip()
        res = db_anon.auth.sign_in_with_password({
            "email": clean_email,
            "password": req.password.strip()
        })
        user = res.user
        meta = user.user_metadata or {}
        nombre = meta.get("nombre", user.email.split("@")[0])
        rol = meta.get("rol", req.role or "student")
        area = meta.get("area", "Informática, Ciberseguridad y Telecomunicaciones")
        carrera = meta.get("carrera", "Ingeniería en Informática")
        cargo = meta.get("cargo")

        # Enriquecer desde tabla pública napi_usuarios si existe registro
        if db_admin:
            try:
                prof = db_admin.table("napi_usuarios").select("*").eq("email", clean_email).limit(1).execute()
                if prof.data and len(prof.data) > 0:
                    row = prof.data[0]
                    nombre = row.get("nombre") or nombre
                    rol = row.get("rol") or rol
                    area = row.get("area") or area
                    carrera = row.get("carrera") or carrera
            except Exception:
                pass

        # Normalizar rol admin para garantizar acceso consistente entre web y móvil
        rol_norm = normalize_role(rol) if rol in ("admin", "administrador", "crai") else rol

        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "nombre": nombre,
                "rol": rol_norm,
                "role": rol_norm,
                "area": area,
                "carrera": carrera,
                "cargo": cargo
            },
            "access_token": res.session.access_token if res.session else None
        }
    except Exception as e:
        err_msg = str(e)
        log.warning(f"Error login Supabase para {req.email}: {err_msg}")
        raise HTTPException(status_code=401, detail="Correo institucional o contraseña incorrectos.")

@app.post("/api/auth/register")
def register(req: RegisterRequest, requester: Optional[AuthUser] = Depends(security.get_optional_user)):
    """Registra un usuario en Supabase Auth y en napi_usuarios.
    El registro público solo permite el rol estudiante; docentes y administradores
    deben ser creados por un Administrador CRAI autenticado (evita escalamiento de privilegios)."""
    if not db_admin:
        raise HTTPException(status_code=503, detail="Servicio de administración Supabase no configurado.")
    if security.canonical_role(req.rol) != security.ROLE_STUDENT and not (requester and requester.is_admin):
        raise HTTPException(
            status_code=403,
            detail="Solo un Administrador CRAI puede registrar cuentas de docente o administrador."
        )
    try:
        clean_email = req.email.strip()
        clean_nombre = req.nombre.strip()
        raw_rol = (req.rol or "student").strip().lower()
        allowed_roles = {"student", "teacher", "admin", "estudiante", "docente", "administrador"}
        if raw_rol not in allowed_roles:
            raise HTTPException(status_code=400, detail=f"Rol no válido: {req.rol}")

        # Guardar admin siempre como 'admin'; preservar student/teacher o equivalentes
        clean_rol = "admin" if raw_rol in ("admin", "administrador") else raw_rol
        clean_cargo = (req.cargo or ("Administrador CRAI" if clean_rol == "admin" else "")).strip() or None
        clean_area = req.area.strip() if req.area else ("Biblioteca CRAI · Sede Maipú" if clean_rol == "admin" else "Informática, Ciberseguridad y Telecomunicaciones")
        clean_carrera = req.carrera.strip() if req.carrera else (clean_cargo or "Ingeniería en Informática")

        user_meta = {
            "nombre": clean_nombre,
            "rol": clean_rol,
            "area": clean_area,
            "carrera": clean_carrera
        }
        if clean_cargo:
            user_meta["cargo"] = clean_cargo

        res = db_admin.auth.admin.create_user({
            "email": clean_email,
            "password": req.password.strip(),
            "email_confirm": True,
            "user_metadata": user_meta
        })
        user = res.user

        try:
            db_admin.table("napi_usuarios").upsert({
                "id": user.id,
                "email": clean_email,
                "nombre": clean_nombre,
                "rol": clean_rol,
                "area": clean_area,
                "carrera": clean_carrera
            }).execute()
        except Exception as t_err:
            log.info(f"Aviso al sincronizar tabla napi_usuarios en registro: {t_err}")

        return {
            "success": True,
            "message": f"Usuario {clean_nombre} ({clean_rol}) creado exitosamente.",
            "user": {
                "id": user.id,
                "email": user.email,
                "nombre": clean_nombre,
                "rol": clean_rol,
                "role": clean_rol,
                "area": clean_area,
                "carrera": clean_carrera,
                "cargo": clean_cargo
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error al registrar usuario: {e}")
        raise HTTPException(status_code=400, detail=str(e))

class UserUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    rol: Optional[str] = None
    area: Optional[str] = None
    carrera: Optional[str] = None
    password: Optional[str] = None

class UserCreateAdminRequest(BaseModel):
    nombre: str
    email: str
    rol: str = "estudiante"
    area: Optional[str] = "Tecnología Aplicada"
    carrera: Optional[str] = "Ingeniería en Informática"
    password: str = "InacapPassword123!"

@app.get("/api/auth/users")
@app.get("/api/admin/users")
def get_users(admin: AuthUser = Depends(security.require_admin)):
    """Obtiene la lista de usuarios registrados (solo Administrador CRAI)."""
    try:
        user_list = []
        # 1. Intentar leer desde tabla pública en Supabase
        if db_admin:
            try:
                tbl_res = db_admin.table("napi_usuarios").select("*").order("created_at", desc=True).execute()
                if tbl_res.data and len(tbl_res.data) > 0:
                    return {"users": tbl_res.data}
            except Exception as tbl_err:
                log.info(f"Tabla napi_usuarios no consultable ({tbl_err}), leyendo auth.users")

            # 2. Respaldo desde auth.users
            try:
                users_res = db_admin.auth.admin.list_users()
                users = getattr(users_res, 'users', users_res) if not isinstance(users_res, list) else users_res
                for u in users:
                    meta = getattr(u, 'user_metadata', {}) or {}
                    user_list.append({
                        "id": getattr(u, 'id', str(u)),
                        "email": getattr(u, 'email', ''),
                        "nombre": meta.get("nombre", getattr(u, 'email', 'Usuario').split("@")[0]),
                        "rol": meta.get("rol", "estudiante"),
                        "area": meta.get("area", "Informática, Ciberseguridad y Telecomunicaciones"),
                        "carrera": meta.get("carrera", "Ingeniería en Informática"),
                        "created_at": getattr(u, 'created_at', None)
                    })
            except Exception as e:
                log.warning(f"Error listando usuarios en Supabase Auth: {e}")
        return {"users": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def to_db_role(raw_role: Optional[str]) -> str:
    """Convierte el rol al formato español exigido por el CHECK constraint de public.napi_usuarios."""
    r = (raw_role or "student").strip().lower()
    if r in ("admin", "administrador", "crai"):
        return "administrador"
    if r in ("teacher", "docente", "profesor"):
        return "docente"
    return "estudiante"

@app.post("/api/admin/users")
def admin_create_user(req: UserCreateAdminRequest, admin: AuthUser = Depends(security.require_admin)):
    """Crea un usuario (Alumno, Docente o Administrador) en Supabase Auth y en public.napi_usuarios."""
    if not db_admin:
        raise HTTPException(status_code=503, detail="Servicio de administración Supabase no configurado.")
    try:
        clean_email = req.email.strip().lower()
        clean_nombre = req.nombre.strip()
        db_rol = to_db_role(req.rol)
        auth_rol = normalize_role(req.rol)
        clean_area = req.area.strip() if req.area else "Informática, Ciberseguridad y Telecomunicaciones"
        clean_carrera = req.carrera.strip() if req.carrera else "Ingeniería en Informática"

        user_id = None
        # 1. Crear en Supabase Auth (o recuperar su ID si ya existía en Auth)
        try:
            res = db_admin.auth.admin.create_user({
                "email": clean_email,
                "password": req.password.strip(),
                "email_confirm": True,
                "user_metadata": {
                    "nombre": clean_nombre,
                    "rol": auth_rol,
                    "area": clean_area,
                    "carrera": clean_carrera
                }
            })
            if res and hasattr(res, 'user') and res.user:
                user_id = res.user.id
        except Exception as auth_e:
            log.warning(f"Aviso al crear en Supabase Auth ({auth_e}). Buscando si ya existe en Auth...")
            try:
                users_res = db_admin.auth.admin.list_users()
                users = getattr(users_res, 'users', users_res) if not isinstance(users_res, list) else users_res
                for u in users:
                    if getattr(u, 'email', '').lower() == clean_email:
                        user_id = getattr(u, 'id', None)
                        db_admin.auth.admin.update_user_by_id(user_id, {
                            "password": req.password.strip(),
                            "email_confirm": True,
                            "user_metadata": {
                                "nombre": clean_nombre,
                                "rol": auth_rol,
                                "area": clean_area,
                                "carrera": clean_carrera
                            }
                        })
                        break
            except Exception as list_e:
                log.warning(f"No se pudo recuperar usuario existente en Auth: {list_e}")

        user_id = None
        last_auth_err = ""
        # 1. Crear en Supabase Auth (Admin API)
        try:
            res = db_admin.auth.admin.create_user({
                "email": clean_email,
                "password": req.password.strip(),
                "email_confirm": True,
                "user_metadata": {
                    "nombre": clean_nombre,
                    "rol": auth_rol,
                    "area": clean_area,
                    "carrera": clean_carrera
                }
            })
            if res and hasattr(res, 'user') and res.user:
                user_id = res.user.id
        except Exception as auth_e:
            last_auth_err = str(auth_e)
            log.warning(f"Aviso al crear en Supabase Auth ({last_auth_err}). Buscando si ya existe...")
            try:
                users_res = db_admin.auth.admin.list_users(page=1, per_page=1000)
                users = getattr(users_res, 'users', users_res) if not isinstance(users_res, list) else users_res
                for u in users:
                    if getattr(u, 'email', '').lower() == clean_email:
                        user_id = getattr(u, 'id', None)
                        db_admin.auth.admin.update_user_by_id(user_id, {
                            "password": req.password.strip(),
                            "email_confirm": True,
                            "user_metadata": {
                                "nombre": clean_nombre,
                                "rol": auth_rol,
                                "area": clean_area,
                                "carrera": clean_carrera
                            }
                        })
                        break
            except Exception as list_e:
                last_auth_err += f" | list: {list_e}"

        # Respaldo con sign_up público si admin API no tiene permisos service_role
        if not user_id and db_anon:
            try:
                su_res = db_anon.auth.sign_up({
                    "email": clean_email,
                    "password": req.password.strip(),
                    "options": {
                        "data": {
                            "nombre": clean_nombre,
                            "rol": auth_rol,
                            "area": clean_area,
                            "carrera": clean_carrera
                        }
                    }
                })
                if su_res and getattr(su_res, "user", None):
                    user_id = su_res.user.id
            except Exception as su_e:
                last_auth_err += f" | sign_up: {su_e}"

        if not user_id:
            raise HTTPException(status_code=400, detail=f"Supabase Auth rechazó el registro: {last_auth_err}")
            
        # 2. Guardar perfil en tabla pública napi_usuarios con el rol en español ('estudiante', 'docente', 'administrador')
        row_payload = {
            "id": str(user_id),
            "email": clean_email,
            "nombre": clean_nombre,
            "rol": db_rol,
            "area": clean_area,
            "carrera": clean_carrera
        }
        db_admin.table("napi_usuarios").upsert(row_payload).execute()

        return {
            "success": True,
            "message": f"Usuario {clean_nombre} ({db_rol}) creado exitosamente en Supabase.",
            "user": row_payload
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error al crear usuario por admin: {e}")
        raise HTTPException(status_code=400, detail=f"Error al guardar en Supabase: {str(e)}")

@app.put("/api/admin/users/{user_id}")
def admin_update_user(user_id: str, req: UserUpdateRequest, admin: AuthUser = Depends(security.require_admin)):
    """Actualiza los datos de un usuario en Supabase."""
    try:
        db_rol = to_db_role(req.rol) if req.rol is not None else None
        auth_rol = normalize_role(req.rol) if req.rol is not None else None

        meta_updates = {}
        if req.nombre is not None: meta_updates["nombre"] = req.nombre.strip()
        if auth_rol is not None: meta_updates["rol"] = auth_rol
        if req.area is not None: meta_updates["area"] = req.area.strip()
        if req.carrera is not None: meta_updates["carrera"] = req.carrera.strip()

        if db_admin:
            attrs = {"user_metadata": meta_updates}
            if req.email: attrs["email"] = req.email.strip().lower()
            if req.password: attrs["password"] = req.password.strip()
            try:
                db_admin.auth.admin.update_user_by_id(user_id, attrs)
            except Exception as e:
                log.warning(f"Error actualizando usuario en Supabase Auth ({user_id}): {e}")

            payload = {"id": user_id}
            if req.email: payload["email"] = req.email.strip().lower()
            if req.nombre: payload["nombre"] = req.nombre.strip()
            if db_rol: payload["rol"] = db_rol
            if req.area: payload["area"] = req.area.strip()
            if req.carrera: payload["carrera"] = req.carrera.strip()
            db_admin.table("napi_usuarios").upsert(payload).execute()

        return {
            "success": True,
            "message": "Usuario actualizado correctamente en Supabase.",
            "user": {
                "id": user_id,
                "email": req.email,
                "nombre": req.nombre,
                "rol": db_rol or req.rol,
                "area": req.area,
                "carrera": req.carrera
            }
        }
    except Exception as e:
        log.error(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/admin/users/{user_id}")
def admin_delete_user(user_id: str, admin: AuthUser = Depends(security.require_admin)):
    """Elimina un usuario de Supabase (solo Administrador CRAI)."""
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta de administrador.")
    try:
        if db_admin:
            try:
                db_admin.table("napi_usuarios").delete().eq("id", user_id).execute()
            except Exception as t_err:
                log.info(f"Aviso eliminando de tabla napi_usuarios: {t_err}")
            try:
                db_admin.auth.admin.delete_user(user_id)
            except Exception as e:
                log.warning(f"Error eliminando usuario de Supabase Auth ({user_id}): {e}")
        return {"success": True, "message": "Usuario eliminado exitosamente de Supabase."}
    except Exception as e:
        log.error(f"Error al eliminar usuario: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ── Historial de Chat NAPI en Supabase (Aislamiento por Usuario y Rol) ──
def _ensure_own_chat(user: AuthUser, email: str) -> str:
    """Cada usuario solo puede leer, escribir o borrar su propio historial de conversación."""
    clean_email = (email or "").strip().lower()
    if not clean_email or clean_email != user.email:
        raise HTTPException(status_code=403, detail="Solo puedes acceder a tu propio historial de chat.")
    return clean_email

@app.get("/api/chat/history")
def get_chat_history(email: str, role: Optional[str] = None, user: AuthUser = Depends(security.get_current_user)):
    """Recupera el historial de chat persistido en Supabase para el usuario y rol específicos."""
    clean_email = _ensure_own_chat(user, email)
    try:
        if not db_admin:
            return {"messages": []}
        query = db_admin.table("napi_chat_history").select("*").eq("user_email", clean_email)
        if role:
            query = query.eq("user_role", role.strip().lower())
        res = query.order("created_at", desc=False).execute()
        return {"messages": res.data or []}
    except Exception as e:
        log.warning(f"Error consultando historial de chat en Supabase ({e})")
        return {"messages": []}

@app.post("/api/chat/message")
def save_chat_message(req: ChatMessageRequest, user: AuthUser = Depends(security.get_current_user)):
    """Guarda un mensaje en la base de datos Supabase para mantener los chats aislados en la nube."""
    clean_email = _ensure_own_chat(user, req.email)
    try:
        if not db_admin:
            return {"success": False, "detail": "Supabase no conectado"}
        payload = {
            "user_email": clean_email,
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
def clear_chat_history(email: str, role: Optional[str] = None, user: AuthUser = Depends(security.get_current_user)):
    """Elimina el historial de chat del usuario en Supabase."""
    clean_email = _ensure_own_chat(user, email)
    try:
        if not db_admin:
            return {"success": False}
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
def get_projects(role: Optional[str] = None, user: Optional[AuthUser] = Depends(security.get_optional_user)):
    """Obtiene los proyectos registrados en Supabase.
    La visibilidad se decide con la sesión validada en el servidor (no con el parámetro 'role',
    que puede ser manipulado): visitantes y estudiantes solo ven proyectos públicos."""
    puede_ver_privados = bool(user and user.is_staff)
    if role and role.strip().lower() in ("estudiante", "student"):
        puede_ver_privados = False
    try:
        cols_full = "id, titulo, resumen, carrera, anio, autores, created_at, archivo_url, estado, area, stack, nota"
        cols_safe = "id, titulo, resumen, carrera, anio, autores, created_at, archivo_url"
        try:
            query = db_anon.table("proyectos_titulo").select(cols_full)
            if not puede_ver_privados:
                query = query.eq("estado", "Público")
            response = query.order("anio", desc=True).execute()
        except Exception:
            response = db_anon.table("proyectos_titulo").select(cols_safe).order("anio", desc=True).execute()
        projects = response.data or []
        if not puede_ver_privados:
            # Los estudiantes y visitantes no reciben la URL directa del documento completo:
            # solo el nombre del archivo (para mostrar el tipo) y deben solicitar acceso al CRAI.
            for p in projects:
                url = p.get("archivo_url")
                if url:
                    p["archivo"] = url.split("?")[0].rstrip("/").split("/")[-1]
                    p["archivo_url"] = None
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GuidelineUpdateRequest(BaseModel):
    system_prompt: str
    temperature: float = 0.7
    is_active: bool = True


@app.get("/api/admin/guidelines")
def get_admin_guidelines(slug: str = "napi_chat_principal", admin: AuthUser = Depends(security.require_admin)):
    """Obtiene la directriz de IA actual desde Supabase."""
    prompt, temp = get_cloud_guideline(slug)
    return {"slug": slug, "system_prompt": prompt, "temperature": temp, "is_active": True}


@app.put("/api/admin/guidelines")
def update_admin_guidelines(req: GuidelineUpdateRequest, slug: str = "napi_chat_principal", admin: AuthUser = Depends(security.require_admin)):
    """Actualiza la directriz de IA en Supabase (public.ai_guidelines) y limpia la caché."""
    if not db_admin:
        raise HTTPException(status_code=503, detail="Supabase Admin no configurado.")
    try:
        temp = max(0.0, min(1.5, float(req.temperature)))
        payload = {
            "slug": slug,
            "system_prompt": req.system_prompt.strip(),
            "temperature": temp,
            "is_active": req.is_active
        }
        db_admin.table("ai_guidelines").upsert(payload, on_conflict="slug").execute()
        _GUIDELINES_CACHE.pop(slug, None)
        return {"success": True, "guideline": payload}
    except Exception as e:
        log.error(f"Error actualizando ai_guidelines: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects")
async def create_project(request: Request, staff: AuthUser = Depends(security.require_staff)):
    """Inserta un nuevo proyecto validando nota >= 6.0, calculando embeddings y subiendo archivo opcional a Supabase Storage."""
    try:
        content_type = request.headers.get("content-type", "")
        titulo = ""
        resumen = ""
        carrera = ""
        anio = 2025
        autores = ""
        nota = 6.5
        area = "Informática, Ciberseguridad y Telecomunicaciones"
        stack = ""
        estado = "Público"
        archivo_url = None

        if "multipart/form-data" in content_type:
            form = await request.form()
            titulo = str(form.get("titulo") or "").strip()
            resumen = str(form.get("resumen") or "").strip()
            carrera = str(form.get("carrera") or "").strip()
            try:
                anio = int(form.get("anio", 2025))
            except (ValueError, TypeError):
                anio = 2025
            autores = str(form.get("autores") or "").strip()
            try:
                nota = float(form.get("nota", 6.5))
            except (ValueError, TypeError):
                nota = 6.5
            area = str(form.get("area") or "Informática, Ciberseguridad y Telecomunicaciones").strip()
            stack = str(form.get("stack") or "").strip()
            estado = str(form.get("estado") or "Público").strip()

            file_item = form.get("archivo")
            if file_item and hasattr(file_item, "filename") and file_item.filename:
                # Validar el documento ANTES de subirlo (extensión, tamaño y firma real del archivo)
                file_bytes = await file_item.read()
                clean_fn, content_type_file = validar_documento_subido(file_item.filename, file_bytes)
                if db_admin:
                    try:
                        try:
                            db_admin.storage.create_bucket("proyectos-docs", options={"public": True})
                        except Exception:
                            pass

                        if file_bytes:
                            safe_name = f"{uuid.uuid4().hex}_{clean_fn}"
                            
                            db_admin.storage.from_("proyectos-docs").upload(
                                path=safe_name,
                                file=file_bytes,
                                file_options={"content-type": content_type_file}
                            )

                            try:
                                url_res = db_admin.storage.from_("proyectos-docs").get_public_url(safe_name)
                                if isinstance(url_res, dict):
                                    archivo_url = url_res.get("publicUrl") or url_res.get("public_url")
                                elif hasattr(url_res, "public_url"):
                                    archivo_url = url_res.public_url
                                else:
                                    archivo_url = str(url_res)
                            except Exception:
                                archivo_url = f"{SUPABASE_URL}/storage/v1/object/public/proyectos-docs/{safe_name}"
                            log.info(f"Archivo subido exitosamente a Supabase Storage: {archivo_url}")
                    except Exception as upload_err:
                        log.warning(f"Error subiendo archivo a Supabase Storage ({upload_err})")
        else:
            data = await request.json()
            titulo = str(data.get("titulo") or "").strip()
            resumen = str(data.get("resumen") or "").strip()
            carrera = str(data.get("carrera") or "").strip()
            anio = int(data.get("anio", 2025))
            autores = str(data.get("autores") or "").strip()
            nota = float(data.get("nota", 6.5)) if data.get("nota") is not None else 6.5
            area = str(data.get("area") or "Informática, Ciberseguridad y Telecomunicaciones").strip()
            stack = str(data.get("stack") or "").strip()
            estado = str(data.get("estado") or "Público").strip()
            archivo_url = data.get("archivo_url")
            # Solo se aceptan URLs de documentos alojados en el Storage propio del proyecto
            storage_prefix = f"{SUPABASE_URL}/storage/v1/object/public/proyectos-docs/"
            if archivo_url and not str(archivo_url).startswith(storage_prefix):
                raise HTTPException(status_code=400, detail="URL de documento no permitida.")

        # Validación de nota según normativa Inacap
        if nota is not None and (nota < 6.0 or nota > 7.0):
            raise HTTPException(
                status_code=400, 
                detail="Normativa Inacap: Solo se pueden registrar proyectos con nota final igual o superior a 6.0."
            )

        texto_completo = f"{titulo}. {resumen}"
        embedding = get_doc_embedding(texto_completo)

        payload = {
            "titulo": titulo,
            "resumen": resumen,
            "carrera": carrera,
            "anio": anio,
            "autores": autores,
            "embedding": embedding
        }
        if archivo_url:
            payload["archivo_url"] = archivo_url
        if area:
            payload["area"] = area
        if stack:
            payload["stack"] = stack
        if nota is not None:
            payload["nota"] = nota
        if estado:
            payload["estado"] = estado

        if db_admin:
            try:
                res = db_admin.table("proyectos_titulo").insert(payload).execute()
                return {"success": True, "project": res.data[0] if res.data else payload}
            except Exception as db_e:
                log.warning(f"Aviso guardando con metadata completa ({db_e}). Reintentando con esquema seguro...")
                try:
                    safe_payload = {
                        "titulo": titulo,
                        "resumen": resumen,
                        "carrera": carrera,
                        "anio": anio,
                        "autores": autores,
                        "embedding": embedding
                    }
                    if archivo_url:
                        safe_payload["archivo_url"] = archivo_url
                    res = db_admin.table("proyectos_titulo").insert(safe_payload).execute()
                    safe_payload["estado"] = estado
                    safe_payload["area"] = area
                    safe_payload["stack"] = stack
                    safe_payload["nota"] = nota
                    return {"success": True, "project": res.data[0] if res.data else safe_payload}
                except Exception as fb_e:
                    log.error(f"Error definitivo insertando en Supabase: {fb_e}")
                    raise HTTPException(status_code=500, detail=str(fb_e))

        return {"success": True, "project": payload}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/projects/{project_id}")
async def update_project(project_id: str, request: Request, admin: AuthUser = Depends(security.require_admin)):
    """Actualiza metadatos de un proyecto (incluyendo visibilidad y estado)."""
    try:
        data = await request.json()
        update_data = {}
        for field in ["titulo", "resumen", "carrera", "anio", "autores", "estado", "area", "stack", "nota"]:
            if field in data and data[field] is not None:
                update_data[field] = data[field]

        if "titulo" in update_data and "resumen" in update_data:
            texto = f"{update_data['titulo']}. {update_data['resumen']}"
            update_data["embedding"] = get_doc_embedding(texto)

        if db_admin and update_data:
            try:
                res = db_admin.table("proyectos_titulo").update(update_data).eq("id", project_id).execute()
                return {"success": True, "data": res.data}
            except Exception as db_e:
                safe_update = {k: v for k, v in update_data.items() if k in ["titulo", "resumen", "carrera", "anio", "autores", "embedding"]}
                if safe_update:
                    db_admin.table("proyectos_titulo").update(safe_update).eq("id", project_id).execute()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str, admin: AuthUser = Depends(security.require_admin)):
    """Elimina un proyecto del repositorio en Supabase."""
    try:
        if db_admin:
            db_admin.table("proyectos_titulo").delete().eq("id", project_id).execute()
        return {"success": True, "message": "Proyecto eliminado correctamente de Supabase."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────
# BANCO DE INNOVACIÓN LOCAL Y RESILIENTE (16 PROPUESTAS TÉCNICAS)
# ──────────────────────────────────────────
BANCO_INNOVACION = [
    {
        "id": "iot_edge",
        "keywords": ["iot", "edge", "telemetria", "esp32", "arduino", "raspberry", "sensorica"],
        "plantilla": "**Telemetría en el borde (Edge Computing):** Procesar señales de {tema} directamente en microcontroladores (ESP32 o Edge Gateway) antes de subir a la nube, reduciendo latencia y consumo de datos."
    },
    {
        "id": "ia_predictiva",
        "keywords": ["predictiv", "machine learning", "clasificacion", "patron", "redes neuronales", "anomalia"],
        "plantilla": "**Modelos predictivos de fallas:** Implementar algoritmos de machine learning ligeros para anticipar averías o comportamientos anómalos en {tema} a partir de series temporales."
    },
    {
        "id": "pwa_offline",
        "keywords": ["pwa", "offline", "movil", "sincroniz", "cache", "service worker"],
        "plantilla": "**PWA con soporte offline-first:** Diseñar una Progressive Web App instalable que permita registrar operaciones de {tema} en terreno sin conexión y sincronice al recuperar señal."
    },
    {
        "id": "ciberseguridad",
        "keywords": ["ciberseguridad", "cifrado", "tls", "hash", "rbac", "seguridad", "criptograf"],
        "plantilla": "**Ciberseguridad y auditoría criptográfica:** Blindar la transmisión y almacenamiento de datos de {tema} mediante cifrado TLS 1.3, autenticación basada en roles y firmas hash para evitar alteraciones."
    },
    {
        "id": "analitica_dashboards",
        "keywords": ["dashboard", "kpi", "analitica", "tablero", "bi", "visualizacion"],
        "plantilla": "**Analítica de datos y tableros interactivos:** Construir un dashboard en tiempo real con métricas operativas y umbrales preventivos de {tema} para toma de decisiones técnicas informadas."
    },
    {
        "id": "vision_computacional",
        "keywords": ["vision", "computacional", "opencv", "camara", "imagen", "deteccion", "reconocimiento"],
        "plantilla": "**Inspección visual asistida por computadora:** Incorporar procesamiento de imágenes con OpenCV o MediaPipe para inspección visual automática o control de calidad en {tema}."
    },
    {
        "id": "sostenibilidad_energia",
        "keywords": ["energia", "consumo", "sostenibil", "eficiencia", "huella", "electr"],
        "plantilla": "**Eficiencia energética y sustentabilidad:** Integrar algoritmos de optimización de consumo eléctrico y medición de huella de carbono en los ciclos de operación de {tema}."
    },
    {
        "id": "accesibilidad_voz",
        "keywords": ["accesibilidad", "voz", "asistiv", "audio", "wcag", "inclusi"],
        "plantilla": "**Accesibilidad universal y control por voz:** Implementar interfaces adaptativas bajo estándar WCAG y comandos de voz para que operadores con distintas capacidades interactúen con {tema}."
    },
    {
        "id": "automatizacion_actuadores",
        "keywords": ["actuador", "rele", "corte", "valvula", "automatico", "mecanismo", "disyuntor"],
        "plantilla": "**Automatización activa con actuadores:** Integrar corte de energía o conmutación mecánica inmediata con relés industriales cuando {tema} sobrepase los límites de seguridad."
    },
    {
        "id": "apis_abiertas",
        "keywords": ["api", "meteorolog", "clima", "geolocaliz", "opendata", "web service", "interoperab"],
        "plantilla": "**Interoperabilidad con APIs abiertas:** Cruzar la información de {tema} con fuentes externas públicas (clima, tránsito, índices comunales de Maipú) para enriquecer el contexto operativo."
    },
    {
        "id": "gemelo_digital",
        "keywords": ["gemelo", "digital twin", "simulacion", "virtual", "modelo 3d"],
        "plantilla": "**Gemelo digital y simulación virtual:** Desarrollar un modelo virtual interactivo en tiempo real que replique el comportamiento físico y dinámico de los componentes de {tema}."
    },
    {
        "id": "agentes_llm",
        "keywords": ["asistente", "chatbot", "agente", "llm", "conversacional", "soporte"],
        "plantilla": "**Agente inteligente de soporte técnico:** Integrar un asistente conversacional contextual que ayude a técnicos o usuarios a resolver problemas y diagnósticos de {tema} paso a paso."
    },
    {
        "id": "alta_disponibilidad",
        "keywords": ["failover", "alta disponibilidad", "redundancia", "toleran", "resilien"],
        "plantilla": "**Arquitectura resiliente y failover:** Diseñar redundancia a nivel de nodo o base de datos local para que {tema} no detenga sus funciones esenciales ante caídas de servidor."
    },
    {
        "id": "georreferenciacion",
        "keywords": ["gps", "mapa", "georrefer", "geolocal", "gis", "rutas"],
        "plantilla": "**Georreferenciación y mapeo GIS:** Ubicar geográficamente eventos, activos o muestreos de {tema} en mapas interactivos para optimizar cobertura y tiempos de respuesta."
    },
    {
        "id": "alertas_multicanal",
        "keywords": ["notificacion", "push", "websocket", "telegram", "sms", "alerta"],
        "plantilla": "**Alertas críticas multicanal en tiempo real:** Disparar notificaciones instantáneas de eventos anómalos de {tema} a través de WebSockets, bots de Telegram o correo electrónico."
    },
    {
        "id": "mantenimiento_vibraciones",
        "keywords": ["vibracion", "acustic", "frecuencia", "desgaste", "sonido", "mantenimiento"],
        "plantilla": "**Diagnóstico por análisis de vibraciones/acústica:** Monitorear frecuencias y patrones sonoros para predecir desgaste de piezas o descalibraciones mecánicas en {tema}."
    }
]

def extraer_tema(query: str) -> str:
    limpio = (query or "").strip()
    frases_quitar = [
        "quiero hacer un proyecto de", "quiero hacer un proyecto sobre",
        "quiero hacer una idea de", "tengo una idea de", "tengo una idea sobre",
        "mi proyecto es de", "mi idea es sobre", "se trata de", "quisiera desarrollar",
        "quiero desarrollar", "me gustaría hacer", "me gustaria hacer", "quiero hacer",
        "tengo pensado", "proyecto de", "idea de", "sistema de", "quiero crear", "como hacer"
    ]
    low = limpio.lower()
    for f in frases_quitar:
        if low.startswith(f):
            limpio = limpio[len(f):].strip()
            low = limpio.lower()
            break
    limpio = limpio.rstrip(".!?:; ")
    if len(limpio) >= 3 and len(limpio) <= 60:
        return limpio
    return "tu propuesta"

def generar_respuesta_banco(query: str, history: list, similares: list, is_followup: bool) -> str:
    tema = extraer_tema(query)
    hist_text = " ".join([getattr(h, 'content', '') if hasattr(h, 'content') else str(h.get('content', '')) for h in (history or [])]).lower()
    
    # Filtrar candidatas que no hayan aparecido en el historial
    candidatas = [item for item in BANCO_INNOVACION if not any(kw in hist_text for kw in item["keywords"])]
    if len(candidatas) < 3:
        candidatas = list(BANCO_INNOVACION)
        
    random.shuffle(candidatas)
    elegidas = candidatas[:3]
    
    if not is_followup:
        tema_display = tema.capitalize() if tema != "tu propuesta" else "Tu propuesta"
        frase_inicio = f"¡Buena idea! {tema_display} ofrece gran potencial para innovar y resolver desafíos técnicos reales."
        
        if similares:
            lista_projs = "\n".join([
                f"• \"{s.get('titulo')}\" ({s.get('carrera', 'Inacap')} · {s.get('anio', 2025)}) — {int(s.get('porcentaje_similitud', 60))}% de similitud"
                for s in similares[:3]
            ])
            bloque_sim = f"Tu idea tiene similitud con estos proyectos registrados en Inacap Sede Maipú:\n{lista_projs}"
        else:
            bloque_sim = "Tu idea se ve original y no presenta coincidencias directas en el repositorio de Inacap Sede Maipú."
            
        sug1 = elegidas[0]["plantilla"].format(tema=tema)
        sug2 = elegidas[1]["plantilla"].format(tema=tema)
        bloque_dif = f"¿Qué deberías enfocar para diferenciarte?\n• {sug1}\n• {sug2}"
        cierre = "Recuerda validar el alcance técnico y factibilidad con tu docente guía."
        
        return f"{frase_inicio}\n\n{bloque_sim}\n\n{bloque_dif}\n\n{cierre}"
    else:
        sug1 = elegidas[0]["plantilla"].format(tema=tema)
        sug2 = elegidas[1]["plantilla"].format(tema=tema)
        return f"Para profundizar y añadir nuevas capas técnicas a {tema}:\n\n• {sug1}\n• {sug2}\n\nComenta estas alternativas con tu docente guía para definir la viabilidad del anteproyecto."

# ── Voz para dispositivos ESP32 (audio PCM -> texto -> NAPI -> voz PCM) ──
import re as _re
import wave as _wave
import array as _array
import io as _io
from starlette.concurrency import run_in_threadpool
from fastapi.responses import Response

VOICE_DEVICE_KEY  = os.environ.get("VOICE_DEVICE_KEY", "")
GEMINI_STT_MODEL  = os.environ.get("GEMINI_STT_MODEL", "gemini-3.8-flash")
GEMINI_TTS_MODEL  = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
GEMINI_TTS_VOICE  = os.environ.get("GEMINI_TTS_VOICE", "Kore")
VOICE_RATE        = 16000   # Hz, mono 16 bits (igual que el ESP32)
VOICE_MAX_CHARS   = 450
voice_history: list = []


def _voice_pcm_to_wav(pcm: bytes) -> bytes:
    buf = _io.BytesIO()
    with _wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(VOICE_RATE)
        w.writeframes(pcm)
    return buf.getvalue()


def _voice_normalize(samples: "_array.array", target: float = 30000.0, max_gain: float = 60.0) -> "_array.array":
    if not samples:
        return samples
    dc = sum(samples) / len(samples)
    peak = max(abs(s - dc) for s in samples) or 1.0
    gain = min(target / peak, max_gain)
    return _array.array("h", (max(-32767, min(32767, int((s - dc) * gain))) for s in samples))


def _voice_retry(fn, intentos: int = 3):
    """Reintenta si Gemini responde 503/429 (alta demanda)."""
    for i in range(intentos):
        try:
            return fn()
        except Exception as e:
            if i == intentos - 1:
                raise
            log.warning(f"[VOZ] Gemini fallo ({e}); reintentando...")
            time.sleep(1.5)


def _voice_transcribe(pcm: bytes) -> str:
    samples = _array.array("h")
    samples.frombytes(pcm[: len(pcm) - (len(pcm) % 2)])
    wav = _voice_pcm_to_wav(_voice_normalize(samples).tobytes())
    if groq_client:
        try:
            tr = groq_client.audio.transcriptions.create(file=("voz.wav", wav, "audio/wav"), model="whisper-large-v3-turbo", language="es", response_format="text")
            texto_gq = (tr if isinstance(tr, str) else getattr(tr, "text", "") or "").strip()
            if texto_gq:
                return texto_gq
        except Exception as gq_err:
            log.warning(f"[VOZ] Groq Whisper fallo ({gq_err}), pasando a Gemini STT...")
    resp = _voice_retry(lambda: gemini_client.models.generate_content(
        model=GEMINI_STT_MODEL,
        contents=[
            genai_types.Part.from_bytes(data=wav, mime_type="audio/wav"),
            "Transcribe literalmente este audio en español de Chile. Responde SOLO con la transcripción, "
            "sin comillas ni comentarios. Si no hay voz entendible responde exactamente: [SILENCIO]",
        ],
    ))
    texto = (resp.text or "").strip()
    return "" if (not texto or "[SILENCIO]" in texto.upper()) else texto


def _voice_clean_for_speech(texto: str) -> str:
    t = _re.sub(r"https?://\S+", "", texto)
    t = _re.sub(r"[`*_#>|~\[\]{}]", "", t)
    t = _re.sub(r"^\s*[-•·\d]+[.)]?\s+", "", t, flags=_re.M)
    t = _re.sub(r"[^\w\s.,;:¿?¡!()%/\-áéíóúüñÁÉÍÓÚÜÑ]", "", t)
    t = _re.sub(r"\s+", " ", t).strip()
    if len(t) > VOICE_MAX_CHARS:
        corte = t[:VOICE_MAX_CHARS]
        ultimo = max(corte.rfind("."), corte.rfind("?"), corte.rfind("!"))
        t = corte[: ultimo + 1] if ultimo > 120 else corte
    return t


def _voice_tts(texto: str) -> bytes:
    """Texto -> PCM 16 kHz mono 16 bits (Gemini TTS entrega 24 kHz y se remuestrea)."""
    resp = _voice_retry(lambda: gemini_client.models.generate_content(
        model=GEMINI_TTS_MODEL,
        contents=texto,
        config=genai_types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=genai_types.SpeechConfig(
                voice_config=genai_types.VoiceConfig(
                    prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(voice_name=GEMINI_TTS_VOICE)
                )
            ),
        ),
    ))
    raw = resp.candidates[0].content.parts[0].inline_data.data
    src = _array.array("h")
    src.frombytes(raw[: len(raw) - (len(raw) % 2)])
    ratio = 24000 / VOICE_RATE
    n_out = int(len(src) / ratio)
    out = _array.array("h", bytes(2 * n_out))
    for i in range(n_out):
        pos = i * ratio
        idx = int(pos)
        frac = pos - idx
        a = src[idx]
        b = src[idx + 1] if idx + 1 < len(src) else a
        out[i] = int(a + (b - a) * frac)
    peak = max((abs(s) for s in out), default=1) or 1
    gain = min(31000.0 / peak, 20.0)
    return _array.array("h", (max(-32767, min(32767, int(s * gain))) for s in out)).tobytes()


def _voice_pipeline(pcm: bytes) -> bytes:
    if not gemini_client:
        raise RuntimeError("GEMINI_API_KEY no configurada")
    texto = _voice_transcribe(pcm)
    log.info(f"[VOZ] Usuario dijo: {texto!r}")
    if not texto:
        return _voice_tts("No te escuché bien. Inténtalo de nuevo.")

    req = AnalyzeRequest(
        query=texto + "\n\n(Responde para ser hablado en voz alta: maximo 3 frases cortas, sin listas ni formato.)",
        history=[ChatHistoryItem(role=h["role"], content=h["content"]) for h in voice_history[-6:]] or None,
    )
    respuesta = (analyze_project(req).get("analisis") or "").strip()
    voice_history.append({"role": "user", "content": texto})
    voice_history.append({"role": "assistant", "content": respuesta})
    del voice_history[:-12]

    hablado = _voice_clean_for_speech(respuesta) or "No tengo una respuesta para eso."
    log.info(f"[VOZ] NAPI responde: {hablado!r}")
    return _voice_tts(hablado)


@app.post("/api/voice")
async def voice_endpoint(request: Request):
    """
    Recibe audio crudo (PCM 16-bit mono 16 kHz) desde el ESP32 y devuelve la respuesta de NAPI
    como audio crudo (mismo formato) para reproducirlo directo por el parlante.
    """
    if VOICE_DEVICE_KEY and request.headers.get("x-device-key") != VOICE_DEVICE_KEY:
        raise HTTPException(status_code=401, detail="Clave de dispositivo inválida.")
    pcm = await request.body()
    if len(pcm) < VOICE_RATE * 2 // 2:  # menos de 0.5 s
        raise HTTPException(status_code=400, detail="Audio demasiado corto")
    try:
        audio = await run_in_threadpool(_voice_pipeline, pcm)
    except Exception as e:
        log.error(f"Error en /api/voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return Response(content=audio, media_type="application/octet-stream")


# ── Motor RAG y Asistente NAPI ──
@app.post("/api/analyze")
def analyze_project(req: AnalyzeRequest):
    """
    Motor RAG: Realiza búsqueda semántica vía RPC en Supabase
    y genera el diagnóstico interactivo de NAPI con límite de 16s y banco resiliente.
    """
    start_time = time.time()
    TOTAL_TIMEOUT = 16.0
    deadline = start_time + TOTAL_TIMEOUT

    def get_time_left():
        return max(0.0, deadline - time.time())

    similares = []
    top_similitud = 0.0
    nivel_riesgo = "SIN RIESGO"
    analisis_texto = ""
    fuente = "desconocido"
    is_followup = bool(req.history and len(req.history) > 0)

    try:
        # 1. Intentar búsqueda semántica con Gemini Embeddings + Supabase pgvector (solo en el primer mensaje)
        if not is_followup and gemini_client and db_anon and get_time_left() > 2.0:
            try:
                emb = get_query_embedding(req.query)
                rpc_params = {
                    "query_embedding": emb,
                    "match_threshold": req.umbral or 0.35,
                    "match_count": req.limite or 3,
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
                        res = q.limit(req.limite or 3).execute()
                        similares = res.data or []
                        for s in similares:
                            s["similitud"] = 0.65
                except Exception as txt_err:
                    log.warning(f"Búsqueda por texto también falló: {txt_err}")
                    similares = []

        if not is_followup:
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

            # Limitar a máximo 3 proyectos similares en el contexto
            similares = similares[:3]

            # Formatear contexto RAG
            if not similares:
                contexto = f"## Proyecto del estudiante\n{req.query}\n\n## Resultado RAG\nNo se encontraron proyectos con similitud suficiente en el repositorio de Inacap Sede Maipú."
            else:
                items_txt = "\n\n".join([
                    f"**Proyecto {i+1}** ({s.get('porcentaje_similitud', 60)}% similitud)\n"
                    f"- Título: {s.get('titulo', '')}\n"
                    f"- Carrera: {s.get('carrera', '')} ({s.get('anio', '')})\n"
                    f"- Autores: {s.get('autores', '')}\n"
                    f"- Resumen: {s.get('resumen', '')}"
                    for i, s in enumerate(similares)
                ])
                contexto = f"## Proyecto del estudiante\n{req.query}\n\n## Proyectos Similares en Repositorio Inacap Maipú\n{items_txt}"
        else:
            similares = []
            contexto = ""

        # 2. Obtener directriz desde Supabase (con caché y respaldo local)
        SYSTEM_PROMPT, ai_temperature = get_cloud_guideline("napi_chat_principal")

        # Construir secuencia de contenidos para Gemini (últimos 4 mensajes)
        contents_list = []
        if req.history and len(req.history) > 0:
            for item in req.history[-4:]:
                r = "user" if item.role in ["user", "human"] else "model"
                contents_list.append(genai_types.Content(
                    role=r,
                    parts=[genai_types.Part.from_text(text=item.content)]
                ))

        file_info = ""
        if req.file_name:
            file_info = f"\n\n[DOCUMENTO ADJUNTO: {req.file_name}]\nContenido:\n{req.file_content or '(Documento cargado)'}\n"

        carrera_info = f"\n[Área/Carrera del estudiante: {req.carrera}]" if req.carrera else ""

        if is_followup:
            user_prompt_content = (
                f"{req.query}{file_info}{carrera_info}\n\n"
                f"[NOTA DE CONTEXTO: Este es un mensaje de seguimiento en la conversación en curso. "
                f"Responde directamente a la consulta del estudiante. "
                f"NO repitas la lista de proyectos similares ni la introducción del primer mensaje]."
            )
        else:
            user_prompt_content = f"{req.query}{file_info}{carrera_info}\n\n[Repositorio Inacap Maipú - Proyectos detectados]:\n{contexto}"

        contents_list.append(genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=user_prompt_content)]
        ))

        def _texto_cortado(txt: str) -> bool:
            if not txt:
                return True
            t = txt.rstrip()
            return not any(t.endswith(c) for c in ('.', '!', '?', '"', '»', '”', '…', ')', '`'))

        # 0. Groq (capa rápida con gpt-oss-120b de razonamiento, con reasoning_effort='low', max_tokens=1200 y reintentos)
        if groq_client:
            gq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if req.history:
                for h in req.history[-4:]:
                    role_name = "user" if h.role in ["user", "human"] else "assistant"
                    gq_messages.append({"role": role_name, "content": h.content})
            gq_messages.append({"role": "user", "content": user_prompt_content})

            for gmod in GROQ_MODELS:
                if get_time_left() <= 1.0 or analisis_texto:
                    break

                groq_extra = {}
                if any(rm in gmod.lower() for rm in ["gpt-oss", "reason"]):
                    groq_extra = {"extra_body": {"reasoning_effort": "low"}}

                def _llamar_groq(modelo, max_tok, extra_kws):
                    t_out = min(6.0, get_time_left())
                    return groq_client.chat.completions.create(
                        model=modelo,
                        messages=gq_messages,
                        temperature=ai_temperature,
                        max_tokens=max_tok,
                        timeout=t_out,
                        **extra_kws
                    )

                try:
                    resp_gq = _llamar_groq(gmod, 1200, groq_extra)
                    finish_reason = resp_gq.choices[0].finish_reason if resp_gq.choices else None
                    raw_content = (resp_gq.choices[0].message.content or "").strip() if resp_gq.choices else ""
                    log.info(f"Groq ({gmod}) finish_reason='{finish_reason}', len={len(raw_content)}")

                    if (finish_reason == "length" or _texto_cortado(raw_content)) and get_time_left() > 2.0:
                        log.warning(f"Groq ({gmod}) respuesta cortada (finish_reason='{finish_reason}'). Reintentando con max_tokens=2000...")
                        try:
                            resp_retry = _llamar_groq(gmod, 2000, groq_extra)
                            f_reason_r = resp_retry.choices[0].finish_reason if resp_retry.choices else None
                            raw_retry = (resp_retry.choices[0].message.content or "").strip() if resp_retry.choices else ""
                            log.info(f"Groq ({gmod}) reintento corte finish_reason='{f_reason_r}', len={len(raw_retry)}")
                            if raw_retry and (not _texto_cortado(raw_retry) or len(raw_retry) > len(raw_content)):
                                raw_content = raw_retry
                                finish_reason = f_reason_r
                        except Exception as re_err:
                            log.warning(f"Error en reintento por corte de Groq: {re_err}")

                    if raw_content:
                        analisis_texto = raw_content
                        fuente = "groq"
                        log.info(f"Respuesta generada exitosamente con Groq ({gmod})")
                        break

                except Exception as gq_ex:
                    status_code = getattr(gq_ex, 'status_code', None) or getattr(getattr(gq_ex, 'response', None), 'status_code', None)
                    err_str = str(gq_ex)
                    log.warning(f"Groq ({gmod}) falló [status={status_code}]: {err_str}")

                    if "reasoning_effort" in err_str.lower() and groq_extra:
                        try:
                            resp_no_extra = _llamar_groq(gmod, 1200, {})
                            f_reason_ne = resp_no_extra.choices[0].finish_reason if resp_no_extra.choices else None
                            raw_ne = (resp_no_extra.choices[0].message.content or "").strip() if resp_no_extra.choices else ""
                            log.info(f"Groq ({gmod}) fallback sin reasoning_effort: finish_reason='{f_reason_ne}'")
                            if raw_ne:
                                analisis_texto = raw_ne
                                fuente = "groq"
                                log.info(f"Respuesta generada exitosamente con Groq ({gmod}) sin reasoning_effort")
                                break
                        except Exception as ne_err:
                            log.warning(f"Groq ({gmod}) reintento sin reasoning falló: {ne_err}")

                    is_retryable = False
                    if status_code and (status_code == 429 or 500 <= status_code < 600):
                        is_retryable = True
                    elif any(k in err_str for k in ["429", "500", "502", "503", "504", "rate_limit", "Rate limit"]):
                        is_retryable = True

                    if is_retryable and get_time_left() > 2.5:
                        log.info(f"Reintentando Groq ({gmod}) tras espera de 1.5s por rate limit/servidor...")
                        time.sleep(1.5)
                        try:
                            resp_gq = _llamar_groq(gmod, 1200, groq_extra)
                            finish_reason = resp_gq.choices[0].finish_reason if resp_gq.choices else None
                            raw_content = (resp_gq.choices[0].message.content or "").strip() if resp_gq.choices else ""
                            log.info(f"Groq ({gmod}) reintento 429/5xx finish_reason='{finish_reason}'")
                            if raw_content:
                                analisis_texto = raw_content
                                fuente = "groq"
                                log.info(f"Respuesta generada en reintento exitoso con Groq ({gmod})")
                                break
                        except Exception as gq_retry_ex:
                            status_code_r = getattr(gq_retry_ex, 'status_code', None)
                            log.warning(f"Reintento Groq ({gmod}) falló [status={status_code_r}]: {gq_retry_ex}")

        # 1. DeepSeek (solo si Groq no respondió y no está deshabilitado permanentemente)
        global DEEPSEEK_DISABLED
        if not analisis_texto and deepseek_client and not DEEPSEEK_DISABLED and get_time_left() > 1.2:
            try:
                ds_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                if req.history:
                    for h in req.history[-4:]:
                        role_name = "user" if h.role in ["user", "human"] else "assistant"
                        ds_messages.append({"role": role_name, "content": h.content})
                ds_messages.append({"role": "user", "content": user_prompt_content})

                t_out_ds = min(6.0, get_time_left())
                resp_ds = deepseek_client.chat.completions.create(
                    model=DEEPSEEK_MODEL,
                    messages=ds_messages,
                    temperature=ai_temperature,
                    max_tokens=1200,
                    timeout=t_out_ds
                )
                if resp_ds.choices and resp_ds.choices[0].message.content:
                    ds_finish = resp_ds.choices[0].finish_reason
                    log.info(f"DeepSeek ({DEEPSEEK_MODEL}) finish_reason='{ds_finish}'")
                    analisis_texto = resp_ds.choices[0].message.content.strip()
                    fuente = "deepseek"
                    log.info(f"Respuesta generada exitosamente con DeepSeek ({DEEPSEEK_MODEL})")
            except Exception as ds_ex:
                status_code = getattr(ds_ex, 'status_code', None) or getattr(getattr(ds_ex, 'response', None), 'status_code', None)
                err_str = str(ds_ex)
                log.warning(f"DeepSeek ({DEEPSEEK_MODEL}) falló [status={status_code}]: {err_str}")
                if status_code == 402 or "402" in err_str or "insufficient" in err_str.lower() or "balance" in err_str.lower() or "payment" in err_str.lower():
                    DEEPSEEK_DISABLED = True
                    log.warning("⛔ DeepSeek marcado como DESHABILITADO permanentemente por falta de saldo (402/insufficient balance)")

        # 2. Intentar con Gemini si DeepSeek no respondió y queda tiempo
        if not analisis_texto and gemini_client and get_time_left() > 1.5:
            try:
                def _llamar_gemini(mod_name):
                    try:
                        resp = gemini_client.models.generate_content(
                            model=mod_name,
                            contents=contents_list,
                            config=genai_types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=ai_temperature,
                                max_output_tokens=1200
                            )
                        )
                        return resp.text if resp and resp.text else ""
                    except Exception as e:
                        log.warning(f"Error llamando {mod_name}: {e}")
                        return ""

                t_out_gem = min(8.0, get_time_left())
                fut = gemini_executor.submit(_llamar_gemini, "gemini-3.8-flash")
                gem_res = fut.result(timeout=t_out_gem)
                if gem_res and gem_res.strip():
                    analisis_texto = gem_res.strip()
                    fuente = "gemini"
                    log.info("Respuesta generada exitosamente con Gemini (gemini-3.8-flash)")
            except Exception as ex:
                log.warning(f"Gemini falló o timeout tras {t_out_gem:.1f}s: {ex}")

        # 3. Intentar con OpenAI si Gemini no respondió y no está deshabilitado por cuota
        global OPENAI_DISABLED
        if not analisis_texto and openai_client and not OPENAI_DISABLED and get_time_left() > 1.2:
            try:
                oa_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                if req.history:
                    for h in req.history[-4:]:
                        role_name = "user" if h.role in ["user", "human"] else "assistant"
                        oa_messages.append({"role": role_name, "content": h.content})
                oa_messages.append({"role": "user", "content": user_prompt_content})

                t_out_oa = min(5.0, get_time_left())
                resp_oa = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=oa_messages,
                    temperature=ai_temperature,
                    max_tokens=1200,
                    timeout=t_out_oa
                )
                if resp_oa.choices and resp_oa.choices[0].message.content:
                    oa_finish = resp_oa.choices[0].finish_reason
                    log.info(f"OpenAI finish_reason='{oa_finish}'")
                    analisis_texto = resp_oa.choices[0].message.content.strip()
                    fuente = "openai"
                    log.info("Respuesta generada exitosamente con OpenAI gpt-4o-mini")
            except Exception as oax:
                status_code = getattr(oax, 'status_code', None) or getattr(getattr(oax, 'response', None), 'status_code', None)
                err_str = str(oax)
                log.warning(f"OpenAI error [status={status_code}]: {err_str}")
                if "insufficient_quota" in err_str.lower() or (status_code == 429 and "quota" in err_str.lower()) or status_code == 402:
                    OPENAI_DISABLED = True
                    log.warning("⛔ OpenAI marcado como DESHABILITADO permanentemente por cuota insuficiente (insufficient_quota)")

        # 4. Último recurso: Banco local con 16 ideas variadas
        if not analisis_texto:
            fuente = "banco_local"
            analisis_texto = generar_respuesta_banco(
                query=req.query,
                history=req.history or [],
                similares=similares,
                is_followup=is_followup
            )
            log.info("Respuesta generada exitosamente desde el banco local de innovación")

        elapsed = time.time() - start_time
        log.info(f"Finalizando /api/analyze en {elapsed:.2f}s con fuente='{fuente}'")
        return {
            "query": req.query,
            "top_similitud": top_similitud,
            "nivel_riesgo": nivel_riesgo,
            "similares": similares,
            "analisis": analisis_texto,
            "fuente": fuente
        }

    except Exception as e:
        log.error(f"Error general en /api/analyze: {e}")
        fuente = "banco_local"
        analisis_texto = generar_respuesta_banco(
            query=req.query,
            history=req.history or [],
            similares=similares,
            is_followup=is_followup
        )
        return {
            "query": req.query,
            "top_similitud": 40.0,
            "nivel_riesgo": "MODERADO",
            "similares": similares,
            "analisis": analisis_texto,
            "fuente": fuente
        }
# ══════════════════════════════════════════════════════════
#  SOLICITUDES DE AUTORIZACIÓN DE ACCESO Y MÉTRICAS REALES
# ══════════════════════════════════════════════════════════
class AccessRequestCreate(BaseModel):
    project_id: Optional[str] = None
    project_name: str
    carrera: Optional[str] = "General"
    student_name: str
    student_email: str
    proposito: Optional[str] = "Consulta Académica"
    motivo: str

class AccessRequestUpdate(BaseModel):
    estado: Literal["Pendiente", "Aprobada", "Rechazada"]

@app.get("/api/access-requests")
def get_access_requests(admin: AuthUser = Depends(security.require_admin)):
    client_sb = db_admin or db_anon
    if not client_sb:
        return {"requests": []}
    try:
        res = client_sb.table("napi_access_requests").select("*").order("created_at", desc=True).execute()
        return {"requests": res.data or []}
    except Exception as e:
        log.error(f"Error obteniendo solicitudes: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo solicitudes: {str(e)}")

@app.post("/api/access-requests")
def create_access_request(payload: AccessRequestCreate, user: AuthUser = Depends(security.get_current_user)):
    # Un usuario solo puede crear solicitudes a su propio nombre (el correo se toma de la sesión)
    if not user.is_admin:
        payload.student_email = user.email
    client_sb = db_admin or db_anon
    if not client_sb:
        raise HTTPException(status_code=503, detail="Servicio Supabase no configurado.")
    try:
        data = payload.model_dump()
        res = client_sb.table("napi_access_requests").insert(data).execute()
        if not res.data:
            raise HTTPException(status_code=500, detail="No se pudo registrar la solicitud en Supabase")
        return {"success": True, "request": res.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error creando solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error creando solicitud: {str(e)}")

@app.put("/api/access-requests/{req_id}")
def update_access_request(req_id: str, payload: AccessRequestUpdate, admin: AuthUser = Depends(security.require_admin)):
    client_sb = db_admin or db_anon
    if not client_sb:
        raise HTTPException(status_code=503, detail="Servicio Supabase no configurado.")
    try:
        res = client_sb.table("napi_access_requests").update({"estado": payload.estado}).eq("id", req_id).execute()
        return {"success": True, "request": res.data[0] if res.data else None}
    except Exception as e:
        log.error(f"Error actualizando solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error actualizando solicitud: {str(e)}")

@app.get("/api/metrics/summary")
def get_metrics_summary(admin: AuthUser = Depends(security.require_admin)):
    client_sb = db_admin or db_anon
    if not client_sb:
        log.warning("Error en métricas summary: cliente Supabase no inicializado")
        return {"total_consultas_ia": 0, "solicitudes_pendientes": 0}
    try:
        # Total de registros acumulados en napi_chat_history
        chat_res = client_sb.table("napi_chat_history").select("id", count="exact").execute()
        total_ia = chat_res.count if chat_res.count is not None else len(chat_res.data or [])

        # Total de solicitudes pendientes en napi_access_requests
        req_res = client_sb.table("napi_access_requests").select("id", count="exact").eq("estado", "Pendiente").execute()
        total_req = req_res.count if req_res.count is not None else len(req_res.data or [])

        return {
            "total_consultas_ia": int(total_ia),
            "solicitudes_pendientes": int(total_req)
        }
    except Exception as e:
        log.error(f"Error en métricas summary: {e}")
        return {"total_consultas_ia": 0, "solicitudes_pendientes": 0}
                       
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
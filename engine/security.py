# -*- coding: utf-8 -*-
"""
ArchivaIA · INACAP Sede Maipú
Módulo de seguridad: autenticación por token Bearer (Supabase Auth) y control de acceso por rol.

Uso en server.py:
    import security
    security.init(auth_client=db_anon or db_admin, profile_client=db_admin)

    @app.get("/api/admin/users")
    def get_users(user: security.AuthUser = Depends(security.require_admin)):
        ...
"""

import logging
import time
from dataclasses import dataclass
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status

log = logging.getLogger("ArchivaIA-API.security")

ROLE_ADMIN = "admin"
ROLE_TEACHER = "teacher"
ROLE_STUDENT = "student"

# Clientes Supabase inyectados desde server.py
_auth_client = None      # Cliente usado para validar el JWT (auth.get_user)
_profile_client = None   # Cliente con permisos para leer public.napi_usuarios

# Caché corta de tokens validados para no consultar Supabase en cada request
TOKEN_CACHE_TTL_SECONDS = 60
_token_cache: dict = {}


@dataclass
class AuthUser:
    id: str
    email: str
    role: str  # 'admin' | 'teacher' | 'student'

    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN

    @property
    def is_staff(self) -> bool:
        """Docentes y administradores CRAI."""
        return self.role in (ROLE_ADMIN, ROLE_TEACHER)


def init(auth_client=None, profile_client=None) -> None:
    """Registra los clientes Supabase que se usarán para validar sesiones."""
    global _auth_client, _profile_client
    _auth_client = auth_client
    _profile_client = profile_client or auth_client
    _token_cache.clear()


def canonical_role(raw_role: Optional[str]) -> str:
    r = (raw_role or ROLE_STUDENT).strip().lower()
    if r in ("admin", "administrador", "crai"):
        return ROLE_ADMIN
    if r in ("teacher", "docente", "profesor"):
        return ROLE_TEACHER
    return ROLE_STUDENT


def extract_bearer_token(request: Request) -> Optional[str]:
    header = request.headers.get("authorization") or ""
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def _lookup_profile_role(user_id: str, email: str) -> Optional[str]:
    if not _profile_client:
        return None
    try:
        res = (
            _profile_client.table("napi_usuarios")
            .select("rol")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        if not res.data and email:
            res = (
                _profile_client.table("napi_usuarios")
                .select("rol")
                .eq("email", email.lower())
                .limit(1)
                .execute()
            )
        if res.data:
            return res.data[0].get("rol")
    except Exception as e:
        log.warning(f"No se pudo leer el rol desde napi_usuarios: {e}")
    return None


def resolve_user(token: str) -> Optional[AuthUser]:
    """Valida el JWT contra Supabase Auth y devuelve el usuario con su rol real (desde la BD)."""
    now = time.time()
    cached = _token_cache.get(token)
    if cached and (now - cached[1]) < TOKEN_CACHE_TTL_SECONDS:
        return cached[0]

    if not _auth_client:
        log.error("Autenticación no configurada: falta cliente Supabase.")
        return None
    try:
        res = _auth_client.auth.get_user(token)
        sb_user = getattr(res, "user", None)
    except Exception as e:
        log.info(f"Token rechazado por Supabase Auth: {e}")
        return None
    if not sb_user:
        return None

    email = (getattr(sb_user, "email", "") or "").lower()
    meta = getattr(sb_user, "user_metadata", None) or {}
    # La tabla napi_usuarios es la fuente de verdad del rol; user_metadata es solo respaldo.
    raw_role = _lookup_profile_role(sb_user.id, email) or meta.get("rol")
    user = AuthUser(id=str(sb_user.id), email=email, role=canonical_role(raw_role))

    if len(_token_cache) > 1000:
        _token_cache.clear()
    _token_cache[token] = (user, now)
    return user


def get_optional_user(request: Request) -> Optional[AuthUser]:
    """Devuelve el usuario autenticado o None si la petición es anónima."""
    token = extract_bearer_token(request)
    if not token:
        return None
    return resolve_user(token)


def get_current_user(request: Request) -> AuthUser:
    """Exige una sesión válida (cabecera Authorization: Bearer <token>)."""
    token = extract_bearer_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debes iniciar sesión para realizar esta acción.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = resolve_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada. Inicia sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*roles: str) -> Callable[..., AuthUser]:
    allowed = {canonical_role(r) for r in roles}

    def dependency(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción.",
            )
        return user

    return dependency


require_admin = require_roles(ROLE_ADMIN)
require_staff = require_roles(ROLE_ADMIN, ROLE_TEACHER)

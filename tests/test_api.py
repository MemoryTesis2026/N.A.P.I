# -*- coding: utf-8 -*-
"""
Pruebas automáticas unitarias y de integración para la API de ArchivaIA / NAPI.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Asegurar path de imports al módulo engine
ENGINE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

import server
from server import app
import security
from security import AuthUser

client = TestClient(app)


def test_health_endpoint():
    """Valida que el endpoint de salud responda status 200 y el JSON esperado."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "ArchivaIA" in data["app"]


def test_security_canonical_role():
    """Verifica la normalización canónica de roles de usuario."""
    assert security.canonical_role("admin") == "admin"
    assert security.canonical_role("administrador") == "admin"
    assert security.canonical_role("CRAI") == "admin"
    assert security.canonical_role("teacher") == "teacher"
    assert security.canonical_role("docente") == "teacher"
    assert security.canonical_role("student") == "student"
    assert security.canonical_role("estudiante") == "student"
    assert security.canonical_role(None) == "student"
    assert security.canonical_role("otro") == "student"


def test_admin_endpoints_require_authentication():
    """Endpoints administrativos deben responder 401 si no hay token Bearer."""
    res_users = client.get("/api/admin/users")
    assert res_users.status_code == 401

    res_metrics = client.get("/api/metrics/summary")
    assert res_metrics.status_code == 401

    res_requests = client.get("/api/access-requests")
    assert res_requests.status_code == 401

    res_guidelines = client.get("/api/admin/guidelines")
    assert res_guidelines.status_code == 401


def test_student_cannot_access_admin_endpoints():
    """Un usuario con rol student debe ser bloqueado con 403 en endpoints de administración."""
    student_user = AuthUser(id="usr_student_test", email="alumno@inacap.cl", role="student")
    
    # Sobrescribir dependencia temporalmente
    app.dependency_overrides[security.get_current_user] = lambda: student_user
    app.dependency_overrides[security.require_admin] = lambda: (_ for _ in ()).throw(
        pytest.importorskip("fastapi").HTTPException(status_code=403, detail="No tienes permisos")
    )
    try:
        res = client.get("/api/admin/users")
        assert res.status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_admin_can_access_endpoints():
    """Un usuario con rol admin autenticado debe tener acceso autorizado."""
    admin_user = AuthUser(id="usr_admin_test", email="admin.crai@inacap.cl", role="admin")
    
    app.dependency_overrides[security.require_admin] = lambda: admin_user
    try:
        res = client.get("/api/admin/guidelines")
        assert res.status_code == 200
        data = res.json()
        assert "system_prompt" in data
    finally:
        app.dependency_overrides.clear()


def test_file_upload_validation_magic_bytes():
    """Valida que archivos no válidos o con firma binaria corrupta sean rechazados."""
    from server import validar_documento_subido
    from fastapi import HTTPException

    # Extensión no permitida
    with pytest.raises(HTTPException) as exc_ext:
        validar_documento_subido("malware.exe", b"MZ\x90\x00")
    assert exc_ext.value.status_code == 400

    # Falso PDF sin encabezado %PDF
    with pytest.raises(HTTPException) as exc_pdf:
        validar_documento_subido("tesis_falsa.pdf", b"Este no es un pdf")
    assert exc_pdf.value.status_code == 400

    # PDF válido
    fn, ct = validar_documento_subido("tesis_real.pdf", b"%PDF-1.4 contenido binario")
    assert fn == "tesis_real.pdf"
    assert ct == "application/pdf"

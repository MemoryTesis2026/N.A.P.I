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


def test_file_upload_sanitizes_unicode_filename():
    """Asegura que los nombres con tildes, eñes, espacios o símbolos se normalicen a ASCII."""
    from server import validar_documento_subido

    fn, ct = validar_documento_subido("Tesis Ingeniería Diseño (2026).pdf", b"%PDF-1.4 contenido")
    assert fn == "Tesis_Ingenieria_Diseno_2026.pdf"
    assert fn.isascii()
    assert ct == "application/pdf"

    fn_empty_stem, _ = validar_documento_subido("🚀.pdf", b"%PDF-1.4 contenido")
    assert fn_empty_stem == "documento.pdf"


def test_create_project_uploads_without_create_bucket(monkeypatch):
    """Verifica que POST /api/projects suba el archivo directamente sin invocar create_bucket()."""
    from unittest.mock import MagicMock

    staff_user = AuthUser(id="usr_teacher_test", email="docente@inacap.cl", role="teacher")
    mock_bucket = MagicMock()
    mock_bucket.get_public_url.side_effect = (
        lambda name: f"{server.SUPABASE_URL}/storage/v1/object/public/{server.SUPABASE_STORAGE_BUCKET}/{name}"
    )

    inserted_payloads = []

    def _fake_insert(payload):
        inserted_payloads.append(payload)
        exec_mock = MagicMock()
        exec_mock.execute.return_value = MagicMock(data=[{"id": 999, **payload}])
        return exec_mock

    mock_db = MagicMock()
    mock_db.storage.from_.return_value = mock_bucket
    mock_db.table.return_value.insert.side_effect = _fake_insert

    monkeypatch.setattr(server, "db_admin", mock_db)
    monkeypatch.setattr(server, "get_doc_embedding", lambda _text: [0.0] * server.EMBEDDING_DIMS)
    app.dependency_overrides[security.require_staff] = lambda: staff_user

    try:
        res = client.post(
            "/api/projects",
            data={
                "titulo": "Sistema NAPI",
                "resumen": "Resumen de prueba",
                "carrera": "Ingeniería en Informática",
                "anio": "2026",
                "autores": "Equipo Prueba",
                "nota": "6.5",
            },
            files={
                "archivo": ("Memoria Diseño 2026.pdf", b"%PDF-1.4 dummy content", "application/pdf"),
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["project"]["archivo_url"].endswith("_Memoria_Diseno_2026.pdf")
    assert len(inserted_payloads) == 1
    assert inserted_payloads[0]["archivo_url"] == body["project"]["archivo_url"]

    mock_db.storage.create_bucket.assert_not_called()
    mock_db.storage.from_.assert_called_with(server.SUPABASE_STORAGE_BUCKET)
    mock_bucket.upload.assert_called_once()
    upload_kwargs = mock_bucket.upload.call_args.kwargs
    assert upload_kwargs["path"].endswith("_Memoria_Diseno_2026.pdf")
    assert upload_kwargs["file"] == b"%PDF-1.4 dummy content"
    assert upload_kwargs["file_options"] == {"content-type": "application/pdf", "upsert": "true"}


def test_update_project_uploads_file_to_storage(monkeypatch):
    """Verifica que PUT /api/projects/{id} soporte multipart/form-data y suba el archivo a Supabase Storage."""
    from unittest.mock import MagicMock

    admin_user = AuthUser(id="usr_admin_test", email="admin@inacap.cl", role="admin")
    mock_bucket = MagicMock()
    mock_bucket.get_public_url.side_effect = (
        lambda name: f"{server.SUPABASE_URL}/storage/v1/object/public/{server.SUPABASE_STORAGE_BUCKET}/{name}"
    )

    updated_payloads = []

    def _fake_update(payload):
        updated_payloads.append(payload)
        eq_mock = MagicMock()
        eq_mock.eq.return_value.execute.return_value = MagicMock(data=[{"id": "proj-1", **payload}])
        return eq_mock

    mock_db = MagicMock()
    mock_db.storage.from_.return_value = mock_bucket
    mock_db.table.return_value.update.side_effect = _fake_update

    monkeypatch.setattr(server, "db_admin", mock_db)
    monkeypatch.setattr(server, "get_doc_embedding", lambda _text: None)
    app.dependency_overrides[security.require_admin] = lambda: admin_user

    try:
        res = client.put(
            "/api/projects/proj-1",
            data={
                "titulo": "Proyecto Actualizado",
                "resumen": "Resumen actualizado",
                "carrera": "Ingeniería en Informática",
                "anio": "2026",
                "autores": "Equipo Prueba",
                "nota": "6.8",
            },
            files={
                "archivo": ("Informe Final (2026).pdf", b"%PDF-1.4 updated content", "application/pdf"),
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["project"]["archivo_url"].endswith("_Informe_Final_2026.pdf")
    assert len(updated_payloads) == 1
    assert updated_payloads[0]["archivo_url"] == body["project"]["archivo_url"]
    assert "embedding" not in updated_payloads[0]
    mock_bucket.upload.assert_called_once()


def test_large_100mb_file_splits_and_downloads_seamlessly(monkeypatch):
    """
    Verifica que un documento de casi 100 MB (que supera el límite de 50 MB por objeto en Supabase Free)
    se divida automáticamente en fragmentos <= 40 MB en Supabase Storage y se reensamble al descargarlo.
    """
    from unittest.mock import MagicMock

    # Simular umbrales pequeños en memoria para probar el flujo multiparte sin reservar 100 MB en el test runner
    monkeypatch.setattr(server, "SUPABASE_SINGLE_OBJECT_MAX_BYTES", 100)
    monkeypatch.setattr(server, "STORAGE_PART_SIZE_BYTES", 60)

    storage_objects: dict[str, bytes] = {}
    mock_bucket = MagicMock()

    def _fake_upload(path, file, file_options=None):
        storage_objects[path] = file

    def _fake_download(path):
        return storage_objects[path]

    mock_bucket.upload.side_effect = _fake_upload
    mock_bucket.download.side_effect = _fake_download
    mock_bucket.get_public_url.side_effect = (
        lambda name: f"{server.SUPABASE_URL}/storage/v1/object/public/{server.SUPABASE_STORAGE_BUCKET}/{name}"
    )

    mock_db = MagicMock()
    mock_db.storage.from_.return_value = mock_bucket
    monkeypatch.setattr(server, "db_admin", mock_db)

    raw_pdf = b"%PDF-1.4 " + (b"A" * 150)  # 159 bytes (> 100 bytes threshold -> 3 fragmentos de 60, 60 y 39 bytes)
    url = server.upload_file_to_supabase_storage("Memoria 100MB.pdf", raw_pdf)

    assert url.endswith("_Memoria_100MB.pdf?multipart=1")
    part_keys = [k for k in storage_objects if k.startswith("parts/")]
    assert len(part_keys) == 3

    # Simular lectura del proyecto desde la tabla para probar GET /api/projects/{id}/download
    mock_db.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = MagicMock(
        data=[{"id": "proj-100mb", "titulo": "Memoria 100MB", "archivo_url": url}]
    )

    dl_res = client.get("/api/projects/proj-100mb/download")
    assert dl_res.status_code == 200
    assert dl_res.content == raw_pdf
    assert dl_res.headers["content-type"] == "application/pdf"
    assert "Memoria_100MB.pdf" in dl_res.headers.get("content-disposition", "")

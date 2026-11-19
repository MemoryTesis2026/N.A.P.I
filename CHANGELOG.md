# Changelog

Todas las modificaciones notables realizadas en el proyecto **N.A.P.I (ArchivaIA)** se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-11-18

### Añadido (Security & Hardening)
- **Módulo de Seguridad (`engine/security.py`)**:
  - Validación de sesiones con tokens Bearer (JWT) directamente contra Supabase Auth.
  - Decoradores y dependencias FastAPI `require_admin`, `require_staff` y `get_current_user`.
  - Caché de verificación de sesiones en memoria con TTL de 60 segundos para alto rendimiento.
- **Validación de Archivos Binarios**:
  - Comprobación estricta de Magic Bytes (`%PDF`, `PK\x03\x04` para DOCX y Compound Binary para DOC).
  - Límite de carga validado tanto en frontend como en backend (100 MB).
- **Aislamiento de Datos por Rol**:
  - Acceso a historiales de conversación en NAPI (`/api/chat/history`) restringido al propio usuario autenticado.
  - Ofuscación de URLs directas de documentos de tesis para perfiles con rol alumno (descarga protegida mediante solicitud al CRAI).
  - Bloqueo en servidor para evitar autorregistro en roles con privilegios de docente o administrador.
- **Control de Acceso a Endpoints Administrativos**:
  - Protección estricta en endpoints de gestión de usuarios (`/api/admin/users`), métricas (`/api/metrics/summary`), directrices (`/api/admin/guidelines`) y solicitudes (`/api/access-requests`).
- **Pruebas y Calidad**:
  - Suite de pruebas unitarias y de integración con `pytest` en `tests/test_api.py`.
  - Pipeline de CI en GitHub Actions (`.github/workflows/ci.yml`) con linting (`ruff`) y ejecución automática de pruebas.
  - Configuración de formato de líneas con `.gitattributes` y `.editorconfig`.

### Modificado
- `js/app.js`: Inyección automática de cabecera `Authorization: Bearer <token>` mediante intercepción global de `window.fetch`.
- `engine/server.py`: Políticas de CORS restringidas a orígenes autorizados y reemplazo de llamadas `print` por logging estructurado.
- `requirements.txt`: Estandarización de dependencias con rangos semánticos compatibles.

### Eliminado
- Carpeta `img/` redundante (unificada en `assets/`).
- Componente obsoleto de React `src/components/PillNav/`.

---

## [1.1.0] - 2026-11-16
### Añadido
- Soporte para hardware interactivo ESP32 vía endpoint `/api/voice` con transcripción Whisper y síntesis de voz Gemini TTS.
- Respuestas de IA estructuradas concisas sin tablas complejas adaptadas para síntesis de voz y pantallas móviles.
- Filtros por área académica y carrera en el repositorio de proyectos.

---

## [1.0.0] - 2026-11-10
### Añadido
- Lanzamiento de la plataforma N.A.P.I / ArchivaIA para INACAP Sede Maipú.
- Motor RAG con cálculo de similitud semántica de proyectos de titulación usando embeddings vectoriales.
- Panel administrativo CRAI con estadísticas y gestión de catálogos.

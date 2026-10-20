# N.A.P.I — Arquitectura de Software Enterprise
### *Núcleo Académico de Proyectos e Innovación · INACAP Sede Maipú (2026)*

Bienvenido al repositorio de diseño y arquitectura de software de **N.A.P.I**. Esta suite documental modela integralmente el sistema bajo estándares de la industria (equivalentes a especificaciones generadas en **Sparx Systems Enterprise Architect**, **TOGAF** y el modelo **C4 / UML 2.5**).

---

## 🏛️ Patrón Arquitectónico del Sistema: Arquitectura en 5 Tiers + Bloque Transversal

El sistema está estructurado formalmente bajo el patrón de **Arquitectura en Capas (Layered / N-Tier Architecture)** sobre un modelo **Cliente-Servidor (Client-Server)** desacoplado, separando estrictamente la seguridad perimetral de la lógica de dominio:

```
┌────────────────────────────────────────────────────────────────────────┐
│  TIER 1: CAPA DE PRESENTACIÓN (Presentation Tier - SPA HTML5 / CSS3)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Req: HTTPS POST/GET (JSON/Multipart, Bearer Token)
                                    │ Res: JSON (Status, JWT, Texto/Citas) [AbortController 20s]
┌───────────────────────────────────▼────────────────────────────────────┐
│  TIER 2: SEGURIDAD PERIMETRAL Y ACCESO (Security & Gateway Tier)       │
│  • Reverse Proxy / SSL (TLS 1.3)   • Middleware Seguridad (CORS/Rate)  │
│  • Validador JWT (GoTrue / RBAC)   • Gestor de Secretos (.env Vault)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ In-process / Localhost pass (Contexto saneado, UserContext)
┌───────────────────────────────────▼────────────────────────────────────┐
│  TIER 3: NEGOCIO Y APLICACIÓN (Application & Domain Tier - FastAPI)    │
│  • FastAPI Controller (server.py)  • Validador Académico (Nota >= 6.0) │
│  • Gestor de Sesiones e Historial Aislado (Estudiante, Docente, Admin) │
└───────────────────────┬───────────────────────────────┬────────────────┘
                        │ Invocación RAG                │ Multipart / Logs / CRUD
                        │ Req: Prompt, Query, Doc       │ Req: Upload S3, DML
                        │ Res: Contexto + Síntesis      │ Res: Signed URL, IDs
┌───────────────────────▼──────────────┐ ┌──────────────▼────────────────┐
│ TIER 4: INTELIGENCIA Y MOTOR RAG     │ │ TIER 5: PERSISTENCIA CLOUD     │
│ (RAG Engine Tier)                    │ │ (Data Tier - Supabase BaaS)    │
│ • ArchivaIAEngine (motor_rag.py)     │ │ • PostgreSQL 15+ & pgvector    │
│ • Embeddings 1536d (gemini-embed-2)  │ │ • Índice HNSW (vector_cosine)  │
│ • ThreadPool (Timeout 15s) Fallback  │ │ • Supabase Storage (S3 Docs)   │
└───────────────────────┬──────────────┘ │ • GoTrue Auth & Chat History   │
                        │                └───────────────────────────────┘
                        │ RPC buscar_proyectos_similares(vector 1536d)
                        │ Res: Top-K chunks + Cosine similarity score
                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│  BLOQUE TRANSVERSAL: SERVICIOS COGNITIVOS EXTERNOS (Multi-LLM)         │
│  • Intento 1: DeepSeek API (deepseek-chat) [Timeout 15s]               │
│  • Intento 2: Google Cloud Gemini Flash (2.0 / 1.5) [Fallback]         │
│  • Intento 3: OpenAI Platform API (gpt-4o-mini) [Fallback Final]       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📑 Índice de Especificaciones Arquitectónicas

Los artefactos se dividen en 5 dimensiones fundamentales de la ingeniería de software:

1. [🏛️ **01 — Diagrama de Arquitectura Global**](01_diagrama_arquitectura.md)
   - Vista C4 de Contenedores y Capas Enterprise con inclusión explícita de la **Capa de Seguridad, Identidad y Perímetro**.
   - Diagrama de flujos bidireccionales: Ingestión Upstream (Docente $\to$ Nota $\ge 6.0 \to$ S3 $\to$ Vectorial) y Consulta Downstream (Estudiante $\to$ RAG $\to$ Multi-LLM Cascada).
   - Políticas de desacoplamiento, resiliencia y SLA de timeouts.

2. [🧩 **02 — Diagrama de Componentes (UML 2.5)**](02_diagrama_componentes.md)
   - Especificación formal de subsistemas, puertos, interfaces provistas e interfaces requeridas (Lollipop & Socket).
   - Componentes perimetrales de seguridad (CORS, JWT GoTrue, RBAC, Pydantic V2, Secret Vault).
   - Desglose de conectores cloud: Groq LPU, DeepSeek, Gemini, OpenAI y Supabase BaaS.

3. [📊 **03 — Modelo de Datos y Repositorio Vectorial**](03_modelo_datos.md)
   - Diagrama Entidad-Relación (ERD) en notación Crow's Foot.
   - Modelo Híbrido Relacional + Vectorial (`pgvector` 1536 dimensiones e índice HNSW `vector_cosine_ops`).
   - Diccionario de datos exhaustivo, procedimiento almacenado RPC `buscar_proyectos_similares`, triggers y políticas de seguridad a nivel de fila (RLS).

4. [🌐 **04 — Topología de Comunicación y Red**](04_topologia_comunicacion.md)
   - Topología de despliegue físico y lógico en entornos cliente, DMZ y nube.
   - Matriz de protocolos de transporte (HTTPS, TLS 1.3, S3 Storage API, Direct PostgreSQL SSL).
   - Nodos de inferencia con SLA de timeouts y amortiguación de arranques en frío (*cold starts*).

5. [🏗️ **05 — Diagrama de Estructura y Clases**](05_diagrama_estructura.md)
   - Diagrama de Estructura Compuesta y Diagrama de Paquetes.
   - Jerarquía de clases backend (DTOs Pydantic tipados, `ArchivaIAEngine`, enrutadores) y controladores frontend SPA (`NapiClientController`, `PillNavInteractive`).

---

## 🎯 Resumen Ejecutivo de la Arquitectura

```mermaid
graph TB
    subgraph Tier1 ["TIER 1: PRESENTACIÓN (Presentation Tier)"]
        SPA["Cliente Web SPA (HTML5/CSS3)"]
        Nav["PillNav Flotante (GSAP)"]
        Speech["Web Speech Subsystem (Micrófono / Audio TTS)"]
        Access["Motor Accesibilidad CVD"]
    end

    subgraph Tier2 ["TIER 2: SEGURIDAD PERIMETRAL Y ACCESO (Security & Gateway Tier)"]
        Proxy["Reverse Proxy / SSL (TLS 1.3)"]
        SecMiddleware["Middleware Seguridad (CORS, Rate Limiting, Anti-Injection)"]
        JWTValidator["Validador Criptográfico JWT (GoTrue / RBAC)"]
        Vault["Bóveda de Secretos (.env Vault)"]
    end

    subgraph Tier3 ["TIER 3: NEGOCIO Y APLICACIÓN (Application & Domain Tier)"]
        Gateway["FastAPI Controller (server.py)"]
        AcademicValidator["Validador Académico (Nota >= 6.0)"]
        SessionMgr["Gestor de Sesiones e Historial Aislado"]
    end

    subgraph Tier4 ["TIER 4: INTELIGENCIA Y MOTOR RAG (RAG Engine Tier)"]
        Engine["Motor RAG (ArchivaIAEngine)"]
        Embedder["Generador Embeddings 1536d (gemini-embed-2)"]
        ThreadPool["ThreadPool Concurrente (15s Timeout)"]
    end

    subgraph Tier5 ["TIER 5: PERSISTENCIA CLOUD (Data Tier - Supabase BaaS)"]
        PG[("PostgreSQL 15+ & pgvector (HNSW 1536d)")]
        Storage[("Supabase Storage (Bucket proyectos-docs)")]
        AuthService["Supabase Auth (GoTrue)"]
        ChatHistoryStore[("napi_chat_history / napi_usuarios")]
    end

    subgraph ExternalTier ["BLOQUE TRANSVERSAL: SERVICIOS COGNITIVOS (Multi-LLM)"]
        DeepSeek["DeepSeek API (deepseek-chat - Intento 1)"]
        Gemini["Google Cloud Gemini Flash (Intento 2 Fallback)"]
        OpenAI["OpenAI API Platform (gpt-4o-mini - Fallback Final)"]
    end

    SPA -->|"Req: HTTPS (Payload JSON/Multipart, Bearer Token)"| Proxy
    Proxy -->|"Res: JSON (Status, JWT, Texto/Citas) [AbortController 20s]"| SPA
    Proxy --> SecMiddleware
    SecMiddleware --> JWTValidator
    JWTValidator <-->|"Verificación tokens"| AuthService
    SecMiddleware -.-> Vault

    JWTValidator -->|"In-process / Localhost pass (Contexto saneado, UserContext)"| Gateway
    Gateway <--> AcademicValidator
    Gateway <--> SessionMgr

    Gateway -->|"Req: Upload S3 / DML logs"| Storage
    Storage -->|"Res: Signed URL, IDs"| Gateway
    Gateway <-->|"Persistencia turnos aislados"| ChatHistoryStore

    Gateway -->|"Req: Prompt saneado, query semántica"| Engine
    Engine -->|"Res: Contexto recuperado + Síntesis LLM"| Gateway

    Engine -->|"Generación vector 1536d"| Embedder
    Embedder -->|"gemini-embedding-2"| Gemini
    Engine -->|"Req: Vector 1536d vía RPC buscar_proyectos_similares"| PG
    PG -->|"Res: Top-K chunks + Cosine score"| Engine

    Engine --> ThreadPool
    ThreadPool -->|"Intento 1 (Timeout 15s)"| DeepSeek
    DeepSeek -.->|"Fallback condicional"| Gemini
    Gemini -.->|"Fallback condicional"| OpenAI
```

---

## 📌 Guía de Trazabilidad con el Código Fuente

| Componente Arquitectónico | Implementación en Repositorio | Función Principal |
| :--- | :--- | :--- |
| **API Gateway & RAG Routing** | `engine/server.py` | Exposición REST, inyección de contexto y control de timeouts. |
| **Capa de Seguridad & RBAC** | `engine/server.py` | Control perimetral, tokens GoTrue, validación Pydantic y filtro de nota $\ge 6.0$. |
| **Motor Vectorial y Embeddings** | `engine/motor_rag.py` | Generación de tensores de 1536 dimensiones y fallback semántico. |
| **Población & Indexación Inicial** | `engine/seed_all_projects.py` | Vectorización en lote del catálogo histórico de INACAP Maipú. |
| **Esquema DDL & Procedimientos RPC** | `engine/archivaia_schema_gemini.sql` | Definición de tablas, índices HNSW e índices relacionales en PostgreSQL. |
| **Frontend SPA y Controladores** | `js/app.js` | Estado de la aplicación, interacción por voz, renderizado y RBAC. |
| **Controlador de Navegación** | `js/PillNav.js` | Animaciones dinámicas de interfaz con GSAP. |
| **Punto de Entrada del Servidor** | `run_server.py` | Servidor ASGI Uvicorn para despliegue local y en producción (Render). |

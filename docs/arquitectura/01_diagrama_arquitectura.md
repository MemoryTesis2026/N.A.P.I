# 01 — Diagrama de Arquitectura Global (Enterprise Architecture / C4 Model)
### *N.A.P.I — Núcleo Académico de Proyectos e Innovación · INACAP Sede Maipú*

El presente documento define la **Arquitectura Global del Sistema** siguiendo el estándar del **Modelo C4 (Nivel 2: Contenedores)** y el marco de capas del **Enterprise Architect (EA)**. La solución está diseñada bajo una arquitectura orientada a servicios desacoplada, optimizada para baja latencia, resiliencia ante arranques en frío (*cold starts*) y precisión semántica en recuperación de información.

---

## 🏛️ Diagrama de Arquitectura en Capas Enterprise

```mermaid
graph TB
    %% Definición de Estilos
    classDef actorStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef clientStyle fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef appStyle fill:#0369a1,stroke:#0284c7,stroke-width:2px,color:#ffffff;
    classDef ragStyle fill:#4338ca,stroke:#6366f1,stroke-width:2px,color:#ffffff;
    classDef dataStyle fill:#065f46,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef aiStyle fill:#701a75,stroke:#d946ef,stroke-width:2px,color:#ffffff;

    %% Actores del Negocio
    subgraph Actors ["👥 Actores del Negocio (Stakeholders INACAP)"]
        Estudiante["👨‍🎓 Estudiante INACAP\n(Valida originalidad y consulta tesis)"]:::actorStyle
        Docente["👨‍🏫 Docente / Revisor\n(Audita e indexa memorias >= 6.0)"]:::actorStyle
        Admin["👨‍💼 Administrador Sede Maipú\n(Gobernanza y gestión RBAC)"]:::actorStyle
    end

    %% Capa de Presentación
    subgraph PresentationLayer ["💻 Capa de Presentación (Presentation Tier - SPA)"]
        UI_SPA["Cliente Web SPA\n(HTML5 Semántico + CSS3 Design System)"]:::clientStyle
        UI_Audio["Subsistema de Voz y Audio\n(Web Speech API: Reconocimiento & TTS)"]:::clientStyle
        UI_Nav["Navegación Flotante y Animaciones\n(PillNav.js + GSAP GreenSock)"]:::clientStyle
        UI_Access["Módulo de Accesibilidad Universal\n(Filtros Daltonismo CVD + Alto Contraste)"]:::clientStyle
    end

    %% Capa de Aplicación y Gateway
    subgraph ApplicationLayer ["⚡ Capa de Aplicación (Application & Gateway Tier)"]
        FastAPI_Gateway["API Gateway & Controlador Central\n(engine/server.py en FastAPI 3.12 / Uvicorn)"]:::appStyle
        Security_RBAC["Módulo de Seguridad & RBAC\n(Interceptor de Roles: Estudiante, Docente, Admin)"]:::appStyle
        Doc_Manager["Gestor de Memorias & Storage\n(Validador de nota >= 6.0 y Upload Multipart)"]:::appStyle
        Chat_Manager["Gestor de Sesión & Historial de Chat\n(Aislamiento de mensajes por usuario)"]:::appStyle
    end

    %% Capa del Motor RAG
    subgraph RAGLayer ["🧠 Capa de Inteligencia y Motor RAG (RAG Engine Tier)"]
        RAG_Orchestrator["Orquestador RAG (ArchivaIAEngine)\n(Inyección de contexto, carrera y turnos)"]:::ragStyle
        ThreadPool["ThreadPoolExecutor Concurrente\n(Control de timeouts de 15s para llamadas LLM)"]:::ragStyle
        Embedding_Client["Generador de Embeddings Semánticos\n(Google gemini-embedding-2 / 1536 dimensiones)"]:::ragStyle
    end

    %% Capa de Servicios Cognitivos Externos
    subgraph CognitiveLayer ["🤖 Capa de Servicios Cognitivos Externos (AI Cloud Providers)"]
        LLM_DeepSeek["DeepSeek API\n(Motor Principal de Razonamiento)"]:::aiStyle
        LLM_Gemini["Google Gemini 2.0 / 1.5 Flash\n(Motor Secundario de Alta Concurrencia)"]:::aiStyle
        LLM_OpenAI["OpenAI GPT-4o-mini\n(Respaldo Final de Contingencia)"]:::aiStyle
    end

    %% Capa de Persistencia y Datos
    subgraph PersistenceLayer ["🐘 Capa de Persistencia y Datos (Supabase Cloud BaaS)"]
        PG_Vector[("PostgreSQL 15+ & pgvector\n(Tabla proyectos_titulo con HNSW)")]:::dataStyle
        PG_Relational[("Almacén Relacional\n(napi_chat_history & napi_usuarios)")]:::dataStyle
        Supabase_Storage[("Supabase Object Storage\n(Bucket: proyectos-docs para PDF/Word)")]:::dataStyle
        Supabase_Auth[("Supabase GoTrue Auth\n(Identidad criptográfica y JWTs)")]:::dataStyle
    end

    %% Relaciones de Actores con la UI
    Estudiante -->|"Interactúa vía web o voz"| UI_SPA
    Docente -->|"Carga memorias y evalúa notas"| UI_SPA
    Admin -->|"Gestiona usuarios y carreras"| UI_SPA

    %% Relaciones Internas de UI
    UI_SPA <--> UI_Audio
    UI_SPA <--> UI_Nav
    UI_SPA <--> UI_Access

    %% Comunicación Frontend -> Backend
    UI_SPA <-->|"REST HTTPS / JSON\n(Timeout Resiliente 20s)"| FastAPI_Gateway

    %% Flujos de Backend Internos
    FastAPI_Gateway <--> Security_RBAC
    FastAPI_Gateway <--> Doc_Manager
    FastAPI_Gateway <--> Chat_Manager
    FastAPI_Gateway <--> RAG_Orchestrator

    %% Flujo RAG
    RAG_Orchestrator -->|"1. Vectoriza texto consulta"| Embedding_Client
    Embedding_Client -->|"Solicita vector 1536d"| LLM_Gemini
    RAG_Orchestrator -->|"2. Búsqueda vectorial RPC"| PG_Vector
    RAG_Orchestrator -->|"3. Despacho concurrente"| ThreadPool

    %% Cascada de Fallbacks LLM
    ThreadPool -->|"Intento 1: DeepSeek"| LLM_DeepSeek
    LLM_DeepSeek -.->|"Fallo / Timeout"| LLM_Gemini
    LLM_Gemini -.->|"Fallo / Timeout"| LLM_OpenAI

    %% Persistencia y Datos
    Doc_Manager -->|"Sube memoria PDF/DOC"| Supabase_Storage
    Doc_Manager -->|"Registra proyecto"| PG_Vector
    Chat_Manager <-->|"Persiste turnos de chat"| PG_Relational
    Security_RBAC <-->|"Valida credenciales / JWT"| Supabase_Auth
```

---

## 🔍 Descripción de Capas y Responsabilidades

### 1. Capa de Presentación (Presentation Tier)
- **Portal SPA (Single Page Application):** Construido en HTML5 semántico y CSS3 con variables de diseño personalizadas. No requiere bundlers pesados, logrando una carga instantánea con First Contentful Paint (FCP) inferior a 400 ms.
- **Subsistema de Voz (`Web Speech API`):** Permite entrada por reconocimiento de voz continuo (`webkitSpeechRecognition`) y respuesta por síntesis de voz (`SpeechSynthesisUtterance`) para usuarios con discapacidad motora o preferencia conversacional.
- **Micro-interacciones y UI Flotante:** Implementadas mediante el controlador `PillNav.js` y la biblioteca **GSAP (GreenSock)**, proporcionando una barra de navegación con seguimiento dinámico de secciones.
- **Accesibilidad Universal (CVD):** Modos visuales adaptados para deficiencias de visión del color (Deuteranopia, Protanopia, Tritanopia y Acromatopsia) junto con bordes de alto contraste.

### 2. Capa de Aplicación y API Gateway (Application Tier)
- **FastAPI / Uvicorn Server:** Servidor asíncrono en Python 3.12 que expone endpoints RESTful bajo OpenAPI 3.0.
- **Mapeo de Rutas y Proxy Estático:** Sirve simultáneamente los activos de cliente (`/`, `/css`, `/js`, `/assets`) y los servicios de API (`/api/*`).
- **Control de Acceso Basado en Roles (RBAC):** Restricción jerárquica de operaciones según los perfiles institucionales:
  - `Estudiante`: Solo lectura de proyectos públicos y consulta a NAPI.
  - `Docente`: Capacidad de indexación y carga de documentos con validación de nota $\ge 6.0$.
  - `Administrador`: Auditoría global, CRUD de usuarios e indexación sin restricciones.

### 3. Capa de Lógica de Negocio y Motor RAG (RAG Engine Tier)
- **Vectorización Semántica:** Transforma consultas y memorias en vectores densos de **1536 dimensiones** mediante el modelo `gemini-embedding-2`, configurado con `task_type="RETRIEVAL_QUERY"` para preguntas y `task_type="RETRIEVAL_DOCUMENT"` para documentos.
- **Inyección Contextual Dinámica:** Ensambla prompts enriquecidos con:
  1. Top-K proyectos más afines recuperados por similitud coseno.
  2. Especialidad académica del estudiante (área formativa INACAP).
  3. Extracto de archivos adjuntos (PDF / DOCX / TXT).
  4. Historial conversacional reciente para soporte multi-turno.
- **Cascada de Resiliencia Multi-LLM:**
  1. Intento primario: **DeepSeek Chat API**.
  2. Fallback secundario: **Google Gemini 2.0 / 1.5 Flash**.
  3. Respaldo final: **OpenAI GPT-4o-mini**.
  - Todo orquestado mediante `ThreadPoolExecutor` con **timeout estricto de 15 segundos**.

### 4. Capa de Persistencia y Servicios en la Nube (Data & BaaS Tier)
- **Supabase Cloud (PostgreSQL 15+ con `pgvector`):** Base de datos relacional y vectorial de alto desempeño. El índice **HNSW** (`vector_cosine_ops`) permite búsquedas en sub-segundo incluso con decenas de miles de registros.
- **Supabase Storage:** Bucket S3-compatible (`proyectos-docs`) para almacenamiento seguro de las memorias de titulación con enlaces protegidos según rol.
- **Supabase Auth:** Sistema de autenticación de identidades con tokens criptográficos e integración a la tabla de metadatos `napi_usuarios`.

---

## ⏱️ Presupuesto de Tiempos y Resiliencia (SLA Arquitectónico)

| Nivel de Operación | Límite Máximo (Timeout) | Acción de Contingencia ante Excedente |
| :--- | :--- | :--- |
| **Cliente Web (`app.js`)** | **20 Segundos** | `AbortController` cancela la llamada y despliega mensaje de ayuda sin congelar la interfaz. |
| **Llamada a Modelos LLM** | **15 Segundos** | `ThreadPoolExecutor` interrumpe el intento primario y activa automáticamente el siguiente proveedor en cascada. |
| **Búsqueda Vectorial HNSW** | **100 Milisegundos** | Si falla la conexión RPC vectorial, se activa un fallback inmediato de búsqueda léxica (`ILIKE`) ponderada por palabras clave. |

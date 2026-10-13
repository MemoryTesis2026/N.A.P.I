# N.A.P.I — Repositorio Inteligente y Asistente RAG para Proyectos de Título
### *Núcleo Académico de Proyectos e Innovación · INACAP Sede Maipú (2026)*

[![INACAP Sede Maipú](https://img.shields.io/badge/Instituci%C3%B3n-INACAP%20Sede%20Maip%C3%BA-red.svg)](https://www.inacap.cl)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/IA-Google%20Gemini%20RAG-8E75C2.svg)](https://ai.google.dev/)
[![Supabase pgvector](https://img.shields.io/badge/Database-Supabase%20%2B%20pgvector-3ECF8E.svg)](https://supabase.com/)
[![License](https://img.shields.io/badge/Acceso-Acad%C3%A9mico%20Institucional-blueviolet.svg)](#)

---

## 📋 Resumen del Proyecto (Abstract)

En el ámbito de la educación superior técnico-profesional, los proyectos de titulación representan la culminación del ciclo formativo y una fuente invaluable de innovación aplicada. Sin embargo, en instituciones de gran envergadura como **INACAP Sede Maipú**, históricamente gran parte de este conocimiento ha quedado fragmentado en archivos físicos, correos electrónicos o repositorios locales aislados, lo que dificulta su consulta, propicia la duplicidad temática involuntaria y desaprovecha el valor pedagógico del trabajo previo.

**N.A.P.I** (*Núcleo Académico de Proyectos e Innovación*) es una plataforma web integral diseñada para centralizar, preservar, auditar y difundir el acervo de proyectos de título de INACAP Sede Maipú. La solución integra un **Motor RAG (Retrieval-Augmented Generation)** de última generación con **embeddings vectoriales semánticos** y un asistente conversacional interactivo (**NAPI**). A través de esta tecnología, estudiantes y docentes pueden validar ideas de tesis en tiempo real, evaluar porcentajes de similitud respecto al histórico institucional, recibir sugerencias técnicas de diferenciación e innovación adaptadas a su carrera, y gestionar la gobernanza de proyectos bajo estrictos estándares de aprobación académica.

---

## 💡 ¿Cómo Funciona N.A.P.I? (Funcionamiento Integral)

El sistema conecta una interfaz de usuario accesible y moderna con un motor de backend inteligente que combina bases de datos vectoriales e inteligencia artificial generativa. A continuación se desglosan los flujos operativos fundamentales:

```mermaid
sequenceDiagram
    autonumber
    actor Estudiante as 👨‍🎓 Estudiante / Docente
    participant UI as 💻 Frontend (Vanilla JS / Web Speech)
    participant API as ⚡ Backend FastAPI (server.py)
    participant Embed as 🧬 Google Gemini Embeddings
    participant DB as 🐘 Supabase (PostgreSQL + pgvector)
    participant LLM as 🤖 Google Gemini Flash / OpenAI

    Estudiante->>UI: Ingresa idea de tesis (texto, voz o archivo adjunto)
    UI->>API: POST /api/analyze (query, carrera, historial, archivo) con Timeout Resiliente
    
    rect rgb(240, 248, 255)
        note over API,DB: Fase 1: Recuperación Semántica (Retrieval)
        API->>Embed: Vectorizar consulta (gemini-embedding-2, 1536 dims)
        Embed-->>API: Vector denso de características
        API->>DB: RPC buscar_proyectos_similares(vector, umbral, carrera)
        DB-->>API: Top-K proyectos más afines + % similitud coseno
    end

    rect rgb(255, 250, 240)
        note over API,LLM: Fase 2: Generación Aumentada (Augmentation & Generation)
        API->>API: Inyectar contexto: Proyectos + Carrera Alumno + Archivo adjunto
        API->>LLM: Inferencia asistida por ThreadPool (gemini-2.0-flash / gemini-1.5-flash)
        LLM-->>API: Diagnóstico sintetizado (Similitud, Innovación personalizada, Siguiente paso)
    end

    API-->>UI: Respuesta JSON (diagnóstico + tarjetas de proyectos similares)
    UI-->>Estudiante: Renderizado interactivo en chat + audio TTS opcional
```

---

### 1. El Flujo del Estudiante: Validación de Propuestas en Tiempo Real
1. **Definición de Perfil y Carrera:** El estudiante indica o tiene configurada su carrera o área formativa (por ejemplo, *Ingeniería en Informática*, *Telecomunicaciones*, *Mecánica y Electromovilidad Automotriz*, etc.). Esto es crucial porque la IA no entregará recomendaciones genéricas, sino aterrizadas en las herramientas, normas y enfoques propios de su disciplina.
2. **Ingreso de la Idea:**
   - **Texto directo:** Redacción libre de la problemática o solución planteada.
   - **Documento adjunto:** Carga de anteproyectos preliminares en formato PDF, Word (DOCX) o texto plano (TXT).
   - **Entrada por Voz:** Integración nativa con la **Web Speech API** del navegador, permitiendo dictar la idea cómodamente desde cualquier dispositivo.
3. **Resiliencia en Frontend (`js/app.js`):** La petición se envía con un `AbortController` configurado con **20 segundos de margen**, protegiendo la experiencia de usuario contra arranques en frío (*cold start*) de servidores cloud en capas gratuitas (como Render) y garantizando que el usuario siempre reciba retroalimentación.

---

### 2. El Pipeline del Motor RAG en el Backend (`engine/server.py`)
Cuando la API recibe la petición en el endpoint `/api/analyze`, se ejecuta un proceso en dos etapas:

#### A. Recuperación de Información (Retrieval)
- **Vectorización Semántica:** Se limpia y envía el texto de la consulta al modelo `gemini-embedding-2` de Google Cloud con la configuración `task_type="RETRIEVAL_QUERY"`, obteniendo un vector normalizado de **1536 dimensiones**.
- **Búsqueda Vectorial por Similitud Coseno:** La API invoca la función RPC de PostgreSQL `buscar_proyectos_similares` en Supabase. Gracias al índice **HNSW** (`vector_cosine_ops`), la base de datos compara el vector con miles de proyectos aprobados en milisegundos:
  $$\text{Similitud} = 1 - \text{Distancia Coseno}(\vec{u}, \vec{v})$$
- **Clasificación del Nivel de Riesgo Institucional:**
  - 🟢 **Sin Riesgo (< 45%):** Propuesta altamente original en el contexto de la sede.
  - 🟡 **Moderado (45% – 64%):** Existen antecedentes temáticos; se sugiere enfocar la diferenciación técnica.
  - 🟠 **Alto (65% – 79%):** Coincidencia significativa con proyectos previos; se exige justificación metodológica clara.
  - 🔴 **Crítico ($\ge 80\%$):** Alta probabilidad de duplicidad temática involuntaria con tesis ya aprobadas.
- **Fallback Automático:** Si los servicios vectoriales experimentan micro-cortes, el sistema activa automáticamente un fallback de búsqueda léxica/textual ponderada en PostgreSQL para nunca dejar al alumno sin respuesta.

#### B. Generación Aumentada y Personalizada (Generation)
- **Inyección de Contexto y Carrera:** El sistema construye dinámicamente el prompt inyectando:
  1. Los proyectos más parecidos encontrados en la base de datos (Título, Carrera, Año, Autores y Resumen).
  2. El contexto explícito de la carrera o área del estudiante (`[Área/Carrera del estudiante: ...]`).
  3. El extracto de documentos adjuntos (si existen).
  4. Los últimos turnos del historial conversacional para mantener la memoria del diálogo.
- **Orquestación Concurrente y Gestión de Timeouts:** Para evitar bloqueos, las llamadas a los modelos de lenguaje se procesan mediante un `ThreadPoolExecutor` con **timeout estricto de 15 segundos**. La arquitectura implementa cascada inteligente:
  - Intento principal: `gemini-2.0-flash` (alta velocidad y razonamiento refinado).
  - Segundo intento: `gemini-1.5-flash` (alta tolerancia a latencia).
  - Respaldo final (Fallback): OpenAI `gpt-4o-mini`.
- **Estructura Estricta de la Respuesta NAPI:** El modelo está parametrizado para generar respuestas sintéticas, directas y profesionales en español chileno:
  1. **Grado de Similitud:** Porcentaje exacto y mención de las tesis antecedentes (o declaración explícita de idea 100% original).
  2. **Vías Técnicas de Innovación:** 2 puntos concretos orientados a su especialidad (sensores específicos, arquitecturas, metodologías, algoritmos o frameworks).
  3. **Paso Siguiente:** Llamado a la acción para validar el enfoque refinado con su docente guía de titulación.
- **Preguntas de Seguimiento (Follow-ups):** Si el alumno repregunta (por ejemplo: *"¿qué sensores me recomiendas?"* o *"¿cómo lo hago más innovador?"*), NAPI detecta que es una consulta de profundización y responde de manera puntual y quirúrgica, sin repetir listas de proyectos anteriores.

---

### 3. El Flujo del Docente: Aseguramiento de la Calidad y Aprobación
- **Filtro Académico Riguroso:** Para salvaguardar la excelencia del repositorio, el sistema solo permite indexar proyectos con calificación igual o superior a **6.0 ($\ge 6.0$)**.
- **Carga Rápida (Drag-and-Drop):** Los profesores pueden arrastrar memorias de titulación o completar formularios guiados.
- **Indexación Vectorial Inmediata:** Al guardar un proyecto, el backend genera el vector denso (`RETRIEVAL_DOCUMENT`) y lo almacena transaccionalmente en Supabase, dejándolo inmediatamente disponible para el motor de búsqueda semántica.

---

### 4. El Flujo del Administrador: Gobernanza y Auditoría
- **Gestión Jerárquica de Usuarios:** Altas, bajas y modificaciones de cuentas para estudiantes, docentes y coordinadores.
- **Organización por 13 Áreas INACAP:** Clasificación automática y filtrado según las áreas oficiales institucionales (Administración, Construcción, Informática y Ciberseguridad, Minería, Mecánica, etc.).
- **Auditoría e Historial:** Monitoreo de consultas en `napi_chat_history` para analizar tendencias temáticas de titulación e identificar áreas con baja tasa de innovación.

---

## 🎯 Objetivos de la Memoria / Tesis

### Objetivo General
Desarrollar e implementar una plataforma web institucional que integre un repositorio digital de proyectos de titulación y un asistente virtual basado en IA y Recuperación Aumentada por Generación (RAG), optimizando la visibilidad, gobernanza y originalidad de las propuestas académicas en INACAP Sede Maipú.

### Objetivos Específicos
1. **Centralizar y categorizar el histórico de proyectos** aprobados en las 13 áreas académicas oficiales de INACAP.
2. **Implementar una arquitectura de búsqueda semántica vectorial** utilizando modelos de lenguaje de gran escala (LLM) y la extensión `pgvector` sobre PostgreSQL.
3. **Construir el agente conversacional NAPI**, capaz de interactuar en lenguaje natural, evaluar memorias y propuestas técnicas, calcular similitud porcentual y orientar la diferenciación metodológica según la carrera del alumno.
4. **Diseñar un sistema de control de accesos basado en roles (RBAC)** con flujos especializados para Estudiantes, Docentes y Administradores.
5. **Incorporar estándares de diseño y accesibilidad universal**, incluyendo navegación interactiva moderna (PillNav), modos de alto contraste y soporte de visión para daltonismo (CVD).

---

## 🏛️ 1. Diagrama de Arquitectura Global (C4 Containers & Enterprise Layering)

El sistema implementa una **Arquitectura en Capas Enterprise** desacoplada y orientada a servicios, modelada bajo el estándar **C4 (Nivel 2: Contenedores)** y las prácticas de **Enterprise Architect**:

```mermaid
graph TB
    subgraph PresentationTier ["💻 Capa de Presentación (Presentation Tier - SPA)"]
        UI["Portal Web SPA (HTML5 Semántico + CSS3 Variables)"]
        Audio["Subsistema de Voz (Web Speech API: Micrófono & TTS)"]
        Nav["PillNav Flotante (GSAP Micro-animaciones)"]
        Access["Motor de Accesibilidad CVD (Daltonismo & Alto Contraste)"]
    end

    subgraph ApplicationTier ["⚡ Capa de Aplicación (Application & Gateway Tier)"]
        Gateway["FastAPI Gateway (server.py en Python 3.12 / Uvicorn)"]
        RBAC["Control de Acceso RBAC (Estudiante, Docente, Admin)"]
        DocManager["Gestor de Memorias & Validación (Nota >= 6.0)"]
        ChatManager["Gestor de Historial Aislado por Usuario"]
    end

    subgraph RAGTier ["🧠 Capa de Inteligencia y Motor RAG (RAG Engine Tier)"]
        RAGOrchestrator["Orquestador RAG (ArchivaIAEngine)"]
        VectorService["Generador de Embeddings Semánticos (1536 dimensiones)"]
        ThreadPool["ThreadPoolExecutor Concurrente (Control Timeout 15s)"]
    end

    subgraph AITier ["🤖 Capa de Servicios Cognitivos Externos (Multi-LLM)"]
        DeepSeek["DeepSeek API (Motor de Razonamiento Principal)"]
        Gemini["Google Gemini 2.0 / 1.5 Flash (Secundario)"]
        OpenAI["OpenAI GPT-4o-mini (Fallback de Contingencia)"]
    end

    subgraph PersistenceTier ["🐘 Capa de Persistencia Cloud (Supabase BaaS)"]
        PGVector[("PostgreSQL 15+ & pgvector (Índice HNSW Coseno)")]
        PGRelational[("Almacén Relacional (napi_chat_history & napi_usuarios)")]
        Storage[("Supabase Storage (Bucket proyectos-docs para PDF/Word)")]
        AuthService["Supabase Auth (GoTrue RBAC & JWTs)"]
    end

    UI <--> Audio
    UI <--> Nav
    UI <--> Access
    UI <-->|"HTTPS REST / JSON (Timeout Resiliente 20s)"| Gateway

    Gateway <--> RBAC
    Gateway <--> DocManager
    Gateway <--> ChatManager
    Gateway <--> RAGOrchestrator

    RAGOrchestrator -->|"1. Vectorizar texto"| VectorService
    VectorService -->|"gemini-embedding-2"| Gemini
    RAGOrchestrator -->|"2. RPC buscar_proyectos_similares"| PGVector
    RAGOrchestrator -->|"3. Inferencia asistida"| ThreadPool

    ThreadPool -->|"Intento 1"| DeepSeek
    DeepSeek -.->|"Fallback"| Gemini
    Gemini -.->|"Fallback"| OpenAI

    DocManager -->|"Subida multipart"| Storage
    DocManager -->|"Indexación"| PGVector
    ChatManager <--> PGRelational
    RBAC <--> AuthService
```

**Aspectos Clave de la Arquitectura Global:**
- **Separación de Responsabilidades:** El cliente SPA nunca interactúa directamente con los modelos de lenguaje ni posee credenciales privilegiadas; toda transacción pasa por el API Gateway en FastAPI.
- **Resiliencia ante Cold Starts:** El cliente maneja un margen de 20 segundos mediante `AbortController`, absorbiendo reinicios de servidores cloud sin interrumpir al usuario.
- **Cascada de Tolerancia a Fallos:** Despacho secuencial concurrente con timeout de 15 segundos entre DeepSeek, Google Gemini y OpenAI.

---

## 🧩 2. Diagrama de Componentes (UML 2.5 Component Specification)

Modela los subsistemas de software modulares, sus interfaces provistas (endpoints REST) y sus interfaces requeridas:

```mermaid
graph LR
    subgraph FrontendComponents ["«subsystem» Componentes Frontend"]
        C_Catalog["«component»\nCatálogo de Proyectos\n(js/app.js)"]
        C_Chat["«component»\nAsistente NAPI Chat\n(js/app.js)"]
        C_Voice["«component»\nControlador de Voz\n(Web Speech API)"]
        C_Docente["«component»\nPanel Docente\n(js/app.js)"]
        C_Admin["«component»\nPanel Administrador\n(js/app.js)"]
        C_Nav["«component»\nPillNav GSAP\n(js/PillNav.js)"]
    end

    subgraph InterfacesProvistas ["Interfaces Provistas API (RESTful Gateway)"]
        I_Analyze("(o) IAnalyzeService\nPOST /api/analyze")
        I_Projects("(o) IProjectManagement\nCRUD /api/projects")
        I_Auth("(o) IAuthManagement\n/api/auth/* & /api/admin/*")
        I_History("(o) IChatPersistence\n/api/chat/history")
    end

    subgraph BackendComponents ["«subsystem» Componentes Backend"]
        C_Gateway["«component»\nFastAPI Gateway Router\n(engine/server.py)"]
        C_Validator["«component»\nValidador de Memorias\n(Nota >= 6.0)"]
        C_RAG["«component»\nOrquestador RAG\n(ArchivaIAEngine)"]
        C_Embedder["«component»\nServicio Vectorial 1536d\n(engine/motor_rag.py)"]
        C_Dispatcher["«component»\nDespachador Multi-LLM\n(ThreadPool 15s)"]
        C_Storage["«component»\nAdaptador Supabase Storage\n(engine/server.py)"]
    end

    subgraph CloudServices ["«subsystem» Persistencia y Servicios Externos"]
        S_PG[("PostgreSQL 15 + pgvector\n(proyectos_titulo)")]
        S_Storage[("Supabase Storage\n(proyectos-docs)")]
        S_Gemini["Google Cloud GenAI\n(gemini-embedding-2)"]
        S_DeepSeek["DeepSeek Cloud API\n(deepseek-chat)"]
        S_OpenAI["OpenAI API Platform\n(gpt-4o-mini)"]
    end

    C_Chat --> I_Analyze
    C_Chat <--> C_Voice
    C_Chat --> I_History
    C_Catalog --> I_Projects
    C_Docente --> I_Projects
    C_Admin --> I_Auth
    C_Admin --> I_Projects

    I_Analyze --> C_Gateway
    I_Projects --> C_Gateway
    I_Auth --> C_Gateway
    I_History --> C_Gateway

    C_Gateway --> C_Validator
    C_Gateway --> C_RAG
    C_Gateway --> C_Storage

    C_Validator --> C_Embedder
    C_Validator --> S_PG
    C_Storage --> S_Storage

    C_RAG --> C_Embedder
    C_RAG --> C_Dispatcher
    C_RAG -->|"RPC Similitud Coseno"| S_PG

    C_Embedder --> S_Gemini
    C_Dispatcher --> S_DeepSeek
    C_Dispatcher -.-> S_Gemini
    C_Dispatcher -.-> S_OpenAI
```

**Interfaces Principales:**
- `IAnalyzeService`: Recibe la propuesta, área académica y adjunto; ejecuta el pipeline semántico RAG y retorna diagnóstico sintético.
- `IProjectManagement`: Controla altas, bajas y modificaciones de memorias de título, validando obligatoriamente que `nota >= 6.0`.
- `IChatPersistence`: Almacena y recupera los mensajes garantizando aislamiento por usuario y rol en Supabase.

---

## 📊 3. Modelo de Datos (Relational & Vectorial ERD Specification)

Diagrama Entidad-Relación en **Notación Crow's Foot** que integra el esquema relacional con la capa vectorial de `pgvector`:

```mermaid
erDiagram
    PROYECTOS_TITULO {
        uuid id PK "Identificador único (gen_random_uuid)"
        text titulo "Título del proyecto de titulación"
        text resumen "Resumen ejecutivo / abstract"
        text carrera "Carrera académica de titulación"
        int anio "Año de defensa (CHECK >= 2000 AND <= 2100)"
        text autores "Autores y tesistas de la memoria"
        vector_1536 embedding "Vector de 1536 dimensiones (gemini-embedding-2)"
        text archivo_url "URL a PDF/Word en Supabase Storage"
        text estado "Público | En Revisión | Archivado"
        text area "Una de las 13 áreas oficiales INACAP"
        text stack "Tecnologías y herramientas utilizadas"
        numeric nota "Calificación final (CHECK >= 6.0 AND <= 7.0)"
        timestamptz created_at "Fecha y hora de registro"
        timestamptz updated_at "Actualizada por Trigger set_updated_at()"
    }

    NAPI_CHAT_HISTORY {
        uuid id PK "Identificador único del mensaje"
        text user_email "Correo institucional del emisor"
        text user_role "estudiante | docente | administrador"
        text sender "user | napi | card"
        text message "Cuerpo del mensaje en texto o Markdown"
        jsonb metadata "Metadatos técnicos y contexto RAG"
        timestamptz created_at "Marca de tiempo cronológica"
    }

    NAPI_USUARIOS {
        text id PK "Identificador de usuario (auth.users)"
        text email UK "Correo institucional único"
        text nombre "Nombre completo del usuario"
        text rol "estudiante | docente | administrador"
        text area "Área académica institucional"
        text carrera "Carrera de especialidad"
        timestamptz created_at "Fecha de creación del perfil"
    }

    AUTH_USERS {
        uuid id PK "ID criptográfico de identidad GoTrue"
        varchar email "Correo de autenticación"
        varchar encrypted_password "Hash Bcrypt de contraseña"
        jsonb raw_user_meta_data "Metadatos de sesión y rol"
    }

    STORAGE_OBJECTS {
        text id PK "ID de objeto en bucket"
        text bucket_id "Bucket: proyectos-docs"
        text name "Ruta segura sanitizada de archivo"
    }

    AUTH_USERS ||--o| NAPI_USUARIOS : "extiende perfil en"
    NAPI_USUARIOS ||--o{ NAPI_CHAT_HISTORY : "posee historial aislado en"
    NAPI_USUARIOS ||--o{ PROYECTOS_TITULO : "supervisa / indexa"
    STORAGE_OBJECTS ||--o| PROYECTOS_TITULO : "vincula documento PDF/DOC en"
```

**Especificación Técnica del Almacén Vectorial:**
- **Dimensión Óptima (1536 dims):** Se utiliza `gemini-embedding-2` con `output_dimensionality = 1536`. Esto garantiza la máxima fidelidad semántica manteniéndose estrictamente por debajo del límite de 2000 dimensiones impuesto por los índices HNSW de `pgvector`.
- **Índice HNSW:**
  ```sql
  CREATE INDEX idx_proyectos_embedding_hnsw
    ON public.proyectos_titulo
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
  ```
- **Procedimiento Almacenado RPC:** `public.buscar_proyectos_similares(query_embedding vector(1536), match_threshold float, match_count int, filtro_carrera text)` calcula la similitud mediante el operador de distancia coseno `1 - (p.embedding <=> query_embedding)`.

---

## 🌐 4. Topología de Comunicación y Red (Deployment & Protocols)

Describe los nodos computacionales, fronteras de seguridad (**DMZ**), canales de transporte, protocolos y puertos involucrados:

```mermaid
graph TB
    subgraph ClientNode ["📱 Nodo Cliente (Edge User Device)"]
        ClientBrowser["Navegador Web (Chrome / Edge / Firefox)\n- Single Page Application (SPA)\n- Web Speech Subsystem (Micrófono local & TTS)\n- AbortController (Timeout 20 segundos)"]
    end

    subgraph AppServerNode ["☁️ Servidor de Aplicación (Host Local / Render Cloud PaaS)"]
        UvicornServer["Servidor ASGI Uvicorn (Puerto 8000)\n- Python 3.12 Runtime\n- FastAPI Gateway & Reverse Proxy\n- ThreadPoolExecutor Concurrente (4 Workers / Timeout 15s)"]
        EnvSecret["Bóveda de Variables (.env)\n- GEMINI_API_KEY\n- SUPABASE_SERVICE_KEY\n- DEEPSEEK_API_KEY\n- OPENAI_API_KEY"]
    end

    subgraph SupabaseCluster ["🐘 Nodo Supabase BaaS (AWS Cloud Cluster)"]
        PostgresEngine["PostgreSQL 15+ (Puerto 5432 / TLS Directo & Puerto 443)\n- Extensión pgvector con índice HNSW\n- Tablas: proyectos_titulo, napi_chat_history, napi_usuarios\n- Stored Procedure: buscar_proyectos_similares"]
        StorageEngine["Supabase Storage S3 API (Puerto 443 / HTTPS)\n- Bucket protegido: proyectos-docs (Memorias PDF/DOCX)"]
        AuthEngine["Supabase GoTrue Auth (Puerto 443 / HTTPS)\n- Criptografía de sesiones y JWTs institucionales"]
    end

    subgraph CognitiveCluster ["🤖 Nodos de Inteligencia Artificial (AI Cloud Endpoints)"]
        GoogleAPI["Google Cloud AI Studio / Vertex (Puerto 443 / TLS 1.3)\n- gemini-embedding-2 (1536 dimensiones)\n- gemini-2.0-flash / gemini-1.5-flash"]
        DeepSeekAPI["DeepSeek Cloud API (Puerto 443 / TLS 1.3)\n- deepseek-chat (Motor LLM Principal)"]
        OpenAIAPI["OpenAI API Platform (Puerto 443 / TLS 1.3)\n- gpt-4o-mini (Fallback Terciario)"]
    end

    ClientBrowser <-->|"HTTPS / TLS 1.3 (Puerto 8000 / 443)\nREST JSON & Multipart Stream (Timeout 20s)"| UvicornServer

    UvicornServer <-->|"TCP 5432 (SSL require) & HTTPS 443\nConsultas Relacionales & RPC HNSW Vectorial"| PostgresEngine
    UvicornServer <-->|"HTTPS 443 (S3 REST Protocol)\nUpload Binario Multipart"| StorageEngine
    UvicornServer <-->|"HTTPS 443\nValidación de Tokens de Sesión"| AuthEngine

    UvicornServer -->|"HTTPS 443 (SDK google-genai)\nGeneración de Embeddings 1536d"| GoogleAPI
    UvicornServer -->|"HTTPS 443 (OpenAI Compatible REST)\nInferencia LLM Primaria (Timeout 15s)"| DeepSeekAPI
    DeepSeekAPI -.->|"Conmutación automática ante fallo/timeout"| GoogleAPI
    GoogleAPI -.->|"Conmutación automática ante fallo/timeout"| OpenAIAPI
```

**Matriz de Comunicaciones y Seguridad:**
| Canal | Protocolo | Puerto | Payload / Contenido | Autenticación | SLA / Timeout |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **Cliente $\to$ FastAPI** | HTTPS / TLS 1.3 | `443` / `8000` | JSON / Multipart Form-Data | JWT / Sesión | 20s (`AbortController`) |
| **FastAPI $\to$ PostgreSQL** | Direct TCP / SSL | `5432` | Protocolo Binario pgvector / RPC | `service_role` | < 100 ms |
| **FastAPI $\to$ Supabase Storage** | HTTPS S3 REST | `443` | Stream Binario (PDF / DOCX) | `service_role` Secret | 10s |
| **FastAPI $\to$ Google AI** | HTTPS / gRPC | `443` | Vectorización 1536d | `GEMINI_API_KEY` | 3s |
| **FastAPI $\to$ DeepSeek** | HTTPS REST | `443` | Chat Completions | `DEEPSEEK_API_KEY` | 15s (`ThreadPool`) |

---

## 🏗️ 5. Diagrama de Estructura y Clases (Composite Structure & Class Hierarchy)

Modela la jerarquía de paquetes del sistema, las clases del motor RAG, los modelos de validación Pydantic y los controladores de cliente:

```mermaid
classDiagram
    class ArchivaIAEngine {
        +OpenAI openai
        +Client db_admin
        +Client db
        +generar_embedding(texto: str) list
        +generar_embedding_consulta(texto: str) list
        +buscar_proyectos_similares(query_embedding: list, umbral: float, limite: int, carrera: str) list
        +buscar_por_texto(query: str, limite: int) list
        +analizar_propuesta(query: str, carrera: str, history: list) dict
    }

    class AnalyzeRequest {
        +str query
        +float umbral
        +int limite
        +str carrera
        +List history
        +str file_name
        +str file_content
    }

    class ChatHistoryItem {
        +str role
        +str content
    }

    class ChatMessageRequest {
        +str email
        +str role
        +str sender
        +str message
        +dict metadata
    }

    class ProjectCreateRequest {
        +str titulo
        +str resumen
        +str carrera
        +int anio
        +str autores
        +float nota
        +str area
        +str stack
    }

    class LoginRequest {
        +str email
        +str password
        +str role
    }

    class RegisterRequest {
        +str email
        +str password
        +str nombre
        +str rol
        +str carrera
    }

    class NapiClientController {
        -Array activeProjects
        -Object currentAuthSession
        -AbortController currentAbort
        +init() void
        +handleLogin(email, pass, rol) void
        +submitNapiChat(prompt, attachment) void
        +startSpeechRecognition() void
        +speakUtterance(text) void
        +applyAccessibilityFilter(mode) void
        +renderProjectsCatalog(containerId) void
    }

    class PillNavInteractive {
        -HTMLElement navElement
        -Timeline gsapTimeline
        +init() void
        +animateActiveIndicator(targetPill) void
        +bindScrollSpy() void
    }

    AnalyzeRequest *-- ChatHistoryItem : "contiene lista de"
    ArchivaIAEngine ..> AnalyzeRequest : "procesa"
    ArchivaIAEngine ..> ProjectCreateRequest : "genera embedding"
    NapiClientController ..> AnalyzeRequest : "envia via REST"
    NapiClientController ..> ChatMessageRequest : "persiste via REST"
    NapiClientController ..> LoginRequest : "autentica via REST"
    NapiClientController --> PillNavInteractive : "coordina con"
```

**Detalle de Módulos y Clases:**
- **`ArchivaIAEngine` (`engine/motor_rag.py`):** Encapsula la generación de tensores de 1536 dimensiones, la invocación de la función RPC `buscar_proyectos_similares` en Supabase y el fallback léxico por texto.
- **DTOs Pydantic (`engine/server.py`):** `AnalyzeRequest`, `ProjectCreateRequest`, `ChatMessageRequest`, etc., aseguran tipificación fuerte y sanitización en tiempo de ejecución.
- **`NapiClientController` (`js/app.js`):** Gestiona el estado de la SPA, la interacción por voz con la Web Speech API, los filtros de daltonismo CVD y el renderizado dinámico de tarjetas y diagnósticos.
- **`PillNavInteractive` (`js/PillNav.js`):** Controlador de navegación flotante animado mediante **GSAP**.

---

---

## 🛠️ Tecnologías Empleadas

### **Frontend**
- **HTML5 & CSS3 Vanilla:** Estructura semántica, diseño responsivo, CSS Variables, glassmorphism y paleta corporativa moderna.
- **JavaScript Moderno (ES6+):** Programación reactiva modular (`app.js`, `PillNav.js`), manipulación de DOM sin sobrecarga de frameworks, gestión de llamadas asíncronas con `AbortController`.
- **Web Speech API:** Reconocimiento de voz por micrófono y síntesis de voz (Text-to-Speech) integrado en el asistente.
- **GSAP (GreenSock):** Micro-animaciones para el componente de navegación flotante (`PillNav`).

### **Backend**
- **Python 3.12 & FastAPI:** Framework asíncrono de alto rendimiento para exponer la API REST de búsqueda, autenticación y chat.
- **Uvicorn:** Servidor ASGI para ejecución en producción y desarrollo.
- **ThreadPoolExecutor:** Gestión concurrente de llamadas a modelos LLM con control de timeouts para evitar bloqueos del hilo principal.
- **Pydantic:** Validación estricta de esquemas de datos y peticiones HTTP.

### **Inteligencia Artificial & Base de Datos**
- **Google GenAI SDK (`google-genai`):** Embeddings de 1536 dimensiones (`gemini-embedding-2`) e inferencia con `gemini-2.0-flash` y `gemini-1.5-flash`.
- **OpenAI API (`openai`):** Motor de respaldo (fallback) con `gpt-4o-mini`.
- **Supabase (PostgreSQL 15+):** Base de datos relacional en la nube con soporte nativo de la extensión `pgvector` y Row Level Security (RLS).

---

## 🚀 Instalación y Despliegue Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/MemoryTesis2026/N.A.P.I.git
cd N.A.P.I
```

### 2. Configurar el Entorno Virtual de Python
```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Instalar dependencias del backend
pip install -r engine/requirements.txt
```

### 3. Configurar Variables de Entorno (`.env`)
Crear un archivo `.env` dentro de la carpeta `engine/` o en la raíz del proyecto:
```env
GEMINI_API_KEY=tu_api_key_de_google_ai_studio
OPENAI_API_KEY=tu_api_key_de_openai_opcional
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu_service_role_key_supabase
SUPABASE_ANON_KEY=tu_anon_key_supabase
PORT=8000
```

### 4. Configurar la Base de Datos en Supabase
1. Ingresar a la consola de [Supabase](https://supabase.com/).
2. Abrir el **SQL Editor**.
3. Ejecutar el script completo ubicado en [`engine/archivaia_schema_gemini.sql`](file:///c:/Users/franc/OneDrive/Escritorio/Pagina%20de%20N.A.P.I%20celeste/Pagina%20de%20N.A.P.I/engine/archivaia_schema_gemini.sql).
4. Opcional: Ejecutar `python engine/seed_all_projects.py` para cargar los proyectos iniciales con sus respectivos embeddings vectoriales.

### 5. Iniciar la Aplicación
#### Opción A (Windows con archivo por lotes):
Hacer doble clic en `iniciar_servidor.bat`.

#### Opción B (Línea de comandos):
```bash
python run_server.py
```
El servidor backend quedará disponible en `http://127.0.0.1:8000` y servirá el frontend automáticamente en la ruta raíz `/`.

---

## 📂 Estructura del Repositorio

```plaintext
N.A.P.I/
├── assets/                     # Recursos gráficos, fotografías del campus y fondos hero
├── css/
│   ├── PillNav.css             # Estilos de navegación flotante interactiva
│   └── styles.css              # Sistema de diseño global, modo oscuro, CVD y layout
├── engine/                     # Núcleo del servidor backend y RAG
│   ├── archivaia_schema_gemini.sql # Esquema DDL de PostgreSQL, pgvector y RPC
│   ├── motor_rag.py            # Clase principal ArchivaIAEngine para embeddings y búsqueda
│   ├── requirements.txt        # Dependencias de Python
│   ├── seed_all_projects.py    # Script de población de datos con vectorización inicial
│   └── server.py               # Servidor FastAPI con endpoints REST y lógica de negocio RAG
├── img/                        # Recursos de respaldo para visualizadores de sedes
├── js/
│   ├── PillNav.js              # Controlador JS del menú de navegación
│   └── app.js                  # Lógica del frontend (autenticación, CRUD, chat RAG, voz, timeouts)
├── src/                        # Componentes fuente reutilizables (JSX / CSS)
├── .gitignore                  # Exclusión de archivos sensibles (.env, cachés, venv)
├── index.html                  # Punto de entrada principal SPA
├── iniciar_servidor.bat        # Acceso directo para ejecución en entornos Windows
├── motor_rag.py                # Wrapper de ejecución rápida desde raíz
├── README.md                   # Documentación académica e integral del proyecto de título
└── run_server.py               # Lanzador principal ASGI con Uvicorn
```

---

## 🔒 Consideraciones de Seguridad y Ética de la Información

1. **Aislamiento de Credenciales:** Las llaves de API (`GEMINI_API_KEY`, `SUPABASE_SERVICE_KEY`) se administran estrictamente mediante variables de entorno en el servidor, sin exposición directa en el código del cliente.
2. **Políticas RLS en Base de Datos:** PostgreSQL aplica *Row Level Security*, restringiendo la inserción y modificación de proyectos únicamente a peticiones autenticadas vía `service_role`.
3. **Privacidad del Estudiante:** El historial conversacional (`napi_chat_history`) se encuentra aislado por identificador de usuario y rol, impidiendo el cruce no autorizado de consultas preliminares de titulación.
4. **Resiliencia Operativa:** Control estricto de timeouts (20s en cliente, 15s en backend) para amortiguar periodos de alta demanda o arranques en frío en infraestructuras de nube.

---

## 🎓 Autores y Agradecimientos

- **Desarrollo y Memoria de Título:** Estudiantes de Ingeniería en Informática — INACAP Sede Maipú (2026).
- **Institución:** Universidad Tecnológica de Chile INACAP · Sede Maipú.
- **Docente Guía y Comisión Evaluadora:** Área Tecnologías de la Información y Ciberseguridad.

---
*© 2026 INACAP Sede Maipú · N.A.P.I. Todos los derechos reservados.*
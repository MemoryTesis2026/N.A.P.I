# 02 — Diagrama de Componentes (UML 2.5 Component Specification)
### *N.A.P.I — Núcleo Académico de Proyectos e Innovación · INACAP Sede Maipú*

El **Diagrama de Componentes** describe la organización estructural del software, ilustrando los componentes modulares, sus dependencias internas y los contratos de interfaz (interfaces provistas y requeridas) bajo la notación estándar de **UML 2.5 / Enterprise Architect**.

---

## 🧩 Diagrama de Componentes UML

```mermaid
graph TB
    %% Estilos de Nodos
    classDef compStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef ifaceStyle fill:#334155,stroke:#a855f7,stroke-dasharray: 5 5,color:#e2e8f0;
    classDef extStyle fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;

    %% SUBSISTEMA FRONTEND
    subgraph Subsystem_Frontend ["«subsystem» Frontend Client (Vanilla Web Architecture)"]
        Comp_UI_Catalog["«component»\nCatálogo de Proyectos\n(js/app.js)"]:::compStyle
        Comp_UI_Chat["«component»\nAsistente NAPI Chat\n(js/app.js)"]:::compStyle
        Comp_UI_Voice["«component»\nControlador de Voz\n(Web Speech API)"]:::compStyle
        Comp_UI_Docente["«component»\nPanel Docente & Upload\n(js/app.js)"]:::compStyle
        Comp_UI_Admin["«component»\nPanel Administrador\n(js/app.js)"]:::compStyle
        Comp_UI_PillNav["«component»\nNavegador Flotante\n(js/PillNav.js)"]:::compStyle
        Comp_UI_Theme["«component»\nMotor de Temas y Accesibilidad\n(css/styles.css)"]:::compStyle
    end

    %% INTERFACES REST EXPUESTAS
    subgraph REST_Interfaces ["Interfaces Provistas API (RESTful Endpoints)"]
        IF_Analyze("(o) IAnalyzeService\nPOST /api/analyze"]:::ifaceStyle
        IF_Projects("(o) IProjectManagement\nGET, POST, PUT, DELETE /api/projects"]:::ifaceStyle
        IF_Auth("(o) IAuthManagement\nPOST /api/auth/login, register, users"]:::ifaceStyle
        IF_ChatHistory("(o) IChatPersistence\nGET, POST, DELETE /api/chat/history"]:::ifaceStyle
    end

    %% SUBSISTEMA BACKEND
    subgraph Subsystem_Backend ["«subsystem» Backend Application (FastAPI & RAG Engine)"]
        Comp_Gateway["«component»\nFastAPI Gateway & Router\n(engine/server.py)"]:::compStyle
        Comp_RBAC["«component»\nRBAC & Security Interceptor\n(engine/server.py)"]:::compStyle
        Comp_ProjectValidator["«component»\nValidador de Memorias & Nota >= 6.0\n(engine/server.py)"]:::compStyle
        Comp_StorageProxy["«component»\nAdaptador Supabase Storage\n(engine/server.py)"]:::compStyle
        Comp_ChatManager["«component»\nAdministrador de Historial Aislado\n(engine/server.py)"]:::compStyle
        Comp_RAGPipeline["«component»\nOrquestador RAG\n(ArchivaIAEngine)"]:::compStyle
        Comp_VectorService["«component»\nServicio de Embeddings (1536d)\n(engine/motor_rag.py)"]:::compStyle
        Comp_LLMDispatcher["«component»\nDespachador Multi-LLM en Concurrencia\n(ThreadPoolExecutor 15s)"]:::compStyle
    end

    %% SUBSISTEMA SERVICIOS EXTERNOS Y PERSISTENCIA
    subgraph Subsystem_CloudServices ["«subsystem» Persistencia y Servicios Cloud"]
        Comp_PGVector["«component»\nPostgreSQL 15 + pgvector\n(Tabla proyectos_titulo)"]:::extStyle
        Comp_PGRelational["«component»\nPostgreSQL Relational Store\n(napi_chat_history / napi_usuarios)"]:::extStyle
        Comp_RPC_Search["«component»\nProcedimiento Almacenado RPC\n(buscar_proyectos_similares)"]:::extStyle
        Comp_S3Bucket["«component»\nSupabase Storage Bucket\n(proyectos-docs)"]:::extStyle
        Comp_GoogleGenAI["«component»\nGoogle Cloud GenAI API\n(gemini-embedding-2 / Flash)"]:::extStyle
        Comp_DeepSeek["«component»\nDeepSeek Cloud API\n(deepseek-chat)"]:::extStyle
        Comp_OpenAI["«component»\nOpenAI Cloud API\n(gpt-4o-mini)"]:::extStyle
    end

    %% Conexiones Frontend a Interfaces
    Comp_UI_Chat --> IF_Analyze
    Comp_UI_Chat --> IF_ChatHistory
    Comp_UI_Chat <--> Comp_UI_Voice
    Comp_UI_Catalog --> IF_Projects
    Comp_UI_Docente --> IF_Projects
    Comp_UI_Admin --> IF_Auth
    Comp_UI_Admin --> IF_Projects
    Comp_UI_PillNav -.-> Comp_UI_Catalog

    %% Conexiones Interfaces a Backend Gateway
    IF_Analyze --> Comp_Gateway
    IF_Projects --> Comp_Gateway
    IF_Auth --> Comp_Gateway
    IF_ChatHistory --> Comp_Gateway

    %% Conexiones Internas Backend
    Comp_Gateway --> Comp_RBAC
    Comp_Gateway --> Comp_ProjectValidator
    Comp_Gateway --> Comp_StorageProxy
    Comp_Gateway --> Comp_ChatManager
    Comp_Gateway --> Comp_RAGPipeline

    Comp_ProjectValidator --> Comp_VectorService
    Comp_ProjectValidator --> Comp_StorageProxy

    Comp_RAGPipeline --> Comp_VectorService
    Comp_RAGPipeline --> Comp_LLMDispatcher

    %% Conexiones Backend a Cloud y Persistencia
    Comp_StorageProxy -->|"Sube PDF/DOC vía S3 REST"| Comp_S3Bucket
    Comp_ProjectValidator -->|"Inserta metadata y vector"| Comp_PGVector
    Comp_ChatManager <-->|"CRUD historial por usuario"| Comp_PGRelational
    Comp_RAGPipeline -->|"Ejecuta RPC búsqueda semántica"| Comp_RPC_Search
    Comp_RPC_Search -->|"Índice HNSW vector_cosine_ops"| Comp_PGVector

    Comp_VectorService -->|"Genera vector 1536d"| Comp_GoogleGenAI
    Comp_LLMDispatcher -->|"1. Inferencia principal"| Comp_DeepSeek
    Comp_LLMDispatcher -.->|"2. Fallback secundario"| Comp_GoogleGenAI
    Comp_LLMDispatcher -.->|"3. Fallback terciario"| Comp_OpenAI
```

---

## 📋 Catálogo de Componentes y Responsabilidades

### A. Componentes del Cliente Web (Frontend)

| Componente | Archivo Fuente | Descripción Funcional | Interfaces Usadas |
| :--- | :--- | :--- | :--- |
| `Comp_UI_Catalog` | `js/app.js` | Renderiza las tarjetas de proyectos con filtros dinámicos por carrera, año y búsqueda de texto. | `IProjectManagement` |
| `Comp_UI_Chat` | `js/app.js` | Gestiona el chat conversacional con NAPI, visualización de diagnósticos de riesgo y memoria de diálogo. | `IAnalyzeService`, `IChatPersistence` |
| `Comp_UI_Voice` | `Web Speech API` | Provee reconocimiento continuo por micrófono y retroalimentación acústica por síntesis de voz (TTS). | Nativa Navegador |
| `Comp_UI_Docente` | `js/app.js` | Formulario guiado de indexación con validación estricta de notas $\ge 6.0$ y drag-and-drop de archivos. | `IProjectManagement` |
| `Comp_UI_Admin` | `js/app.js` | Panel de gestión jerárquica de usuarios, asignación de áreas académicas y auditoría de la plataforma. | `IAuthManagement`, `IProjectManagement` |
| `Comp_UI_PillNav` | `js/PillNav.js` | Controlador de barra de navegación flotante interactiva con interpolaciones mediante **GSAP**. | DOM Engine |

---

### B. Componentes del Servidor de Aplicación (Backend)

| Componente | Archivo Fuente | Rol en la Arquitectura |
| :--- | :--- | :--- |
| `Comp_Gateway` | `engine/server.py` | Enrutador principal de FastAPI. Gestiona las políticas de CORS, sirve los estáticos y enruta peticiones hacia los controladores especializados. |
| `Comp_RBAC` | `engine/server.py` | Intercepta solicitudes para autenticar la identidad del usuario y garantizar que solo docentes y administradores modifiquen el repositorio. |
| `Comp_ProjectValidator` | `engine/server.py` | Aplica la regla de negocio institucional: **rechaza cualquier proyecto cuya calificación final sea inferior a 6.0**. |
| `Comp_StorageProxy` | `engine/server.py` | Controla la transferencia de memorias en formatos PDF y Word hacia el bucket protegido de Supabase Storage. |
| `Comp_ChatManager` | `engine/server.py` | Garantiza el aislamiento multi-inquilino de las conversaciones, vinculando cada mensaje con el correo institucional y rol del usuario. |
| `Comp_RAGPipeline` | `engine/motor_rag.py` | Orquesta el proceso RAG en dos tiempos: (1) recuperación semántica por similitud coseno y (2) síntesis contextual personalizada según la carrera del alumno. |
| `Comp_VectorService` | `engine/motor_rag.py` | Genera representaciones vectoriales densas de 1536 dimensiones mediante Google Cloud GenAI con truncamiento controlado. |
| `Comp_LLMDispatcher` | `engine/server.py` | Ejecuta las inferencias en hilos dedicados con timeout estricto de 15 segundos y activación secuencial de fallbacks ante contingencias. |

---

### C. Especificación de Interfaces (Contratos de Servicio)

#### 1. `IAnalyzeService`
- **Método:** `POST /api/analyze`
- **Firma del DTO Entrante:**
  ```json
  {
    "query": "string (obligatorio)",
    "umbral": "float (opcional, default: 0.40)",
    "limite": "int (opcional, default: 4)",
    "carrera": "string (opcional)",
    "history": "[{ role: string, content: string }]",
    "file_name": "string (opcional)",
    "file_content": "string (opcional)"
  }
  ```
- **Salida:** Diagnóstico sintético NAPI, porcentaje de similitud calculado, nivel de riesgo institucional y lista de proyectos más afines.

#### 2. `IProjectManagement`
- **Métodos:**
  - `GET /api/projects`: Recupera catálogo de proyectos aprobados.
  - `POST /api/projects`: Registra una nueva memoria (admite `multipart/form-data` con archivo binario o JSON directo). Valida nota $\ge 6.0$.
  - `PUT /api/projects/{id}`: Actualiza metadatos y recalcula tensores vectoriales.
  - `DELETE /api/projects/{id}`: Remueve de forma definitiva el registro del repositorio.

#### 3. `IChatPersistence`
- **Métodos:**
  - `GET /api/chat/history?email={email}&role={rol}`: Recupera turnos previos del usuario.
  - `POST /api/chat/message`: Persiste mensaje emitido por el estudiante o por NAPI.
  - `DELETE /api/chat/history`: Purga el historial del usuario solicitante.

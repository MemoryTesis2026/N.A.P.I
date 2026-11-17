# 02 — Diagrama de Componentes (UML 2.5 Component Specification)
### *N.A.P.I — Núcleo Académico de Proyectos e Innovación · INACAP Sede Maipú*

El **Diagrama de Componentes** describe la organización modular del software, ilustrando los componentes funcionales, sus dependencias internas y los contratos de interfaz (interfaces provistas y requeridas) bajo la notación estándar de **UML 2.5 / Enterprise Architect**, incorporando explícitamente el subsistema perimetral de seguridad y la orquestación multi-proveedor LLM.

---

## 🧩 Diagrama de Componentes UML

```mermaid
graph TB
    %% Estilos de Nodos
    classDef compStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef secStyle fill:#3b0764,stroke:#c084fc,stroke-width:2px,color:#ffffff;
    classDef ifaceStyle fill:#334155,stroke:#a855f7,stroke-dasharray: 5 5,color:#e2e8f0;
    classDef extStyle fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    classDef aiStyle fill:#701a75,stroke:#f472b6,stroke-width:2px,color:#ffffff;

    %% SUBSISTEMA FRONTEND
    subgraph Subsystem_Frontend ["«subsystem» Capa de Presentación (Frontend SPA)"]
        Comp_UI_Catalog["«component»\nCatálogo de Proyectos\n(js/app.js)"]:::compStyle
        Comp_UI_Chat["«component»\nAsistente NAPI Chat\n(js/app.js)"]:::compStyle
        Comp_UI_Voice["«component»\nControlador de Voz\n(Web Speech API)"]:::compStyle
        Comp_UI_Docente["«component»\nPanel Docente & Upload\n(js/app.js)"]:::compStyle
        Comp_UI_Admin["«component»\nPanel Administrador\n(js/app.js)"]:::compStyle
        Comp_UI_PillNav["«component»\nNavegador Flotante\n(js/PillNav.js)"]:::compStyle
        Comp_UI_Theme["«component»\nMotor de Accesibilidad CVD\n(css/styles.css)"]:::compStyle
    end

    %% INTERFACES REST EXPUESTAS
    subgraph REST_Interfaces ["Interfaces Provistas API (RESTful Endpoints)"]
        IF_Analyze("(o) IAnalyzeService\nPOST /api/analyze"]:::ifaceStyle
        IF_Projects("(o) IProjectManagement\nGET, POST, PUT, DELETE /api/projects"]:::ifaceStyle
        IF_Auth("(o) IAuthManagement\nPOST /api/auth/login, register, users"]:::ifaceStyle
        IF_ChatHistory("(o) IChatPersistence\nGET, POST, DELETE /api/chat/history"]:::ifaceStyle
    end

    %% SUBSISTEMA SEGURIDAD Y PERÍMETRO
    subgraph Subsystem_Security ["«subsystem» Capa de Seguridad y Control Perimetral (DMZ)"]
        Comp_CORS["«component»\nMiddleware CORS\n(FastAPI)"]:::secStyle
        Comp_PydanticValidator["«component»\nSanitizador DTOs Pydantic V2\n(Anti-Prompt Injection)"]:::secStyle
        Comp_AuthManager["«component»\nGestor de Autenticación\n(Supabase GoTrue JWT)"]:::secStyle
        Comp_RBACGuard["«component»\nInterceptor de Roles RBAC\n(Estudiante, Docente, Admin)"]:::secStyle
        Comp_SecretVault["«component»\nBóveda de Secretos\n(.env en Servidor)"]:::secStyle
    end

    %% SUBSISTEMA BACKEND Y RAG
    subgraph Subsystem_Backend ["«subsystem» Capa de Aplicación y Lógica de Negocio"]
        Comp_Gateway["«component»\nFastAPI Gateway & Router\n(engine/server.py)"]:::compStyle
        Comp_ProjectValidator["«component»\nValidador Académico Normativo (Nota >= 6.0)\n(engine/server.py)"]:::compStyle
        Comp_StorageProxy["«component»\nAdaptador Supabase Storage\n(engine/server.py)"]:::compStyle
        Comp_ChatManager["«component»\nAdministrador de Historial Aislado\n(engine/server.py)"]:::compStyle
        Comp_RAGPipeline["«component»\nOrquestador RAG\n(ArchivaIAEngine)"]:::compStyle
        Comp_VectorService["«component»\nServicio de Embeddings (1536d)\n(engine/motor_rag.py)"]:::compStyle
        Comp_LLMDispatcher["«component»\nDespachador Multi-LLM Concurrente\n(ThreadPoolExecutor 15s)"]:::compStyle
    end

    %% SUBSISTEMA PERSISTENCIA BAAS
    subgraph Subsystem_Persistence ["«subsystem» Persistencia Cloud (Supabase BaaS)"]
        Comp_PGVector["«component»\nPostgreSQL 15 + pgvector\n(Tabla proyectos_titulo + HNSW)"]:::extStyle
        Comp_PGRelational["«component»\nPostgreSQL Relational Store\n(napi_chat_history / napi_usuarios)"]:::extStyle
        Comp_RPC_Search["«component»\nProcedimiento Almacenado RPC\n(buscar_proyectos_similares)"]:::extStyle
        Comp_S3Bucket["«component»\nSupabase Storage Bucket\n(proyectos-docs)"]:::extStyle
        Comp_GoTrue["«component»\nServidor GoTrue Auth\n(Identidad criptográfica)"]:::extStyle
    end

    %% SUBSISTEMA SERVICIOS COGNITIVOS EXTERNOS
    subgraph Subsystem_Cognitive ["«subsystem» Inferencia Multi-Proveedor (Cognitive Services)"]
        Comp_Groq["«component»\nGroq Cloud LPU API\n(llama-3.3-70b-versatile - Primario)"]:::aiStyle
        Comp_DeepSeek["«component»\nDeepSeek Cloud API\n(deepseek-chat - Secundario)"]:::aiStyle
        Comp_GoogleGenAI["«component»\nGoogle Cloud GenAI API\n(gemini-embedding-2 / Flash)"]:::aiStyle
        Comp_OpenAI["«component»\nOpenAI Platform API\n(gpt-4o-mini - Respaldo)"]:::aiStyle
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

    %% Conexiones Interfaces a Capa de Seguridad
    IF_Analyze --> Comp_CORS
    IF_Projects --> Comp_CORS
    IF_Auth --> Comp_CORS
    IF_ChatHistory --> Comp_CORS

    %% Pipeline de Seguridad Perimetral
    Comp_CORS --> Comp_PydanticValidator
    Comp_PydanticValidator --> Comp_AuthManager
    Comp_AuthManager --> Comp_RBACGuard
    Comp_RBACGuard --> Comp_Gateway
    Comp_Gateway -.-> Comp_SecretVault

    %% Conexiones Internas Backend
    Comp_Gateway --> Comp_ProjectValidator
    Comp_Gateway --> Comp_StorageProxy
    Comp_Gateway --> Comp_ChatManager
    Comp_Gateway --> Comp_RAGPipeline

    Comp_ProjectValidator --> Comp_VectorService
    Comp_ProjectValidator --> Comp_StorageProxy

    Comp_RAGPipeline --> Comp_VectorService
    Comp_RAGPipeline --> Comp_LLMDispatcher

    %% Conexiones Backend a Persistencia Cloud
    Comp_StorageProxy -->|"Sube PDF/DOC vía S3 REST"| Comp_S3Bucket
    Comp_ProjectValidator -->|"Inserta metadata y vector"| Comp_PGVector
    Comp_ChatManager <-->|"CRUD historial por usuario"| Comp_PGRelational
    Comp_AuthManager <-->|"Valida firma JWT"| Comp_GoTrue
    Comp_RAGPipeline -->|"Ejecuta RPC búsqueda semántica"| Comp_RPC_Search
    Comp_RPC_Search -->|"Índice HNSW vector_cosine_ops"| Comp_PGVector

    %% Conexiones Backend a Servicios Cognitivos
    Comp_VectorService -->|"Genera vector 1536d"| Comp_GoogleGenAI
    Comp_LLMDispatcher -->|"Nivel 1 (Sub-segundo)"| Comp_Groq
    Comp_Groq -.->|"Fallback ante falla/timeout"| Comp_DeepSeek
    Comp_DeepSeek -.->|"Fallback ante saldo/timeout"| Comp_GoogleGenAI
    Comp_GoogleGenAI -.->|"Fallback ante cuota/error"| Comp_OpenAI
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
| `Comp_UI_Theme` | `css/styles.css` | Motor de variables CSS para daltonismo (CVD: Protanopia, Deuteranopia, Tritanopia, Acromatopsia) y alto contraste. | DOM Engine |

---

### B. Componentes de Seguridad y Control Perimetral (DMZ)

| Componente | Archivo Fuente | Rol en la Arquitectura |
| :--- | :--- | :--- |
| `Comp_CORS` | `engine/server.py` | Aplica cabeceras de control de acceso cruzado restrictivas para prevenir CSRF y peticiones arbitrarias. |
| `Comp_PydanticValidator` | `engine/server.py` | Deserializa payloads y sanitiza entradas textuales, neutralizando intentos de SQL Injection y Prompt Injection. |
| `Comp_AuthManager` | `engine/server.py` | Intercepta tokens Bearer (JWT) y valida firmas asimétricas contra el servicio GoTrue de Supabase. |
| `Comp_RBACGuard` | `engine/server.py` | Valida que el rol asignado (`estudiante`, `docente`, `administrador`) tenga permisos suficientes para la ruta solicitada. |
| `Comp_SecretVault` | `.env` | Almacena perimetralmente en el servidor las credenciales maestras sin exponerlas al cliente bajo ninguna circunstancia. |

---

### C. Componentes de Aplicación y RAG (Backend)

| Componente | Archivo Fuente | Rol en la Arquitectura |
| :--- | :--- | :--- |
| `Comp_Gateway` | `engine/server.py` | Enrutador principal de FastAPI. Sirve estáticos y enruta peticiones hacia los controladores especializados. |
| `Comp_ProjectValidator` | `engine/server.py` | Aplica la regla institucional estricta de INACAP: **rechaza cualquier proyecto cuya nota final sea inferior a 6.0**. |
| `Comp_StorageProxy` | `engine/server.py` | Controla la transferencia binaria de memorias (PDF y Word) hacia el bucket `proyectos-docs` de Supabase Storage. |
| `Comp_ChatManager` | `engine/server.py` | Garantiza el aislamiento multi-inquilino de las conversaciones, vinculando cada mensaje con el correo institucional y rol del usuario. |
| `Comp_RAGPipeline` | `engine/motor_rag.py` | Orquesta el proceso RAG: recuperación semántica por similitud coseno e inyección de contexto según especialidad. |
| `Comp_VectorService` | `engine/motor_rag.py` | Genera representaciones vectoriales densas de 1536 dimensiones mediante Google Cloud GenAI con truncamiento controlado. |
| `Comp_LLMDispatcher` | `engine/server.py` | Despacha llamadas en hilos paralelos con timeout de 15s y cascada: **Groq $\to$ DeepSeek $\to$ Gemini $\to$ OpenAI**. |

---

### D. Especificación de Interfaces (Contratos de Servicio)

#### 1. `IAnalyzeService`
- **Método:** `POST /api/analyze`
- **Firma del DTO Entrante (`AnalyzeRequest`):**
  ```json
  {
    "query": "string (obligatorio)",
    "umbral": "float (opcional, default: 0.40)",
    "limite": "int (opcional, default: 4)",
    "carrera": "string (opcional)",
    "history": "[{ \"role\": \"user|model\", \"content\": \"string\" }]",
    "file_name": "string (opcional)",
    "file_content": "string (opcional)"
  }
  ```
- **Salida:** Diagnóstico sintético NAPI, porcentaje de similitud calculado, nivel de riesgo institucional y lista de proyectos antecedentes con enlaces directos al documento PDF en Supabase Storage.

#### 2. `IProjectManagement`
- **Métodos:**
  - `GET /api/projects?role={rol}`: Recupera catálogo de proyectos aprobados (si `role=estudiante`, filtra solo los públicos).
  - `POST /api/projects`: Registra una nueva memoria (soporta `multipart/form-data` con archivo binario y metadatos). Valida obligatoriamente `nota >= 6.0`.
  - `PUT /api/projects/{id}`: Actualiza metadatos y recalcula tensores vectoriales.
  - `DELETE /api/projects/{id}`: Remueve de forma definitiva el registro del repositorio y su archivo asociado en Supabase Storage.

#### 3. `IAuthManagement`
- **Métodos:**
  - `POST /api/auth/login`: Autentica credenciales contra Supabase Auth y entrega perfil con JWT.
  - `POST /api/auth/register`: Registra un nuevo usuario asociando su rol y carrera institucional.
  - `GET /api/admin/users`: Consulta la lista de usuarios y roles (restringido a `administrador`).

#### 4. `IChatPersistence`
- **Métodos:**
  - `GET /api/chat/history?email={email}&role={rol}`: Recupera turnos previos del usuario aislado por sesión.
  - `POST /api/chat/message`: Persiste mensaje emitido por el estudiante o por NAPI.
  - `DELETE /api/chat/history`: Purga el historial del usuario solicitante.

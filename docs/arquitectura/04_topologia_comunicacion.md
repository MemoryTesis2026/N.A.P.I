# 04 — Topología de Comunicación y Red (Deployment & Network Architecture)
### *N.A.P.I — Núcleo Académico de Proyectos e Innovación · INACAP Sede Maipú*

La **Topología de Comunicación y Red** describe los nodos computacionales físicos y virtuales que componen la infraestructura de N.A.P.I, los canales de interconexión, los protocolos de transporte, los puertos involucrados y las fronteras de seguridad de red (**DMZ**, entornos seguros de backend y servicios gestionados en la nube).

---

## 🌐 Diagrama de Topología de Red y Despliegue Físico/Lógico

```mermaid
graph TB
    %% Estilos de Nodos de Infraestructura
    classDef clientNode fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef dmzNode fill:#3b0764,stroke:#c084fc,stroke-width:2px,color:#ffffff;
    classDef appNode fill:#0369a1,stroke:#0ea5e9,stroke-width:2px,color:#ffffff;
    classDef dbNode fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef cloudAINode fill:#581c87,stroke:#f472b6,stroke-width:2px,color:#ffffff;

    %% NODO CLIENTE
    subgraph Node_Client ["📱 Nodo de Usuario Final (Client Edge / Endpoints)"]
        Browser["Navegador Web Moderno (Chrome, Edge, Firefox)\n- Runtime: JavaScript ES6+ (SPA)\n- Web Speech Subsystem (Micrófono local & Síntesis)\n- AbortController (Timeout de 20 segundos)"]:::clientNode
    end

    %% ZONA DMZ Y PASARELA DE SEGURIDAD
    subgraph Node_DMZ ["🛡️ Perímetro DMZ & Pasarela de Seguridad Perimetral"]
        CORSControl["Control CORS & Cabeceras HTTP Restrictivas"]:::dmzNode
        PydanticSanitize["Sanitizador Tipado Pydantic V2\n(Anti-SQL Injection & Anti-Prompt Injection)"]:::dmzNode
        TokenValidator["Verificador Criptográfico JWT (GoTrue)"]:::dmzNode
    end

    %% NODO SERVIDOR DE APLICACIÓN
    subgraph Node_AppServer ["☁️ Nodo de Aplicación (Application Server / Render PaaS / Localhost)"]
        Uvicorn["Servidor ASGI Uvicorn (Puerto 8000)\n- Runtime: Python 3.12 (Linux / Windows)\n- FastAPI Gateway (Reverse Proxy / Routing)\n- ThreadPoolExecutor Concurrente (4 Workers / Timeout 15s)"]:::appNode
        EnvFile["Bóveda de Variables de Entorno (.env)\n- GROQ_API_KEY / GROQ_MODELS\n- DEEPSEEK_API_KEY / DEEPSEEK_MODEL\n- GEMINI_API_KEY\n- SUPABASE_SERVICE_KEY / SUPABASE_ANON_KEY"]:::appNode
    end

    %% ZONA CLOUD BAAS SUPABASE
    subgraph Node_SupabaseCloud ["🐘 Nodo de Persistencia Cloud (Supabase BaaS / AWS Cluster)"]
        PG_Instance["Clúster PostgreSQL 15+ (Puerto 5432 SSL & Puerto 443)\n- Motor Vectorial pgvector (HNSW Index)\n- Tablas: proyectos_titulo, napi_chat_history, napi_usuarios\n- Stored Procedure: buscar_proyectos_similares\n- Políticas Row Level Security (RLS)"]:::dbNode
        Storage_Gateway["Supabase Storage Service (Puerto 443)\n- Protocolo S3-Compatible REST\n- Bucket: proyectos-docs (Memorias PDF/DOCX)"]:::dbNode
        Auth_GoTrue["Servidor GoTrue Auth (Puerto 443)\n- Gestión de JWTs y Sesiones Criptográficas"]:::dbNode
    end

    %% ZONA DE SERVICIOS COGNITIVOS EN LA NUBE
    subgraph Node_CognitiveCloud ["🤖 Nodos de Inteligencia Artificial (Multi-LLM Cloud Providers)"]
        Groq_AI["Groq Cloud LPU API (Puerto 443 / TLS 1.3)\n- llama-3.3-70b-versatile (Inferencia Sub-Segundo)"]:::cloudAINode
        DeepSeek_AI["DeepSeek Cloud API (Puerto 443 / TLS 1.3)\n- deepseek-chat (Motor Secundario de Razonamiento)"]:::cloudAINode
        Google_AI["Google Cloud AI Studio / Vertex (Puerto 443 / TLS 1.3)\n- gemini-embedding-2 (1536 dimensiones)\n- gemini-2.0-flash / gemini-1.5-flash (Inferencia Terciaria)"]:::cloudAINode
        OpenAI_AI["OpenAI API Platform (Puerto 443 / TLS 1.3)\n- gpt-4o-mini (Fallback final de contingencia)"]:::cloudAINode
    end

    %% CANALES DE COMUNICACIÓN Y PROTOCOLOS
    Browser <-->|"HTTPS / TLS 1.3 (Puerto 8000 / 443)\nREST JSON & Multipart Upload\nTimeout Máximo: 20s"| Node_DMZ

    Node_DMZ <-->|"Tráfico Filtrado & Sanitizado"| Uvicorn
    Uvicorn -.->|"Lectura Segura de Secretos"| EnvFile

    Uvicorn <-->|"TCP 5432 (SSL require) & HTTPS 443\nConsultas DDL / RPC HNSW / RLS"| PG_Instance
    Uvicorn <-->|"HTTPS 443 (S3 API REST)\nUpload Multipart Binario & Download Stream"| Storage_Gateway
    Uvicorn <-->|"HTTPS 443\nVerificación y Validación de Tokens JWT"| Auth_GoTrue

    Uvicorn -->|"HTTPS 443 (OpenAI Compatible REST)\nInferencia Primaria Sub-Segundo (Timeout 15s)"| Groq_AI
    Groq_AI -.->|"Conmutación automática ante fallo/timeout"| DeepSeek_AI
    DeepSeek_AI -.->|"Conmutación automática ante saldo/timeout"| Google_AI
    Google_AI -.->|"Conmutación automática ante cuota/timeout"| OpenAI_AI

    Uvicorn -->|"HTTPS / gRPC (Puerto 443)\nSDK google-genai\nVectorización 1536d"| Google_AI
```

---

## 📊 Matriz de Comunicaciones y Protocolos de Red

| Flujo / Canal | Origen | Destino | Protocolo / Transporte | Puerto | Formato Payload | Autenticación | SLA / Timeout |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :---: |
| **C1: Interacción de Usuario** | Navegador Web | Perímetro DMZ | **HTTPS / TLS 1.3** | `443` / `8000` | JSON / Form-Data | Bearer Token / Cookie | 20s (`AbortController`) |
| **C2: Audio y Reconocimiento** | Micrófono Usuario | Motor Web Speech | **Internal OS API** | N/A | PCM Audio Stream | Permiso de Navegador | Inmediato |
| **C3: Vectorización Semántica** | Servidor FastAPI | Google AI Studio | **HTTPS / REST** | `443` | JSON (Texto $\to$ 1536d) | `GEMINI_API_KEY` | 3s |
| **C4: Búsqueda Vectorial HNSW** | Servidor FastAPI | PostgreSQL Supabase | **Direct PostgreSQL / TLS** | `5432` | Binary pgvector RPC | `SUPABASE_SERVICE_KEY` | < 100 ms |
| **C5: Inferencia Primaria (Groq)**| Servidor FastAPI | Groq Cloud LPU | **HTTPS / REST** | `443` | JSON (Chat Completions) | `GROQ_API_KEY` | 15s (`ThreadPool`) |
| **C6: Fallback Secundario** | Servidor FastAPI | DeepSeek API | **HTTPS / REST** | `443` | JSON (Chat Completions) | `DEEPSEEK_API_KEY` | 15s (`ThreadPool`) |
| **C7: Fallback Terciario** | Servidor FastAPI | Google Gemini API | **HTTPS / gRPC** | `443` | JSON (Generate Content) | `GEMINI_API_KEY` | 15s (`ThreadPool`) |
| **C8: Fallback de Emergencia** | Servidor FastAPI | OpenAI API | **HTTPS / REST** | `443` | JSON (Chat Completions) | `OPENAI_API_KEY` | 12s |
| **C9: Subida de Memorias PDF** | Servidor FastAPI | Supabase Storage | **HTTPS / S3 REST** | `443` | Binary Multipart Stream | `service_role` Secret | 10s |
| **C10: Historial Conversacional**| Servidor FastAPI | PostgreSQL Supabase | **HTTPS / PostgREST** | `443` | JSON (Insert / Select) | `SUPABASE_ANON_KEY` | 500 ms |

---

## 🛡️ Zonas de Seguridad y Políticas de Protección Perimetral

### 1. Perímetro de Cliente (Untrusted Edge)
- Todo el código JavaScript en el navegador del usuario se ejecuta en el espacio de aislamiento del navegador (*sandbox*).
- **Cero Exposición de Secretos:** El cliente **nunca** posee las llaves maestras de Groq, DeepSeek, Gemini, OpenAI ni la `service_role` de Supabase. Cualquier transacción privilegiada viaja obligatoriamente a través del servidor FastAPI.

### 2. Zona DMZ y Control Perimetral
- **FastAPI** actúa como barrera de sanitización y cortafuegos de aplicación.
- Políticas de **CORS** explícitas para permitir consumo controlado desde dominios institucionales autorizados.
- Validación de esquemas y tipos en tiempo de compilación/ejecución mediante **Pydantic V2**.
- Inyección de variables de entorno mediante archivos locales protegidos con permisos de lectura restringidos (`chmod 600` en producción).

### 3. Zona Privada de Persistencia (Secure Cloud BaaS)
- Acceso directo a base de datos cifrado mediante **SSL/TLS**.
- Activación de **Row Level Security (RLS)** en PostgreSQL: aunque un usuario malicioso interceptase la clave anónima (`SUPABASE_ANON_KEY`), no puede alterar proyectos aprobados ni manipular calificaciones.
- La inserción de proyectos está reservada al canal autenticado con la llave `SUPABASE_SERVICE_KEY`.

---

## ⚡ Mitigación de Arranques en Frío (*Cold Starts*) y Latencia

Al desplegar en plataformas cloud con contenedores que se suspenden por inactividad (como la capa gratuita de Render):
1. **Margen Resiliente de 20 Segundos en Frontend:** El cliente (`app.js`) configura el `AbortController` con una ventana de tolerancia de 20.000 ms, evitando que un arranque en frío de 8 a 12 segundos corte la experiencia del estudiante.
2. **Inferencia de Ultra-Baja Latencia con Groq:** El LPU de Groq procesa los tokens de respuesta a más de 250 tokens/segundo, reduciendo el tiempo de generación final a menos de 800 ms una vez activo el servidor.
3. **Casacada de Contingencia:** Si cualquiera de las APIs presenta congestión de red o límite de cuota, el sistema conmuta automáticamente en cascada sin notificar un error fatal al usuario.

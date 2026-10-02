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

**N.A.P.I** (*Núcleo Académico de Proyectos e Innovación*) es una plataforma web integral diseñada para centralizar, preservar, auditar y difundir el acervo de proyectos de título de INACAP Sede Maipú. La solución integra un **Motor RAG (Retrieval-Augmented Generation)** de última generación con **embeddings vectoriales semánticos** y un asistente conversacional interactivo (**NAPI**). A través de esta tecnología, estudiantes y docentes pueden validar ideas de tesis en tiempo real, evaluar porcentajes de similitud respecto al histórico institucional, recibir sugerencias técnicas de diferenciación e innovación, y gestionar la gobernanza de proyectos bajo estrictos estándares de aprobación académica.

---

## 🎯 Objetivos de la Memoria / Tesis

### Objetivo General
Desarrollar e implementar una plataforma web institucional que integre un repositorio digital de proyectos de titulación y un asistente virtual basado en IA y Recuperación Aumentada por Generación (RAG), optimizando la visibilidad, gobernanza y originalidad de las propuestas académicas en INACAP Sede Maipú.

### Objetivos Específicos
1. **Centralizar y categorizar el histórico de proyectos** aprobados en las 13 áreas académicas oficiales de INACAP.
2. **Implementar una arquitectura de búsqueda semántica vectorial** utilizando modelos de lenguaje de gran escala (LLM) y la extensión `pgvector` sobre PostgreSQL.
3. **Construir el agente conversacional NAPI**, capaz de interactuar en lenguaje natural, evaluar memorias y propuestas técnicas, calcular similitud porcentual y orientar la diferenciación metodológica.
4. **Diseñar un sistema de control de accesos basado en roles (RBAC)** con flujos especializados para Estudiantes, Docentes y Administradores.
5. **Incorporar estándares de diseño y accesibilidad universal**, incluyendo navegación interactiva moderna (PillNav), modos de alto contraste y soporte de visión para daltonismo (CVD).

---

## 🏗️ Arquitectura Técnica del Sistema

El sistema implementa una arquitectura desacoplada y orientada a servicios, optimizada para baja latencia y alta precisión en la recuperación de información.

```mermaid
graph TD
    subgraph Frontend [Cliente Web - UX/UI Accesible]
        UI[Portal Web SPA - Vanilla JS / CSS3]
        Nav[PillNav Flotante + Accesibilidad CVD]
        Voice[Web Speech API - Voz Bidireccional]
        Modals[Modales de Autenticación RBAC]
    end

    subgraph Backend [Servidor de Aplicación - FastAPI]
        API[FastAPI Gateway - server.py]
        Auth[Gestor de Sesiones & Auditoría]
        AdminModule[CRUD Jerárquico de Usuarios y Carreras]
        ProjectModule[Validador de Notas >= 6.0 & Drag-and-Drop]
        ChatModule[Gestor de Historial por Usuario/Rol]
    end

    subgraph RAG_Engine [Motor RAG & Inteligencia Artificial]
        EmbedEngine[Generador de Embeddings gemini-embedding-2]
        CosineCalc[Cálculo de Distancia Coseno & HNSW]
        PromptGen[Prompt de Sistema NAPI & Memoria Multi-Turno]
        LLM[Google Gemini 2.5/3.6 Flash / Fallback OpenAI]
    end

    subgraph Database [Capa de Persistencia - Supabase]
        PG[(PostgreSQL + pgvector)]
        TableProjects[public.proyectos_titulo - 1536 dims]
        TableChat[public.napi_chat_history]
        TableUsers[public.napi_usuarios]
    end

    UI <-->|HTTP / JSON REST| API
    Voice <--> UI
    API <--> Auth
    API <--> AdminModule
    API <--> ProjectModule
    API <--> ChatModule
    ProjectModule -->|Indexación de Proyectos| EmbedEngine
    ChatModule <--> TableChat
    AdminModule <--> TableUsers
    EmbedEngine --> TableProjects
    API -->|Consulta Semántica| CosineCalc
    CosineCalc <-->|Búsqueda HNSW vector_cosine_ops| TableProjects
    CosineCalc -->|Contexto Recuperado Top-K| PromptGen
    PromptGen -->|Inferencia Contextual| LLM
    LLM -->|Diagnóstico Técnico Sintético| API
```

---

## 🧠 Flujo de Trabajo del Motor RAG (Retrieval-Augmented Generation)

1. **Vectorización de Documentos:**
   - Cada proyecto registrado con nota aprobatoria ($\ge 6.0$) procesa su título, resumen, objetivos y metadatos técnicos.
   - El modelo `gemini-embedding-2` de Google genera un vector denso de **1536 dimensiones**, normalizado e insertado en la columna vectorial de PostgreSQL.
2. **Indexación Vectorial HNSW:**
   - La tabla `proyectos_titulo` utiliza un índice **HNSW (Hierarchical Navigable Small World)** con parámetros optimizados `(m = 16, ef_construction = 64)`, permitiendo búsquedas de similitud coseno en tiempo sub-segundo incluso sobre miles de registros.
3. **Consulta del Estudiante:**
   - El estudiante describe su idea de titulación o sube un documento técnico preliminar (PDF, DOCX o TXT).
   - El sistema vectoriza la consulta del usuario en el mismo espacio vectorial de 1536 dimensiones.
4. **Recuperación Semántica (RPC en Base de Datos):**
   - La función PostgreSQL `buscar_proyectos_similares(query_embedding, match_threshold, match_count, filtro_carrera)` calcula la distancia coseno:
   $$\text{Similitud} = 1 - (\vec{u} \cdot \vec{v})$$
   - Se recuperan los proyectos que superan el umbral de similitud configurado ($\ge 0.70$), priorizando los 2 más cercanos para evitar sobrecarga de información.
5. **Generación Condicionada de la Respuesta:**
   - El LLM (Gemini / OpenAI) recibe un prompt de sistema restrictivo diseñado para evitar alucinaciones, estructurando la respuesta en 3 bloques precisos:
     - **Grado de Coincidencia:** Porcentaje de similitud y referencias de proyectos similares encontrados.
     - **Vías de Innovación y Diferenciación:** 2 sugerencias técnicas concretas para aportar valor diferencial.
     - **Validación Académica:** Recomendaciones de contraste con el docente guía.

---

## 👥 Módulos Funcionales y Control de Accesos (RBAC)

| Módulo | Perfil de Acceso | Descripción Funcional |
| :--- | :--- | :--- |
| **Landing & Catálogo Público** | Libre / Estudiantes | Exploración de proyectos aprobados, filtrado por carrera/año/área, visualización de fichas técnicas y carrusel institucional interactivo. |
| **Asistente NAPI (Chat & Voz)** | Estudiantes / Docentes | Diagnóstico de originalidad, análisis de archivos adjuntos, memoria conversacional multi-turno y consultas guiadas por voz. |
| **Panel Docente** | Docente / Revisor | Indexación de nuevas tesis, validación obligatoria de calificación ($\ge 6.0$), drag-and-drop de archivos y visualización de métricas de sede. |
| **Panel Administrador** | Administrador | CRUD completo de usuarios (alumnos y profesores), doble filtro jerárquico por Área Académica (13 áreas INACAP) y Carrera, auditoría del repositorio. |
| **Accesibilidad Universal (CVD)** | Todos los usuarios | Selector de temas (Claro / Oscuro) con bordes de alto contraste y simulación de daltonismo: Deuteranopia, Protanopia, Tritanopia y Acromatopsia. |

---

## 📊 Modelo de Datos (PostgreSQL + Supabase)

### 1. Tabla `proyectos_titulo` (Repositorio Vectorial)
```sql
CREATE TABLE public.proyectos_titulo (
  id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  titulo      TEXT        NOT NULL,
  resumen     TEXT        NOT NULL,
  carrera     TEXT        NOT NULL,
  anio        INT         NOT NULL CHECK (anio >= 2000 AND anio <= 2100),
  autores     TEXT        NOT NULL,
  embedding   VECTOR(1536), -- Generado con gemini-embedding-2
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Índice vectorial de alta velocidad
CREATE INDEX idx_proyectos_embedding_hnsw
  ON public.proyectos_titulo
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

### 2. Tabla `napi_chat_history` (Historial Aislado)
```sql
CREATE TABLE public.napi_chat_history (
  id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  user_email  TEXT        NOT NULL,
  user_role   TEXT        NOT NULL DEFAULT 'estudiante',
  sender      TEXT        NOT NULL, -- 'user' | 'napi' | 'card'
  message     TEXT        NOT NULL,
  metadata    JSONB       DEFAULT '{}'::jsonb,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_napi_chat_user 
  ON public.napi_chat_history (user_email, user_role, created_at);
```

---

## 🛠️ Tecnologías Empleadas

### **Frontend**
- **HTML5 & CSS3 Vanilla:** Estructura semántica, diseño responsivo, CSS Variables, glassmorphism y paleta corporativa moderna.
- **JavaScript Moderno (ES6+):** Programación reactiva modular (`app.js`, `PillNav.js`), manipulaciones de DOM sin sobrecarga de frameworks.
- **Web Speech API:** Reconocimiento de voz por micrófono y síntesis de voz (Text-to-Speech) integrado en el asistente.
- **GSAP (GreenSock):** Micro-animaciones para el componente de navegación flotante (`PillNav`).

### **Backend**
- **Python 3.12 & FastAPI:** Framework asíncrono de alto rendimiento para exponer la API REST de búsqueda, autenticación y chat.
- **Uvicorn:** Servidor ASGI para ejecución en producción y desarrollo.
- **Pydantic:** Validación estricta de esquemas de datos y peticiones HTTP.

### **Inteligencia Artificial & Base de Datos**
- **Google GenAI SDK (`google-genai`):** Embeddings de 1536 dimensiones (`gemini-embedding-2`) e inferencia con Gemini Flash.
- **OpenAI API (`openai`):** Motor de respaldo (fallback) con GPT-4o-mini.
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
4. Opcional: Ejecutar `python engine/seed_all_projects.py` para cargar los 12 proyectos iniciales con sus respectivos embeddings vectoriales.

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
│   └── server.py               # Servidor FastAPI con endpoints REST y lógica de negocio
├── img/                        # Recursos de respaldo para visualizadores de sedes
├── js/
│   ├── PillNav.js              # Controlador JS del menú de navegación
│   └── app.js                  # Lógica del frontend (autenticación, CRUD, chat RAG, voz)
├── src/                        # Componentes fuente reutilizables (JSX / CSS)
├── .gitignore                  # Exclusión de archivos sensibles (.env, cachés, venv)
├── index.html                  # Punto de entrada principal SPA
├── iniciar_servidor.bat        # Acceso directo para ejecución en entornos Windows
├── motor_rag.py                # Wrapper de ejecución rápida desde raíz
├── README.md                   # Documentación académica del proyecto de título
└── run_server.py               # Lanzador principal ASGI con Uvicorn
```

---

## 🔒 Consideraciones de Seguridad y Ética de la Información

1. **Aislamiento de Credenciales:** Las llaves de API (`GEMINI_API_KEY`, `SUPABASE_SERVICE_KEY`) se administran estrictamente mediante variables de entorno en el servidor, sin exposición directa en el código del cliente.
2. **Políticas RLS en Base de Datos:** PostgreSQL aplica *Row Level Security*, restringiendo la inserción y modificación de proyectos únicamente a peticiones autenticadas vía `service_role`.
3. **Privacidad del Estudiante:** El historial conversacional (`napi_chat_history`) se encuentra aislado por identificador de usuario y rol, impidiendo el cruce no autorizado de consultas preliminares de titulación.

---

## 🎓 Autores y Agradecimientos

- **Desarrollo y Memoria de Título:** Estudiantes de Ingeniería en Informática — INACAP Sede Maipú (2026).
- **Institución:** Universidad Tecnológica de Chile INACAP · Sede Maipú.
- **Docente Guía y Comisión Evaluadora:** Área Tecnologías de la Información y Ciberseguridad.

---
*© 2026 INACAP Sede Maipú · N.A.P.I. Todos los derechos reservados.*
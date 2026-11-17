-- ============================================================
--  ArchivaIA - INACAP Sede Maipu
--  Motor RAG - Fase 1 (v3): Google Gemini Embeddings
--  Modelo: gemini-embedding-2 (1536 dimensiones truncadas, GRATIS)
--  IMPORTANTE: Este script recrea la tabla con vector(1536).
-- ============================================================

-- ─────────────────────────────────────────────────────────────
-- 1. ACTIVAR EXTENSIÓN pgvector (si no está activa)
-- ─────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS vector;


-- ─────────────────────────────────────────────────────────────
-- 2. TABLA PRINCIPAL: proyectos_titulo
--    Usa vector(1536) - gemini-embedding-2 con output_dimensionality=1536
--    (pgvector HNSW soporta max 2000 dims; 1536 es optimo)
-- ─────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS public.proyectos_titulo CASCADE;

CREATE TABLE public.proyectos_titulo (
  id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  titulo      TEXT        NOT NULL,
  resumen     TEXT        NOT NULL,
  carrera     TEXT        NOT NULL,
  anio        INT         NOT NULL CHECK (anio >= 2000 AND anio <= 2100),
  autores     TEXT        NOT NULL,
  embedding   VECTOR(1536),                   -- gemini-embedding-2, 1536 dims truncadas
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE  public.proyectos_titulo         IS 'Repositorio de proyectos de titulo INACAP Sede Maipu con embeddings vectoriales RAG (gemini-embedding-2, 1536 dims).';
COMMENT ON COLUMN public.proyectos_titulo.embedding IS 'Vector de 1536 dimensiones generado por Google gemini-embedding-2 con output_dimensionality=1536.';


-- ─────────────────────────────────────────────────────────────
-- 3. ÍNDICE HNSW con distancia coseno
-- ─────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_proyectos_embedding_hnsw
  ON public.proyectos_titulo
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);


-- ─────────────────────────────────────────────────────────────
-- 4. TRIGGER: updated_at automático
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_proyectos_updated_at ON public.proyectos_titulo;
CREATE TRIGGER trg_proyectos_updated_at
  BEFORE UPDATE ON public.proyectos_titulo
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


-- ─────────────────────────────────────────────────────────────
-- 5. FUNCIÓN RPC: buscar_proyectos_similares
--    Ahora espera vector(768) para Gemini
-- ─────────────────────────────────────────────────────────────
DROP FUNCTION IF EXISTS public.buscar_proyectos_similares CASCADE;

CREATE OR REPLACE FUNCTION public.buscar_proyectos_similares(
  query_embedding  VECTOR(1536),
  match_threshold  FLOAT   DEFAULT 0.70,
  match_count      INT     DEFAULT 10,
  filtro_carrera   TEXT    DEFAULT NULL
)
RETURNS TABLE (
  id          UUID,
  titulo      TEXT,
  resumen     TEXT,
  carrera     TEXT,
  anio        INT,
  autores     TEXT,
  similitud   FLOAT
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  RETURN QUERY
  SELECT
    p.id,
    p.titulo,
    p.resumen,
    p.carrera,
    p.anio,
    p.autores,
    (1 - (p.embedding <=> query_embedding))::FLOAT AS similitud
  FROM public.proyectos_titulo p
  WHERE
    (filtro_carrera IS NULL OR p.carrera ILIKE '%' || filtro_carrera || '%')
    AND (1 - (p.embedding <=> query_embedding)) >= match_threshold
  ORDER BY
    p.embedding <=> query_embedding ASC
  LIMIT match_count;
END;
$$;

COMMENT ON FUNCTION public.buscar_proyectos_similares IS
  'RPC ArchivaIA v3: busqueda semantica con gemini-embedding-2 (1536 dims) via HNSW coseno.';


-- ─────────────────────────────────────────────────────────────
-- 6. ROW LEVEL SECURITY
-- ─────────────────────────────────────────────────────────────
ALTER TABLE public.proyectos_titulo ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Lectura publica de proyectos"
  ON public.proyectos_titulo
  FOR SELECT
  USING (true);

CREATE POLICY "Escritura restringida a service_role"
  ON public.proyectos_titulo
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);


-- ─────────────────────────────────────────────────────────────
-- 7. DATOS DE EJEMPLO (seed data)
-- ─────────────────────────────────────────────────────────────
INSERT INTO public.proyectos_titulo (titulo, resumen, carrera, anio, autores)
VALUES
  (
    'Sistema de monitoreo IoT para invernaderos con alertas inteligentes',
    'Desarrollo de una plataforma IoT para monitorear temperatura, humedad y CO2 en invernaderos agrícolas usando sensores ESP32, MQTT y un dashboard en tiempo real con alertas predictivas basadas en ML.',
    'Ingenieria en Informatica',
    2024,
    'Gonzalez R., Martinez K.'
  ),
  (
    'Aplicacion movil para gestion de inventario en PyMEs con codigo QR',
    'Solucion Android/iOS para el control de inventario en pequenas empresas, integrando lectura de codigos QR, sincronizacion en la nube y generacion automatica de reportes de stock.',
    'Ingenieria en Informatica',
    2023,
    'Perez A., Rojas F.'
  ),
  (
    'Chatbot de atencion al cliente para empresa retail usando NLP',
    'Implementacion de un asistente virtual con procesamiento de lenguaje natural para automatizar la atencion al cliente de una cadena retail, integrado con WhatsApp Business API.',
    'Ingenieria en Computacion e Informatica',
    2024,
    'Soto L., Vega M.'
  ),
  (
    'Plataforma web para digitalizacion de expedientes clinicos en centros de salud',
    'Sistema de gestion de historia clinica electronica para CESFAM, con modulo de firma digital, auditoria de accesos y exportacion a formato HL7 FHIR.',
    'Ingenieria en Administracion de Empresas',
    2023,
    'Campos B., Herrera J.'
  ),
  (
    'Analisis predictivo de desercion estudiantil usando Machine Learning',
    'Modelo de clasificacion para predecir el riesgo de desercion en estudiantes universitarios, entrenado con datos historicos academicos y socioeconomicos, con visualizacion en dashboard para tutores.',
    'Ingenieria en Informatica',
    2024,
    'Fuentes P., Diaz C.'
  )
-- ─────────────────────────────────────────────────────────────
-- 8. TABLA DE HISTORIAL DE CHATS (AISLADO POR USUARIO Y ROL)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.napi_chat_history (
  id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  user_email  TEXT        NOT NULL,
  user_role   TEXT        NOT NULL DEFAULT 'estudiante',
  sender      TEXT        NOT NULL, -- 'user' | 'napi' | 'card'
  message     TEXT        NOT NULL,
  metadata    JSONB       DEFAULT '{}'::jsonb,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_napi_chat_user ON public.napi_chat_history (user_email, user_role, created_at);

ALTER TABLE public.napi_chat_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Acceso publico lectura/escritura a napi_chat_history"
  ON public.napi_chat_history
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- ─────────────────────────────────────────────────────────────
-- FIN DEL SCRIPT v2 (Gemini 768/1536 dims + Chat History)
-- ─────────────────────────────────────────────────────────────

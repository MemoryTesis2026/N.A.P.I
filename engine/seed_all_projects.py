# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Script para sincronizar los 12 proyectos oficiales de INACAP Sede Maipú
en la base de datos de Supabase con embeddings generados por Gemini.
"""

import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from supabase import create_client, Client

load_dotenv()

GEMINI_API_KEY       = os.environ["GEMINI_API_KEY"]
SUPABASE_URL         = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

PROJECTS_INACAP = [
  {
    "titulo": "Sistema IoT de Monitoreo y Eficiencia Energética para Planta Industrial Maipú",
    "carrera": "Electricidad y Electrónica",
    "anio": 2025,
    "autores": "Diego Álvarez, Valentina Cruz",
    "resumen": "Plataforma IoT con ESP32 y sensores SCT-013 para telemetría energética en tiempo real. Algoritmo predictivo por turnos con alertas automáticas vía Telegram."
  },
  {
    "titulo": "App Móvil de Gestión de Stock y Trazabilidad QR para PyMEs Logísticas",
    "carrera": "Informática / Ing. en Computación",
    "anio": 2025,
    "autores": "Camila Herrera, Francisco Sepúlveda",
    "resumen": "App multiplataforma para control de inventario con escaneo masivo QR, sincronización offline-first, reporte de stock crítico y backend distribuido en FastAPI."
  },
  {
    "titulo": "Plataforma E-Commerce con Motor de Recomendación IA y Pagos Webpay",
    "carrera": "Informática / Ing. en Computación",
    "anio": 2024,
    "autores": "Matías Rojas, Sofía Morales, Ignacio Vega",
    "resumen": "E-commerce con filtrado colaborativo en Python para recomendación personalizada, panel analítico de conversión y chatbot transaccional integrado."
  },
  {
    "titulo": "Diagnóstico Predictivo de Vibraciones en Motores Diésel",
    "carrera": "Mecánica Automotriz e Industrial",
    "anio": 2025,
    "autores": "Pablo Fuentes, Andrés Muñoz",
    "resumen": "Telemetría mecánica con FFT y acelerómetros MEMS para prevención de desalineaciones y desbalances en maquinaria pesada industrial."
  },
  {
    "titulo": "Dashboard BI y Predicción RFM para Retail Maipú",
    "carrera": "Administración de Empresas",
    "anio": 2024,
    "autores": "Javiera Contreras, Rodrigo Sánchez",
    "resumen": "Inteligencia de negocios para retail local: consolida ERP, segmenta clientes por RFM y proyecta ventas estacionales con modelos predictivos."
  },
  {
    "titulo": "Simulador Inmersivo WebGL de Circuitos Eléctricos Trifásicos",
    "carrera": "Electricidad y Electrónica",
    "anio": 2023,
    "autores": "Nicolás Torres, Ángela Ramírez",
    "resumen": "Plataforma 3D interactiva en el navegador para ensayar tableros eléctricos trifásicos con multímetro virtual y cálculo de caídas de tensión seguro."
  },
  {
    "titulo": "Gestor Documental y Trazabilidad Aduanera para Embarques Marítimos",
    "carrera": "Comercio Internacional",
    "anio": 2024,
    "autores": "Carolina Espinoza, Luis Medina",
    "resumen": "Automatización de carpeta de importaciones con cálculo de aranceles Ad-Valorem, validación de Certificados de Origen y tracking GPS de contenedores."
  },
  {
    "titulo": "Control de Acceso Biométrico por Reconocimiento Facial con Edge AI",
    "carrera": "Informática / Ing. en Computación",
    "anio": 2024,
    "autores": "Maximiliano Bravo, Renata Castillo",
    "resumen": "Seguridad física con validación facial en tiempo real usando embeddings DeepFace, generación de informes de asistencia e integración con relé electromagnético."
  },
  {
    "titulo": "Asistente Conversacional NLP para Mantenimiento de Maquinaria Pesada",
    "carrera": "Mecánica Automotriz e Industrial",
    "anio": 2025,
    "autores": "Emilia Castro, Daniel Flores",
    "resumen": "Chatbot técnico especializado en manuales de talleres mecánicos que diagnóstica fallas hidráulicas y eléctricas mediante procesamiento de lenguaje natural."
  },
  {
    "titulo": "Software BIM y Estimación Presupuestaria para Edificación",
    "carrera": "Edificación y Construcción",
    "anio": 2024,
    "autores": "Felipe Gutiérrez, Sebastián Vargas",
    "resumen": "Extrae cantidades de obra de archivos IFC/Revit y genera presupuestos de materiales automatizados según normativas chilenas."
  },
  {
    "titulo": "Rover Teleoperado para Minería Subterránea con Sensores de Gas",
    "carrera": "Minería y Metalurgia",
    "anio": 2025,
    "autores": "Gonzalo Parra, Tamara Henríquez",
    "resumen": "Prototipo de rover explorador con detección remota de CO y CH4, cámara infrarroja y transmisión de mapa térmico 2D a estación de control."
  },
  {
    "titulo": "Plataforma de Auditoría Ambiental y Huella de Carbono Corporativa",
    "carrera": "Administración de Empresas",
    "anio": 2023,
    "autores": "Bastián Morales, Camila Silva",
    "resumen": "Sistema cloud para calcular emisiones CO2eq (Alcances 1, 2 y 3) en empresas de servicios, compatible con estándar GHG Protocol."
  }
]

def seed_database():
    print("=" * 60)
    print(" Sincronizando los 12 proyectos en Supabase con Gemini...")
    print("=" * 60)

    # Limpiar registros previos para evitar duplicados
    supabase.table("proyectos_titulo").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print("Tabla limpiada para inserción limpia.")

    for i, p in enumerate(PROJECTS_INACAP, 1):
        print(f"[{i}/{len(PROJECTS_INACAP)}] Vectorizando: {p['titulo'][:50]}...")
        texto_embedding = f"{p['titulo']}. {p['resumen']}"
        
        res = gemini_client.models.embed_content(
            model="gemini-embedding-2",
            contents=texto_embedding,
            config=genai_types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=1536
            )
        )
        embedding = list(res.embeddings[0].values)

        payload = {
            "titulo": p["titulo"],
            "resumen": p["resumen"],
            "carrera": p["carrera"],
            "anio": p["anio"],
            "autores": p["autores"],
            "embedding": embedding
        }

        supabase.table("proyectos_titulo").insert(payload).execute()
        print(f"   ✓ Insertado con embedding de 1536 dims")
        time.sleep(0.4)

    print("\n✓ ¡Los 12 proyectos oficiales de INACAP Maipú fueron guardados y vectorizados en Supabase!")

if __name__ == "__main__":
    seed_database()

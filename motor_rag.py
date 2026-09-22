# -*- coding: utf-8 -*-
"""
ArchivaIA · INACAP Sede Maipú
Acceso directo al motor RAG desde la raíz del proyecto.
"""
import os
import sys

# Redirigir ejecución al directorio engine
engine_dir = os.path.join(os.path.dirname(__file__), "engine")
if engine_dir not in sys.path:
    sys.path.insert(0, engine_dir)

os.chdir(engine_dir)

from motor_rag import ArchivaIAEngine, analizar_con_napi

if __name__ == "__main__":
    print("=" * 60)
    print("  ArchivaIA - Motor RAG v3 (Google Gemini GRATIS)")
    print("  INACAP Sede Maipu")
    print("=" * 60)

    motor = ArchivaIAEngine()

    tesis_estudiante = (
        "Sistema IoT para monitoreo remoto de cultivos hidroponicos con alertas "
        "automaticas y panel de control en tiempo real. El sistema usara sensores "
        "de temperatura, pH y nutrientes conectados por WiFi a una Raspberry Pi, "
        "enviando datos a un servidor en la nube con notificaciones SMS y email "
        "cuando los valores esten fuera de rango."
    )

    print("\n[*] Buscando proyectos similares...")
    similares = motor.buscar_similares(texto_consulta=tesis_estudiante, umbral=0.50, limite=5)

    if similares:
        print(f"\n[OK] Se encontraron {len(similares)} proyectos similares en Supabase:\n")
        for i, p in enumerate(similares, 1):
            print(f"  {i}. [{p['porcentaje_similitud']}%] {p['titulo']}")
            print(f"     Carrera: {p['carrera']} - {p['anio']}")
    else:
        print("\n[OK] No se encontraron proyectos similares. Idea original!")

    print("\n[*] Generando analisis preventivo con NAPI...")
    analisis = analizar_con_napi(tesis_estudiante, similares, motor)

    print("\n" + "-" * 60)
    print("ANALISIS DE NAPI:")
    print("-" * 60)
    print(analisis)
    print("-" * 60)
    print("\n[OK] Ejecución completada exitosamente.")

# -*- coding: utf-8 -*-
"""
ArchivaIA · INACAP Sede Maipú
Lanzador del Servidor API FastAPI
"""
import os
import sys
import uvicorn

engine_dir = os.path.join(os.path.dirname(__file__), "engine")
if engine_dir not in sys.path:
    sys.path.insert(0, engine_dir)

os.chdir(engine_dir)

if __name__ == "__main__":
    print("=" * 60)
    print("  ArchivaIA - Servidor Backend API (FastAPI + Supabase + Gemini)")
    print("  INACAP Sede Maipú")
    print("  URL: http://127.0.0.1:8080")
    print("=" * 60)
    
    # Inicia en el puerto 8080
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)

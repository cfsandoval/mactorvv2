"""
Script de inicio para la aplicación MACTOR PROSP.
Ejecuta el servidor web FastAPI y sirve la interfaz en el navegador.
"""

import sys
import webbrowser
import threading
import time
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

import uvicorn
from app import app

def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\n[+] Abriendo MACTOR PROSP en su navegador: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 70)
    print("   SISTEMA PROSPECTIVO MACTOR & INTELIGENCIA TERRITORIAL")
    print("   Metodología Michel Godet (LIPSOR) & Variante SoftProsp")
    print("   Replicación del Manual: Villabona, Oyola & Franco (2018)")
    print("=" * 70)
    print("[*] Servidor iniciado en http://127.0.0.1:8000")
    print("[*] Presione CTRL + C para detener el servidor.\n")
    
    # Launch browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run with reload
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[str(backend_dir)], log_level="info")

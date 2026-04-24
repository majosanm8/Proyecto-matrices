# -*- coding: utf-8 -*-
from services.usuario_service import buscar_por_usuario
import logging

logging.basicConfig(level=logging.INFO)

def test_busqueda():
    try:
        # Probamos con un usuario que sabemos que existe (según el diagnóstico)
        usuario = "jramirez"
        resultados = buscar_por_usuario(usuario)
        print(f"DEBUG: Resultados para '{usuario}': {resultados}")
        
        if not resultados:
            print("DEBUG: No se encontraron resultados.")
            
    except Exception as e:
        print(f"DEBUG: Error en la búsqueda: {e}")

if __name__ == "__main__":
    test_busqueda()

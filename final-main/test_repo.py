# -*- coding: utf-8 -*-
from repositories.cargo_repository import repo_obtener_dependencias
import logging

logging.basicConfig(level=logging.INFO)

def test_dependencias():
    try:
        deps = repo_obtener_dependencias()
        print(f"DEBUG: Dependencias obtenidas: {deps}")
        if not deps:
            print("DEBUG: La lista de dependencias está VACÍA.")
    except Exception as e:
        print(f"DEBUG: Error al obtener dependencias: {e}")

if __name__ == "__main__":
    test_dependencias()

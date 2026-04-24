from repositories.rol_repository import repo_buscar_rol
from utils.formatter import formatear_resultados


def buscar_por_rol(rol: str, aplicativo: str) -> list[dict]:
    # 🔹 Validación completa
    if not rol or not aplicativo:
        return []

    try:
        resultados = repo_buscar_rol(rol, aplicativo)

        # 🔹 Evita procesar vacío
        if not resultados:
            return []

        return formatear_resultados(resultados)

    except Exception:
        # Opcional: loggear si quieres trazabilidad
        return []
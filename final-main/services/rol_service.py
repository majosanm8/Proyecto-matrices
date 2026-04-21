from repositories.rol_repository import repo_buscar_rol
from utils.formatter import formatear_resultados


def buscar_por_rol(rol: str, aplicativo: str) -> list[dict]:
    if not rol:
        return []

    df = repo_buscar_rol(rol, aplicativo)
    return formatear_resultados(df)
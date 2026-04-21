from repositories.usuario_repository import repo_buscar_usuario
from utils.formatter import formatear_resultados


def buscar_por_usuario(usuario: str) -> list[dict]:
    if not usuario:
        return []

    df = repo_buscar_usuario(usuario)
    resultados = formatear_resultados(df)

    resultados_filtrados = []

    for r in resultados:
        resultados_filtrados.append({
            "usuario": r.get("usuario", ""),
            "identificacion": r.get("identificacion", ""),
            "nombre_completo": r.get("nombre_completo", ""),
            "dependencia": r.get("dependencia", ""),
            "cargo": r.get("cargo", ""),
            "aplicativo": r.get("aplicativo", ""),
            "rol": r.get("rol", ""),
        })

    return resultados_filtrados
from repositories.cargo_repository import repo_buscar_cargo
from utils.formatter import formatear_resultados


def buscar_por_cargo(cargo: str, dependencia: str) -> list[dict]:
    # 🔹 Validación robusta
    if not cargo or not dependencia:
        return []

    try:
        resultados = repo_buscar_cargo(cargo, dependencia)

        # 🔹 Si no hay resultados, evita procesar de más
        if not resultados:
            return []

        return formatear_resultados(resultados)

    except Exception as e:
        # Aquí podrías loggear si quieres
        return []
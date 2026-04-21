from repositories.cargo_repository import repo_buscar_cargo
from utils.formatter import formatear_resultados


def buscar_por_cargo(cargo: str, dependencia: str) -> list[dict]:
    if not cargo:
        return []

    df = repo_buscar_cargo(cargo, dependencia)
    return formatear_resultados(df)
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db import get_engine
from queries.cargo_queries import (
    QUERY_BUSCAR_CARGO,
    QUERY_OBTENER_DEPENDENCIAS,
    QUERY_OBTENER_CARGOS_POR_DEPENDENCIA
)

logger = logging.getLogger(__name__)


def repo_buscar_cargo(cargo: str, dependencia: str) -> list[dict]:
    """
    Busca usuarios por cargo y dependencia
    """
    try:
        params = {
            "cargo": (cargo or "").strip(),
            "dependencia": (dependencia or "").strip()
        }

        with get_engine().begin() as conn:
            resultado = conn.execute(text(QUERY_BUSCAR_CARGO), params)
            rows = [dict(row._mapping) for row in resultado]

        return rows

    except SQLAlchemyError as e:
        logger.error("❌ Error consultando cargo: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar cargo") from e


def repo_obtener_dependencias() -> list[str]:
    """
    Obtiene lista única de dependencias
    """
    try:
        with get_engine().begin() as conn:
            resultado = conn.execute(text(QUERY_OBTENER_DEPENDENCIAS))
            dependencias = [row[0] for row in resultado]

        return dependencias

    except SQLAlchemyError as e:
        logger.error("❌ Error obteniendo dependencias: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar dependencias") from e


def repo_obtener_cargos_por_dependencia(dependencia: str) -> list[str]:
    """
    Obtiene cargos según dependencia
    """
    try:
        params = {
            "dependencia": (dependencia or "").strip()
        }

        with get_engine().begin() as conn:
            resultado = conn.execute(
                text(QUERY_OBTENER_CARGOS_POR_DEPENDENCIA),
                params
            )
            cargos = [row[0] for row in resultado]

        return cargos

    except SQLAlchemyError as e:
        logger.error("❌ Error obteniendo cargos: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar cargos") from e
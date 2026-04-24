# -*- coding: utf-8 -*-

import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from db import get_engine

from queries.rol_queries import (
    QUERY_BUSCAR_ROL,
    QUERY_OBTENER_APLICATIVOS,
    QUERY_OBTENER_ROLES_POR_APP
)

logger = logging.getLogger(__name__)


def repo_buscar_rol(rol: str, aplicativo: str) -> list[dict]:
    """
    Busca usuarios por rol y aplicativo
    """
    try:
        params = {
            "rol": (rol or "").strip(),
            "aplicativo": (aplicativo or "").strip()
        }

        with get_engine().begin() as conn:
            result = conn.execute(text(QUERY_BUSCAR_ROL), params)
            rows = [dict(row._mapping) for row in result]

        return rows

    except SQLAlchemyError as e:
        logger.error("❌ Error consultando rol: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar rol") from e


def repo_obtener_aplicativos() -> list[str]:
    """
    Obtiene lista única de aplicativos
    """
    try:
        with get_engine().begin() as conn:
            result = conn.execute(text(QUERY_OBTENER_APLICATIVOS))
            aplicativos = [row[0] for row in result]

        return aplicativos

    except SQLAlchemyError as e:
        logger.error("❌ Error obteniendo aplicativos: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar aplicativos") from e


def repo_obtener_roles_por_app(aplicativo: str) -> list[str]:
    """
    Obtiene roles según aplicativo
    """
    try:
        params = {
            "aplicativo": (aplicativo or "").strip()
        }

        with get_engine().begin() as conn:
            result = conn.execute(
                text(QUERY_OBTENER_ROLES_POR_APP),
                params
            )
            roles = [row[0] for row in result]

        return roles

    except SQLAlchemyError as e:
        logger.error("❌ Error obteniendo roles: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar roles") from e
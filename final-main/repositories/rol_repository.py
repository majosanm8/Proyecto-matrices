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

    try:

        params = {
            "rol": rol,
            "aplicativo": aplicativo
        }

        with get_engine().connect() as conn:

            result = conn.execute(text(QUERY_BUSCAR_ROL), params)

            return [dict(row._mapping) for row in result]

    except SQLAlchemyError as e:

        logger.error("Error consultando rol: %s", e, exc_info=True)

        raise RuntimeError("Error al consultar rol") from e


def repo_obtener_aplicativos():

    try:

        with get_engine().connect() as conn:

            result = conn.execute(text(QUERY_OBTENER_APLICATIVOS))

            return [row[0] for row in result]

    except SQLAlchemyError as e:

        logger.error("Error obteniendo aplicativos: %s", e, exc_info=True)

        raise RuntimeError("Error al consultar aplicativos") from e


def repo_obtener_roles_por_app(aplicativo):

    with get_engine().connect() as conn:

        result = conn.execute(
            text(QUERY_OBTENER_ROLES_POR_APP),
            {"aplicativo": aplicativo}
        )

        return [row[0] for row in result]
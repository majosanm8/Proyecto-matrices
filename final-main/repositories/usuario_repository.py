# -*- coding: utf-8 -*-
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db import get_engine
from queries.usuario_queries import QUERY_BUSCAR_USUARIO

logger = logging.getLogger(__name__)


def repo_buscar_usuario(usuario: str) -> list[dict]:
    try:
        # Preparamos el patrón para LIKE
        busqueda = f"%{usuario.strip()}%"
        params = {
            "usuario": busqueda
        }

        with get_engine().connect() as conn:
            resultado = conn.execute(text(QUERY_BUSCAR_USUARIO), params)
            return [dict(row._mapping) for row in resultado]

    except SQLAlchemyError as e:
        logger.error("Error consultando usuario: %s", e, exc_info=True)
        raise RuntimeError("Error al consultar usuario") from e
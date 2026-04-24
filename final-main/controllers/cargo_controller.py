# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, render_template, request, jsonify

from services.cargo_service import buscar_por_cargo
from repositories.cargo_repository import (
    repo_obtener_dependencias,
    repo_obtener_cargos_por_dependencia
)

logger = logging.getLogger(__name__)

cargo_bp = Blueprint("cargo", __name__)


@cargo_bp.route("/consulta-cargo", methods=["GET", "POST"])
def consulta_cargo():

    resultados = []
    error = None

    cargo_val = ""
    dependencia_val = ""

    try:
        dependencias = repo_obtener_dependencias()
    except Exception as e:
        logger.error("Error cargando dependencias: %s", e)
        dependencias = []
        error = "No se pudieron cargar las dependencias"

    if request.method == "POST":

        cargo_val = (request.form.get("cargo") or "").strip()
        dependencia_val = (request.form.get("dependencia") or "").strip()

        if not cargo_val or not dependencia_val:
            error = "Debe seleccionar una dependencia y un cargo"
        else:
            try:
                resultados = buscar_por_cargo(cargo_val, dependencia_val)

                if not resultados:
                    error = "No se encontraron resultados"

            except Exception as e:
                logger.error("Error consultando cargo: %s", e, exc_info=True)
                error = "Ocurrió un error al consultar"

    return render_template(
        "consulta_cargo.html",
        resultados=resultados,
        dependencias=dependencias,
        cargo_val=cargo_val,
        dependencia_val=dependencia_val,
        error=error
    )


@cargo_bp.route("/api/cargos/<path:dependencia>")
def api_cargos(dependencia):
    try:
        dependencia = (dependencia or "").strip()

        if not dependencia:
            return jsonify({"error": "Dependencia requerida"}), 400

        cargos = repo_obtener_cargos_por_dependencia(dependencia)

        return jsonify(cargos if cargos else [])

    except Exception as e:
        logger.error("Error en API cargos: %s", e, exc_info=True)
        return jsonify({"error": "Error interno"}), 500
# -*- coding: utf-8 -*-

QUERY_BUSCAR_CARGO = """
    SELECT
        usuario,
        identificacion,
        nombre_completo,
        cargo,
        area,
        dependencia,
        rol,
        aplicativo
    FROM usuarios
    WHERE LOWER(cargo) = LOWER(:cargo)
      AND LOWER(dependencia) = LOWER(:dependencia)
    ORDER BY usuario
"""

QUERY_OBTENER_DEPENDENCIAS = """
SELECT DISTINCT dependencia
FROM usuarios
WHERE dependencia IS NOT NULL AND dependencia != ''
ORDER BY dependencia
"""

QUERY_OBTENER_CARGOS_POR_DEPENDENCIA = """
SELECT DISTINCT cargo
FROM usuarios
WHERE LOWER(dependencia) = LOWER(:dependencia)
  AND cargo IS NOT NULL AND cargo != ''
ORDER BY cargo
"""


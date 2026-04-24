# -*- coding: utf-8 -*-

QUERY_BUSCAR_CARGO = """
    SELECT
        usuario,
        nombre_completo,
        identificacion,
        cargo,
        area,
        dependencia,
        rol,
        aplicativo
    FROM usuarios
    WHERE LOWER(TRIM(cargo)) = LOWER(TRIM(:cargo))
      AND LOWER(TRIM(dependencia)) = LOWER(TRIM(:dependencia))
    ORDER BY usuario
"""

QUERY_OBTENER_DEPENDENCIAS = """
SELECT DISTINCT UPPER(TRIM(dependencia)) as dependencia
FROM usuarios
WHERE dependencia IS NOT NULL AND dependencia != ''
ORDER BY dependencia
"""

QUERY_OBTENER_CARGOS_POR_DEPENDENCIA = """
SELECT DISTINCT UPPER(TRIM(cargo)) as cargo
FROM usuarios
WHERE LOWER(TRIM(dependencia)) = LOWER(TRIM(:dependencia))
  AND cargo IS NOT NULL AND cargo != ''
ORDER BY cargo
"""


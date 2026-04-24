QUERY_BUSCAR_USUARIO = """
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
WHERE 
    LOWER(usuario) LIKE LOWER(:usuario)
    OR LOWER(nombre_completo) LIKE LOWER(:usuario)
    OR CAST(identificacion AS TEXT) LIKE :usuario
ORDER BY usuario
"""
QUERY_BUSCAR_USUARIO = """
SELECT 
    usuario,
    cargo,
    area,
    dependencia,
    rol,
    aplicativo
FROM usuarios
WHERE LOWER(usuario) LIKE LOWER(:usuario)
ORDER BY usuario;
"""
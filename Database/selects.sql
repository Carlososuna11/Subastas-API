use subastas;
SELECT * FROM caj_monedas;

SELECT * FROM caj_monedas
INNER JOIN caj_divisas
ON caj_monedas.id_divisa = caj_divisas.id
INNER JOIN caj_paises as paises_divisas
ON caj_monedas.id_pais_divisa = paises_divisas.id
INNER JOIN caj_paises
ON caj_monedas.id_pais = caj_paises.id
LEFT JOIN caj_M_A
ON caj_monedas.id = caj_M_A.id_moneda
LEFT JOIN caj_artistas
ON caj_M_A.id_artista = caj_artistas.id;

SELECT * FROM caj_Catalogo_Moneda_Tienda;

SELECT * FROM caj_Catalogo_Moneda_Tienda
INNER JOIN caj_monedas
ON caj_Catalogo_Moneda_Tienda.id_moneda = caj_monedas.id
INNER JOIN caj_divisas
ON caj_monedas.id_divisa = caj_divisas.id
INNER JOIN caj_paises as paises_divisas
ON caj_monedas.id_pais_divisa = paises_divisas.id
INNER JOIN caj_paises as caj_paises_monedas
ON caj_monedas.id_pais = caj_paises_monedas.id
LEFT JOIN caj_M_A
ON caj_monedas.id = caj_M_A.id_moneda
LEFT JOIN caj_artistas
ON caj_M_A.id_artista = caj_artistas.id
LEFT JOIN caj_coleccionistas
ON caj_Catalogo_Moneda_Tienda.id_coleccionista = caj_coleccionistas.id
LEFT JOIN caj_organizaciones
ON caj_Catalogo_Moneda_Tienda.id_organizacion = caj_organizaciones.id;

SELECT * FROM caj_Catalogo_Pintura_Tienda;

SELECT * FROM caj_Catalogo_Pintura_Tienda
LEFT JOIN caj_P_A
ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
LEFT JOIN caj_artistas
ON caj_P_A.id_artista = caj_artistas.id
LEFT JOIN caj_coleccionistas
ON caj_Catalogo_Pintura_Tienda.id_coleccionista = caj_coleccionistas.id
LEFT JOIN caj_organizaciones
ON caj_Catalogo_Pintura_Tienda.id_organizacion = caj_organizaciones.id;

SELECT * FROM caj_organizaciones;

SELECT * FROM caj_coleccionistas;



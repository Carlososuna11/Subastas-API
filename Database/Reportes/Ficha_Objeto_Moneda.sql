SELECT 
caj_Catalogo_Moneda_Tienda.nur as catalogo_nur, caj_Catalogo_Moneda_Tienda.id_moneda as catalogo_id_moneda, caj_Catalogo_Moneda_Tienda.id_coleccionista as catalogo_id_coleccionista, caj_Catalogo_Moneda_Tienda.id_organizacion as catalogo_id_organizacion,
caj_monedas.id as moneda_id, caj_monedas.nombre as moneda_nombre, caj_monedas.denominacion as moneda_denominacion, caj_monedas.mintage as moneda_mintage, caj_monedas.forma as moneda_forma, caj_monedas.metal as moneda_metal, caj_monedas.diametromm as moneda_diametromm, caj_monedas.canto as moneda_canto, caj_monedas.pesogr as moneda_pesogr, caj_monedas.ano as moneda_ano, caj_monedas.motivo as moneda_motivo, caj_monedas.acunacion as moneda_acunacion, caj_monedas.anverso as moneda_anverso, caj_monedas.reverso as moneda_reverso, caj_monedas.id_pais_divisa as moneda_id_pais_divisa, caj_monedas.id_pais as moneda_id_pais, caj_monedas.id_divisa as moneda_id_divisa, caj_monedas.imagen as moneda_imagen,
caj_divisas.id as divisa_id, caj_divisas.id_pais as divisa_id_pais, caj_divisas.nombre as divisa_nombre,
`divisa_pais`.id as divisa_pais_id, `divisa_pais`.nombre as divisa_pais_nombre, `divisa_pais`.nacionalidad as divisa_pais_nacionalidad,
moneda_pais.id as moneda_pais_id, moneda_pais.nombre as moneda_pais_nombre, moneda_pais.nacionalidad as moneda_pais_nacionalidad,
caj_coleccionistas.id as coleccionista_id, caj_coleccionistas.dni as coleccionista_dni, caj_coleccionistas.nombre as coleccionista_nombre, COALESCE(caj_coleccionistas.segundoNombre, '') as coleccionista_segundoNombre, caj_coleccionistas.apellido as coleccionista_apellido, caj_coleccionistas.segundoApellido as coleccionista_segundoApellido, caj_coleccionistas.telefono as coleccionista_telefono, caj_coleccionistas.email as coleccionista_email, caj_coleccionistas.fechaNacimiento as coleccionista_fechaNacimiento, caj_coleccionistas.id_pais_nacio as coleccionista_id_pais_nacio, caj_coleccionistas.id_pais_reside as coleccionista_id_pais_reside,
pais_nacio.id as pais_nacio_id, pais_nacio.nombre as pais_nacio_nombre, pais_nacio.nacionalidad as pais_nacio_nacionalidad,
pais_reside.id as pais_reside_id, pais_reside.nombre as pais_reside_nombre, pais_reside.nacionalidad as pais_reside_nacionalidad,
caj_organizaciones.id as organizacion_id, caj_organizaciones.nombre as organizacion_nombre, caj_organizaciones.proposito as organizacion_proposito, caj_organizaciones.fundacion as organizacion_fundacion, caj_organizaciones.alcance as organizacion_alcance, caj_organizaciones.tipo as organizacion_tipo, caj_organizaciones.telefonoPrincipal as organizacion_telefonoPrincipal, caj_organizaciones.paginaWeb as organizacion_paginaWeb, caj_organizaciones.emailCorporativo as organizacion_emailCorporativo, caj_organizaciones.id_pais as organizacion_id_pais,
organizacion_pais.id as organizacion_pais_id, organizacion_pais.nombre as organizacion_pais_nombre, organizacion_pais.nacionalidad as organizacion_pais_nacionalidad,
GROUP_CONCAT(CONCAT(COALESCE(caj_artistas.nombre,''),' ',COALESCE(caj_artistas.apellido,''), 'Nombre Artistico: ', COALESCE(caj_artistas.nombreArtistico,'No posee')) SEPARATOR '; ') as nombre_artistas,
COUNT(caj_artistas.id) as cantidad_artistas
FROM caj_Catalogo_Moneda_Tienda
INNER JOIN caj_monedas
ON caj_monedas.id = caj_Catalogo_Moneda_Tienda.id_moneda
INNER JOIN caj_divisas
ON caj_divisas.id = caj_monedas.id_divisa AND caj_divisas.id_pais = caj_monedas.id_pais_divisa
INNER JOIN caj_paises as `divisa_pais`
ON caj_divisas.id_pais = divisa_pais.id
INNER JOIN caj_paises as moneda_pais
ON caj_monedas.id_pais = moneda_pais.id
LEFT JOIN caj_organizaciones
ON caj_organizaciones.id = caj_Catalogo_Moneda_Tienda.id_organizacion
LEFT JOIN caj_paises as organizacion_pais
ON organizacion_pais.id = caj_organizaciones.id_pais
LEFT JOIN caj_coleccionistas
ON caj_coleccionistas.id = caj_Catalogo_Moneda_Tienda.id_coleccionista
LEFT JOIN caj_paises as pais_nacio
ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
LEFT JOIN caj_paises as pais_reside
ON pais_reside.id = caj_coleccionistas.id_pais_reside
LEFT JOIN caj_M_A
ON caj_M_A.id_moneda = caj_monedas.id
LEFT JOIN caj_artistas
ON caj_artistas.id = caj_M_A.id_artista
WHERE caj_Catalogo_Moneda_Tienda.nur = $P{nur_moneda}
GROUP BY caj_Catalogo_Moneda_Tienda.id_moneda

SELECT
COUNT(*) OVER (), 
caj_M_A.id_moneda as moneda_artista_id_moneda, caj_M_A.id_artista as moneda_artista_id_artista,
caj_artistas.id as artista_id, COALESCE(caj_artistas.nombre,'') as artista_nombre, COALESCE(caj_artistas.apellido,'') as artista_apellido, COALESCE(caj_artistas.nombreArtistico,'') as artista_nombreArtistico
FROM caj_M_A
INNER JOIN caj_artistas
ON caj_M_A.id_artista = caj_artistas.id;



SELECT
caj_M_A.id_moneda as moneda_artista_id_moneda, caj_M_A.id_artista as moneda_artista_id_artista,
caj_artistas.id as artista_id,CONCAT(COALESCE(caj_artistas.nombre,''),' ',COALESCE(caj_artistas.apellido,'')) as "Nombre del Artista", COALESCE(caj_artistas.nombreArtistico,'') as "Nombre Artistico"
FROM caj_M_A
INNER JOIN caj_artistas
ON caj_M_A.id_artista = caj_artistas.id;
                        
SELECT 
caj_Lista_Objetos.id_evento as lista_id_evento, 
caj_Lista_Objetos.id_eventoParticipante as lista_id_eventoParticipante, 
caj_Lista_Objetos.id as lista_id, 
caj_Lista_Objetos.id_pintura as lista_id_pintura, 
caj_Lista_Objetos.nur_moneda as lista_nur_moneda, 
caj_Lista_Objetos.id_moneda as lista_id_moneda, 
caj_Lista_Objetos.porcentajeGananciaMin as lista_porcentajeGananciaMin, 
caj_Lista_Objetos.bid as lista_bid, 
caj_Lista_Objetos.ask as lista_ask, 
caj_Lista_Objetos.precioAlcanzado as lista_precioAlcanzado, 
caj_Lista_Objetos.orden as lista_orden, 
caj_Lista_Objetos.duracionmin as lista_duracionmin, 
caj_Lista_Objetos.razonNoVenta as lista_razonNoVenta, 
caj_Lista_Objetos.fechaIngresoParticipante as lista_fechaIngresoParticipante, 
caj_Lista_Objetos.id_coleccionistaParticipante as lista_id_coleccionistaParticipante,
caj_Lista_Objetos.id_organizacionParticipante as lista_id_organizacionParticipante
FROM caj_Lista_Objetos
                        
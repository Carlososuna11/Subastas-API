SELECT COUNT(*) OVER(),
	`caj_P_A`.id_pintura AS pintura_artista_id_pintura,
	`caj_P_A`.id_artista AS pintura_artista_id_artista,
	caj_artistas.id AS artista_id,
	COALESCE( caj_artistas.nombre,'') AS artista_nombre,
	COALESCE( caj_artistas.apellido,'') AS artista_apellido,
	COALESCE( caj_artistas.nombreArtistico,'') AS artista_nombreArtistico
FROM `caj_P_A`
INNER JOIN caj_artistas 
ON `caj_P_A`.id_artista = caj_artistas.id
WHERE `caj_P_A`.id_pintura = $P{id_pintura}

SELECT 
caj_Catalogo_Pintura_Tienda.nur as catalogo_nur, caj_Catalogo_Pintura_Tienda.titulo as catalogo_titulo, caj_Catalogo_Pintura_Tienda.dimensionescm as catalogo_dimensionescm, caj_Catalogo_Pintura_Tienda.estilo as catalogo_estilo, caj_Catalogo_Pintura_Tienda.ano as catalogo_ano, caj_Catalogo_Pintura_Tienda.imagen as catalogo_imagen, caj_Catalogo_Pintura_Tienda.id_coleccionista as catalogo_id_coleccionista, caj_Catalogo_Pintura_Tienda.id_organizacion as catalogo_id_organizacion,
caj_coleccionistas.id as coleccionista_id, caj_coleccionistas.dni as coleccionista_dni, caj_coleccionistas.nombre as coleccionista_nombre, COALESCE(caj_coleccionistas.segundoNombre, '') as coleccionista_segundoNombre, caj_coleccionistas.apellido as coleccionista_apellido, caj_coleccionistas.segundoApellido as coleccionista_segundoApellido, caj_coleccionistas.telefono as coleccionista_telefono, caj_coleccionistas.email as coleccionista_email, caj_coleccionistas.fechaNacimiento as coleccionista_fechaNacimiento, caj_coleccionistas.id_pais_nacio as coleccionista_id_pais_nacio, caj_coleccionistas.id_pais_reside as coleccionista_id_pais_reside,
pais_nacio.id as pais_nacio_id, pais_nacio.nombre as pais_nacio_nombre, pais_nacio.nacionalidad as pais_nacio_nacionalidad,
pais_reside.id as pais_reside_id, pais_reside.nombre as pais_reside_nombre, pais_reside.nacionalidad as pais_reside_nacionalidad,
caj_organizaciones.id as organizacion_id, caj_organizaciones.nombre as organizacion_nombre, caj_organizaciones.proposito as organizacion_proposito, caj_organizaciones.fundacion as organizacion_fundacion, caj_organizaciones.alcance as organizacion_alcance, caj_organizaciones.tipo as organizacion_tipo, caj_organizaciones.telefonoPrincipal as organizacion_telefonoPrincipal, caj_organizaciones.paginaWeb as organizacion_paginaWeb, caj_organizaciones.emailCorporativo as organizacion_emailCorporativo, caj_organizaciones.id_pais as organizacion_id_pais,
organizacion_pais.id as organizacion_pais_id, organizacion_pais.nombre as organizacion_pais_nombre, organizacion_pais.nacionalidad as organizacion_pais_nacionalidad,

FROM caj_Catalogo_Pintura_Tienda
LEFT JOIN caj_organizaciones
ON caj_organizaciones.id = caj_Catalogo_Pintura_Tienda.id_organizacion
LEFT JOIN caj_paises as organizacion_pais
ON organizacion_pais.id = caj_organizaciones.id_pais
LEFT JOIN caj_coleccionistas
ON caj_coleccionistas.id = caj_Catalogo_Pintura_Tienda.id_coleccionista
LEFT JOIN caj_paises as pais_nacio
ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
LEFT JOIN caj_paises as pais_reside
ON pais_reside.id = caj_coleccionistas.id_pais_reside;


SELECT
	`caj_P_A`.id_pintura AS pintura_artista_id_pintura,
	`caj_P_A`.id_artista AS pintura_artista_id_artista,
	caj_artistas.id AS artista_id,
    CONCAT(COALESCE( caj_artistas.nombre,''),COALESCE( caj_artistas.apellido,'')) as "Nombre del Artista"
	COALESCE( caj_artistas.nombreArtistico,'') as "Nombre Artistico"
FROM `caj_P_A`
INNER JOIN caj_artistas 
ON `caj_P_A`.id_artista = caj_artistas.id
WHERE `caj_P_A`.id_pintura = $P{id_pintura}

SELECT `caj_Catalogo_Pintura_Tienda`.nur AS catalogo_nur,
	`caj_Catalogo_Pintura_Tienda`.titulo AS catalogo_titulo,
	`caj_Catalogo_Pintura_Tienda`.dimensionescm AS catalogo_dimensionescm,
	`caj_Catalogo_Pintura_Tienda`.estilo AS catalogo_estilo,
	`caj_Catalogo_Pintura_Tienda`.ano AS catalogo_ano,
	`caj_Catalogo_Pintura_Tienda`.imagen AS catalogo_imagen,
	`caj_Catalogo_Pintura_Tienda`.id_coleccionista AS catalogo_id_coleccionista,
	`caj_Catalogo_Pintura_Tienda`.id_organizacion AS catalogo_id_organizacion,
	caj_coleccionistas.id AS coleccionista_id,
	caj_coleccionistas.dni AS coleccionista_dni,
	caj_coleccionistas.nombre AS coleccionista_nombre,
	COALESCE( caj_coleccionistas.segundoNombre,'') AS coleccionista_segundoNombre,
	caj_coleccionistas.apellido AS coleccionista_apellido,
	caj_coleccionistas.`segundoApellido` AS coleccionista_segundoApellido,
	caj_coleccionistas.telefono AS coleccionista_telefono,
	caj_coleccionistas.email AS coleccionista_email,
	caj_coleccionistas.`fechaNacimiento` AS coleccionista_fechaNacimiento,
	caj_coleccionistas.id_pais_nacio AS coleccionista_id_pais_nacio,
	caj_coleccionistas.id_pais_reside AS coleccionista_id_pais_reside,
	pais_nacio.id AS pais_nacio_id,
	pais_nacio.nombre AS pais_nacio_nombre,
	pais_nacio.nacionalidad AS pais_nacio_nacionalidad,
	pais_reside.id AS pais_reside_id,
	pais_reside.nombre AS pais_reside_nombre,
	pais_reside.nacionalidad AS pais_reside_nacionalidad,
	caj_organizaciones.id AS organizacion_id,
	caj_organizaciones.nombre AS organizacion_nombre,
	caj_organizaciones.proposito AS organizacion_proposito,
	caj_organizaciones.fundacion AS organizacion_fundacion,
	caj_organizaciones.alcance AS organizacion_alcance,
	caj_organizaciones.tipo AS organizacion_tipo,
	caj_organizaciones.`telefonoPrincipal` AS organizacion_telefonoPrincipal,
	caj_organizaciones.`paginaWeb` AS organizacion_paginaWeb,
	caj_organizaciones.`emailCorporativo` AS organizacion_emailCorporativo,
	caj_organizaciones.id_pais AS organizacion_id_pais,
	organizacion_pais.id AS organizacion_pais_id,
	organizacion_pais.nombre AS organizacion_pais_nombre,
	organizacion_pais.nacionalidad AS organizacion_pais_nacionalidad
    
FROM `caj_Catalogo_Pintura_Tienda`
	LEFT JOIN caj_organizaciones ON 
	 caj_organizaciones.id = `caj_Catalogo_Pintura_Tienda`.id_organizacion 
	LEFT JOIN caj_paises AS organizacion_pais ON 
	 'NULL' = caj_organizaciones.id_pais 
	LEFT JOIN caj_coleccionistas ON 
	 caj_coleccionistas.id = `caj_Catalogo_Pintura_Tienda`.id_coleccionista 
	LEFT JOIN caj_paises AS pais_nacio ON 
	 pais_nacio.id = caj_coleccionistas.id_pais_nacio 
	LEFT JOIN caj_paises AS pais_reside ON 
	 pais_reside.id = caj_coleccionistas.id_pais_reside
	 WHERE caj_Catalogo_Pintura_Tienda.nur = $P{nur_pintura}


     SELECT `caj_Catalogo_Pintura_Tienda`.nur AS catalogo_nur,
	`caj_Catalogo_Pintura_Tienda`.titulo AS catalogo_titulo,
	`caj_Catalogo_Pintura_Tienda`.dimensionescm AS catalogo_dimensionescm,
	`caj_Catalogo_Pintura_Tienda`.estilo AS catalogo_estilo,
	`caj_Catalogo_Pintura_Tienda`.ano AS catalogo_ano,
	`caj_Catalogo_Pintura_Tienda`.id_coleccionista AS catalogo_id_coleccionista,
	`caj_Catalogo_Pintura_Tienda`.id_organizacion AS catalogo_id_organizacion,
    CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ',caj_coleccionistas.segundoApellido) as coleccionista_nombre,
	caj_organizaciones.nombre AS organizacion_nombre,
    GROUP_CONCAT(CONCAT(COALESCE(caj_artistas.nombre,''),' ',COALESCE(caj_artistas.apellido,''), 'Nombre Artistico: ', COALESCE(caj_artistas.nombreArtistico,'No posee')) SEPARATOR '; ') as nombre_artistas,
    COUNT(caj_artistas.id) as cantidad_artistas
FROM `caj_Catalogo_Pintura_Tienda`
	LEFT JOIN caj_organizaciones ON 
	 caj_organizaciones.id = `caj_Catalogo_Pintura_Tienda`.id_organizacion 
	LEFT JOIN caj_coleccionistas ON 
	 caj_coleccionistas.id = `caj_Catalogo_Pintura_Tienda`.id_coleccionista 
     LEFT JOIN caj_P_A ON
     caj_P_A.id_pintura = `caj_Catalogo_Pintura_Tienda`.nur
     LEFT JOIN caj_artistas ON
     caj_artistas.id = caj_P_A.id_artista
	 WHERE caj_Catalogo_Pintura_Tienda.nur = $P{nur_pintura}
     GROUP BY `caj_Catalogo_Pintura_Tienda`.nur
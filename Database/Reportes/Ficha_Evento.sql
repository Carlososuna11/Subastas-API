SELECT 
caj_eventos.id as evento_id,
caj_eventos.inscripcionCliente as evento_inscripcionCliente,
caj_eventos.inscripcionClienteNuevo as evento_inscripcionClienteNuevo,
caj_eventos.fecha as evento_fecha,
caj_eventos.status as evento_status,
caj_eventos.tipo as evento_tipo,
caj_eventos.tipoPuja as evento_tipoPuja,
caj_eventos.duracionHoras as evento_duracionHoras,
CONCAT(COALESCE(caj_eventos.lugar,''),' ',COALESCE(pais_evento.nombre,'') ) as evento_lugar,
caj_eventos.id_pais as evento_id_pais,
pais_evento.id as pais_evento_id,
pais_evento.nacionalidad as pais_evento_nacionalidad,
GROUP_CONCAT(caj_organizaciones.nombre SEPARATOR ', '),
COUNT(caj_organizaciones.nombre)
FROM caj_eventos
LEFT JOIN caj_paises as pais_evento
ON pais_evento.id = caj_eventos.id_pais
LEFT JOIN caj_planificadores
ON caj_planificadores.id_evento = caj_eventos.id
LEFT JOIN caj_organizaciones
ON caj_organizaciones.id = caj_planificadores.id_organizacion
WHERE caj_eventos.id = 3
GROUP BY caj_eventos.id


SELECT
caj_Lista_Objetos.id_pinturaas "NUR",
caj_Lista_Objetos.bid as "BID",
caj_Lista_Objetos.ask as "ASK",
caj_Lista_Objetos.duracionmin as "DURACION (MIN)",
caj_Catalogo_Pintura_Tienda.titulo as "NOMBRE"
FROM caj_Lista_Objetos
INNER JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_Lista_Objetos.id_evento = 1
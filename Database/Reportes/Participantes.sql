SELECT caj_participantes.id_evento AS participante_id_evento,
	caj_participantes.`fechaIngresoCliente` AS participante_fechaIngresoCliente,
	CONCAT( caj_coleccionistas.nombre,' ',COALESCE( caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ',caj_coleccionistas.segundoApellido) as 'Nombre Participante',
	caj_organizaciones.nombre AS "Nombre Organizacion",
FROM caj_participantes
	INNER JOIN caj_coleccionistas ON 
	 caj_coleccionistas.id = caj_participantes.id_coleccionista_cliente 
	INNER JOIN caj_organizaciones ON 
	 caj_organizaciones.id = caj_participantes.id_organizacion_cliente 
WHERE 
	 caj_participantes.id_evento = $P{id_evento}
ORDER BY caj_participantes.fechaIngresoCliente
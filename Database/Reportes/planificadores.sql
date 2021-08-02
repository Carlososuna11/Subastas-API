SELECT 
	caj_organizaciones.nombre AS organizacion_nombre,
	FROM caj_planificadores
	INNER JOIN caj_organizaciones ON 
	 caj_planificadores.id_organizacion = caj_organizaciones.id 
WHERE 
	 caj_planificadores.id_evento = $P{id_evento}
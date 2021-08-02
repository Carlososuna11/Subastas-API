SELECT
caj_eventos.id
caj_eventos.fecha
caj_eventos.status
from caj_planificadores
inner join caj_eventos on caj_planificadores.id_evento = caj_eventos.id
WHERE
caj_planificadores.id_organizacion = 1
AND (caj_eventos.fecha >= $P{fecha_inicio} AND caj_eventos.fecha <= $P{fecha_fin} OR ($P{fecha_fin} IS NULL OR $P{fecha_inicio} IS NULL))
AND (caj_eventos.fecha >= $P{fecha_inicio} OR $P{fecha_inicio} IS NULL)
AND (caj_eventos.fecha <= $P{fecha_fin} OR $P{fecha_fin} IS NULL)
ORDER BY caj_eventos.fecha DESC;

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
GROUP_CONCAT(caj_organizaciones.nombre SEPARATOR ', ')
FROM caj_eventos
LEFT JOIN caj_paises as pais_evento
ON pais_evento.id = caj_eventos.id_pais
LEFT JOIN caj_planificadores
ON caj_planificadores.id_evento = caj_eventos.id
LEFT JOIN caj_organizaciones
ON caj_organizaciones.id = caj_planificadores.id_organizacion
WHERE caj_planificadores.id_organizacion = $P{id_organizacion}
AND (caj_eventos.fecha >= $P{fecha_inicio} AND caj_eventos.fecha <= $P{fecha_fin} OR ($P{fecha_fin} IS NULL OR $P{fecha_inicio} IS NULL))
AND (caj_eventos.fecha >= $P{fecha_inicio} OR $P{fecha_inicio} IS NULL)
AND (caj_eventos.fecha <= $P{fecha_fin} OR $P{fecha_fin} IS NULL)
GROUP BY caj_eventos.id
ORDER BY caj_eventos.fecha DESC;
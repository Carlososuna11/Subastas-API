SELECT 
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ',caj_coleccionistas.segundoApellido) as "Nombre Completo",
caj_coleccionistas.dni as "DNI",
caj_paises.nombre as "Pais Reside",
caj_paises_nacionalidad.nacionalidad as "Nacionalidad",
caj_coleccionistas.fechaNacimiento as "Fecha de Nacimiento",
caj_coleccionistas.email as "Email",
caj_coleccionistas.telefono as "Teléfono"
FROM caj_coleccionistas
INNER JOIN caj_paises
ON caj_coleccionistas.id_pais_reside = caj_paises.id
INNER JOIN caj_paises as caj_paises_nacionalidad
ON caj_coleccionistas.id_pais_nacio = caj_paises_nacionalidad.id
WHERE caj_coleccionistas.id = $P{id_coleccionista}

SELECT
caj_organizaciones.nombre as "Organizacion",
caj_clientes.fechaIngreso as "Fecha de Ingreso"
FROM caj_clientes
INNER JOIN caj_organizaciones
ON caj_clientes.id_organizacion = caj_organizaciones.id
WHERE caj_clientes.id_coleccionista = $P{id_coleccionista}
AND ((caj_clientes.id_organizacion = $P{id_organizacion} AND $P{id_organizacion} IS NOT NULL) OR $P{id_organizacion} IS NULL)
ORDER BY caj_clientes.fechaIngreso DESC

SELECT
caj_eventos.fecha as "Fecha del Evento",
GROUP_CONCAT(caj_organizaciones.nombre SEPARATOR ', ') as "Organizaciones",
caj_eventos.tipo as "Tipo de Evento",
caj_eventos.tipoPuja as "Tipo de Puja"
from caj_participantes
INNER JOIN caj_eventos
ON caj_participantes.id_evento = caj_eventos.id
LEFT JOIN caj_planificadores
ON caj_planificadores.id_evento = caj_eventos.id
LEFT JOIN caj_organizaciones
ON caj_planificadores.id_organizacion = caj_organizaciones.id
WHERE caj_participantes.id_coleccionista_cliente =$P{id_coleccionista} AND caj_eventos.fecha < CURDATE() AND caj_eventos.status = 'realizado'
AND (caj_participantes.id_organizacion_cliente = $P{id_organizacion} OR $P{id_organizacion} IS NULL)
GROUP BY caj_eventos.id
ORDER BY caj_eventos.fecha DESC


GROUP_CONCAT(caj_organizaciones.nombre SEPARATOR ', ') as "Organizaciones",

SELECT DISTINCT
caj_Lista_Objetos.id as "id objeto",
caj_eventos.id as "id_evento",
caj_eventos.fecha as "Fecha del Evento",
caj_eventos.tipo as "Tipo de Evento",
caj_eventos.tipoPuja as "Tipo de Puja",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, "PINTURA", "MONEDA") AS "TIPO DE OBJETO",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL,caj_Lista_Objetos.id_pintura,caj_Lista_Objetos.nur_moneda) AS "NUR",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, caj_Catalogo_Pintura_Tienda.titulo,caj_monedas.nombre ) as "Nombre",
caj_Lista_Objetos.precioAlcanzado as "Precio Alcanzado",
caj_Lista_Objetos.bid as "Bid",
caj_Lista_Objetos.ask as "Ask"
from caj_participantes
INNER JOIN caj_eventos
ON caj_participantes.id_evento = caj_eventos.id
INNER JOIN caj_Lista_Objetos
ON caj_eventos.id = caj_Lista_Objetos.id_evento AND caj_Lista_Objetos.id_coleccionistaParticipante = caj_participantes.id_coleccionista_cliente
LEFT JOIN caj_monedas
ON caj_Lista_Objetos.id_moneda = caj_monedas.id
LEFT JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_participantes.id_coleccionista_cliente = $P{id_coleccionista}
AND (caj_participantes.id_organizacion_cliente = $P{id_organizacion} OR $P{id_organizacion} IS NULL)
AND caj_eventos.fecha <= CURDATE()
AND (caj_eventos.fecha >= $P{fecha_inicio} AND caj_eventos.fecha <= $P{fecha_fin} OR ($P{fecha_fin} IS NULL OR $P{fecha_inicio} IS NULL))
AND (caj_eventos.fecha >= $P{fecha_inicio} OR $P{fecha_inicio} IS NULL)
AND (caj_eventos.fecha <= $P{fecha_fin} OR $P{fecha_fin} IS NULL)
ORDER BY caj_eventos.fecha DESC, caj_Lista_Objetos.precioAlcanzado DESC,"TIPO DE OBJETO" DESC;

AND (caj_participantes.id_organizacion_cliente = $P{id_organizacion} OR $P{id_organizacion} IS NULL)
AND caj_eventos.fecha <= CURDATE()
AND (caj_eventos.fecha >= $P{fecha_inicio} AND caj_eventos.fecha <= $P{fecha_fin} OR ($P{fecha_fin} IS NULL OR $P{fecha_inicio} IS NULL))
AND (caj_eventos.fecha >= $P{fecha_inicio} OR $P{fecha_inicio} IS NULL)
AND (caj_eventos.fecha <= $P{fecha_fin} OR $P{fecha_fin} IS NULL)

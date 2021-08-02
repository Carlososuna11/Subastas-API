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
COUNT(caj_organizaciones.nombre),
SUM(caj_Lista_Objetos.precioAlcanzado) as evento_precioAlcanzado
FROM caj_eventos
LEFT JOIN caj_paises as pais_evento
ON pais_evento.id = caj_eventos.id_pais
LEFT JOIN caj_planificadores
ON caj_planificadores.id_evento = caj_eventos.id
LEFT JOIN caj_organizaciones
ON caj_organizaciones.id = caj_planificadores.id_organizacion
LEFT JOIN caj_Lista_Objetos
ON caj_Lista_Objetos.id_evento = caj_eventos.id AND caj_Lista_Objetos.id_coleccionistaParticipante IS NOT NULL
WHERE caj_eventos.id = 3
GROUP BY caj_eventos.id


SELECT
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, "PINTURA", "MONEDA") AS "TIPO DE OBJETO",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL,caj_Lista_Objetos.id_pintura,caj_Lista_Objetos.nur_moneda) AS "NUR",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, caj_Catalogo_Pintura_Tienda.titulo,caj_monedas.nombre ) as "Nombre",
caj_Lista_Objetos.precioAlcanzado as "Precio Alcanzado",
caj_Lista_Objetos.bid as "Bid",
caj_Lista_Objetos.ask as "Ask",
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ', caj_coleccionistas.segundoApellido) as "Nombre del Coleccionista",
caj_organizaciones.nombre as "Organizacion"
from caj_eventos
INNER JOIN caj_Lista_Objetos
ON caj_eventos.id = caj_Lista_Objetos.id_evento AND caj_Lista_Objetos.id_coleccionistaParticipante IS NOT NULL
INNER JOIN caj_coleccionistas
ON caj_Lista_Objetos.id_coleccionistaParticipante = caj_coleccionistas.id
INNER JOIN caj_organizaciones
ON caj_organizaciones.id = caj_Lista_Objetos.id_organizacionParticipante
LEFT JOIN caj_monedas
ON caj_Lista_Objetos.id_moneda = caj_monedas.id
LEFT JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_eventos.id = $P{id_evento}
ORDER BY caj_eventos.fecha DESC, "TIPO DE OBJETO", caj_Lista_Objetos.precioAlcanzado DESC;

SELECT
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, "PINTURA", "MONEDA") AS "TIPO DE OBJETO",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL,caj_Lista_Objetos.id_pintura,caj_Lista_Objetos.nur_moneda) AS "NUR",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, caj_Catalogo_Pintura_Tienda.titulo,caj_monedas.nombre ) as "Nombre",
caj_Lista_Objetos.precioAlcanzado as "Precio Alcanzado",
caj_Lista_Objetos.bid as "Bid",
caj_Lista_Objetos.ask as "Ask",
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ', caj_coleccionistas.segundoApellido) as "Nombre del Coleccionista"
from caj_eventos
INNER JOIN caj_Lista_Objetos
ON caj_eventos.id = caj_Lista_Objetos.id_evento AND caj_Lista_Objetos.id_coleccionistaParticipante IS NOT NULL
INNER JOIN caj_coleccionistas
ON  caj_coleccionistas.id = caj_Lista_Objetos.id_coleccionistaParticipante
LEFT JOIN caj_monedas
ON caj_Lista_Objetos.id_moneda = caj_monedas.id
LEFT JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_eventos.id = 3
ORDER BY caj_eventos.fecha DESC, "TIPO DE OBJETO", caj_Lista_Objetos.precioAlcanzado DESC;


SELECT
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, "PINTURA", "MONEDA") AS "TIPO DE OBJETO",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL,caj_Lista_Objetos.id_pintura,caj_Lista_Objetos.nur_moneda) AS "NUR",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, caj_Catalogo_Pintura_Tienda.titulo,caj_monedas.nombre ) as "Nombre",
caj_Lista_Objetos.precioAlcanzado as "Precio Alcanzado",
caj_Lista_Objetos.bid as "Bid",
caj_Lista_Objetos.ask as "Ask",
caj_Lista_Objetos.razonNoVenta
from caj_eventos
INNER JOIN caj_Lista_Objetos
ON caj_eventos.id = caj_Lista_Objetos.id_evento AND caj_Lista_Objetos.id_coleccionistaParticipante IS NULL
LEFT JOIN caj_monedas
ON caj_Lista_Objetos.id_moneda = caj_monedas.id
LEFT JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_eventos.id = 3
ORDER BY caj_eventos.fecha DESC, "TIPO DE OBJETO", caj_Lista_Objetos.precioAlcanzado DESC;


SELECT
caj_organizaciones.nombre AS "Nombre de la Organizacion",
SUM(caj_Lista_Objetos.precioAlcanzado) as "Ganancia Total"
from caj_organizaciones
INNER JOIN caj_planificadores
ON caj_organizaciones.id = caj_planificadores.id_organizacion
INNER JOIN caj_eventos
ON caj_planificadores.id_evento = caj_eventos.id
LEFT JOIN caj_Lista_Objetos
ON caj_Lista_Objetos.id_evento = caj_eventos.id AND caj_Lista_Objetos.id_organizacionParticipante = caj_organizaciones.id
WHERE caj_eventos.id = $P{id_evento}
GROUP BY caj_organizaciones.id


SELECT
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, "PINTURA", "MONEDA") AS "TIPO DE OBJETO",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL,caj_Lista_Objetos.id_pintura,caj_Lista_Objetos.nur_moneda) AS "NUR",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, caj_Catalogo_Pintura_Tienda.titulo,caj_monedas.nombre ) as "Nombre",
caj_Lista_Objetos.precioAlcanzado as "Precio Alcanzado",
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ', caj_coleccionistas.segundoApellido) as "Nombre del Coleccionista",
caj_coleccionistas.dni as "DNI",
caj_organizaciones.nombre as "Organizacion",
caj_eventos.fecha AS "Fecha"
FROM caj_Lista_Objetos
INNER JOIN caj_coleccionistas
ON caj_Lista_Objetos.id_coleccionistaParticipante = caj_coleccionistas.id
INNER JOIN caj_organizaciones
ON caj_organizaciones.id = caj_Lista_Objetos.id_organizacionParticipante
INNER JOIN caj_eventos
ON caj_Lista_Objetos.id_evento = caj_eventos.id
LEFT JOIN caj_monedas
ON caj_Lista_Objetos.id_moneda = caj_monedas.id
LEFT JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_Lista_Objetos.id = $P{id_objeto}


SELECT
caj_facturas.total as "Total",
caj_facturas.fechaEmision as "Fecha",
caj_facturas.numeroFactura as "id_factura",
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ', caj_coleccionistas.segundoApellido) as "Nombre del Coleccionista",
caj_coleccionistas.dni as "DNI",
COALESCE(caj_costoEnvios.costoExtra,0) as "Costo Extra"
FROM caj_facturas
INNER JOIN caj_coleccionistas
ON caj_facturas.id_coleccionistaParticipante = caj_coleccionistas.id
INNER JOIN caj_participantes
ON caj_facturas.id_coleccionistaParticipante = caj_participantes.id_coleccionista_cliente AND caj_facturas.id_organizacionParticipante = caj_participantes.id_organizacion_cliente AND caj_facturas.id_evento = caj_participantes.id_evento
LEFT JOIN caj_costoEnvios
ON caj_facturas.id_evento = caj_costoEnvios.id_evento AND caj_participantes.id_pais = caj_costoEnvios.id_pais
WHERE caj_facturas.numeroFactura = $P{id_factura}

SELECT
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, "PINTURA", "MONEDA") AS "TIPO DE OBJETO",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL,caj_Lista_Objetos.id_pintura,caj_Lista_Objetos.nur_moneda) AS "NUR",
IF(caj_Lista_Objetos.id_pintura IS NOT NULL, caj_Catalogo_Pintura_Tienda.titulo,caj_monedas.nombre ) as "Nombre",
caj_Lista_Objetos.precioAlcanzado as "Precio Alcanzado",
caj_Lista_Objetos.bid as "Bid",
caj_Lista_Objetos.ask as "Ask",
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ', caj_coleccionistas.segundoApellido) as "Nombre del Coleccionista"
from caj_detFacturas
INNER JOIN caj_Lista_Objetos
ON caj_detFacturas.id_objeto = caj_Lista_Objetos.id
INNER JOIN caj_coleccionistas
ON  caj_coleccionistas.id = caj_Lista_Objetos.id_coleccionistaParticipante
LEFT JOIN caj_monedas
ON caj_Lista_Objetos.id_moneda = caj_monedas.id
LEFT JOIN caj_Catalogo_Pintura_Tienda
ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
WHERE caj_detFacturas.numeroFactura = 3
ORDER BY "TIPO DE OBJETO", caj_Lista_Objetos.precioAlcanzado DESC;

SELECT
CONCAT(caj_coleccionistas.nombre,' ',COALESCE(caj_coleccionistas.segundoNombre,''),' ',caj_coleccionistas.apellido,' ', caj_coleccionistas.segundoApellido) as "Nombre del Coleccionista",
caj_clientes.fechaIngreso as "Fecha Ingreso",
caj_coleccionistas.dni as "DNI",
caj_paises.nacionalidad as "Nacionalidad"
from caj_clientes
INNER JOIN caj_coleccionistas
ON caj_clientes.id_coleccionista = caj_coleccionistas.id
INNER JOIN caj_paises
ON caj_paises.id = caj_coleccionistas.id_pais_nacio
WHERE caj_clientes.id = $P{id_cliente}
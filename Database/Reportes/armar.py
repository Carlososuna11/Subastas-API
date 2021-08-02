pais = ['id','nombre','nacionalidad']
organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
contacto = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'cargo','id_organizacion']
moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
divisa = ['id','id_pais','nombre']
artista = ['id','nombre','apellido','nombreArtistico']
moneda_artista = ['id_moneda','id_artista']
coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                'fechaNacimiento','id_pais_nacio','id_pais_reside']
catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
planificador = ['id_organizacion','id_evento']
evento = ['id','inscripcionCliente','inscripcionClienteNuevo','fecha','status',
                'tipo','tipoPuja','duracionHoras','lugar','id_pais']
artista = ['id','nombre','apellido','nombreArtistico']
pintura_artista = ['id_pintura','id_artista']
#catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
pintura = ['nur','titulo','dimensionescm','estilo','ano','imagen','id_coleccionista','id_organizacion']
moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
'imagen']
pais = ['id','nombre','nacionalidad']
divisa = ['id','id_pais','nombre']
moneda_artista = ['id_moneda','id_artista']
catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
lista_objeto = ['id_evento','id_eventoParticipante','id','id_pintura','nur_moneda','id_moneda','porcentajeGananciaMin',
                'bid','ask','precioAlcanzado','orden','duracionmin','razonNoVenta','fechaIngresoParticipante','id_coleccionistaParticipante',
                'id_organizacionParticipante']
cliente = ['fechaIngreso','numeroExpedienteUnico','id_coleccionista','id_organizacion']
participante = ['id_evento','fechaIngresoCliente','id_coleccionista_cliente','id_organizacion_cliente','id_pais']
factura = ['id_evento','numeroFactura','fechaEmision','total','fechaIngresoParticipante','id_coleccionistaParticipante','id_organizacionParticipante']
detFactura = ['id_evento','id_objeto','id','numeroFactura','precio']


#-------------Ficha Tienda-----------------
# query_action =  f"""SELECT 
#                         {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
#                         {', '.join([f'caj_paises.{i} as pais_{i}' for i in pais])},
#                         {', '.join([f'caj_contactos.{i} as contacto_{i}' for i in contacto])}
#                         FROM caj_organizaciones
#                         INNER JOIN caj_paises
#                         ON caj_paises.id = caj_organizaciones.id_pais
#                         LEFT JOIN caj_contactos
#                         ON caj_contactos.id_organizacion = caj_organizaciones.id
#                         """
# query_action1 =  f"""SELECT 
#                         {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
#                         {', '.join([f'caj_paises.{i} as pais_{i}' for i in pais])}
#                         FROM caj_organizaciones
#                         INNER JOIN caj_paises
#                         ON caj_paises.id = caj_organizaciones.id_pais
#                         """
# query_action2 = f"""SELECT
#                     {', '.join([f'caj_contactos.{i} as contacto_{i}' for i in contacto])}
#                     FROM caj_contactos
#                     WHERE id_organizacion = %s
#                 """
# print(query_action1)
# print(query_action2)

#-------------Ficha Cliente-----------------
# mysql_cliente = f"""SELECT
#                 {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
#                 {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
#                 {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
#                 {', '.join([f'caj_clientes.{i} as cliente_{i}' for i in cliente])},
#                 {', '.join([f'caj_participantes.{i} as participante_{i}' for i in participante])},
#                 {', '.join([f'caj_eventos.{i} as evento_{i}' for i in evento])},
#                 {', '.join([f'caj_Lista_Objetos.{i} as objeto_{i}' for i in lista_objeto])},
#                 {', '.join([f'caj_detFacturas.{i} as detFactura_{i}' for i in detFactura])},
#                 {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_pintura_{i}' for i in pintura])},
#                 {', '.join([f'caj_Catalogo_Moneda_Tienda.{i} as catalogo_moneda_{i}' for i in catalogo_moneda_tienda])},
#                 {', '.join([f'caj_monedas.{i} as moneda_{i}' for i in moneda])}
#                 FROM caj_coleccionistas
#                 INNER JOIN caj_paises as pais_nacio
#                 ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
#                 INNER JOIN caj_paises as pais_reside
#                 ON pais_reside.id = caj_coleccionistas.id_pais_reside
#                 LEFT JOIN caj_clientes
#                 ON caj_clientes.id_coleccionista = caj_coleccionistas.id
#                 LEFT JOIN caj_participantes
#                 ON (caj_participantes.id_coleccionista_cliente,caj_participantes.id_organizacion_cliente) = (caj_coleccionistas.id,caj_clientes.id_organizacion)
#                 LEFT JOIN caj_eventos
#                 ON caj_eventos.id = caj_participantes.id_evento
#                 LEFT JOIN caj_Lista_Objetos
#                 ON (caj_Lista_Objetos.id_coleccionistaParticipante,caj_Lista_Objetos.id_evento,caj_Lista_Objetos.id_organizacionParticipante) = (caj_coleccionistas.id,caj_participantes.id_evento,caj_participantes.id_organizacion_cliente)
#                 LEFT JOIN caj_detFacturas
#                 ON caj_detFacturas.id_objeto = caj_Lista_Objetos.id
#                 LEFT JOIN caj_Catalogo_Pintura_Tienda
#                 ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
#                 LEFT JOIN caj_Catalogo_Moneda_Tienda
#                 ON caj_Lista_Objetos.nur_moneda = caj_Catalogo_Moneda_Tienda.nur
#                 LEFT JOIN caj_monedas
#                 ON caj_Catalogo_Moneda_Tienda.id_moneda = caj_monedas.id
# """

# print(mysql_cliente)

#-------------Ficha Moneda-----------------
moneda_query = f"""SELECT 
                        {', '.join([f'caj_Catalogo_Moneda_Tienda.{i} as catalogo_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'caj_monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'caj_divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_Catalogo_Moneda_Tienda
                        INNER JOIN caj_monedas
                        ON caj_monedas.id = caj_Catalogo_Moneda_Tienda.id_moneda
                        INNER JOIN caj_divisas
                        ON (caj_divisas.id,caj_divisas.id_pais) = (caj_monedas.id_divisa,caj_monedas.id_pais_divisa) 
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
                        WHERE caj_Catalogo_Moneda_Tienda.nur = %s
                    """
                    # {', '.join([f'caj_M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                    #     {', '.join([f'caj_artistas.{i} as artista_{i}' for i in artista])},
                    # LEFT JOIN caj_M_A
                    #     ON caj_M_A.id_moneda = caj_monedas.id
                    #     LEFT JOIN caj_artistas
                    #     ON caj_M_A.id_artista = caj_artistas.id
moneda_artista_query = f"""SELECT
                        {', '.join([f'caj_M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'caj_artistas.{i} as artista_{i}' for i in artista])},
                        LEFT JOIN caj_M_A
                        ON caj_M_A.id_moneda = caj_monedas.id
                        LEFT JOIN caj_artistas
                        ON caj_M_A.id_artista = caj_artistas.id
                        """
# print(moneda_query)
# print(moneda_artista_query)
# pintura_query = f"""SELECT 
#                         {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
#                         {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
#                         {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
#                         {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
#                         {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
#                         {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
#                         FROM caj_Catalogo_Pintura_Tienda
#                         LEFT JOIN caj_organizaciones
#                         ON caj_organizaciones.id = caj_Catalogo_Pintura_Tienda.id_organizacion
#                         LEFT JOIN caj_paises as organizacion_pais
#                         ON organizacion_pais.id = caj_organizaciones.id_pais
#                         LEFT JOIN caj_coleccionistas
#                         ON caj_coleccionistas.id = caj_Catalogo_Pintura_Tienda.id_coleccionista
#                         LEFT JOIN caj_paises as pais_nacio
#                         ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
#                         LEFT JOIN caj_paises as pais_reside
#                         ON pais_reside.id = caj_coleccionistas.id_pais_reside
#                         """

# # print(pintura_query)

# participantes_query = f"""SELECT
#                     {', '.join([f'caj_participantes.{i} as participante_{i}' for i in participante])},
#                     {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
#                     {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
#                     FROM caj_participantes
#                     INNER JOIN caj_coleccionistas
#                     ON caj_coleccionistas.id = caj_participantes.id_coleccionista_cliente
#                     INNER JOIN caj_organizaciones
#                     ON caj_organizaciones.id = caj_participantes.id_organizacion_cliente
#                     """

# # print(participantes_query)

# planificadores_query = f"""SELECT 
#                         {', '.join([f'caj_planificadores.{i} as planificador_{i}' for i in planificador])},
#                         {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])}
#                         FROM caj_planificadores
#                         INNER JOIN caj_organizaciones
#                         ON caj_planificadores.id_organizacion = caj_organizaciones.id
#                         """
# # print(planificadores_query)

# lista_objeto = f"""SELECT 
#                         {', '.join([f'caj_Lista_Objetos.{i} as lista_{i}' for i in lista_objeto])}
#                         FROM caj_Lista_Objetos
#                         """

# evento_query = f"""SELECT 
#                         {', '.join([f'caj_eventos.{i} as evento_{i}' for i in evento])},
#                         {', '.join([f'pais_evento.{i} as pais_evento_{i}' for i in pais])}
#                         FROM caj_eventos
#                         LEFT JOIN caj_paises as pais_evento
#                         ON pais_evento.id = caj_eventos.id_pais
#                         """

# print(evento_query)

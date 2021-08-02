#### PARÁMETROS POR REPORTE

### FICHA TIENDA
- id_organizacion:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6

Hacer el select 
- Organizacion:
```sql
SELECT * from caj_organizaciones where id = 1;
```
- Contactos:
```sql
SELECT * from caj_contactos where id_organizacion = 1;
```
- Clientes:
```sql
SELECT * from caj_clientes where id_organizacion = 1;
```

### Expediente del cliente:
- id_coleccionista:
    - 1
    - 2
    - 3
- id_organizacion:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6

Hacer el select
- Coleccionistas:
```sql
SELECT * from caj_coleccionistas where id=1;
```
- Cliente:
```sql
SELECT * from caj_clientes where id_coleccionista = 1;
```
- Participante
```sql
SELECT * from caj_participantes where id_coleccionista_cliente = 1;
```
- Objetos comprados:
```sql
SELECT * from caj_Lista_Objetos where id_coleccionistaParticipante = 1;
```

### Ficha Evento:
- id_evento:
    - 1
    - 2
    - 3
    - 4
    - 5
    - 6

- Evento:
```sql
SELECT * from caj_eventos where id = 1;
```
- planificadores:
```sql
SELECT * from caj_planificadores where id_evento = 1;
```
- participantes:
```sql
SELECT * from caj_participantes where id_evento = 1;
```
- Objetos a subastar:
```sql
SELECT * from caj_Lista_Objetos where id_evento = 1;
```

### Ficha Objeto Pintura
- id_pintura:
    - 10021  - coleccionista dueño
    - 10022  - coleccionista dueño
    - 10023  - coleccionista dueño
    - 10024
    - 10025
    - 10026
    - 10027
    - 10028
    - 10029
    - 10030
    - 10031
    - 10032
    - 10033
    - 10034
    - 10035
    - 10036
    - 10037  - coleccionista dueño

- Hacer el select
- Pinturas:
```sql
SELECT * FROM caj_Catalogo_Pintura_Tienda where nur = 10021;
```

### Ficha Moneda
- id_moneda:
    - 10000
    - 10001
    - 10002
    - 10003  - coleccionista dueño
    - 10004  - coleccionista dueño
    - 10005
    - 10006
    - 10007
    - 10008
    - 10009
    - 10010
    - 10011
    - 10012
    - 10013
    - 10014
    - 10015
    - 10016
    - 10017

- Hacer el select
- Monedas:
```sql
SELECT * FROM caj_Catalogo_Moneda_Tienda where nur = 10000;
```
### Informe Resultados por evento
- id_evento:
    - 1 - realizado
    - 2 - realizado
    - 3 - realizado
    - 4 - realizado
    - 5 - pendiente
    - 6 - realizado

- Hacer el select
- Resultados por evento:
```sql
SELECT * FROM caj_eventos where id = 1;
```
- planificadores:
```sql
SELECT * from caj_planificadores where id_evento = 1;
```
- participantes:
```sql
SELECT * from caj_participantes where id_evento = 1;
```
- Objetos a subastar:
```sql
SELECT * from caj_Lista_Objetos where id_evento = 1;
```

### Certificados
- id_Objeto:
    - 1
    - 6
    - 7
    - 8
    - 9
    - 10

- Hacer el select

- Evento:
```sql
SELECT * from caj_eventos where id = 1;
```
- coleccionista:
```sql
SELECT * from caj_coleccionistas where id=1;
```
- Objetos a subastar:
```sql
SELECT * from caj_Lista_Objetos where id_evento = 1;
```

### Facturas
- id_factura:
    - 1
    - 2
    - 3
    - 4
    - 5

- Facturas:
```sql
SELECT * from caj_facturas where numeroFactura = 1;
```

- detFacturas:
```sql
SELECT * from caj_detFacturas where numeroFactura = 1;
```

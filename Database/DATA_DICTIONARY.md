# Schema documentation

Generated by MySQL Workbench Model Documentation v1.0.0 - Copyright (c) 2015 Hieu Le

## Table: `Catalogo_Moneda_Tienda`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_moneda` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `monedas`. |
| `nur` | INT | PRIMARY, Not null, Unique |   |   |
| `id_coleccionista` | INT |  | `NULL` |  **foreign key** to column `dni` on table `coleccionistas`. |
| `id_organizacion` | INT |  | `NULL` |  **foreign key** to column `id` on table `organizaciones`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id_moneda`, `nur` | PRIMARY |   |
| nur | `nur` | UNIQUE |   |
| fk_coleccionista_moneda | `id_coleccionista` | INDEX |   |
| fk_organizacion_moneda | `id_organizacion` | INDEX |   |


## Table: `Catalogo_Pintura_Tienda`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `nur` | INT | PRIMARY, Not null |   |   |
| `titulo` | VARCHAR(100) | Not null |   |   |
| `dimensionescm` | VARCHAR(20) | Not null |   |   |
| `estilo` | VARCHAR(30) | Not null |   |   |
| `ano` | YEAR |  | `NULL` |   |
| `imagen` | VARCHAR(255) |  | `NULL` |   |
| `id_coleccionista` | INT |  | `NULL` |  **foreign key** to column `dni` on table `coleccionistas`. |
| `id_organizacion` | INT |  | `NULL` |  **foreign key** to column `id` on table `organizaciones`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `nur` | PRIMARY |   |
| fk_coleccionista_pintura | `id_coleccionista` | INDEX |   |
| fk_organizacion_pintura | `id_organizacion` | INDEX |   |


## Table: `Lista_Objetos`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_evento` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `eventos`. |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `id_pintura` | INT |  | `NULL` |  **foreign key** to column `nur` on table `Catalogo_Pintura_Tienda`. |
| `id_moneda` | INT |  | `NULL` |  **foreign key** to column `nur` on table `Catalogo_Moneda_Tienda`. |
| `porcentajeGananciaMin` | DECIMAL | Not null |   |   |
| `bid` | DECIMAL | Not null |   |   |
| `ask` | DECIMAL | Not null |   |   |
| `preciAlcanzado` | DECIMAL |  | `NULL` |   |
| `orden` | INT |  | `NULL` |   |
| `duracionmin` | INT |  | `NULL` |   |
| `razonNoVenta` | VARCHAR(20) |  | `NULL` |   |
| `fechaIngresoParticipante` | DATE |  | `NULL` |  **foreign key** to column `fechaIngresoCliente` on table `participantes`. |
| `id_coleccionistaParticipante` | INT |  | `NULL` |   |
| `id_organizacionParticipante` | INT |  | `NULL` |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id`, `id_evento` | PRIMARY |   |
| fk_evento_objetos | `id_evento` | INDEX |   |
| fk_cliente_objeto | `fechaIngresoParticipante`, `id_coleccionistaParticipante`, `id_organizacionParticipante`, `id_evento` | INDEX |   |
| fk_evento_pintura | `id_pintura` | INDEX |   |
| fk_evento_moneda | `id_moneda` | INDEX |   |


## Table: `M_A`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_moneda` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `monedas`. |
| `id_artista` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `artistas`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id_moneda`, `id_artista` | PRIMARY |   |
| fk_artista_M_A | `id_artista` | INDEX |   |


## Table: `P_A`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_pintura` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `monedas`. |
| `id_artista` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `artistas`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id_pintura`, `id_artista` | PRIMARY |   |
| fk_artista_P_A | `id_artista` | INDEX |   |


## Table: `artistas`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `nombre` | VARCHAR(30) |  | `NULL` |   |
| `apellido` | VARCHAR(30) |  | `NULL` |   |
| `nombreArtistico` | VARCHAR(30) |  | `NULL` |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id` | PRIMARY |   |


## Table: `clientes`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `fechaIngreso` | DATE | PRIMARY, Not null |   |   |
| `numeroExpedienteUnico` | INT | Not null, Unique |   |   |
| `id_coleccionista` | INT | PRIMARY, Not null, Unique |   |  **foreign key** to column `dni` on table `coleccionistas`. |
| `id_organizacion` | INT | PRIMARY, Not null, Unique |   |  **foreign key** to column `id` on table `organizaciones`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `fechaIngreso`, `id_coleccionista`, `id_organizacion` | PRIMARY |   |
| numeroExpedienteUnico | `numeroExpedienteUnico` | UNIQUE |   |
| unique_cliente | `id_coleccionista`, `id_organizacion` | UNIQUE |   |
| fk_organizacion_cliente | `id_organizacion` | INDEX |   |


## Table: `coleccionistas`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `dni` | INT | PRIMARY, Not null |   |   |
| `nombre` | VARCHAR(30) | Not null |   |   |
| `segundoNombre` | VARCHAR(30) |  | `NULL` |   |
| `apellido` | VARCHAR(30) | Not null |   |   |
| `segundoApellido` | VARCHAR(30) | Not null |   |   |
| `telefono` | VARCHAR(20) | Not null, Unique |   |   |
| `email` | VARCHAR(50) | Not null, Unique |   |   |
| `fechaNacimiento` | DATE | Not null |   |   |
| `id_pais_nacio` | INT | Not null |   |  **foreign key** to column `id` on table `paises`. |
| `id_pais_reside` | INT | Not null |   |  **foreign key** to column `id` on table `paises`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `dni` | PRIMARY |   |
| telefono | `telefono` | UNIQUE |   |
| email | `email` | UNIQUE |   |
| fk_pais_nacio | `id_pais_nacio` | INDEX |   |
| fk_pais_reside | `id_pais_reside` | INDEX |   |


## Table: `contactos`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_organizacion` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `organizaciones`. |
| `dni` | INT | PRIMARY, Not null |   |   |
| `nombre` | VARCHAR(30) | Not null |   |   |
| `segundoNombre` | VARCHAR(30) |  | `NULL` |   |
| `apellido` | VARCHAR(30) | Not null |   |   |
| `segundoApellido` | VARCHAR(30) | Not null |   |   |
| `telefono` | VARCHAR(20) | Not null, Unique |   |   |
| `email` | VARCHAR(50) | Not null, Unique |   |   |
| `cargo` | VARCHAR(30) | Not null |   |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `dni`, `id_organizacion` | PRIMARY |   |
| telefono | `telefono` | UNIQUE |   |
| email | `email` | UNIQUE |   |
| fk_organizacion | `id_organizacion` | INDEX |   |


## Table: `costoEnvios`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_evento` | INT | PRIMARY, Not null, Unique |   |  **foreign key** to column `id` on table `eventos`. |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `costoExtra` | DECIMAL |  | `NULL` |   |
| `id_pais` | INT | Not null, Unique |   |  **foreign key** to column `id` on table `paises`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id`, `id_evento` | PRIMARY |   |
| unique_costo_envio | `id_pais`, `id_evento` | UNIQUE |   |
| fk_evento_costoEnvio | `id_evento` | INDEX |   |


## Table: `detFacturas`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_evento` | INT | Not null |   |   |
| `id_objeto` | INT | Not null |   |  **foreign key** to column `id` on table `Lista_Objetos`. |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `numeroFactura` | INT | PRIMARY, Not null |   |  **foreign key** to column `numeroFactura` on table `facturas`. |
| `precio` | DECIMAL | Not null |   |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id`, `numeroFactura` | PRIMARY |   |
| fk_detFacturas_objeto | `id_objeto`, `id_evento` | INDEX |   |
| fk_factura_Det | `numeroFactura` | INDEX |   |


## Table: `divisas`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_pais` | INT | PRIMARY, Not null, Unique |   |  **foreign key** to column `id` on table `paises`. |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `nombre` | VARCHAR(30) | Not null, Unique |   |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id`, `id_pais` | PRIMARY |   |
| unique_divisas | `nombre`, `id_pais` | UNIQUE |   |
| fk_pais | `id_pais` | INDEX |   |


## Table: `eventos`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id` | INT | PRIMARY, Not null |   |   |
| `inscripcionCliente` | DECIMAL | Not null |   |   |
| `inscripcionClienteNuevo` | DECIMAL |  | `NULL` |   |
| `fecha` | DATETIME | Not null |   |   |
| `status` | VARCHAR(12) | Not null |   |   |
| `tipo` | VARCHAR(12) | Not null |   |   |
| `tipoPuja` | VARCHAR(20) | Not null |   |   |
| `duracionHoras` | INT | Not null |   |   |
| `lugar` | VARCHAR(100) |  | `NULL` |   |
| `id_pais` | INT |  | `NULL` |  **foreign key** to column `id` on table `paises`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id` | PRIMARY |   |
| fk_pais_evento | `id_pais` | INDEX |   |


## Table: `facturas`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_evento` | INT | Not null |   |   |
| `numeroFactura` | INT | PRIMARY, Auto increments, Not null |   |   |
| `fechaEmision` | DATE | Not null |   |   |
| `total` | DECIMAL | Not null |   |   |
| `fechaIngresoParticipante` | DATE |  | `NULL` |  **foreign key** to column `fechaIngresoCliente` on table `participantes`. |
| `id_coleccionistaParticipante` | INT |  | `NULL` |   |
| `id_organizacionParticipante` | INT |  | `NULL` |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `numeroFactura` | PRIMARY |   |
| fk_participante_factura | `fechaIngresoParticipante`, `id_coleccionistaParticipante`, `id_organizacionParticipante`, `id_evento` | INDEX |   |


## Table: `monedas`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `nombre` | VARCHAR(100) | Not null |   |   |
| `denominacion` | INT | Not null |   |   |
| `mintage` | INT | Not null |   |   |
| `forma` | VARCHAR(10) | Not null |   |   |
| `metal` | VARCHAR(10) | Not null |   |   |
| `diametromm` | INT | Not null |   |   |
| `canto` | VARCHAR(10) | Not null |   |   |
| `pesogr` | INT | Not null |   |   |
| `ano` | YEAR | Not null |   |   |
| `motivo` | VARCHAR(100) | Not null |   |   |
| `acunacion` | VARCHAR(100) | Not null |   |   |
| `anverso` | TEXT | Not null |   |   |
| `reverso` | TEXT | Not null |   |   |
| `id_pais` | INT | Not null |   |  **foreign key** to column `id` on table `paises`. |
| `id_divisa` | INT | Not null |   |  **foreign key** to column `id` on table `divisas`. |
| `imagen` | VARCHAR(255) |  | `NULL` |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id` | PRIMARY |   |
| fk_paisMonedas | `id_pais` | INDEX |   |
| fk_divisa | `id_divisa`, `id_pais` | INDEX |   |


## Table: `organizaciones`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id` | INT | PRIMARY, Not null |   |   |
| `nombre` | VARCHAR(50) | Not null |   |   |
| `proposito` | TEXT | Not null |   |   |
| `fundacion` | DATE | Not null |   |   |
| `alcance` | VARCHAR(15) | Not null |   |   |
| `tipo` | VARCHAR(10) | Not null |   |   |
| `telefonoPrincipal` | VARCHAR(20) | Not null, Unique |   |   |
| `paginaWeb` | VARCHAR(50) | Unique | `NULL` |   |
| `emailCorporativo` | VARCHAR(50) | Unique | `NULL` |   |
| `id_pais` | INT | Not null |   |  **foreign key** to column `id` on table `paises`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id` | PRIMARY |   |
| telefonoPrincipal | `telefonoPrincipal` | UNIQUE |   |
| paginaWeb | `paginaWeb` | UNIQUE |   |
| emailCorporativo | `emailCorporativo` | UNIQUE |   |
| fk_pais_org | `id_pais` | INDEX |   |


## Table: `paises`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id` | INT | PRIMARY, Auto increments, Not null |   |   |
| `nombre` | VARCHAR(30) | Not null, Unique |   |   |
| `nacionalidad` | VARCHAR(30) | Not null, Unique |   |   |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id` | PRIMARY |   |
| nombre | `nombre` | UNIQUE |   |
| nacionalidad | `nacionalidad` | UNIQUE |   |


## Table: `participantes`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_evento` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `eventos`. |
| `fechaIngresoCliente` | DATE | PRIMARY, Not null |   |  **foreign key** to column `fechaIngreso` on table `clientes`. |
| `id_coleccionista_cliente` | INT | PRIMARY, Not null |   |   |
| `id_organizacion_cliente` | INT | PRIMARY, Not null |   |   |
| `id_pais` | INT |  | `NULL` |  **foreign key** to column `id` on table `paises`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `fechaIngresoCliente`, `id_coleccionista_cliente`, `id_organizacion_cliente`, `id_evento` | PRIMARY |   |
| fk_evento_participante | `id_evento` | INDEX |   |
| fk_pais_envio | `id_pais` | INDEX |   |


## Table: `planificadores`

### Description: 



### Columns: 

| Column | Data type | Attributes | Default | Description |
| --- | --- | --- | --- | ---  |
| `id_evento` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `eventos`. |
| `id_organizacion` | INT | PRIMARY, Not null |   |  **foreign key** to column `id` on table `organizaciones`. |


### Indices: 

| Name | Columns | Type | Description |
| --- | --- | --- | --- |
| PRIMARY | `id_evento`, `id_organizacion` | PRIMARY |   |
| fk_organizacion_planificador | `id_organizacion` | INDEX |   |


SELECT
    TABLE_NAME, ENGINE, VERSION, ROW_FORMAT, TABLE_ROWS, AVG_ROW_LENGTH,
    DATA_LENGTH, MAX_DATA_LENGTH, INDEX_LENGTH, DATA_FREE, AUTO_INCREMENT,
    CREATE_TIME, UPDATE_TIME, CHECK_TIME, TABLE_COLLATION, CHECKSUM,
    CREATE_OPTIONS, TABLE_COMMENT
  FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'subastas'
DROP DATABASE IF EXISTS subastas;
CREATE DATABASE subastas;

USE subastas;

CREATE TABLE caj_paises (
    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    nacionalidad VARCHAR(30) NOT NULL
);

CREATE TABLE caj_divisas (
    id_pais TINYINT UNSIGNED  NOT NULL,
    id SMALLINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_divisa PRIMARY KEY (id,id_pais),
    CONSTRAINT fk_pais FOREIGN KEY (id_pais)
        REFERENCES caj_paises(id),
    INDEX IDX_divisa_pais (id_pais)
);

CREATE TABLE caj_monedas (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    denominacion DECIMAL(7,3) NOT NULL,
    mintage NUMERIC(10) NOT NULL,
    forma VARCHAR(10) NOT NULL CHECK (forma in ('circular','cuadrada')),
    metal VARCHAR(10) NOT NULL CHECK (metal in ('plata','oro','platino')),
    diametromm DECIMAL(6,2) NOT NULL,
    canto VARCHAR(10) NOT NULL CHECK (canto in ('estriado','liso')),
    pesogr DECIMAL(6,2) NOT NULL,
    ano NUMERIC(4) NOT NULL,
    motivo VARCHAR(100) NOT NULL,
    acunacion VARCHAR(100) NOT NULL,
    anverso TEXT NOT NULL,
    reverso TEXT NOT NULL,
    id_pais_divisa TINYINT UNSIGNED NOT NULL,
    id_pais TINYINT UNSIGNED NOT NULL,
    id_divisa SMALLINT UNSIGNED  NOT NULL,
    imagen VARCHAR(255),
    CONSTRAINT fk_paiscaj_monedas FOREIGN KEY (id_pais)
        REFERENCES caj_paises(id),
    CONSTRAINT fk_divisa FOREIGN KEY (id_divisa,id_pais_divisa)
        REFERENCES caj_divisas(id,id_pais),
    INDEX IDX_caj_monedas_pais (id_pais),
    INDEX IDX_caj_monedas_divisa (id_divisa,id_pais_divisa) 
);

CREATE TABLE caj_artistas (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    nombreArtistico VARCHAR(30)
);

CREATE TABLE caj_M_A (
    id_moneda MEDIUMINT UNSIGNED  NOT NULL,
    id_artista SMALLINT UNSIGNED  NOT NULL,
    CONSTRAINT pk_caj_M_A  PRIMARY KEY (id_moneda,id_artista),
    CONSTRAINT fk_moneda_caj_M_A FOREIGN KEY (id_moneda)
        REFERENCES caj_monedas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_artista_caj_M_A FOREIGN KEY (id_artista)
        REFERENCES caj_artistas(id)
        ON DELETE CASCADE,
    INDEX IDX_caj_M_A_moneda (id_moneda),
    INDEX IDX_caj_M_A_artista (id_artista)
);

CREATE TABLE caj_coleccionistas (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(20) NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    segundoNombre VARCHAR(30),
    apellido VARCHAR(30) NOT NULL,
    segundoApellido VARCHAR(30) NOT NULL,
    telefono VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    fechaNacimiento DATE NOT NULL,
    id_pais_nacio TINYINT UNSIGNED NOT NULL,
    id_pais_reside TINYINT UNSIGNED NOT NULL,
    CONSTRAINT fk_pais_nacio FOREIGN KEY (id_pais_nacio)
        REFERENCES caj_paises(id),
    CONSTRAINT fk_pais_reside FOREIGN KEY (id_pais_reside)
        REFERENCES caj_paises(id),
    CONSTRAINT unique_coleccionista UNIQUE(id_pais_nacio,dni),
    INDEX IDX_caj_coleccionistas_pais_nacio (id_pais_nacio),
    INDEX IDX_caj_coleccionistas_pais_reside (id_pais_reside)
);

CREATE TABLE caj_organizaciones(
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    proposito TEXT NOT NULL,
    fundacion NUMERIC(4) NOT NULL,
    alcance VARCHAR(15) NOT NULL CHECK (alcance in ('nacional','internacional')),
    tipo VARCHAR(10) NOT NULL CHECK (tipo in ('galeria','tienda','otro')),
    telefonoPrincipal VARCHAR(20) NOT NULL UNIQUE,
    paginaWeb VARCHAR(50) UNIQUE,
    emailCorporativo  VARCHAR(50) UNIQUE,
    id_pais TINYINT UNSIGNED NOT NULL,
    CONSTRAINT fk_pais_org FOREIGN KEY (id_pais)
        REFERENCES caj_paises(id),
    INDEX IDX_caj_organizaciones_pais (id_pais)
);

CREATE TABLE caj_contactos (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_organizacion MEDIUMINT UNSIGNED NOT NULL ,
    dni VARCHAR(20) NOT NULL ,
    nombre VARCHAR(30) NOT NULL,
    segundoNombre VARCHAR(30),
    apellido VARCHAR(30) NOT NULL,
    segundoApellido VARCHAR(30) NOT NULL,
    telefono VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    cargo VARCHAR(30) NOT NULL,
    CONSTRAINT pk_caj_contactos PRIMARY KEY (id,id_organizacion),
    CONSTRAINT fk_organizacion FOREIGN KEY (id_organizacion)
        REFERENCES caj_organizaciones(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_contacto UNIQUE(id_organizacion,dni),
    INDEX IDX_caj_contactos_organizacion (id_organizacion)

);

CREATE TABLE caj_clientes (
    fechaIngreso DATE NOT NULL,
    numeroExpedienteUnico MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_coleccionista MEDIUMINT UNSIGNED NOT NULL,
    id_organizacion MEDIUMINT UNSIGNED NOT NULL,
    CONSTRAINT pk_cliente PRIMARY KEY (fechaIngreso,id_coleccionista,id_organizacion),
    CONSTRAINT fk_coleccionista_cliente FOREIGN KEY (id_coleccionista)
        REFERENCES caj_coleccionistas(id),
    CONSTRAINT fk_organizacion_cliente FOREIGN KEY (id_organizacion)
        REFERENCES caj_organizaciones(id),
    CONSTRAINT unique_cliente UNIQUE(id_coleccionista,id_organizacion),
    INDEX IDX_caj_clientes_organizacion (id_organizacion),
    INDEX IDX_caj_clientes_coleccionista (id_coleccionista)
);

CREATE TABLE caj_Catalogo_Moneda_Tienda (
    id_moneda MEDIUMINT UNSIGNED  NOT NULL,
    nur MEDIUMINT UNSIGNED NOT NULL UNIQUE,
    id_coleccionista MEDIUMINT UNSIGNED,
    id_organizacion MEDIUMINT UNSIGNED,
    CONSTRAINT pk_catalogo_moneda PRIMARY KEY (id_moneda,nur),
    CONSTRAINT fk_moneda_catalogo FOREIGN KEY (id_moneda)
        REFERENCES caj_monedas(id),
    CONSTRAINT fk_coleccionista_moneda FOREIGN KEY (id_coleccionista)
        REFERENCES caj_coleccionistas(id),
    CONSTRAINT fk_organizacion_moneda FOREIGN KEY (id_organizacion)
        REFERENCES caj_organizaciones(id),
    INDEX IDX_caj_catalogo_moneda_tienda (id_moneda),
    INDEX IDX_caj_catalogo_moneda_coleccionista (id_coleccionista),
    INDEX IDX_caj_catalogo_moneda_organizacion (id_organizacion)   
);

CREATE TABLE caj_Catalogo_Pintura_Tienda (
    nur MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    dimensionescm VARCHAR(20) NOT NULL,
    estilo VARCHAR(30) NOT NULL,
    ano NUMERIC(4),
    imagen VARCHAR(255),
    id_coleccionista MEDIUMINT UNSIGNED,
    id_organizacion MEDIUMINT UNSIGNED,
    CONSTRAINT fk_coleccionista_pintura FOREIGN KEY (id_coleccionista)
        REFERENCES caj_coleccionistas(id),
    CONSTRAINT fk_organizacion_pintura FOREIGN KEY (id_organizacion)
        REFERENCES caj_organizaciones(id),
    INDEX IDX_caj_catalogo_pintura_tienda (id_organizacion),
    INDEX IDX_caj_catalogo_pintura_coleccionista (id_coleccionista)   
);

CREATE TABLE caj_P_A (
    id_pintura MEDIUMINT UNSIGNED NOT NULL,
    id_artista SMALLINT UNSIGNED NOT NULL,
    CONSTRAINT pk_p_a  PRIMARY KEY (id_pintura,id_artista),
    CONSTRAINT fk_pintura_P_A FOREIGN KEY (id_pintura)
        REFERENCES caj_Catalogo_Pintura_Tienda(nur)
        ON DELETE CASCADE,
    CONSTRAINT fk_artista_P_A FOREIGN KEY (id_artista)
        REFERENCES caj_artistas(id)
        ON DELETE CASCADE,
    INDEX IDX_caj_p_a_pintura (id_pintura),
    INDEX IDX_caj_p_a_artista (id_artista)
);

CREATE TABLE caj_eventos (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    inscripcionCliente DECIMAL(13,2) NOT NULL,
    inscripcionClienteNuevo DECIMAL(13,2),
    fecha DATE NOT NULL,
    status VARCHAR(12) NOT NULL CHECK (status in ('realizado','pendiente','cancelado')),
    tipo VARCHAR(12) NOT NULL CHECK (tipo in ('virtual','presencial')),
    tipoPuja VARCHAR(20) NOT NULL CHECK (tipoPuja in ('ascendente','sobre cerrado')),
    duracionHoras NUMERIC(1) NOT NULL,
    lugar VARCHAR(100),
    id_pais TINYINT UNSIGNED,
    CONSTRAINT fk_pais_evento FOREIGN KEY (id_pais)
        REFERENCES caj_paises(id),
    INDEX IDX_caj_eventos_pais (id_pais)
);

CREATE TABLE caj_planificadores (
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    id_organizacion MEDIUMINT UNSIGNED NOT NULL,
    CONSTRAINT pk_planificador  PRIMARY KEY (id_evento,id_organizacion),
    CONSTRAINT fk_evento_planificador FOREIGN KEY (id_evento)
        REFERENCES caj_eventos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_organizacion_planificador FOREIGN KEY (id_organizacion)
        REFERENCES caj_organizaciones(id)
        ON DELETE CASCADE,
    INDEX IDX_caj_planificadores_evento (id_evento),
    INDEX IDX_caj_planificadores_organizacion (id_organizacion)
);

CREATE TABLE caj_participantes (
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    fechaIngresoCliente DATE NOT NULL,
    id_coleccionista_cliente MEDIUMINT UNSIGNED NOT NULL,
    id_organizacion_cliente MEDIUMINT UNSIGNED NOT NULL,
    id_pais TINYINT UNSIGNED,
    CONSTRAINT pk_participante  PRIMARY KEY (fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento),
    CONSTRAINT fk_evento_participante FOREIGN KEY (id_evento)
        REFERENCES caj_eventos(id),
    CONSTRAINT fk_pais_envio FOREIGN KEY (id_pais)
        REFERENCES caj_paises(id),
    CONSTRAINT fk_cliente_participantes FOREIGN KEY (fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente)
        REFERENCES caj_clientes(fechaIngreso,id_coleccionista,id_organizacion),
    INDEX IDX_caj_participantes_evento (id_evento),
    INDEX IDX_caj_participantes_pais (id_pais),
    INDEX IDX_caj_participantes_cliente(id_organizacion_cliente,id_coleccionista_cliente)
);

CREATE TABLE caj_costoEnvios (
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    costoExtra DECIMAL(10,2),
    id_pais TINYINT UNSIGNED NOT NULL,
    CONSTRAINT pk_costoEnvio  PRIMARY KEY (id,id_evento),
    CONSTRAINT fk_evento_costoEnvio FOREIGN KEY (id_evento)
        REFERENCES caj_eventos(id),
    CONSTRAINT fk_pais_costoEnvio FOREIGN KEY (id_pais)
        REFERENCES caj_paises(id),
    CONSTRAINT unique_costo_envio UNIQUE(id_pais,id_evento),
    INDEX IDX_caj_costoEnvios_evento (id_evento),
    INDEX IDX_caj_costoEnvios_pais (id_pais)
);

CREATE TABLE caj_Lista_Objetos (
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    id_eventoParticipante MEDIUMINT UNSIGNED,
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_pintura MEDIUMINT UNSIGNED,
    nur_moneda MEDIUMINT UNSIGNED,
    id_moneda MEDIUMINT UNSIGNED,
    porcentajeGananciaMin DECIMAL(8,2) NOT NULL,
    bid DECIMAL(13,2) NOT NULL,
    ask DECIMAL(13,2) NOT NULL,
    precioAlcanzado DECIMAL(13,2),
    orden NUMERIC(3),
    duracionmin NUMERIC(3),
    razonNoVenta VARCHAR(20) CHECK (razonNoVenta in ('sin ofertas','inferior al ask')),
    fechaIngresoParticipante DATE,
    id_coleccionistaParticipante MEDIUMINT UNSIGNED,
    id_organizacionParticipante MEDIUMINT UNSIGNED,
    CONSTRAINT pk_lista_objetos PRIMARY KEY (id,id_evento),
    CONSTRAINT fk_evento_objetos FOREIGN KEY (id_evento)
        REFERENCES caj_eventos(id),
    CONSTRAINT fk_cliente_objeto FOREIGN KEY (fechaIngresoParticipante,id_coleccionistaParticipante,id_organizacionParticipante,id_eventoParticipante)
        REFERENCES caj_participantes(fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento),
    CONSTRAINT fk_evento_pintura FOREIGN KEY (id_pintura)
        REFERENCES caj_Catalogo_Pintura_Tienda(nur),
    CONSTRAINT fk_evento_moneda FOREIGN KEY (nur_moneda,id_moneda)
        REFERENCES caj_Catalogo_Moneda_Tienda(nur,id_moneda),
    INDEX IDX_caj_Lista_Objetos_evento (id_evento),
    INDEX IDX_caj_Lista_Objetos_Participante (id_eventoParticipante,id_coleccionistaParticipante,id_organizacionParticipante,fechaIngresoParticipante),
    INDEX IDX_caj_Lista_Objetos_pintura (id_pintura),
    INDEX IDX_caj_Lista_Objetos_moneda (nur_moneda,id_moneda)
);

CREATE TABLE caj_facturas (
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    numeroFactura MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fechaEmision DATE NOT NULL,
    total DECIMAL(13,2) NOT NULL,
    fechaIngresoParticipante DATE,
    id_coleccionistaParticipante MEDIUMINT UNSIGNED,
    id_organizacionParticipante MEDIUMINT UNSIGNED,
    CONSTRAINT fk_participante_factura FOREIGN KEY (fechaIngresoParticipante,id_coleccionistaParticipante,id_organizacionParticipante,id_evento)
        REFERENCES caj_participantes(fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento),
    INDEX IDX_caj_participantes_factura (id_evento,fechaIngresoParticipante,id_coleccionistaParticipante,id_organizacionParticipante)
);

CREATE TABLE caj_detFacturas (
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    id_objeto MEDIUMINT UNSIGNED  NOT NULL,
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    numeroFactura MEDIUMINT UNSIGNED NOT NULL,
    precio DECIMAL(13,2) NOT NULL,
    CONSTRAINT pk_detFactura PRIMARY KEY (id,numeroFactura),
    CONSTRAINT fk_detFacturas_objeto FOREIGN KEY (id_objeto,id_evento)
        REFERENCES caj_Lista_Objetos(id,id_evento),
    CONSTRAINT fk_factura_Det FOREIGN KEY (numeroFactura)
        REFERENCES caj_facturas(numeroFactura),
    INDEX IDX_caj_detFacturas_evento (id_evento,id_objeto),
    INDEX IDX_caj_detFacturas_factura (numeroFactura)
);

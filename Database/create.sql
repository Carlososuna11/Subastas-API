DROP DATABASE subastas;
CREATE DATABASE subastas;

USE subastas;

CREATE TABLE paises (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    nacionalidad VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE divisas (
    id_pais INT NOT NULL,
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_divisa PRIMARY KEY (id,id_pais),
    CONSTRAINT fk_pais FOREIGN KEY (id_pais)
        REFERENCES paises(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_divisas UNIQUE(nombre,id_pais)
);

CREATE TABLE monedas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    denominacion INT NOT NULL,
    mintage INT NOT NULL,
    forma VARCHAR(10) NOT NULL CHECK (forma in ('circular','cuadrada')),
    metal VARCHAR(10) NOT NULL CHECK (metal in ('plata','oro','platino')),
    diametromm INT NOT NULL,
    canto VARCHAR(10) NOT NULL CHECK (canto in ('estriado','liso')),
    pesogr INT NOT NULL,
    ano YEAR NOT NULL,
    motivo VARCHAR(100) NOT NULL,
    acunacion VARCHAR(100) NOT NULL,
    anverso TEXT NOT NULL,
    reverso TEXT NOT NULL,
    id_pais_divisa INT NOT NULL,
    id_pais INT NOT NULL,
    id_divisa INT NOT NULL,
    imagen VARCHAR(255),
    CONSTRAINT fk_paisMonedas FOREIGN KEY (id_pais)
        REFERENCES paises(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_divisa FOREIGN KEY (id_divisa,id_pais_divisa)
        REFERENCES divisas(id,id_pais)
        ON DELETE CASCADE
);

CREATE TABLE artistas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    nombreArtistico VARCHAR(30)
);

CREATE TABLE M_A (
    id_moneda INT NOT NULL,
    id_artista INT NOT NULL,
    CONSTRAINT pk_m_a  PRIMARY KEY (id_moneda,id_artista),
    CONSTRAINT fk_moneda_M_A FOREIGN KEY (id_moneda)
        REFERENCES monedas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_artista_M_A FOREIGN KEY (id_artista)
        REFERENCES artistas(id)
        ON DELETE CASCADE
);

CREATE TABLE coleccionistas (
    dni INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    segundoNombre VARCHAR(30),
    apellido VARCHAR(30) NOT NULL,
    segundoApellido VARCHAR(30) NOT NULL,
    telefono VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    fechaNacimiento DATE NOT NULL,
    id_pais_nacio INT NOT NULL,
    id_pais_reside INT NOT NULL,
    CONSTRAINT fk_pais_nacio FOREIGN KEY (id_pais_nacio)
        REFERENCES paises(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_pais_reside FOREIGN KEY (id_pais_reside)
        REFERENCES paises(id)
        ON DELETE CASCADE
);

CREATE TABLE organizaciones(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    proposito TEXT NOT NULL,
    fundacion DATE NOT NULL,
    alcance VARCHAR(15) NOT NULL CHECK (alcance in ('nacional','internacional','ambos')),
    tipo VARCHAR(10) NOT NULL CHECK (tipo in ('galeria','tienda','otro')),
    telefonoPrincipal VARCHAR(20) NOT NULL UNIQUE,
    paginaWeb VARCHAR(50) UNIQUE,
    emailCorporativo  VARCHAR(50) UNIQUE,
    id_pais INT NOT NULL,
    CONSTRAINT fk_pais_org FOREIGN KEY (id_pais)
        REFERENCES paises(id)
        ON DELETE CASCADE
);

CREATE TABLE contactos (
    id_organizacion INT NOT NULL,
    dni INT NOT NULL ,
    nombre VARCHAR(30) NOT NULL,
    segundoNombre VARCHAR(30),
    apellido VARCHAR(30) NOT NULL,
    segundoApellido VARCHAR(30) NOT NULL,
    telefono VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    cargo VARCHAR(30) NOT NULL,
    CONSTRAINT pk_contactos PRIMARY KEY (dni,id_organizacion),
    CONSTRAINT fk_organizacion FOREIGN KEY (id_organizacion)
        REFERENCES organizaciones(id)
        ON DELETE CASCADE
);

CREATE TABLE clientes (
    fechaIngreso DATE NOT NULL,
    numeroExpedienteUnico INT NOT NULL UNIQUE,
    id_coleccionista INT NOT NULL,
    id_organizacion INT NOT NULL,
    CONSTRAINT pk_cliente PRIMARY KEY (fechaIngreso,id_coleccionista,id_organizacion),
    CONSTRAINT fk_coleccionista_cliente FOREIGN KEY (id_coleccionista)
        REFERENCES coleccionistas(dni)
        ON DELETE CASCADE,
    CONSTRAINT fk_organizacion_cliente FOREIGN KEY (id_organizacion)
        REFERENCES organizaciones(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_cliente UNIQUE(id_coleccionista,id_organizacion)
);

CREATE TABLE Catalogo_Moneda_Tienda (
    id_moneda INT NOT NULL,
    nur INT NOT NULL AUTO_INCREMENT UNIQUE,
    id_coleccionista INT,
    id_organizacion INT,
    CONSTRAINT pk_catalogo_moneda PRIMARY KEY (id_moneda,nur),
    CONSTRAINT fk_moneda_catalogo FOREIGN KEY (id_moneda)
        REFERENCES monedas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_coleccionista_moneda FOREIGN KEY (id_coleccionista)
        REFERENCES coleccionistas(dni)
        ON DELETE CASCADE,
    CONSTRAINT fk_organizacion_moneda FOREIGN KEY (id_organizacion)
        REFERENCES organizaciones(id)
        ON DELETE CASCADE   
);

CREATE TABLE Catalogo_Pintura_Tienda (
    nur INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    dimensionescm VARCHAR(20) NOT NULL,
    estilo VARCHAR(30) NOT NULL,
    ano YEAR,
    imagen VARCHAR(255),
    id_coleccionista INT,
    id_organizacion INT,
    CONSTRAINT fk_coleccionista_pintura FOREIGN KEY (id_coleccionista)
        REFERENCES coleccionistas(dni)
        ON DELETE CASCADE,
    CONSTRAINT fk_organizacion_pintura FOREIGN KEY (id_organizacion)
        REFERENCES organizaciones(id)
        ON DELETE CASCADE   
);

CREATE TABLE P_A (
    id_pintura INT NOT NULL,
    id_artista INT NOT NULL,
    CONSTRAINT pk_p_a  PRIMARY KEY (id_pintura,id_artista),
    CONSTRAINT fk_pintura_P_A FOREIGN KEY (id_pintura)
        REFERENCES monedas(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_artista_P_A FOREIGN KEY (id_artista)
        REFERENCES artistas(id)
        ON DELETE CASCADE
);


CREATE TABLE eventos (
    id INT NOT NULL PRIMARY KEY,
    inscripcionCliente DECIMAL(13,2) NOT NULL,
    inscripcionClienteNuevo DECIMAL(13,2),
    fecha DATETIME NOT NULL,
    status VARCHAR(12) NOT NULL CHECK (status in ('realizado','pendiente','cancelado')),
    tipo VARCHAR(12) NOT NULL CHECK (tipo in ('virtual','presencial')),
    tipoPuja VARCHAR(20) NOT NULL CHECK (tipoPuja in ('ascendente','sobre cerrado')),
    duracionHoras INT NOT NULL CHECK ((duracionHoras >=4) and (duracionHoras <=6)),
    lugar VARCHAR(100),
    id_pais INT,
    CONSTRAINT fk_pais_evento FOREIGN KEY (id_pais)
        REFERENCES paises(id)
        ON DELETE CASCADE
);

CREATE TABLE planificadores (
    id_evento INT NOT NULL,
    id_organizacion INT NOT NULL,
    CONSTRAINT pk_planificador  PRIMARY KEY (id_evento,id_organizacion),
    CONSTRAINT fk_evento_planificador FOREIGN KEY (id_evento)
        REFERENCES eventos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_organizacion_planificador FOREIGN KEY (id_organizacion)
        REFERENCES organizaciones(id)
        ON DELETE CASCADE
);

CREATE TABLE participantes (
    id_evento INT NOT NULL,
    fechaIngresoCliente DATE NOT NULL,
    id_coleccionista_cliente INT NOT NULL,
    id_organizacion_cliente INT NOT NULL,
    id_pais INT,
    CONSTRAINT pk_participante  PRIMARY KEY (fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento),
    CONSTRAINT fk_evento_participante FOREIGN KEY (id_evento)
        REFERENCES eventos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_pais_envio FOREIGN KEY (id_pais)
        REFERENCES paises(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cliente_participantes FOREIGN KEY (fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente)
        REFERENCES clientes(fechaIngreso,id_coleccionista,id_organizacion)
        ON DELETE CASCADE
);

CREATE TABLE costoEnvios (
    id_evento INT NOT NULL,
    id INT NOT NULL AUTO_INCREMENT,
    costoExtra DECIMAL(13,2),
    id_pais INT NOT NULL,
    CONSTRAINT pk_costoEnvio  PRIMARY KEY (id,id_evento),
    CONSTRAINT fk_evento_costoEnvio FOREIGN KEY (id_evento)
        REFERENCES eventos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_pais_costoEnvio FOREIGN KEY (id_pais)
        REFERENCES paises(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_costo_envio UNIQUE(id_pais,id_evento)
);

CREATE TABLE Lista_Objetos (
    id_evento INT NOT NULL,
    id_eventoParticipante INT,
    id INT NOT NULL AUTO_INCREMENT,
    id_pintura INT,
    id_moneda INT,
    porcentajeGananciaMin DECIMAL(8,2) NOT NULL,
    bid DECIMAL(13,2) NOT NULL,
    ask DECIMAL(13,2) NOT NULL,
    preciAlcanzado DECIMAL(13,2),
    orden INT,
    duracionmin INT,
    razonNoVenta VARCHAR(20) CHECK (razonNoVenta in ('sin ofertas','inferior al ask')),
    fechaIngresoParticipante DATE,
    id_coleccionistaParticipante INT,
    id_organizacionParticipante INT,
    CONSTRAINT pk_lista_objetos PRIMARY KEY (id,id_evento),
    CONSTRAINT fk_evento_objetos FOREIGN KEY (id_evento)
        REFERENCES eventos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cliente_objeto FOREIGN KEY (fechaIngresoParticipante,id_coleccionistaParticipante,id_organizacionParticipante,id_eventoParticipante)
        REFERENCES participantes(fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento)
        ON DELETE CASCADE,
    CONSTRAINT fk_evento_pintura FOREIGN KEY (id_pintura)
        REFERENCES Catalogo_Pintura_Tienda(nur)
        ON DELETE CASCADE,
    CONSTRAINT fk_evento_moneda FOREIGN KEY (id_moneda)
        REFERENCES Catalogo_Moneda_Tienda(nur)
        ON DELETE CASCADE
);


CREATE TABLE facturas (
    id_evento INT NOT NULL,
    numeroFactura INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fechaEmision DATE NOT NULL,
    total DECIMAL(13,2) NOT NULL,
    fechaIngresoParticipante DATE,
    id_coleccionistaParticipante INT,
    id_organizacionParticipante INT,
    CONSTRAINT fk_participante_factura FOREIGN KEY (fechaIngresoParticipante,id_coleccionistaParticipante,id_organizacionParticipante,id_evento)
        REFERENCES participantes(fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento)
        ON DELETE CASCADE
);


CREATE TABLE detFacturas (
    id_evento INT NOT NULL,
    id_objeto INT NOT NULL,
    id INT NOT NULL AUTO_INCREMENT,
    numeroFactura INT NOT NULL,
    precio DECIMAL(13,2) NOT NULL,
    CONSTRAINT pk_  PRIMARY KEY (id,numeroFactura),
    CONSTRAINT fk_detFacturas_objeto FOREIGN KEY (id_objeto,id_evento)
        REFERENCES Lista_Objetos(id,id_evento)
        ON DELETE CASCADE,
    CONSTRAINT fk_factura_Det FOREIGN KEY (numeroFactura)
        REFERENCES facturas(numeroFactura)
        ON DELETE CASCADE
);
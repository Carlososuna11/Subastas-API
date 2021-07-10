# Subastas-API

La rest-api de Subastas, realizado como proyecto para la materia de Base de Datos I en la Universidad Católica Andrés Bello

El planteamiento del problema puede encontrarse en el siguiente [link](https://drive.google.com/file/d/1eIVRWTdv34XnFYZ9WzssBF84NXS1xZPo/view?usp=sharing)


### Pasos a seguir para configurar este proyecto

1) Instalar [mysql](https://dev.mysql.com/downloads/mysql/)
    - Ayuda: [tutorial instalar mysql](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-es)

    - <ins>_Opcional_</ins>: Instalar [mysql Workbench](https://dev.mysql.com/downloads/workbench/)
2) Configurar usuario y contraseña. Un ejemplo de tutorial (Ubuntu) en el siguiente  [configurar usuario](https://www.digitalocean.com/community/tutorials/crear-un-nuevo-usuario-y-otorgarle-permisos-en-mysql-es)

3) Abrir el mysql command line (o usar mysql Workbench) y escribrir lo siguiente

    1) Crear Base de datos
        ```sql
        CREATE DATABASE subastas;
        ```
    2) Usar Base de datos
        ```sql
        USE subastas;
        ```

    3) Crear Tablas
        1) Entidad Pais
            ```sql
            CREATE TABLE paises (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(30) NOT NULL UNIQUE,
                nacionalidad VARCHAR(30) NOT NULL UNIQUE
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE paises;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
               +--------------+-------------+------+-----+---------+----------------+
                | Field        | Type        | Null | Key | Default | Extra          |
                +--------------+-------------+------+-----+---------+----------------+
                | id           | int         | NO   | PRI | NULL    | auto_increment |
                | nombre       | varchar(30) | NO   | UNI | NULL    |                |
                | nacionalidad | varchar(30) | NO   | UNI | NULL    |                |
                +--------------+-------------+------+-----+---------+----------------+
                ```
        2) Entidad Divisa
            ```sql
            CREATE TABLE divisas (
                id_pais INT NOT NULL,
                id INT NOT NULL AUTO_INCREMENT,
                nombre VARCHAR(30) NOT NULL,
                CONSTRAINT pk_divisa PRIMARY KEY (id,id_pais),
                CONSTRAINT fk_pais FOREIGN KEY (id_pais)
                    REFERENCES paises(id)
                    ON DELETE CASCADE
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE divisas;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +---------+-------------+------+-----+---------+----------------+
                | Field   | Type        | Null | Key | Default | Extra          |
                +---------+-------------+------+-----+---------+----------------+
                | id_pais | int         | NO   | PRI | NULL    |                |
                | id      | int         | NO   | PRI | NULL    | auto_increment |
                | nombre  | varchar(30) | NO   |     | NULL    |                |
                +---------+-------------+------+-----+---------+----------------+
                ```
        3) Entidad Moneda
            ```sql
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
                id_pais INT NOT NULL,
                id_divisa INT NOT NULL,
                imagen VARCHAR(255),
                CONSTRAINT fk_paisMonedas FOREIGN KEY (id_pais)
                    REFERENCES paises(id)
                    ON DELETE CASCADE,
                CONSTRAINT fk_divisa FOREIGN KEY (id_divisa,id_pais)
                    REFERENCES divisas(id,id_pais)
                    ON DELETE CASCADE
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE monedas;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +--------------+--------------+------+-----+---------+----------------+
                | Field        | Type         | Null | Key | Default | Extra          |
                +--------------+--------------+------+-----+---------+----------------+
                | id           | int          | NO   | PRI | NULL    | auto_increment |
                | nombre       | varchar(100) | NO   |     | NULL    |                |
                | denominacion | int          | NO   |     | NULL    |                |
                | mintage      | int          | NO   |     | NULL    |                |
                | forma        | varchar(10)  | NO   |     | NULL    |                |
                | metal        | varchar(10)  | NO   |     | NULL    |                |
                | diametromm   | int          | NO   |     | NULL    |                |
                | canto        | varchar(10)  | NO   |     | NULL    |                |
                | pesogr       | int          | NO   |     | NULL    |                |
                | ano          | year         | NO   |     | NULL    |                |
                | motivo       | varchar(100) | NO   |     | NULL    |                |
                | acunacion    | varchar(100) | NO   |     | NULL    |                |
                | anverso      | text         | NO   |     | NULL    |                |
                | reverso      | text         | NO   |     | NULL    |                |
                | id_pais      | int          | NO   | MUL | NULL    |                |
                | id_divisa    | int          | NO   | MUL | NULL    |                |
                +--------------+--------------+------+-----+---------+----------------+

                ```
        4) Entidad Artista
            ```sql
            CREATE TABLE artistas (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(30),
                apellido VARCHAR(30),
                nombreArtistico VARCHAR(30)
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE artistas;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-----------------+-------------+------+-----+---------+----------------+
                | Field           | Type        | Null | Key | Default | Extra          |
                +-----------------+-------------+------+-----+---------+----------------+
                | id              | int         | NO   | PRI | NULL    | auto_increment |
                | nombre          | varchar(30) | YES  |     | NULL    |                |
                | apellido        | varchar(30) | YES  |     | NULL    |                |
                | nombreArtistico | varchar(30) | YES  |     | NULL    |                |
                +-----------------+-------------+------+-----+---------+----------------+
                ```
        4) Entidad M_A
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE M_A;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------+------+------+-----+---------+-------+
                | Field      | Type | Null | Key | Default | Extra |
                +------------+------+------+-----+---------+-------+
                | id_moneda  | int  | NO   | PRI | NULL    |       |
                | id_artista | int  | NO   | PRI | NULL    |       |
                +------------+------+------+-----+---------+-------+
                ```
        5) Entidad Coleccionista
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE coleccionistas;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-----------------+-------------+------+-----+---------+-------+
                | Field           | Type        | Null | Key | Default | Extra |
                +-----------------+-------------+------+-----+---------+-------+
                | dni             | int         | NO   | PRI | NULL    |       |
                | nombre          | varchar(30) | NO   |     | NULL    |       |
                | segundoNombre   | varchar(30) | YES  |     | NULL    |       |
                | apellido        | varchar(30) | NO   |     | NULL    |       |
                | segundoApellido | varchar(30) | NO   |     | NULL    |       |
                | telefono        | varchar(20) | NO   | UNI | NULL    |       |
                | email           | varchar(50) | NO   | UNI | NULL    |       |
                | fechaNacimiento | date        | NO   |     | NULL    |       |
                | id_pais_nacio   | int         | NO   | MUL | NULL    |       |
                | id_pais_reside  | int         | NO   | MUL | NULL    |       |
                +-----------------+-------------+------+-----+---------+-------+
                ```
        6) Entidad Organizacion
            ```sql
            CREATE TABLE organizaciones(
                id INT NOT NULL PRIMARY KEY,
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE organizaciones;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-------------------+-------------+------+-----+---------+-------+
                | Field             | Type        | Null | Key | Default | Extra |
                +-------------------+-------------+------+-----+---------+-------+
                | id                | int         | NO   | PRI | NULL    |       |
                | nombre            | varchar(50) | NO   |     | NULL    |       |
                | proposito         | text        | NO   |     | NULL    |       |
                | fundacion         | date        | NO   |     | NULL    |       |
                | alcance           | varchar(15) | NO   |     | NULL    |       |
                | tipo              | varchar(10) | NO   |     | NULL    |       |
                | telefonoPrincipal | varchar(20) | NO   | UNI | NULL    |       |
                | paginaWeb         | varchar(50) | YES  | UNI | NULL    |       |
                | emailCorporativo  | varchar(50) | YES  | UNI | NULL    |       |
                | id_pais           | int         | NO   | MUL | NULL    |       |
                +-------------------+-------------+------+-----+---------+-------+
                ```
        7) Entidad Contacto
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE contactos;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-----------------+-------------+------+-----+---------+-------+
                | Field           | Type        | Null | Key | Default | Extra |
                +-----------------+-------------+------+-----+---------+-------+
                | id_organizacion | int         | NO   | PRI | NULL    |       |
                | dni             | int         | NO   | PRI | NULL    |       |
                | nombre          | varchar(30) | NO   |     | NULL    |       |
                | segundoNombre   | varchar(30) | YES  |     | NULL    |       |
                | apellido        | varchar(30) | NO   |     | NULL    |       |
                | segundoApellido | varchar(30) | NO   |     | NULL    |       |
                | telefono        | varchar(20) | NO   | UNI | NULL    |       |
                | email           | varchar(50) | NO   | UNI | NULL    |       |
                | cargo           | varchar(30) | NO   |     | NULL    |       |
                +-----------------+-------------+------+-----+---------+-------+
                ```
        8) Entidad Cliente
            ```sql
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
                    ON DELETE CASCADE
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE clientes;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-----------------------+------+------+-----+---------+-------+
                | Field                 | Type | Null | Key | Default | Extra |
                +-----------------------+------+------+-----+---------+-------+
                | fechaIngreso          | date | NO   | PRI | NULL    |       |
                | numeroExpedienteUnico | int  | NO   | UNI | NULL    |       |
                | id_coleccionista      | int  | NO   | PRI | NULL    |       |
                | id_organizacion       | int  | NO   | PRI | NULL    |       |
                +-----------------------+------+------+-----+---------+-------+

                ```
        9) Entidad Catalogo_Moneda_Tienda
            ```sql
            CREATE TABLE Catalogo_Moneda_Tienda (
                id_moneda INT NOT NULL,
                nur INT NOT NULL UNIQUE,
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE Catalogo_Moneda_Tienda;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------------+------+------+-----+---------+-------+
                | Field            | Type | Null | Key | Default | Extra |
                +------------------+------+------+-----+---------+-------+
                | id_moneda        | int  | NO   | PRI | NULL    |       |
                | nur              | int  | NO   | PRI | NULL    |       |
                | id_coleccionista | int  | YES  | MUL | NULL    |       |
                | id_organizacion  | int  | YES  | MUL | NULL    |       |
                +------------------+------+------+-----+---------+-------+
                ```
        10) Entidad Catalogo_Pintura_Tienda
            ```sql
            CREATE TABLE Catalogo_Pintura_Tienda (
                nur INT NOT NULL PRIMARY KEY,
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE Catalogo_Moneda_Tienda;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------------+--------------+------+-----+---------+-------+
                | Field            | Type         | Null | Key | Default | Extra |
                +------------------+--------------+------+-----+---------+-------+
                | nur              | int          | NO   | PRI | NULL    |       |
                | titulo           | varchar(100) | NO   |     | NULL    |       |
                | dimensionescm    | varchar(20)  | NO   |     | NULL    |       |
                | estilo           | varchar(30)  | NO   |     | NULL    |       |
                | ano              | year         | YES  |     | NULL    |       |
                | imagen           | varchar(255) | YES  |     | NULL    |       |
                | id_coleccionista | int          | YES  | MUL | NULL    |       |
                | id_organizacion  | int          | YES  | MUL | NULL    |       |
                +------------------+--------------+------+-----+---------+-------+
                ```
        11) Entidad P_A
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE P_A;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------+------+------+-----+---------+-------+
                | Field      | Type | Null | Key | Default | Extra |
                +------------+------+------+-----+---------+-------+
                | id_pintura | int  | NO   | PRI | NULL    |       |
                | id_artista | int  | NO   | PRI | NULL    |       |
                +------------+------+------+-----+---------+-------+
                ```
        12) Entidad Evento
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE eventos;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-------------------------+---------------+------+-----+---------+-------+
                | Field                   | Type          | Null | Key | Default | Extra |
                +-------------------------+---------------+------+-----+---------+-------+
                | id                      | int           | NO   | PRI | NULL    |       |
                | inscripcionCliente      | decimal(13,2) | NO   |     | NULL    |       |
                | inscripcionClienteNuevo | decimal(13,2) | YES  |     | NULL    |       |
                | fecha                   | datetime      | NO   |     | NULL    |       |
                | status                  | varchar(12)   | NO   |     | NULL    |       |
                | tipo                    | varchar(12)   | NO   |     | NULL    |       |
                | tipoPuja                | varchar(20)   | NO   |     | NULL    |       |
                | duracionHoras           | int           | NO   |     | NULL    |       |
                | lugar                   | varchar(100)  | YES  |     | NULL    |       |
                | id_pais                 | int           | YES  | MUL | NULL    |       |
                +-------------------------+---------------+------+-----+---------+-------+
                ```
        13) Entidad Planificador
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE P_A;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +-----------------+------+------+-----+---------+-------+
                | Field           | Type | Null | Key | Default | Extra |
                +-----------------+------+------+-----+---------+-------+
                | id_evento       | int  | NO   | PRI | NULL    |       |
                | id_organizacion | int  | NO   | PRI | NULL    |       |
                +-----------------+------+------+-----+---------+-------+
                ```
        14) Entidad Participante
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE participantes;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +--------------------------+------+------+-----+---------+-------+
                | Field                    | Type | Null | Key | Default | Extra |
                +--------------------------+------+------+-----+---------+-------+
                | id_evento                | int  | NO   | PRI | NULL    |       |
                | fechaIngresoCliente      | date | NO   | PRI | NULL    |       |
                | id_coleccionista_cliente | int  | NO   | PRI | NULL    |       |
                | id_organizacion_cliente  | int  | NO   | PRI | NULL    |       |
                | id_pais                  | int  | YES  | MUL | NULL    |       |
                +--------------------------+------+------+-----+---------+-------+
                ```
        15) Entidad costoEnvio
            ```sql
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
                    ON DELETE CASCADE
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE costoEnvios;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------+---------------+------+-----+---------+----------------+
                | Field      | Type          | Null | Key | Default | Extra          |
                +------------+---------------+------+-----+---------+----------------+
                | id_evento  | int           | NO   | PRI | NULL    |                |
                | id         | int           | NO   | PRI | NULL    | auto_increment |
                | costoExtra | decimal(13,2) | YES  |     | NULL    |                |
                | id_pais    | int           | NO   | MUL | NULL    |                |
                +------------+---------------+------+-----+---------+----------------+
                ```
        16) Entidad Lista_Objeto
            ```sql
            CREATE TABLE Lista_Objetos (
                id_evento INT NOT NULL,
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
                CONSTRAINT fk_cliente_objeto FOREIGN KEY (fechaIngresoParticipante,id_coleccionistaParticipante,id_organizacionParticipante,id_evento)
                    REFERENCES participantes(fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_evento)
                    ON DELETE CASCADE,
                CONSTRAINT fk_evento_pintura FOREIGN KEY (id_pintura)
                    REFERENCES Catalogo_Pintura_Tienda(nur)
                    ON DELETE CASCADE,
                CONSTRAINT fk_evento_moneda FOREIGN KEY (id_moneda)
                    REFERENCES Catalogo_Moneda_Tienda(nur)
                    ON DELETE CASCADE
            );
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE Lista_Objetos;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------------------------+---------------+------+-----+---------+----------------+
                | Field                        | Type          | Null | Key | Default | Extra          |
                +------------------------------+---------------+------+-----+---------+----------------+
                | id_evento                    | int           | NO   | PRI | NULL    |                |
                | id                           | int           | NO   | PRI | NULL    | auto_increment |
                | id_pintura                   | int           | YES  | MUL | NULL    |                |
                | id_moneda                    | int           | YES  | MUL | NULL    |                |
                | porcentajeGananciaMin        | decimal(8,2)  | NO   |     | NULL    |                |
                | bid                          | decimal(13,2) | NO   |     | NULL    |                |
                | ask                          | decimal(13,2) | NO   |     | NULL    |                |
                | preciAlcanzado               | decimal(13,2) | YES  |     | NULL    |                |
                | orden                        | int           | YES  |     | NULL    |                |
                | duracionmin                  | int           | YES  |     | NULL    |                |
                | razonNoVenta                 | varchar(20)   | YES  |     | NULL    |                |
                | fechaIngresoParticipante     | date          | YES  | MUL | NULL    |                |
                | id_coleccionistaParticipante | int           | YES  |     | NULL    |                |
                | id_organizacionParticipante  | int           | YES  |     | NULL    |                |
                +------------------------------+---------------+------+-----+---------+----------------+
                ```
        17) Entidad Factura
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE facturas;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +------------------------------+---------------+------+-----+---------+----------------+
                | Field                        | Type          | Null | Key | Default | Extra          |
                +------------------------------+---------------+------+-----+---------+----------------+
                | id_evento                    | int           | NO   |     | NULL    |                |
                | numeroFactura                | int           | NO   | PRI | NULL    | auto_increment |
                | fechaEmision                 | date          | NO   |     | NULL    |                |
                | total                        | decimal(13,2) | NO   |     | NULL    |                |
                | fechaIngresoParticipante     | date          | YES  | MUL | NULL    |                |
                | id_coleccionistaParticipante | int           | YES  |     | NULL    |                |
                | id_organizacionParticipante  | int           | YES  |     | NULL    |                |
                +------------------------------+---------------+------+-----+---------+----------------+
                ```
        18) Entidad DetFactura
            ```sql
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
            ```
            - ver estructura de la tabla
                ```sql
                DESCRIBE detFacturas;
                ```
                Si todo funciona, deberia mostrar lo siguiente
                ```
                +---------------+---------------+------+-----+---------+----------------+
                | Field         | Type          | Null | Key | Default | Extra          |
                +---------------+---------------+------+-----+---------+----------------+
                | id_evento     | int           | NO   |     | NULL    |                |
                | id_objeto     | int           | NO   | MUL | NULL    |                |
                | id            | int           | NO   | PRI | NULL    | auto_increment |
                | numeroFactura | int           | NO   | PRI | NULL    |                |
                | precio        | decimal(13,2) | NO   |     | NULL    |                |
                +---------------+---------------+------+-----+---------+----------------+
                ```
4) configurar archivo .env (Localizado en el zip )
```
HOST=<yourhost>
USER=<youruser>
PASSWORD=<youruserpassword>
DATABASE=subastas
PORT=<port>
```
por default el `port` es `3306` y el `host` es `localhost`

5) Instalar librerias necesarias
```
pip install -r requirements.txt
```
6) correr Proyecto
```
python manage.py runserver
```

#### Link de la documentacion
```
<urlbase>/swagger/
<urlbase>/redoc/
```
Ejemplo
```
http://localhost:8000/swagger/
http://127.0.0.1:8000/redoc/
```

**Nota**: Aunque no aparezca el campo de imagen en el post y put, este es necesario enviar, de no requerir enviar imagen simplemente establezca `"imagen":null`


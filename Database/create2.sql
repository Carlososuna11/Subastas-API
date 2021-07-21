USE subastas;

CREATE TABLE caj_Subastas_Activas (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_evento MEDIUMINT UNSIGNED NOT NULL,
    id_objeto MEDIUMINT UNSIGNED  NOT NULL,
    hora_inicio DATETIME NOT NULL,
    hora_fin DATETIME NOT NULL,
    cierre BOOLEAN NOT NULL,
        CONSTRAINT fk_detFacturass_objeto FOREIGN KEY (id_objeto,id_evento)
        REFERENCES caj_Lista_Objetos(id,id_evento),
    INDEX IDX_Subastas_Activas_Lista_Objetos (id_objeto,id_evento)
);

CREATE TABLE caj_Logs_Subastas_Activas (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_subasta_activa MEDIUMINT UNSIGNED NOT NULL,
    id_coleccionista MEDIUMINT UNSIGNED NOT NULL,
    precio DECIMAL(13,2) NOT NULL,
    hora DATETIME NOT NULL,
    CONSTRAINT fk_Logs_Subastas_Activas FOREIGN KEY (id_subasta_activa)
        REFERENCES caj_Subastas_Activas(id)
);

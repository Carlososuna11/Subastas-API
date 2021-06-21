# Test API
Api de prueba creada para demostrar que el sistema esta instalado en el computador

### Diagrama ER

<p align="center"> 
<img src="https://i.ibb.co/0X5RJ6r/entidad-entrega-25.png">
</p>


### Pasos a seguir para configurar este proyecto

1) Instalar [mysql](https://dev.mysql.com/downloads/mysql/)
    - Ayuda: [tutorial instalar mysql](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-es)

    - <ins>_Opcional_</ins>: Instalar [mysql Workbench](https://dev.mysql.com/downloads/workbench/)
2) Configurar usuario y contraseña. Un ejemplo de tutorial (Ubuntu) en el siguiente  [configurar usuario](https://www.digitalocean.com/community/tutorials/crear-un-nuevo-usuario-y-otorgarle-permisos-en-mysql-es)

3) Abrir el mysql command line (o usar mysql Workbench) y escribrir lo siguiente

    1) Crear Base de datos
        ```sql
        CREATE DATABASE testapi;
        ```
    2) Usar Base de datos
        ```sql
        USE testapi;
        ```

    3) Crear Tabla productos
        ```sql
        CREATE TABLE productos (
            id INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(500) NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            imagen VARCHAR(255),
            PRIMARY KEY (id)
        );
        ```
    4) ver estructura de la tabla
        ```sql
        DESCRIBE productos;
        ```
        Si todo funciona, deberia mostrar lo siguiente
        ```
        +-------------+---------------+------+-----+---------+----------------+
        | Field       | Type          | Null | Key | Default | Extra          |
        +-------------+---------------+------+-----+---------+----------------+
        | id          | int           | NO   | PRI | NULL    | auto_increment |
        | nombre      | varchar(50)   | NO   |     | NULL    |                |
        | descripcion | varchar(500)  | NO   |     | NULL    |                |
        | precio      | decimal(10,2) | NO   |     | NULL    |                |
        | imagen      | varchar(255)  | YES  |     | NULL    |                |
        +-------------+---------------+------+-----+---------+----------------+

        ```
    

4) configurar archivo .env (Localizado en el zip )
```
HOST=<yourhost>
USER=<youruser>
PASSWORD=<youruserpassword>
DATABASE=testapi
PORT=<port>
```
por default el `port` es `3306` y el `host` es `localhost`


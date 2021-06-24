# Test API
Api de prueba creada para demostrar que el sistema esta instalado en el computador

### Diagrama ER 1

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
    
    - **Adicional**: Ver los valores que tiene la tabla:
        ```sql
        SELECT * from productos;
        ```
        Un ejemplo de lo que podria retornar:
        ```
        +----+--------+-------------+--------+---------------+
        | id | nombre | descripcion | precio | imagen        |
        +----+--------+-------------+--------+---------------+
        |  3 | string | string      |  15.80 | NULL          |
        |  4 | string | string      |  23.00 | NULL          |
        |  5 | carlos | string      |  10.00 | NULL          |
        |  6 | string | string      | 150.25 | NULL          |
        |  7 | carlos | Crear       |  15.25 | NULL          |
        |  8 | carlos | Crear       |  15.25 | NULL          |
        |  9 | carlos | Crear       |  15.25 | product9.png  |
        | 10 | carlos | Crear       |  15.25 | product10.png |
        | 11 | carlos | Crear       |  15.25 | product11.jpg |
        | 12 | carlos | Crear       |  15.25 | product12.jpg |
        | 13 | carlos | osuna       |  12.00 | NULL          |
        | 14 | carlos | as          |  12.50 | NULL          |
        +----+--------+-------------+--------+---------------+

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

### Diagrama ER 2

<p align="center"> 
<img src="https://i.ibb.co/MRd7zG5/casa.png">
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
        CREATE TABLE casas (
            id INT NOT NULL AUTO_INCREMENT,
            habitaciones INT NOT NULL,
            banos INT NOT NULL,
            gas BOOLEAN NOT NULL,
            balcon BOOLEAN NOT NULL,
            imagen VARCHAR(255),
            PRIMARY KEY (id)
        );
        ```
    4) ver estructura de la tabla
        ```sql
        DESCRIBE casas;
        ```
        Si todo funciona, deberia mostrar lo siguiente
        ```
        +--------------+--------------+------+-----+---------+----------------+
        | Field        | Type         | Null | Key | Default | Extra          |
        +--------------+--------------+------+-----+---------+----------------+
        | id           | int          | NO   | PRI | NULL    | auto_increment |
        | habitaciones | int          | NO   |     | NULL    |                |
        | banos        | int          | NO   |     | NULL    |                |
        | gas          | tinyint(1)   | NO   |     | NULL    |                |
        | balcon       | tinyint(1)   | NO   |     | NULL    |                |
        | imagen       | varchar(255) | YES  |     | NULL    |                |
        +--------------+--------------+------+-----+---------+----------------+

        ```
    
    - **Adicional**: Ver los valores que tiene la tabla:
        ```sql
        SELECT * from productos;
        ```
        Un ejemplo de lo que podria retornar:
        ```
        +----+--------------+-------+-----+--------+------------+
        | id | habitaciones | banos | gas | balcon | imagen     |
        +----+--------------+-------+-----+--------+------------+
        |  3 |            2 |     1 |   1 |      1 | house3.jpg |
        |  7 |           10 |     7 |   0 |      0 | house7.jpg |
        |  8 |            3 |     3 |   1 |      0 | NULL       |
        +----+--------------+-------+-----+--------+------------+
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

### Diagrama ER 3

<p align="center"> 
<img src="https://i.ibb.co/SPDs4fc/estudiante.png">
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
        CREATE TABLE estudiantes (
            dni INT NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            segundoApellido VARCHAR(50) NOT NULL,
            segundoNombre VARCHAR(50) ,
            imagen VARCHAR(255),
            PRIMARY KEY (dni)
        );
        ```
    4) ver estructura de la tabla
        ```sql
        DESCRIBE estudiantes;
        ```
        Si todo funciona, deberia mostrar lo siguiente
        ```
        +-----------------+--------------+------+-----+---------+-------+
        | Field           | Type         | Null | Key | Default | Extra |
        +-----------------+--------------+------+-----+---------+-------+
        | dni             | int          | NO   | PRI | NULL    |       |
        | nombre          | varchar(50)  | NO   |     | NULL    |       |
        | apellido        | varchar(50)  | NO   |     | NULL    |       |
        | segundoApellido | varchar(50)  | NO   |     | NULL    |       |
        | segundoNombre   | varchar(50)  | YES  |     | NULL    |       |
        | imagen          | varchar(255) | YES  |     | NULL    |       |
        +-----------------+--------------+------+-----+---------+-------+

        ```
    
    - **Adicional**: Ver los valores que tiene la tabla:
        ```sql
        SELECT * from productos;
        ```
        Un ejemplo de lo que podria retornar:
        ```
        +----------+-------------------+----------+-----------------+---------------+--------------+
        | dni      | nombre            | apellido | segundoApellido | segundoNombre | imagen       |
        +----------+-------------------+----------+-----------------+---------------+--------------+
        |        4 | Cristiano Ronaldo | Osuna    | Piñero          | Ronaldo       | student4.gif |
        | 29772315 | carlos            | Osuna    | Piñero          | NULL          | NULL         |
        +----------+-------------------+----------+-----------------+---------------+--------------+
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

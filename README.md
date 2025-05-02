#Sistema de administracion de Estudiantes y Evaluaciones

Desarrollado por : Samuel Perez 

Este pequeño proyecto implementa microservicios usando las siguientes tecnologias:
 - Docker, Docker Desktop, Docker compose
 - Python (3.11) 
    Librerias:
    -flask
        -Flask, request, jsonify
    -time
    -psycopg2
    -os
 - PostgreSQL 13
 - Postman (Pruebas)  

Para hacer pruebas en este sistema de micro-servicios sigue los siguientes pasos:

Paso 1 : Clona el repositoro desde este link
    - https://github.com/SamuelPerez21/Desafio_GPS_Samuel_Perez.git

Paso 2 : Desde la consola o desde la terminal de el editor de codigo, ejecutar desde la carpeta raiz:
    - docker-compose -d --build 

Paso 3 : Una vez ejecutado puedes verificar que se hayan creado tanto las imagenes como los contenedores, ademas , de no tenerla,
         revisar si la imagen de postgre 13 se encuentra corriendo todo esto se puede revisar en docker-desktopgm.


PRUEBAS:

Para realizar las pruebas se recomienda usar el software POSTMAN el cual ayuda a probar el envio y recepcion de la info por JSON desde las rutas web.

Rutas de prueba Estudiantes:

- Tipo GET, Ruta: localhost:5000/estudiantes
    - Esta ruta debe obtener todos los estudiantes creados, pero si aunn no crear ninguno solo te devolvera un "[]"

- Tipo GET, Ruta: localhost:5000/estudiantes/<rut> (Debes reemplazar la etiqueta <rut> por el rut del estudiante solicitado,    Formato  del rut: XXXXXXXX-X):
    - Esta ruta a diferencia de la ruta anterior, devuelve la información de un estudiante en especifico buscandolo por su rut.

- Tipo POST, Ruta: localhost:5000/estudiantes/
    - Ahora si bien esta ruta es similar a la anterior,  es de tipo POST y para hacerla funcionar se deben de ingresar en un JSON en este formato : 

            {
            "rut_estudiante":"XXXXXXXX-X",
            "semestre": "X",
            "asignatura":"X",
            "nota": 1.0  
            }
    
Rutas de prueba Evaluaciones:

- Tipo GET, Ruta: localhost:5001/evaluaciones
    - Esta ruta debe obtener todas las evaluaciones creadas, pero si aun no se crea ninguna solo te devolvera un "[]"

- Tipo GET, Ruta: localhost:5001/evaluaciones/<rut> (Formato del rut: XXXXXXXX-X)
    - Esta ruta a diferencia de la ruta anterior, devuelve la información la evaluacion en especifico buscandolo por el rut del estudiante.

- Tipo POST, Ruta: localhost:5001/evaluaciones/
    - Ahora si bien esta ruta es similar a la anterior,  es de tipo POST y para hacerla funcionar se deben de ingresar en un JSON en este formato : 
            {
            "asignatura": "X",
            "nota": 1.0,
            "rut_estudiante": "XXXXXXXX-X",
            "semestre": "X"
            }
    Ahora es importante mencionar que este metodo solo funciona si ya hay un estudiante previamente creado, por lo cual para que funcione se debe crear primero un estudiante con exito y despues crear dicha evaluacion con el rut.

    Finalmente si se desea terminar con la instacia y eliminar todo rastro de lo creado, se debe ejecutar dicho codigo en el CMD o en la terminal del editor de codigo el siguiente comando:

    docker-compose down -v --rmi all --remove-orphans


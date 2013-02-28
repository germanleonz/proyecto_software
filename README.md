Proyecto de gestion de pizarras y actividades (proyecto_pizarra)

Requisitos para la instalacion del sistema 
(Probado en Debian, Ubuntu y Linux Mint)

1.- Python >= 2.6

    sudo apt-get install python

2.- Django

    wget http://www.djangoproject.com/m/releases/1.4/Django-1.4.3.tar.gz
    tar xvfz Django-1.4.3.tar.gz
    cd Django-1.4.3
    sudo python setup.py install

3.- PostgreSQL

    sudo apt-get install postgresql

4.- Psycopg2

    sudo apt-get install python-psycopg2

Puede que esto les de problemas, en ese caso revisen que tengan instaladas las siguientes librerias: libpq-dev, python-dev.
Si no las tienen hagan:
    
    sudo apt-get install libpq-dev python-dev

5.- Dajax

    git clone https://github.com/jorgebastida/django-dajax.git
    cd ./django-dajax
    sudo python setup.py install

6.- Dajax-ice

    git clone https://github.com/jorgebastida/django-dajaxice.git
    cd ./django-dajaxice
    sudo python setup.py install

Una vez que tengan instalado todo lo anterior hagan lo siguiente.

1.- Clonar el repositorio  

    git clone https://github.com/germanleonz/proyecto_software.git  

2.- Para el usuario postgres creen una base de datos que se llame proyecto_pizarra
    desde psql pueden hacerlo con el comando: CREATE DATABASE proyecto_pizarra OWNER postgres;

3.- Desde el directorio raiz del proyecto hacer:
    python manage.py syncdb && python manage.py crear_grupos  
    Django va a darles un mensaje diciendo que no tienen un superusuario definido, sigan las instrucciones y definanlo
    Si todo va bien deberia darle los mensajes: Agregando permisos... Listo

4.- Finalmente arrancar el servidor:  
    python manage.py runserver  
    Esto va a arrancar el servidor http del sistema en el puerto 8000 por defecto

5.- Creen un userprofile para el usuario
    Entren en: localhost:8000/admin
    Para acceder usen el nombre de usuario y clave que definieron en el paso 3
    Luego busquen donde dice User Profiles, hacia la derecha dice add hagan click y agreguenle un numero de telefono a su usuario

6.- Para entrar al sistema entren a localhost:8000
    Usen el nombre de usuario y la contrasena que definieron en el paso tres

Instrucciones para la creacion de respaldos:

    Guardar un archivo llamado .pgpass en el directorio raiz del usuario 
    que vaya a ejecutar el comando que respalda el sistema. Ej: /home/usuario
    Dicho archivo debe tener una unica linea con el siguiente formato:

    hostname:puerto:nombre_bd:nombre_usuario:contrasena

    Hostname: nombre o direccion IP de la maquina donde esta el servidor Postgresql
    Puerto: puerto del servidor postgresql   
    nombre_bd: Nombre de la base de datos del sistema
    nombre_usuario: usuario dueno de la base de datos que se va a respaldar
    contrasena: contrasena del usuario dueno de la base de datos

    Ejecutar el siguiente comando desde el directorio raiz del proyecto_pizarra

    python manage.py crear_respaldo

    Esto guardara un archivo llamado respaldo_bd.txt con los datos del sistema
    Y ademas un archivo respaldo_codigo.tar.gz con el codigo fuente del sistema

Configuracion de respaldos automaticos

    Requisitos: Descargar el modulo python-crontab e instalarlo

    wget http://pypi.python.org/packages/source/p/python-crontab/python-crontab-1.2.tar.gz;
    tar xvfz python-crontab-1.2;
    cd python-crontab-1.2; python setup.py install;

    Para que el sistema genere respaldos automaticos se debe ejecutar el siguiente comando

    python manage.py configurar_respaldos

    Este comando mostrara por el terminal el estado de los respaldos automaticos
    ya configurados, en caso de que lo esten. En caso contrario, hara los pasos
    necesarios para automatizar la generacion de respaldos. Las variables que definen la frecuencia 
    con la que se generaran los respaldos estan definidas en el mismo script

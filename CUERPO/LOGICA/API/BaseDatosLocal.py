'''
BaseDatosLocal.py :
        Contiene las siguientes clases:
            * Conexion
            * Cursor
            * BaseDatos_ClassRoomProgramas

        El objetivo de la existencia de la clase 'Conexion' y 'Cursor' es hacer la programación de la
        clase 'BaseDatos_ClassRoomProgramas' mas practica a la hora de efectuar las sentencias Query.

        El objetivo de la clase 'BaseDatos_ClassRoom' es poder respaldar y retornar la información de:
        las clases de classroom, los topics de classroom y los courseworks de classroom del usuario,
        todo esto con la finalidad de reducir el numero de consultas que se le hacen a la API de google
        classroom y asi no ser tan dependiente del internet para poder funcionar.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"

# librerias estandar
import os
import sys
import sqlite3



#############################################################################################################################
# ACCIONES COMUNES
############################################################################################################################


class Conexion:
    '''
    Permite crear objetos que sean utiles para relizar conexiones sqlite3 a una base de datos
    especifica, dichas conexiones tienen como proposito ser sencillas y seguras.
    '''

    def __init__(self, baseDatos):
        '''
        Parámetros:
            - baseDatos (str): Nombre de la base de datos de la cual se desea hacer
            conexion
        '''

        self.__BASE_DATOS = baseDatos
        self.__conexion = None
        self.__cursor = None

    def obtenerConexion(self):
        """
        Creara un objeto  de tipo 'conexion' el cual sirve para conectarse
        con la base de datos cuyo nombre  es igual a: 'self.__BASE_DATOS'

        Si no hubo exito en la operación se ocasionara el cierre inmediato del programa

        Returns:
            - Objeto de tipo 'conexion' si hubo exito.
        """

        if self.__cursor is None:
            try:
                self.__conexion = sqlite3.connect(self.__BASE_DATOS)
                return self.__conexion

            except Exception as e:
                print(e)
                sys.exit()
        else:
            return self.__conexion


    def obtenerCursor(self):
        """
        Apartir del atributo de instancia: 'self.__cursor' creara un objeto  de tipo 'cursor'
        el cual sirve para ejecutar sentencias de tipo Query a la base de datos cuyo nombre
        es igual a: 'self.__BASE_DATOS'

        Si no hubo exito en la operación se ocasionara el cierre inmediato del programa

        Returns(devoluciones):
            - Objeto de tipo 'conexion' si hubo exito.
        """

        if self.__cursor is None:
            try:
                self.__cursor = self.obtenerConexion().cursor()
                return self.__cursor
            except Exception as e:
                print(e)
                sys.exit()
        else:
            return self.__cursor

    def cerrar(self):
        '''
        Cerrara a los objetos almacenados por los atributos de instancia: 'self.__cursor'
        y 'self.__conexion' y despues los igualara a valores None

        Si no hubo exito en la operación se ocasionara el cierre inmediato del programa
        '''

        if self.__cursor is not None:
            try:
                self.__cursor.close()
            except Exception as e:
                print(e)

        if self.__conexion is not None:
            try:
                self.__conexion.close()
            except Exception as e:
                print(e)

        self.__conexion = None
        self.__cursor = None


class Cursor:
    '''
    Clase cuyo objetivo es que sus instancias permitan omitir las lineas de codigo:
        a) 'conexion=sqlite3.connect()'
        b) 'cursor=conexion.cursor()'
        c) 'conexion.commit() '
        b) 'cursor.close()'
        c) 'conexion.close()'
    Para cada setencia Query que se desea ejecutar en un base de datos local

    Esta clase se define el comportamiento de los metodos especiales '__enter__' y '__exit__'
    los cuales permiten utilizar el 'with as' y con ello encapsular las lineas de
    codigo que se desean dejar de repetir cada vez que se desea ejecutar sentencias de tipo Query.

    Es decir gracias a esta clase bastara con hacer lo siguiente para ejecutar sentencias
    Query en un base de datos:

    with Cursor(nombreBaseDatos) as objetoCursor:
        objetorCursor.execute(sqlOrden)

    Lo cual si no se hiciera uso de esta clase entonces para hacer lo anterior se deberia hacer
    lo siguiente(y eso que no se incluyen las excepcciones respectivas en caso de fallar al ejecutar
    la sentencia Query la base de datos)

    conexion=sqlite3.connect(nombreBaseDatos)
    cursor=conexion.cursor()
    cursor.execute(sqlOrden)
    conexion.commit()
    cursor.close()
    conexion.close()
    '''

    def __init__(self, nombreBase):
        '''
        Parámetros:
            nombreBase (str): Representa el nombre de la base de datos que se desea abrir,
            obtener una conexion, despues un cursor para posteriormente ejecutar una sentencia
            query, y finalmente guardar los cambios realizador y cerrar la conexion y el cursor.
        '''

        self.nombreBase = nombreBase
        self.__objetoConector = Conexion(nombreBase)

    # inicio de with
    def __enter__(self):
        '''
        Lo que returne este metodo es lo que almacenara la variable que le procede a:
        'as' del 'with Cursor() as', es decir si se hiciera lo siguiente:

            'with Cursor(nombreBase) as variableX'

            La variable cuyo nombre es 'variableX' almacenara lo que retorne este metodo

        Returns:
            Objeto de tipo 'cursor' que permitira ejecutar sentencias Query a la base de datos
            cuyo nombre es igual a: 'self.nombreBase'
        '''

        return self.__objetoConector.obtenerCursor()

    # fin del bloque with
    def __exit__(self, exception_type, exception_value, exception_traceback):
        '''
        Este metodo definira lo que se haga una vez que se termine de ejecutar
        la ultima linea de codigo que este definida dentro del 'with() as'
        ejemplo:
            with Cursor(nombreArchivo) as variableX:
                linea de codigo 1 que definide el usuario dentro del 'with as'
                linea de codigo 2 que definide el usuario dentro del 'with as'
                linea de codigo 3 que definide el usuario dentro del 'with as'
                linea de codigo 4 que definide el usuario dentro del 'with as'
                .
                .
                ultima linea de codigo  que se define el usuario dentro del 'with as'
                ACCION DEFINIDA EN ESTE METODO SE EJECUTARA AQUI
        '''


        # if exception_value != None:
        if exception_value:
            print(exception_value)
            sys.exit()

        else:
            # se ejecuta la sentencia Query cargarda
            self.__objetoConector.obtenerConexion().commit()

        # Cerrando conexiones a la base de datos local
        self.__objetoConector.cerrar()

#############################################################################################################################
# A L A R M A
############################################################################################################################

class BaseDatos_ClassRoomProgramas():
    '''
    Clase que servira para crear bases de datos locales que permitan registrar los datos
    de: las 'tareas'(courseWorks) asi como los 'Topics' y 'Clases' del ClassRoom del usuario
    que ha iniciado sesión con su cuenta de google en el programa CACPY.
    '''


    def __init__(self, NOMBRE_BASE_DATOS):
        """
        Parámetros:
            NOMBRE_BASE_DATOS (str)-- Representa el nombre completo de la base de datos que
            almacenara los datos de las  'tareas(courseWorks)' asi como los 'Topics'
            y 'Clases' del ClassRoom del usuario  que ha iniciado sesión con su cuenta de
            e google en el programa CACPY.El nombre completo es aquel que contiene la ruta
            completa de donde se ubica la base de datos.Es importante que el nombre incluya la
            extension del archivo es decir una extension '.sqlite3' o '.db'
        """

        self.NOMBRE_BASE_DATOS = NOMBRE_BASE_DATOS

    def crearBaseDatos(self):
        '''
        Creara la base de datos con el nombre y las secciones requeridas

        Si no hubo exito en la operación se ocasionara el cierra inmediato del programa

        Returns (Devoluciones):
            dato de tipo 'bool' igual a 'True' si hubo exito.
        '''

        # Aspectos tecnicos que recordar para entender la creacion de la  estructura de la base de datos
        # local:

        #  * NOT NULL prohíbe que el valor de una base de datos sea nulo
        #  * UNIQUE en SQL se utiliza para garantizar que no se inserten valores duplicados en una columna
        #    específica o combinación de columnas que participen en la restricción UNIQUE y no formen parte
        #    de la CLAVE PRIMARIA.
        #  * AUTOINCREMENT permite generar automáticamente un número único cuando se inserta un nuevo registro
        #    en una tabla.
        #  * PRIMARY KEY es una columna que se utiliza para identificar la unicidad de las filas en una tabla.
        #    Cada tabla tiene una y solo una clave principal.

        if not (os.path.isfile(self.NOMBRE_BASE_DATOS)):  # si la base de datos no existe
            with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
                cursor.execute('''
                            CREATE TABLE Course(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_api VARCHAR(200) not null unique,
                            nombre VARCHAR(200)
                            )    
                ''')

                cursor.execute('''
                            CREATE TABLE Topic(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_api VARCHAR(200) not null unique ,
                            course_id_api VARCHAR(200),
                            nombre VARCHAR(200),
                            agregado INTEGER
                            )
                ''')

                cursor.execute('''
                            CREATE TABLE CourseWork(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_api VARCHAR(200) not null unique,
                                course_id_api VARCHAR(200),
                                topic_id_api VARCHAR(200),
                                titulo VARCHAR(200),
                                descripccion VARCHAR(500),
                                fechaCreacion TEXT,
                                agregado INTEGER  
                            )              
                ''')

            return True

##########################################################################################################################################
#  Clases de classroom
##########################################################################################################################################

    def add_curso(self, tuplaDatos):
        '''
        Agregara los datos de una clase de google classroom a la base de datos local.
        Los datos que agregara vienen contenidos en el parametro: 'tuplaDatos'

        Parámetros:
            tuplaDatos (tuple): Tupla de dos elementos,  que contiene los datos de la
            clase de classroom que se desea agregar a la base de datos local:
                * El primer elemento de la tupla (str): Representa el ID de la
                clase de google classroom
                * El segundo elemento de la tupla (str): Representa el nombre
                de la clase de classroom

        Returns:
            dato de tipo: 'int' que representa el ID que le asigna la base de datos local
            al renglon en donde se almacenaron los datos de la clase de classroom
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:

            #sqlOrden = "INSERT INTO(id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "INSERT INTO  Course  VALUES(NULL,?,?)"
            cursor.execute(sqlOrden, tuplaDatos)

            idAsignado = cursor.lastrowid
        return idAsignado


    def add_tuplaCursos(self,tuplaDatos):
        '''
        Agregara los datos de las clases de classroom contenidas en el
        parametro: 'tuplaDatos'.

     Parámetros:
            tuplaDatos (tuple): Tupla que contiene los datos de las  clases de classroom
            que se desean agregar a la base de datos local.Dicha tupla debe seguir el
            siguiente formato:
                 (
                    (id_api_1,nombre_1),
                    (id_api_2,nombre_2),
                    (id_api_3,nombre_3),
                            .
                            .
                            .
                )
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO(id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "INSERT INTO  Course  VALUES(NULL,?,?)"

            cursor.executemany(sqlOrden, tuplaDatos)


    def eliminarCursosRegistrados(self):
        """
        Elimina todos los datos de las clases de classroom registradas en la base
        de datos local.
        """
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO(id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "DELETE FROM Course "
            cursor.execute(sqlOrden)


    def getNombre_curso(self,curso_id):
        '''
        Parámetros:
            curso_id (str): Representa el ID de la clase de classrom
            de la cual se quiere saber su nombre respectivo.

        Returns:
            Dato de tipo 'str' que representa el nombre de la clase
            de classroom cuyo ID es igual al valor del parametro:
            'curso_id'
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="SELECT nombre FROM Course WHERE id_api=?"
            cursor.execute(sqlOrden,  (curso_id,) )

            # devuelve una tupla con el siguiente formato: ('Python Pre-Intermedio',)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            nombreCurso = tuple(cursor.fetchone() )

        return nombreCurso[0]


    def get_tuplaClases(self):
        '''
        Returns:
            dato de tipo: 'tuple' que contendra los datos de todas las clases
            de classroom que se encuentran almacenadas en la base de datos
            local. El formato de la tupla que se returnara sera el siguiente:

            (
                (id_api_1,nombre_1),
                (id_api_2,nombre_2),
                (id_api_3,nombre_3),
                        .
                        .
                        .
            )
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="SELECT id_api,nombre FROM Course "
            cursor.execute(sqlOrden)

            # devuelve la tupla:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            listaDatos = tuple(cursor.fetchall())

        return listaDatos

##########################################################################################################################################
#  Courseworks
##########################################################################################################################################

    def registrarCourseworkComoCalificable(self, curso_id, topic_id, idCourseWorkElegido):
        '''
        Registrara en la base de datos local que: FUE SELECCIONADA POR EL USUARIO COMO UNA TAREA CALIFICABLE
        la tarea(coursework):cuyo ID es igual al valor del parametro: 'idCourseWorkElegido' y que dicha
        tarea se encuentra  en la clase de classroom con ID igual al valor del parametro: 'curso_id' y
        topic de classroomm con ID igual al valor del parametro: 'topic_id'

        Parámetros:
            idCourseWork (str): Representa el ID del coursework que fue seleccionado por el usuario
            como coursework calificable
            curso_id (str): Representa el ID de la clase de classroom en donde se encuentra la tarea
            que se registrara como tarea calificable
            topic_id (str):  Representa el ID del topic de classroom en donde se encuentra la tarea
            que se registrara como tarea calificable
        '''

        tuplaDatos=(curso_id,topic_id,idCourseWorkElegido)

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="UPDATE CourseWork SET agregado=1  " \
                "WHERE course_id_api=? AND  topic_id_api=? AND id_api=?"
            cursor.execute( sql,tuplaDatos)


    def eliminarCourseWork(self,curso_id,topic_id,coursework_id):
        '''
        Eliminara de la base de datos local los datos de la tarea(coursework) cuyo
        id corresponde al valor del parámetro: 'courseWork_id'.Es importante  aclarar
        la tarea que se eliminar corresponde a una tarea que se encuentra en la clase
        de classroom y topic cuyos IDs son los valores que tomen  los parametros:
        'curso_id', 'topic_id'

        Parámetros:
            courseWork_id (str): Representa el ID de la tarea que se desea eliminar
            de la base de datos local
            curso_id (str): Representa el ID de la clase de classroom en donde se encuentra la tarea
            que se desea eliminar de la base de datos local
            topic_id (str):  Representa el ID del topic de classroom en donde se encuentra la tarea
            que se desea eliminar de la base de datos local
        '''

        tuplaDatos=(curso_id,topic_id,coursework_id)

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="DELETE FROM CourseWork  " \
                "WHERE course_id_api=? AND  topic_id_api=? AND id_api=?"
            cursor.execute( sql,tuplaDatos)


    def get_courseWorksLibres(self,curso_id,topic_id):
        '''
        Parámetros:
            curso_id (str): Representa el ID de la clase de classroom en donde se encuentran las tareas
            cuyos datos desean ser obtenidos
            topic_id (str):  Representa el ID del topic de classroom en donde se encuentran las tareas
            cuyos datos desean ser obtenidos

        Returns:
            dato de tipo: 'tuple': Retornara una tupla que contendra los datos
            de todas las tareas que cumplan con lo siguiente:
                - Se encuentran registradas en la clase de classroom y topic de classroom
                cuyos IDs son los valores que tomen  los parametros: 'curso_id', 'topic_id'
                - Son tareas que aun NO HAN sido registradas por el usuario como tareas
                calficables

            El formato de la tupla que retorna el metodo es el siguiente:
                [
                    [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
                    [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
                    [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
                                                    .
                                                    .
                                                    .
                ]
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = """SELECT id_api,titulo,descripccion,fechaCreacion FROM  CourseWork 
            WHERE  course_id_api=? AND topic_id_api=? AND agregado=0 """
            cursor.execute(sqlOrden,  (curso_id,topic_id)  )

            # devuelve una tupla:
            # (  (id_api_1,nombre_1,), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            listaDatos = tuple(cursor.fetchall())

        return listaDatos


    def get_courseWorksAgregados(self,curso_id,topic_id):
        '''

        Parámetros:
            curso_id (str): Representa el ID de la clase de classroom en donde se encuentran las tareas
            cuyos datos desean ser obtenidos
            topic_id (str):  Representa el ID del topic de classroom en donde se encuentran las tareas
            cuyos datos desean ser obtenidos

        Returns:
            dato de tipo: 'tuple': Retornara una tupla que contendra los datos
            de todas las tareas que cumplan con lo siguiente:
                - Se encuentran registradas en la clase de classroom y topic de classroom
                cuyos IDs son los valores que tomen  los parametros: 'curso_id', 'topic_id'
                - Son tareas que ACTUALMENTE ESTAN registradas por el usuario como tareas
                calficables

            El formato de la tupla que retorna el metodo es el siguiente:
                [
                    [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
                    [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
                    [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
                                                    .
                                                    .
                                                    .
                ]
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = """SELECT id_api,titulo,descripccion,fechaCreacion FROM  CourseWork 
            WHERE  course_id_api=? AND topic_id_api=? AND agregado=1 """
            cursor.execute(sqlOrden,  (curso_id,topic_id)  )

            # devuelve una tupla:
            # (  (id_api_1,nombre_1,), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            listaDatos = tuple(cursor.fetchall())

        return listaDatos


    def agregar_soloNuevosCourseWorks(self, tuplaDatos,curso_id,topic_id):
        '''
        Agregara a la base de datos local los datos de las tareas(courseworks) que
        se encuentran en el parametro: 'tuplaDatos'.

        Es importante aclarar que este metodo solo agregara los datos de las tareas
        que no esten registrados en la base de datos, es decir evitara la duplicacion
        de los datos.

        Parámetros:
            tuplaDatos (tuple): Tupla que almacena los datos de las tareas que seran
            agregadas a la base de datos local.La tupla de datos tiene agrupados los
            datos de las tareas(courseworks) de la siguiente forma:
            (
                   (id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1),
                   (id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2) ,
                   ....
            )

            curso_id (str) : Representa el ID de la clase de classroom en donde se encuentran
            las tareas cuyos datos vienen dentro de: 'tuplaDatos'

            topic_id (str) : Representa el ID del topic de classroom en donde se encuentran
            las tareas cuyos datos vienen dentro de: 'tuplaDatos'
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO  Topic(id,id_api,course_id_api,topic_id_api,titulo,descripccion,fechaCreacion)  VALUES(NULL,?,?,?,?,?,?)"
            sqlOrden = "INSERT OR IGNORE INTO  CourseWork  VALUES(NULL,?,'{}','{}',?,?,?,0)".format(curso_id,topic_id)
            cursor.executemany(sqlOrden, tuplaDatos)


    def add_courseWork(self, tuplaDatos):
        '''
        Agregara a la base de datos local los datos de la tarea(coursework) cuyos
        datos  se encuentran en el parametro: 'tuplaDatos'.

        Parámetros:
            tuplaDatos (tuple): Tupla que almacena los datos de la tarea
            La tupla de datos tiene agrupados los datos de las tarea(courseworks) de
            la siguiente forma:
                   (id_topic,nombre_topic,descripccion_tarea,fechaCreacion_tarea)

            curso_id (str) : Representa el ID de la clase de classroom en donde se encuentra
            la tarea cuyos datos vienen dentro de: 'tuplaDatos'

            topic_id (str) : Representa el ID del topic de classroom en donde se encuentra
            la tarea cuyos datos vienen dentro de: 'tuplaDatos'

        Returns:
            dato de tipo: 'int' que representa el ID que le asigna la base de datos local
            al renglon en donde se almacenaron los datos de la tarea.
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:

            #sqlOrden = "INSERT INTO  Topic(id_api,course_id_api,topic_id_api,titulo,descripccion,fechaCreacion)  VALUES(NULL,?,?,?,?,?,?)"
            sqlOrden = "INSERT INTO  CourseWork  VALUES(NULL,?,?,?,?,?,?)"
            cursor.execute(sqlOrden, tuplaDatos)

            # recuperando el 'id' que la base de datos le asigno a la alarma que almmaceno
            idAsignado = cursor.lastrowid
        return idAsignado

##########################################################################################################################################
# Topics
##########################################################################################################################################

    def add_topic(self, tuplaDatos):
        '''
        Agregara a la base de datos local los datos del topic cuyos datos  se encuentran en el
        parametro: 'tuplaDatos'.

        Parámetros:
            tuplaDatos (tuple): Tupla que almacena los datos del topic que seran agregados
            a la base de datos local
            La tupla de datos tiene agrupados los datos del  topic de la siguiente forma:
                   (id_topic,nombre_topic)

            curso_id (str) : Representa el ID de la clase de classroom en donde se encuentra
            el topic cuyos datos vienen dentro de: 'tuplaDatos'

         Returns:
            dato de tipo: 'int' que representa el ID que le asigna la base de datos local
            al renglon en donde se almacenaron los datos del topic

        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            #sqlOrden = "INSERT INTO  Topic(id_api,course_id_api,nombre)  VALUES(NULL,?,?,?)"
            sqlOrden = "INSERT INTO  Topic  VALUES(NULL,?,?,?)"
            cursor.execute(sqlOrden, tuplaDatos)
            idAsignado = cursor.lastrowid

        return idAsignado


    def agregar_soloNuevosTopics(self,tuplaDatos,curso_api_id):
        '''
        Agregara a la base de datos local los datos de las topics que se encuentran en el parametro:
        'tuplaDatos'.

        Es importante aclarar que este metodo solo agregara los datos que no esten  registrados
        en la base de datos, es decir evitara la duplicacion de los datos.


        Parámetros:
            tuplaDatos (tuple): Tupla que almacena los datos de los topics que seran agregados
            a la base de datos local
            La tupla de datos tiene agrupados los datos de los topics  de la siguiente forma:
                   (
                        (idApi_topic_1,nombre_topic_1),
                        (idApi_topic_2,nombre_topic_2),
                                    .
                                    .
                                    .
                    )

            curso_id (str) : Representa el ID de la clase de classroom en donde se encuentran
            los topics cuyos datos vienen dentro de: 'tuplaDatos'
        '''


        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO(id_api,course_id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "INSERT OR IGNORE INTO Topic  VALUES(NULL,?,'{}',?,0)".format(curso_api_id)
            cursor.executemany(sqlOrden, tuplaDatos)



    def registrarSelecciono_topic(self,curso_id,topic_id):
        '''
        Registrara en la base de datos local que: FUE SELECCIONADO POR EL USUARIO COMO TOPIC SELECCIONABLE
        el topic cuyo ID es igual al valor del parametro: 'topic_id'

        Parámetros:
            curso_id (str): Representa el ID de la clase de classroom en donde se encuentra el topic
            que se registrara como topic seleccionable
            topic_id (str):  Representa el ID del topic que se registrara como topic seleccionable
        '''

        tuplaDatos=(topic_id,curso_id)

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="UPDATE Topic SET agregado=1  WHERE id_api=? AND  course_id_api=?"
            cursor.execute( sql, tuplaDatos )
        return True


    def get_topicsAgregados(self,course_id_api):
        '''
         Parámetros:
             course_id_api (str): Representa el ID de la clase de classroom en donde se encuentran los topics
             cuyos datos desean ser obtenidos

         Returns:
             dato de tipo: 'tuple': Retornara una tupla que contendra los datos
             de todas los topics  que cumplan con lo siguiente:
                 - Se encuentran registrados en la clase de classroom cuyo ID es el que tomara
                 el parametro: 'course_id_api'
                 - Son topics que ACTUALMENTE ESTAN registrados por el usuario como topics
                 seleccionables.

             El formato de la tupla que retorna el metodo es el siguiente:
                   (
                        (idApi_topic_1,nombre_topic_1),
                        (idApi_topic_2,nombre_topic_2),
                                    .
                                    .
                                    .
                    )
         '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = "SELECT id_api,nombre FROM Topic WHERE  course_id_api=? AND agregado=1"
            cursor.execute(sqlOrden,  (course_id_api,)  )

            # devuelve una tupla:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            listaDatos = tuple(cursor.fetchall())

        return listaDatos



    def get_topicsLibres(self,course_id_api):
        '''
         Parámetros:
             course_id_api (str): Representa el ID de la clase de classroom en donde se encuentran los topics
             cuyos datos desean ser obtenidos

         Returns:
             dato de tipo: 'tuple': Retornara una tupla que contendra los datos
             de todas los topics  que cumplan con lo siguiente:
                 - Se encuentran registrados en la clase de classroom cuyo ID es el que tomara
                 el parametro: 'course_id_api'
                 - Son topics que ACTUALMENTE NO ESTAN registrados por el usuario como topics
                 seleccionables.

             El formato de la tupla que retorna el metodo es el siguiente:
                   (
                        (idApi_topic_1,nombre_topic_1),
                        (idApi_topic_2,nombre_topic_2),
                                    .
                                    .
                                    .
                    )
         '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = "SELECT id_api,nombre FROM Topic WHERE  course_id_api=? AND agregado=0"
            cursor.execute(sqlOrden,  (course_id_api,)  )

            # devuelve una tupla:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            listaDatos = tuple(cursor.fetchall())

        return listaDatos



    def eliminarTopic(self,curso_id,topicProgramas_id):
        '''
        Eliminara de la base de datos local los datos del topic cuyo  id corresponde al valor del
        parámetro: 'topicProgramas_id'.

        Parámetros:
            curso_id (str): Representa el ID de la clase de classroom en donde se encuentra el topic
            que se desea eliminar
            topic_id (str):  Representa el ID del topic que se eliminara
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            tuplaDatos = (topicProgramas_id, curso_id)
            sqlOrden = """DELETE  FROM Topic  WHERE id_api=? AND course_id_api=? """
            cursor.execute(sqlOrden, tuplaDatos )


    def getNombre_topic(self,curso_id,topic_id):
        '''
        Parámetros:
            curso_id (str): Representa el ID de la clase de classroom
            en donde se encuentra el topic cuyo nombre quiere ser obtenido
            topic_id (str): Representa el ID del topic cuyo nombre desea
            ser obtenido

        Returns:
            Dato de tipo 'str' que representa el nombre del topic
            de classroom cuyo ID es igual al valor del parametro:
            'topic_id'
        '''


        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="SELECT nombre FROM Topic WHERE course_id_api=? AND id_api=?"
            cursor.execute(sqlOrden,  (curso_id,topic_id) )

            # devuelve una tupla:
            # ('Python Pre-Intermedio',)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()
            nombreTopic = tuple(cursor.fetchone() )

        return nombreTopic[0]


import os
import sqlite3
from typing import Tuple
import sys
import recursos

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
            baseDatos -- nombre de la base de datos de la cual se desea hacer
            conexion
        '''

        self.__BASE_DATOS = baseDatos
        self.__conexion = None
        self.__cursor = None

    def obtenerConexion(self):
        """
        Creara un objeto  de tipo 'conexion' el cual sirve para conectarse
        con la base de datos cuyo nombre  es igual a: 'self.__BASE_DATOS'

        Returns(devoluciones):
            objeto de tipo 'conexion' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierre inmediato del programa
        """

        if self.__cursor is None:
            try:
                self.__conexion = sqlite3.connect(self.__BASE_DATOS)
                #logger.debug(f'Conexión exitosa: {self.__conexion}')
                return self.__conexion

            except Exception as e:
                print(e)
                #logger.error(f'Error al conectar a la BD: {e}')
                sys.exit()
        else:
            return self.__conexion

    def obtenerCursor(self):
        """
        Apartir del atributo de instancia: 'self.__cursor' creara un objeto  de tipo 'cursor'
        el cual sirve para ejecutar sentencias de tipo Query a la base de datos cuyo nombre
        es igual a: 'self.__BASE_DATOS'

        Returns(devoluciones):
            objeto de tipo 'conexion' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierre inmediato del programa
        """

        if self.__cursor is None:
            try:
                self.__cursor = self.obtenerConexion().cursor()
                #logger.debug(f'Se abrio el cursor con éxito: {self.__cursor}')
                return self.__cursor
            except Exception as e:
                print(e)
                #logger.error(f'Error al obtener cursor:{e}')
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
                pass
                #logger.error(f'Error al cerrar cursor: {e}')

        if self.__conexion is not None:
            try:
                self.__conexion.close()
            except Exception as e:
                print(e)
                pass

                #logger.error(f'Error al cerrar conexión: {e}')

        self.__conexion = None
        self.__cursor = None
        #logger.debug('Se han cerrado los objetos de conexión y cursor')


class Cursor:
    '''
    Clase cuyo objetivo es que sus instancias permitan omitir las lineas de codigo:
        a) 'conexion=sqlite3.connect()'
        b) 'cursor=conexion.cursor()'
        c) 'conexion.commit() '
        b) 'cursor.close()'
        c) 'conexion.close()'
    Para cada setencia Query que se desea ejecutar con la base de datos por ende
    esta clase define a los metodos especiales '__enter__', '__exit__' los cuales
    permiten utilizar el 'with as' y que este hago las lineas de codigo mencionadas
    anteriormente.
    '''

    def __init__(self, nombreBase):
        '''
        Parámetros:
            nombreBase -- dato de tipo 'str' que representa el nombre de la base
            de dato que se desea abrir, obtener una conexion, despues un cursor
            para posteriormente ejecutar una sentencia query, y finalmente
            guardar los cambios realizador y cerrar la conexion y el cursor.
        '''

        self.nombreBase = nombreBase
        self.__objetoConector = Conexion(nombreBase)

    # inicio de with
    def __enter__(self):
        '''
        Lo que returne este metodo es lo que almacenara la variable que le procede a:
        'as' del 'with open() as', es decir si setiene que:
            'with open(nombreBase) as variableX'
            la variable cuyo nombre es 'variableX' almacenara lo que
            retorne este metodo

        Returns(devoluciones):
            Objeto de tipo cursor que permitira ejecutar sentencias
            Query a la base de datos cuyo nombre es igual a:'self.nombreBase'
        '''

        #logger.debug('Inicio de with método __enter__')
        return self.__objetoConector.obtenerCursor()

    # fin del bloque with
    def __exit__(self, exception_type, exception_value, exception_traceback):
        '''
        Este metodo definira lo que se haga una vez que se termine de ejecutar
        la ultima linea de codigo que este definida dentro del 'with() as'
        ejemplo:
            with(nombreArchivo) as:
                linea de codigo 1 que definide el usuario dentro del 'with as'
                linea de codigo 2 que definide el usuario dentro del 'with as'
                linea de codigo 3 que definide el usuario dentro del 'with as'
                linea de codigo 4 que definide el usuario dentro del 'with as'
                .
                .
                ultima linea de codigo  que definide el usuario dentro del 'with as'
                ACCION DEFINIDA EN ESTE METODO SE EJECUTARA AQUI
        '''

        #logger.debug('Se ejecuta método __exit__()')

        # if exception_value is not None:
        if exception_value:
            # self.__conn.rollback()
            print(exception_value)
            #logger.debug(f'Ocurrió una excepción: {exception_value}')
            sys.exit()

        else:
            self.__objetoConector.obtenerConexion().commit()
            #logger.debug('Commit de la transacción')

            # Cerramos las conexiones
        self.__objetoConector.cerrar()

#############################################################################################################################
# A L A R M A
############################################################################################################################

class BaseDatos_ClassRoomProgramas():
    '''
    Clase que servira para crear bases de datos que permitan registrar los datos
    de las alarmas, asi como que permitan que se consulten de la manera mas
    sencilla los datos de las alarmas almacenadas
    '''


    def __init__(self, NOMBRE_BASE_DATOS):
        """

        Parámetros:
            NOMBRE_BASE_DATOS -- Necesita el nombre completo de la base de datos que
            almacenara los datos de las alarmas, el nombre completo es aquel que
            contiene la ruta completa de donde se ubica la base de datos.Es importante
            que el nombre incluya la extension del archivo es decir una extension
            '.sqlite3' o '.db'
        """

        self.NOMBRE_BASE_DATOS = NOMBRE_BASE_DATOS

    def crearBaseDatos(self):
        '''
        Creara la base de datos con el nombre y las secciones requeridas

        Returns (Devoluciones):
            dato de tipo 'bool' igual a 'True' si hubo exito.
            Si no hubo exito en la operación se ocasionara el cierra inmediato del programa
        '''


        if not (os.path.isfile(self.NOMBRE_BASE_DATOS)):  # si la base de datos no existe
            with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
                cursor.execute('''
                            CREATE TABLE Course(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_api VARCHAR(200) not null unique,
                            nombre VARCHAR(200)
                            )    
                ''')

                #nada_tarea_retro INTEGER, # nada=0,tarea=1,retro=2
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
                ''')#0 NO  1 SI

            return True

##########################################################################################################################################
#  CURSOS
##########################################################################################################################################


    def add_curso(self, tuplaDatos):

            with Cursor(self.NOMBRE_BASE_DATOS) as cursor:

                #sqlOrden = "INSERT INTO(id_api,nombre)  Course  VALUES(NULL,?,?)"
                sqlOrden = "INSERT INTO  Course  VALUES(NULL,?,?)"

                cursor.execute(sqlOrden, tuplaDatos)

                idAsignado = cursor.lastrowid
            return idAsignado


    def add_tuplaCursos(self,tuplaDatos):
        '''

        (
           (c1_dato1,c1_dato1),
           (c2_dato1,c1_dato2),
           (c3_dato1,c1_dato3),
           .
           .
        )
        :return:
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO(id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "INSERT INTO  Course  VALUES(NULL,?,?)"

            cursor.executemany(sqlOrden, tuplaDatos)

            idAsignado = cursor.lastrowid
        return idAsignado


    def eliminarCursosRegistrados(self):
        """
        Elimina todos los cursos registrados

        :return:
        """
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO(id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "DELETE FROM Course "
            cursor.execute(sqlOrden)




    def getNombre_curso(self,curso_id):
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="SELECT nombre FROM Course WHERE id_api=?"
            cursor.execute(sqlOrden,  (curso_id,) )

            nombreCurso = tuple(cursor.fetchone() )  # devuelve una tupla:
            # ('Python Pre-Intermedio',)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return nombreCurso[0]




    def get_tuplaClases(self):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="SELECT id_api,nombre FROM Course "
            cursor.execute(sqlOrden)

            listaDatos = tuple(cursor.fetchall())  # devuelve una tupla:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return listaDatos

##########################################################################################################################################
#  COUSERWORKS
##########################################################################################################################################

    def cambiarEstadoEleccion(self,curso_id,topic_id,idCourseWorkElegido):
        tuplaDatos=(curso_id,topic_id,idCourseWorkElegido)

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="UPDATE CourseWork SET agregado=1  " \
                "WHERE course_id_api=? AND  topic_id_api=? AND id_api=?"
            print(sql)
            cursor.execute( sql,tuplaDatos)
        return True



    def eliminarCourseWork(self,curso_id,topic_id,coursework_id):

        tuplaDatos=(curso_id,topic_id,coursework_id)

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="DELETE FROM CourseWork  " \
                "WHERE course_id_api=? AND  topic_id_api=? AND id_api=?"
            cursor.execute( sql,tuplaDatos)
        return True




    def get_courseWorksLibres(self,curso_id,topic_id):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = """SELECT id_api,titulo,descripccion,fechaCreacion FROM  CourseWork 
            WHERE  course_id_api=? AND topic_id_api=? AND agregado=0 """
            cursor.execute(sqlOrden,  (curso_id,topic_id)  )

            listaDatos = tuple(cursor.fetchall())  # devuelve una tupla:
            # (  (id_api_1,nombre_1,), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return listaDatos


    def get_courseWorksAgregados(self,curso_id,topic_id):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = """SELECT id_api,titulo,descripccion,fechaCreacion FROM  CourseWork 
            WHERE  course_id_api=? AND topic_id_api=? AND agregado=1 """
            cursor.execute(sqlOrden,  (curso_id,topic_id)  )

            listaDatos = tuple(cursor.fetchall())  # devuelve una tupla:
            # (  (id_api_1,nombre_1,), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return listaDatos


    def agregar_soloNuevosCourseWorks(self, tuplaDatos,curso_id,topic_id):
        '''
         tarea.get('id'), curso_id, topic_id, tarea.get('title'),
        #    tarea.get('description'), fechaCreacion

        :param tuplaDatos:
        :return:
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO  Topic(id,id_api,course_id_api,topic_id_api,titulo,descripccion,fechaCreacion)  VALUES(NULL,?,?,?,?,?,?)"
            sqlOrden = "INSERT OR IGNORE INTO  CourseWork  VALUES(NULL,?,'{}','{}',?,?,?,0)".format(curso_id,topic_id)
            #'{}',?,NULL)".format(curso_api_id)
            cursor.executemany(sqlOrden, tuplaDatos)


    def add_courseWork(self, tuplaDatos):
        '''
         tarea.get('id'), curso_id, topic_id, tarea.get('title'),
        #    tarea.get('description'), fechaCreacion

        :param tuplaDatos:
        :return:
        '''


        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:

            #sqlOrden = "INSERT INTO  Topic(id_api,course_id_api,topic_id_api,titulo,descripccion,fechaCreacion)  VALUES(NULL,?,?,?,?,?,?)"
            sqlOrden = "INSERT INTO  CourseWork  VALUES(NULL,?,?,?,?,?,?)"
            cursor.execute(sqlOrden, tuplaDatos)

            # recuperando el 'id' que la base de datos le asigno a la alarma que almmaceno
            idAsignado = cursor.lastrowid
        return idAsignado

##########################################################################################################################################
# TOPIC
##########################################################################################################################################

    def add_topic(self, tuplaDatos):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            #sqlOrden = "INSERT INTO  Topic(id_api,course_id_api,nombre)  VALUES(NULL,?,?,?)"
            sqlOrden = "INSERT INTO  Topic  VALUES(NULL,?,?,?)"

            cursor.execute(sqlOrden, tuplaDatos)
            idAsignado = cursor.lastrowid

        return idAsignado



    def agregar_soloNuevosTopics(self,tuplaDatos,curso_api_id):
        '''
        (
            (id_api,nombre),
            (id_api,nombre),
            (id_api,nombre),
                  .
                  .
                  .

        )

        :param tuplaDatos:
        :param curso_api_id:
        :return:
        '''

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            # sqlOrden = "INSERT INTO(id_api,course_id_api,nombre)  Course  VALUES(NULL,?,?)"
            sqlOrden = "INSERT OR IGNORE INTO Topic  VALUES(NULL,?,'{}',?,0)".format(curso_api_id)
            cursor.executemany(sqlOrden, tuplaDatos)

    def get_topicsAgregados(self,course_id_api):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = "SELECT id_api,nombre FROM Topic WHERE  course_id_api=? AND agregado=1"
            cursor.execute(sqlOrden,  (course_id_api,)  )

            listaDatos = tuple(cursor.fetchall())  # devuelve una tupla:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return listaDatos


    def registrarSelecciono_topic(self,curso_id,topic_id):
        tuplaDatos=(topic_id,curso_id)

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sql="UPDATE Topic SET agregado=1  WHERE id_api=? AND  course_id_api=?"
            cursor.execute( sql, tuplaDatos )
        return True


    def get_topicsLibres(self,course_id_api):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden = "SELECT id_api,nombre FROM Topic WHERE  course_id_api=? AND agregado=0"
            cursor.execute(sqlOrden,  (course_id_api,)  )

            listaDatos = tuple(cursor.fetchall())  # devuelve una tupla:
            # (  (id_api_1,nombre_1), (id_api_2,nombre_2), (id_api_3,nombre_3), ....)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return listaDatos


    def eliminarTopic(self,curso_id,topicProgramas_id):

        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            tuplaDatos = (topicProgramas_id, curso_id)
            sqlOrden = """DELETE  FROM Topic  WHERE id_api=? AND course_id_api=? """
            cursor.execute(sqlOrden, tuplaDatos )
            print(sqlOrden)


    def getNombre_topic(self,curso_id,topic_id):
        with Cursor(self.NOMBRE_BASE_DATOS) as cursor:
            sqlOrden="SELECT nombre FROM Topic WHERE course_id_api=? AND id_api=?"
            cursor.execute(sqlOrden,  (curso_id,topic_id) )

            nombreTopic = tuple(cursor.fetchone() )  # devuelve una tupla:
            # ('Python Pre-Intermedio',)
            # sin embargo si no contiene nada devuelve una tupla vacia, como: ()

        return nombreTopic[0]


'''
CalificadorConfiguracion.py :

        Contiene una sola  clase, la clase 'CalificadorConfiguracion', la cual a grosso modo
        sirve para agrupar en un solo objeto todos los datos que se necesitan para poder
        calificar las tareas de programación

'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


# librerias estandar
import os

# fuente local
import recursos

class CalificadorConfiguracion:
    '''
    El objetivo de este clase es crear objetos que contengan de una forma ordenada todos los datos
    necesarios para que se puedan calificar tareas.
    Cuando se califican tareas de programacion se tiene que definir muchas cosas:
        - El nombre y id de la clase de classroom en donde se encuentra la o las tareas que
        se desean calificar
        - El nombre y id del topic en donde se encuentran la o las tareas que se desean calificar
        (de esta manera se delimita aun mas en donde se encuentra la o las tareas que se desean calificar)
        - El nombre de la clase creada con NBGRADER en donde se encuentran  la o las tareas
        que fueron creadas por el maestro(es importante mencionar que las clases de NBGRADER deben estar
        en un ubicacion especifica la cual defino en el script cuyo nombre es 'recursos.py' )
        - El nombre y id de la carpeta en donde se subiran todas las retroalimentaciones de las tareas
        de los alumnos
    '''


    def __init__(self,nombre_profesor=None,correo_profesor=None,curso_nombre=None,
                 curso_idApi=None, topic_nombre=None, topic_idApi=None, claseNbGrader_nombre=None,
                 idCarpetaRetro=None,nombreCarpetaRetro=None):
        '''

        Parámetros:
            - curso_nombre (str): Representa el nombre del curso de classroom en donde se encuentran
              las tareas de programacion que se desean calificar
            - curso_idApi (str): Representa el id del curso de classroom en donde se encuentran las
              tareas de programacion que se desean calificar

            - topic_nombre (str): Representa el nombre del topic en donde se encuentran las tareas de
              programacion que se desean calificar
            - topic-idApi (str): Representa el id del topic de classroom en donde se encuentran las
            tareas de programacion que se desean calificar

            - claseNbGrader_nombre (str): Representa el nombre de la clase de NbGrader
            - idCarpetaRetro (str): Representa el id de la carpeta de google drive que fue elegida
            para respaldar todas las retroalimentaciones
            - nombreCarpetaRetro (str): Representa el nombre de la carpeta de google drive que fue
            elegida para respaldar todas las retroalimentaciones

            -nombre_profesor (str): Representa el nombre del usuario que inicio sesión en CACPY
            -correo_profesor (str): Representa el correo electronico del profesor que inicio
            sesión en CACPY
        '''

        self.curso_idApi = curso_idApi
        self.curso_nombre=curso_nombre

        self.topic_idApi=topic_idApi
        self.topic_nombre=topic_nombre

        self.claseNbGrader_nombre=claseNbGrader_nombre

        self.nombre_profesor=nombre_profesor
        self.correo_profesor=correo_profesor

        self.idCarpetaRetro=idCarpetaRetro
        self.nombreCarpetaRetro=nombreCarpetaRetro



#############################################################################################################################
# SETTERS  Y    GETTERS (solo comente los que no fueran legibles de entender)
#############################################################################################################################

    def setDatosCarpetaRetroalimentacion(self,nombre,idApi):
        self.nombreCarpetaRetro=nombre
        self.idCarpetaRetro=idApi

    def set_clase_nombreNbGrader(self,nuevoValor):
        self.claseNbGrader_nombre=nuevoValor

    def set_nombre_cursoNbGrader(self,nombre):
        self.claseNbGrader_nombre=nombre

    def getNombreCarpetaRetro(self):
        return self.nombreCarpetaRetro

    def getIdApiCarpetaRetro(self):
        return self.idCarpetaRetro

    def getNombreProfesor(self):
        return self.nombre_profesor

    def getCorreoProfesor(self):
        return self.correo_profesor

    def getIdApi_cursoClassroom(self):
        return self.curso_idApi

    def getNombre_cursoClassroom(self):
        return self.curso_nombre

    def getNombre_topicClassroom(self):
        return self.topic_nombre

    def getIdApi_topicClassroom(self):
        return self.topic_idApi

    def get_nombre_cursoNbGrader(self):
        return self.claseNbGrader_nombre


    def get_id_nombre_cursoClassroom(self):
        '''
        Returns:
            Dato de tipo 'tuple', dicha tupla solo tiene dos elementos:
                - el primer elemento (str): Representa el id de la clase de classroom
                - el segundo elemetno (str): Representa el nombre de la clase de
                classroom
        '''

        return self.curso_idApi, self.curso_nombre

    def get_id_nombre_topicClassroom(self):
        '''
        Returns:
            Dato de tipo 'tuple', dicha tupla solo tiene dos elementos:
                - el primer elemento (str): Representa el id del topic de classroom
                - el segundo elemetno (str): Representa el nombre del topic de
                classroom
        '''

        return self.topic_idApi, self.topic_nombre

#############################################################################################################################
# CARGANDO  Y RESPALDANDO DATOS DATOS
#############################################################################################################################

    def cargarDatosProfesorSinArchivo(self,nombre,correo):
        '''
        Cargara los nuevos datos que se tienen del usuario(profesor), es decir
        actualizara el valor de los atributos de instancia: 'self.nombre_profesor'
        y 'self.correo_profesor' por los valores contenidos en los parametros:
        'nombre' y 'correo'

        Parámetros:
            nombre (str): Representa el nuevo valor que se le asignara al atributo
            de instancia: 'self.nombre_profesor'
            correo (str): Representa el nuevo valor que se le asignara al atributo
            de instancia: 'self.correo_profesor'
        '''

        self.nombre_profesor=nombre
        self.correo_profesor=correo

    def cargarDatosTopic(self,programaTopic_id,programaTopic_nombre):
        '''
        Cargara los nuevos datos que se tienen del topic de classroom seleccionado,
        es decir actualizara el valor de los atributos de instancia: 'self.topic_idApi'
        y 'self.topic_nombre'  por los valores contenidos en los parametros:
        'programaTopic_id' y 'programaTopic_nombre'

        Parámetros:
            programaTopic_id: Representa el nuevo valor que se le asignara al atributo
            de instancia: 'self.programaTopic_id'
            programaTopic_nombre: Representa el nuevo valor que se le asignara al atributo
            de instancia: 'self.programaTopic_nombre'
        '''

        self.topic_idApi=programaTopic_id
        self.topic_nombre=programaTopic_nombre


    def cargarDatosClaseClassroom_seleccionada(self, clase_idApi, clase_nombre):
        '''
        Lo que hara es reiniciar a None todos los valores de los atributos de instancia
        que se se ven afectados por el cambio al nuevo valor en la  clase de google
        classroom seleccionada, posteriormente actualizara el valor de los atributos de
        instancia: 'self.curso_idApi' y 'self.curso_nombre'  por los valores contenidos
        en los parametros: 'clase_idApi' y 'clase_nombre'

        El efecto secundario que tendra esto es que al ser:
            - self.claseNbGrader_nombre=None
            - self.topic_idApi=None

        El metodo 'datosListosApartadoTareas()' retornara False, ya que este
        metodo solo retornara True cuando se tenga valor definido para cada atributo
        de instancia.

        Parámetros:
            - clase_idApi (str) : Representa el nuevo valor que se le asignara al atributo
            de instancia: 'self.curso_idApi'
            - clase_nombre (str): Representa el nuevo valor que se le asignara al atributo
            de instancia: 'self.curso_nombre'
        '''

        self.reiniciarValores()
        self.curso_idApi = clase_idApi
        self.curso_nombre=clase_nombre


    def reiniciarValores(self):
        '''
        Igualara a None a todos  los atributos de instancia  que se se ven afectados si el usuario
        cambia la clase de classroom seleccionada por otra diferente.

        El efecto secundario que tendra esto es que al ser:
            - self.claseNbGrader_nombre=None
            - self.topic_idApi=None

        El metodo 'datosListosApartadoTareas()' retornara False, ya que este
        metodo solo retornara True cuando se tenga valor definido para cada atributo
        de instancia.
        '''

        self.curso_nombre = None
        self.curso_idApi = None
        self.topic_nombre = None
        self.topic_idApi=None
        self.claseNbGrader_nombre=None


    def cargarDatosUltimaSesion(self, archivoDatos):
        '''
        Cargara los datos del archivo cuyo nombre es: 'archivoDatos', dicho archivo
        debera contener los siguientes datos en el orden en el que son mencionados:
            * El id de las clase  de classroom que el usuario selecciono la ultima vez que inicio
            sesión con CACPY
            * El id del topic  de classroom que el usuario selecciono la ultima vez que inicio
            sesión con CACPY
            * El id de la carpeta de google drive que el usuario selecciono como la carpeta en
            donde se almacenaran todas las retroalimentaciones
            * El nombre de la carpeta de google drive que el usuario selecciono como la carpeta en
            donde se almacenaran todas las retroalimentaciones
            * El nombre de la clase de NbGrader que el usuario selecciono la ultima vez que inicio
            seisión con CACPY

        Cada dato el  archivo debera tenerlo separado por un salto de linea

        Lo que hace este metodo es una vez cargados los datos del archivo los procede a almacenar
        en los respectivos atributos de instancia.
        '''

        # Leyendo los datos del ultimo curso y topic que el profesor selecciono
        if os.path.isfile(archivoDatos):
            # El archivo que se abrira contiene los datos: curso_id, topic_id
            # cada dato lo tiene separado por un salto de linea
            with open(archivoDatos) as archivo:
                datos = archivo.read()
            curso_idApi, topic_idApi, idCarpetaRetro, nombreCarpetaRetro, claseNbGrader_nombre = datos.split('\n')

            self.curso_idApi = curso_idApi
            self.topic_idApi = topic_idApi
            self.idCarpetaRetro = idCarpetaRetro
            self.nombreCarpetaRetro = nombreCarpetaRetro
            self.claseNbGrader_nombre = claseNbGrader_nombre


    def cargarDatosProfesor(self, archivoDatos):
        '''
        Cargara los datos del archivo cuyo nombre es: 'archivoDatos', dicho archivo
        debera contener los siguientes datos en el orden en el que son mencionados:
            * Nombre del usuario que ingreso a CACPY  y que decidio no cerrar su sesión
            * Correo electronico del usuario que ingreso a CACPY y que decidio no cerrar
            sesion

        Cada dato el  archivo debera tenerlo separado por un salto de linea

        Lo que hace este metodo es una vez cargados los datos del archivo los procede a almacenar
        en los respectivos atributos de instancia.
        '''

        # Leyendo los datos guardados del profesor
        if os.path.isfile(archivoDatos):
            # El archivo que se abrira contiene los datos: correo del profesor, nombre completo del profesor
            # cada dato lo tiene separado por un salto de linea
            with open(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR) as archivo:
                datos = archivo.read()
            self.correo_profesor, self.nombre_profesor = datos.split('\n')

    def respaldarDatosProfesor(self,nombreArchivo):
        '''
        Creara un archivo con el nombre de: 'nombreArchivo' si y solo si TODOS
        los atributos de instancia siguientes tienen un valor diferente a None:
            - self.correo_profesor
            - self.nombre_profesor

        Si alguno de los atributos de instancia antes mencionados almacena
        el valor: None, entonces NO SE CREARA EL ARCHIVO y si ya existia uno
        con dicho nombre, entonces se eliminara dicho archivo, ya que la filosofia de
        guardar los datos, es o todos se guardan o ninguno se guarda

        ¿Que se creara en el archivo?
        En el archivo que se va a crear se guardaran los datos de los atributos de instancia
        antes mencionados cada uno de ellos separados con un salto de linea.El objetivo de
        guardar dichos datos es respaldar los datos del profesor, pues este metodo esta
        pensado para llamarse justo antes de que cierre CACPY con la finalidad de guardar
        dichos datos y la proxima vez que se incie sesión puedan verse los datos trabajados
        la vez anterior.
        '''


        seDebeRespaldar= (self.correo_profesor != None and self.nombre_profesor != None)
        archivoDatosExiste=os.path.isfile(nombreArchivo)
        datosRespaldar=(
            self.correo_profesor,
            self.nombre_profesor
        )

        if seDebeRespaldar:
            with open(nombreArchivo,'w') as archivo:
                archivo.write(  '\n'.join( datosRespaldar )   )

        elif archivoDatosExiste:
            os.remove(nombreArchivo)


    def respaldarDatosSesion(self,nombreArchivo):
        '''
        Creara un archivo con el nombre de: 'nombreArchivo' si y solo si TODOS
        los atributos de instancia siguientes tienen un valor diferente a None:
            - self.curso_idApi
            - self.topic_idApi
            - self.claseNbGrader_nombre
            - self.nombreCarpetaRetro!=None
            - self.idCarpetaRetro

        Si alguno de los atributos de instancia antes mencionados almacena
        el valor: None, entonces NO SE CREARA EL ARCHIVO y si ya existia uno
        con dicho nombre, entonces se eliminara dicho archivo

        ¿Que se creara en el archivo?
        En el archivo que se va a crear se guardaran los datos de los atributos de instancia
        antes mencionados cada uno de ellos separados con un salto de linea.El objetivo de
        guardar dichos datos es respaldar los datos, pues este metodo esta pensado para llamarse
        justo antes de que cierre CACPY con la finalidad de guardar  dichos datos y la proxima vez
        que se incie sesión puedan verse los datos trabajados la vez anterior, ya que la filosofia de
        guardar los datos, es o todos se guardan o ninguno se guarda
        '''

        seDebeRespaldar= self.curso_idApi != None and self.topic_idApi != None and \
                         self.claseNbGrader_nombre!=None and self.nombreCarpetaRetro!=None \
                         and self.idCarpetaRetro!=None


        archivoDatosExiste=os.path.isfile(nombreArchivo)

        datosRespaldar=(
            self.curso_idApi,
            self.topic_idApi,
            self.idCarpetaRetro,
            self.nombreCarpetaRetro,
            self.claseNbGrader_nombre
        )

        if seDebeRespaldar:
            with open(nombreArchivo,'w') as archivo:
                archivo.write(  '\n'.join( datosRespaldar )   )

        elif archivoDatosExiste:
            os.remove(nombreArchivo)




#############################################################################################################################
# RESTRICCIONES PARA PERMITIR EL ACCESO A CADA APARTADO DEL PROGRAMA CACPY
#############################################################################################################################

    def datosListosApartadoTareas(self):
        '''
        Comprobara  si se cuentan con los datos necesarios para poder abrir el apartado
        de: 'Mis tareas'

        Returns:
            True: Si se comprueba que SI SE cuentan con los datos necesarios para poder abrir
            el apartado de: 'Mis tareas'
            False: Si se comprueba que NO SE cuentan con los datos necesarios para poder abrir
            el apartado de: 'Mis tareas'
        '''



        datosListos= self.curso_idApi != None and self.topic_idApi != None and \
                     self.claseNbGrader_nombre!=None and self.nombreCarpetaRetro!=None \
                     and self.idCarpetaRetro!=None

        if datosListos:
            return True
        else:
            return False


    def datosListosApartadoAlumnos(self):
        '''
        Comprobara  si se cuentan con los datos necesarios para poder abrir el apartado
        de: 'Mis alumnos'

        Returns:
            True: Si se comprueba que SI SE cuentan con los datos necesarios para poder abrir
            el apartado de: 'Mis alumnos'
            False: Si se comprueba que NO SE cuentan con los datos necesarios para poder abrir
            el apartado de: 'Mis alumnos'

        '''

        datosListos= self.curso_idApi != None and self.nombreCarpetaRetro!=None \
                     and self.idCarpetaRetro!=None

        if datosListos:
            return True
        else:
            return False









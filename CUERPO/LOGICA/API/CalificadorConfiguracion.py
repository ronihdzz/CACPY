import os
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
            - curso_api_id (str): Representa el id del curso de classroom en donde se encuentran las
              tareas de programacion que se desena calificar
            - topic_nombre (str): Representa el nobre del topic en donde se encuentran las tareas de
              programacion que se desean calificar
            - topic-
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


    def cargarDatosProfesorSinArchivo(self,nombre,correo):
        self.nombre_profesor=nombre
        self.correo_profesor=correo

    #############################################################################################################################
    # SETTERS  Y    GETTERS
    #############################################################################################################################

    def set_clase_nombreNbGrader(self,nuevoValor):
        self.claseNbGrader_nombre=nuevoValor


    def setDatosCarpetaRetroalimentacion(self,nombre,idApi):
        self.nombreCarpetaRetro=nombre
        self.idCarpetaRetro=idApi

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



    def get_id_nombre_cursoClassroom(self):
        return self.curso_idApi, self.curso_nombre

    def get_id_nombre_topicClassroom(self):
        return self.topic_idApi, self.topic_nombre

    def get_nombre_cursoNbGrader(self):
        return self.claseNbGrader_nombre

    def set_nombre_cursoNbGrader(self,nombre):
        self.claseNbGrader_nombre=nombre





    def reiniciarValores(self):
        self.curso_nombre = None
        self.curso_idApi = None
        self.topic_nombre = None
        self.topic_idApi=None
        self.claseNbGrader_nombre=None

    def cargarDatosClaseClassroom_seleccionada(self, clase_idApi, clase_nombre):
        '''
        Lo que hara es reiniciar todos los valores a valores None, ya que se
        cambio de clase de classroom, posteriormente lo que hara es guardar:
            - El 'idApi' de la clase de classroom seleccionada
            - El 'nombre' de la clase seleccionada

        El efecto secundario que tendra esto es que al ser:
            - self.claseNbGrader_nombre=None
            - self.topic_idApi=None

        el metodo 'datosListosApartadoTareas()' retornara False, ya que este
        metodo solo retornara True cuando se tenga valor definido para cada atributo
        de instancia.

        Parametros:
            - clase_idApi (str) : Representa el id de clase de classroom seleccionada
            - clase_nombre (str): Representa el nombre de la clase de classroom seleccionada
        '''


        self.reiniciarValores()
        self.curso_idApi = clase_idApi
        self.curso_nombre=clase_nombre

    def cargarDatosTopic(self,programaTopic_id,programaTopic_nombre):
        self.topic_idApi=programaTopic_id
        self.topic_nombre=programaTopic_nombre


    def datosListosApartadoTareas(self):


        datosListos= self.curso_idApi != None and self.topic_idApi != None and \
                     self.claseNbGrader_nombre!=None and self.nombreCarpetaRetro!=None \
                     and self.idCarpetaRetro!=None

        if datosListos:
            return True
        else:
            return False


    def cargarDatosUltimaSesion(self,archivoDatos):
        '''
        Cargara los datos del archivo que contiene las ultimas configuraciones
        realizadas la ultimas vez que fue usado el programa
        '''

        # Leyendo los datos del ultimo curso y topic que el profesor selecciono
        if os.path.isfile(archivoDatos):
            # El archivo que se abrira contiene los datos: curso_id, topic_id
            # cada dato lo tiene separado por un salto de linea
            with open(recursos.App_Principal.ARCHIVO_TRABAJO_PROFESOR) as archivo:
                datos = archivo.read()
            curso_idApi,topic_idApi,idCarpetaRetro,nombreCarpetaRetro,claseNbGrader_nombre = datos.split('\n')

            self.curso_idApi=curso_idApi
            self.topic_idApi=topic_idApi
            self.idCarpetaRetro=idCarpetaRetro
            self.nombreCarpetaRetro=nombreCarpetaRetro
            self.claseNbGrader_nombre=claseNbGrader_nombre


    def cargarDatosProfesor(self,archivoDatos):
        '''
        Cargara los datos del profesor que ha iniciado sesion en el programa
        y no la a cerrado
        '''

        # Leyendo los datos guardados del profesor
        if os.path.isfile(archivoDatos):
            # El archivo que se abrira contiene los datos: correo del profesor, nombre completo del profesor
            # cada dato lo tiene separado por un salto de linea
            with open(recursos.App_Principal.ARCHIVO_DATOS_PROFESOR) as archivo:
                datos = archivo.read()
            self.correo_profesor, self.nombre_profesor = datos.split('\n')




    def respaldarDatosProfesor(self,nombreArchivo):

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


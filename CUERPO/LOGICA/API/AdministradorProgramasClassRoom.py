'''
AdministradorPorgramasClassRoom.py :
        Contiene una sola  clase, la clase 'AdministradorProgramasClassroom',
        la cual a grosso modo sirve para:
            - Poder calificar todas  las entregas realizadas por los estudiantes.
            - Obtener datos del topic y clase de classroom seleccionados en el apartado
            de configuraciones
            - Obtener datos de las tareas(courseworks) pertenecientes al topic y clase
            de google classroom seleccionados en el apartado de configuraciones
'''

from __future__ import print_function

__author__ = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"

# librerias estandar
import datetime


# Paquetes de terceros
#from __future__ import print_function
from nbgrader.apps import NbGraderAPI
from traitlets.config import Config

# fuente local
import recursos



##########################################################################################################################################
#  IMPORTANCION LOGICA
###########################################################################################################################################

from CUERPO.LOGICA.API.HiloCalificadorTarea import HiloCalificadorTarea

class AdministradorProgramasClassRoom:
    '''
    Agrupa todos los datos y realiza todas las instancias necesarias con el objetivo
    de poder calificar todas las entregas realizadas por los estudiantes con el simple
    hecho de solo llamar a un metodo de esta clase, es decir esta clase esta pensada
    para hacer mas limpia visualmente el proceso de calificacion de entregas de los
    estudiantes.

    Entonces recapitulando, esta clase sirve :
            - Poder calificar todas  las entregas realizadas por los estudiantes.
            - Obtener datos del topic y clase de classroom seleccionados en el apartado
            de configuraciones
            - Obtener datos de las tareas(courseworks) pertenecientes al topic y clase
            de google classroom seleccionados en el apartado de configuraciones
    '''


    def __init__(self,classroom_control,baseDatosLocalClassRoom,configuracionCalificador):
        '''
        Parámetros:
        baseDatosLocalClassRoom (objeto de la clase: BaseDatos_ClassRoomProgramas): dicho
        objeto permitira acceder a la base de datos local, la cual almacena los datos de
        los 'CourseWork' asi como los 'Topics' y 'Clases' del ClassRoom del profesor que ha
        iniciado sesión

        classRoomControl (objeto de la clase: ClassRoomControl): dicho objeto es una capa
        de abstracción para poder hacer algunas peticiones al ClassRoom del profesor, asi
        como al GoogleDrive del profesor

        configuracionCalificador (objeto de la clase: CalificadorConfiguracion): dicho objeto
        contiene ordenados los datos de configuracion que necesitara el programa, asi como tambien
        contiene metodos que serviran para obtener o editar dichos datos
        '''

        self.classroom_control=classroom_control
        self.configuracionCalificador=configuracionCalificador
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.nbGrader_control=None


        self.hiloCalificadorTarea=HiloCalificadorTarea(
            configuracionCalificador=self.configuracionCalificador,
            nbGrader_control=self.nbGrader_control,
            classroom_control=self.classroom_control
        )


    def agregarCourseWorks_baseDatosLocal(self,tuplaDatos):
        '''
        Agregara a la base de datos local los datos de las tareas(courseworks) que
        se encuentran en el parametro: 'tuplaDatos'.Cabe aclarar que dichas tareas
        que se agreguen en la base de datos local seran agregadas como tareas que
        pertenecen a la clase de classroom y topic de classroom que fueron seleccionados
        en el apartado: 'Mis configuraciones'

        Parámetros:
            tuplaDatos (tuple): Tupla que almacena los datos de las tareas que seran
            agregadas a la base de datos local.La tupla de datos tiene agrupados los
            datos de las tareas(courseworks) de la siguiente forma:
            (
                   (id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1),
                   (id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2) ,
                   ....
            )
        '''

        self.baseDatosLocalClassRoom.agregar_soloNuevosCourseWorks(
            tuplaDatos=tuplaDatos,
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi
        )

    def eliminarCourseWork_baseDatosLocal(self,courseWork_id):
        '''
        Eliminar de la base de datos local los datos de la tarea(coursework) cuyo
        id corresponde al valor del parámetro: 'courseWork_id'.Es importante  aclarar
        la tarea que se eliminar corresponde a una tarea que se encuentra en la clase
        de classroom y topic de classroom que fueron seleccionados en el apartado:
        'Mis configuraciones'

        Parámetros:
            courseWork_id (str): Representa el ID de la tarea que se desea eliminar
            de la base de datos local
        '''

        self.baseDatosLocalClassRoom.eliminarCourseWork(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi,
            coursework_id=courseWork_id
        )

    def calificarEstudiantes(self, courseWork_id, courseWork_name, noMaxEstudiantesCalificar=5):
        '''
        Calificara las entregas de los estudiantes de la tarea cuyo ID y NOMBRE es  igual a los valores
        de los parametros 'courseWork_id' y 'courseWork_name'.Es importante mencionar que solo calificara
        un determinado numero de entregas y dicho determinado numero correspondera al valor que tome el
        parámetro: 'noMaxEstudiantesCalificar'.

        Es importante mencionar lo siguiente:
            - La calificacion la efectuara a traves de un hilo, con el objetivo de
            que no se congele la GUI.

            - Por cada alumno cuya tarea vaya siendo  calificada se le compartira la retroalimentación
            de su tarea y la calificación respectiva, todo esto a través de Google classroom, por ende le
            llegaran las respectivas noficaciones a su correo cuando esto suceda. Cuando un alumno que fue
            calificado abra su google classroom en la tarea que fue calificada vera:

                Su calificación respectiva.
                Un link adjunto que lo dirigira a una carpeta de google drive:
                    * Dicha carpeta de google drive unicamente almacenara las retroalimentaciones de ese
                    alumno y esa tarea en particular(las retroalimentaciones son archivos html),
                    sin embargo esta carpeta podra contener mas de una retroalimentacion, ya que el alumno
                    puede entregar la tarea mas de una vez.
                    * Dicha carpeta de google drive se encuentra almacenada en la carpeta de google drive
                    que el usuario eligio en el apartado de: 'Mis configuraciones' y se encuentra almacenada
                    en la ruta: 'nombreClaseClassroom/idDelAlumno/nombreTarea/'
                    * Dicha carpeta de google drive unicamente se comparte en modo de vista con el alumno que
                    realizo la entrega de la tarea, es decir unicamente podra acceder a ella en modo de vista
                    el alumno que realizo la entrega de la tarea.

        Parámetros:
            - courseWork_id (str): Representa el ID de la tarea cuyas entregas realizadas por los alumnos desean
             ser calificadas
            - courseWork_name (str): Representa el nombre de la tarea cuyas entregas realizadas por los alumnos desean
             ser calificadas
            -  noMaxEstudiantesCalificar (int): Representa el numero de entregas que desean ser calificadas.
        '''

        # alistando al hilo para calificar entregas de tareas
        self.hiloCalificadorTarea.activarHiloParaCalificar()

        # cargando los datos de la tarea uyas entregas realizadas por los alumnos desean
        # ser calificadas
        self.hiloCalificadorTarea.setDatosTareaCalificar(
            nuevoCourseWork_id=courseWork_id,
            nuevoCourseWork_name=courseWork_name
        )

        # pasandole el objeto de nbgrader con el cual el hilo podra calificar las
        # entregas de la tarea
        self.hiloCalificadorTarea.nbGrader_control = self.nbGrader_control

        # avisando al hilo cual sera el numero maximo de entregas  entregas realizadas por los alumnos
        # que podra calificar.
        self.hiloCalificadorTarea.setNoMaxEstudiantesCalificar(nuevoValor=noMaxEstudiantesCalificar)

        # comenzando a calificar tareas
        self.hiloCalificadorTarea.start()

    def actualizar_nbGraderControl(self):
        '''
        Cuando el usuario selecciona una clase de NbGrader distinta a la ya seleccionada
        debera ser llamado este metodo, ya que lo que hace este metodo es renovar el objeto
        de NbGrader que califica las  entregas de las tareas, es decir crea un nuevo objeto
        'NbGraderAPI' pero ahora con la RUTA  de la respectiva de la clase de NbGrader que
        fue seleccionada.
        '''

        nombreNuevaClase = self.configuracionCalificador.claseNbGrader_nombre

        config = Config()
        config.CourseDirectory.course_id = nombreNuevaClase
        config.CourseDirectory.root = recursos.App_Principal.RUTA_NB_GRADER + nombreNuevaClase + '/'
        self.nbGrader_control = NbGraderAPI(config=config)


    def existeEsaTarea_cursoNbGrader(self, nombreTarea):
        '''
        Revisara si la clase de NbGrader seleccionada por el usuario en el apartado de
        'Mis configuraciones' tiene una tarea con el nombre del valor que almacena el
        parametro: 'nombreTarea'

        Parámetros:
            - nombreTarea (str): Nombre de la tarea de NbGrader que desea comprobarse su
            existencia en la clase de NbGrader que fue seleccionada por el usuario en el
            apartado 'Mis configuraciones'

        Returns:
            Dato de tipo bool:
                - True: si la clase de NbGrader seleCcionada por el usuario en el apartado de
                'Mis configuraciones', SI TIENE una tarea con el nombre del valor que almacena el
                parametro: 'nombreTarea'
                - False: si la clase de NbGrader seleCcionada por el usuario en el apartado de
                'Mis configuraciones', NO TIENE NINGUNA tarea con el nombre del valor que almacena
                el parametro: 'nombreTarea'
        '''

        if self.nbGrader_control != None:
            tareasExistentes = self.nbGrader_control.get_source_assignments()
            if nombreTarea in tareasExistentes:
                return True
            else:
                return False

    def registrarCourseworkComoCalificable_baseDatosLocal(self, idCourseWork):
        '''
        Registrara en la base de datos local que la tarea(coursework):cuyo ID es igual al
        valor del parametro: 'idCourseWork' y que se encuentra en la clase de classroom y
        topic de classroom que fueron seleccionados en el apartado de mis configuraciones,
        FUE SELECCIONADA POR EL USUARIO COMO UNA TAREA CALIFICABLE, es decir que el usuario
        la agrego a la tabla de tareas calificables por que es una tarea de la cual quiere
        calificar las entregas que realicen los estudiantes de dicha respectiva tarea.

        Parámetros:
            idCourseWork (str): Representa el ID del coursework que fue seleccionado por el usuario
            como coursework calificable y que dicha configuracion sera guardada en la base de datos
            local.
        '''

        self.baseDatosLocalClassRoom.registrarCourseworkComoCalificable(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi,
            idCourseWorkElegido=idCourseWork
        )

    def crearTarea(self,titulo,descripccion,colab_id):
        '''
        Creara una tarea en la clase de  classroom y topic de classroom seleccionados en
        el apartado de: 'Mi configuraciones', pero dicha tarea la creara como borrador,
        es decir no la podran ver los alumnos del usuario, unicamente la podra ver el usuario.

        La tarea la crea con los datos de los parametros de este metodo: 'titulo', 'descripccion',
        'colab_id'

        Parámetros:
            titulo (str): Nombre de la tarea que se creara
            descripccion (str): Instrucciones de la tarea que se creara
            colab_id (str): ID que le asigna google drive al archivo de tarea que deberan
            resolver los alumnos.

        Returns:
            idTarea (str): ID que le asigno google classroom a la tarea que se crea este metodo
            fechaCreacion (str): Fecha en la que se registro la creación de dicha tarea.
        '''

        idTarea= self.classroom_control.create_asignacionPrograma(
                    course_id=self.configuracionCalificador.curso_idApi,
                    topic_programas_id=self.configuracionCalificador.topic_idApi,
                    colab_id=colab_id,
                    titulo=titulo,
                    description=descripccion
        )

        # formato de cadena ISO8601:  YYYY-MM-DD HH:MM:SS.SSS para compatibilidad con sqlite3
        fechaCreacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # agregando los datos de la tarea creada a la base de datos local
        #self.agregarCourseWorks_baseDatosLocal(
        #    tuplaDatos=(  (idTarea,titulo,descripccion,fechaCreacion),   )
        #)

        # registrar como ya agregada
        #self.seleccionarBaseLocal_coursework(idCourseWork=idTarea)

        return idTarea,fechaCreacion

#############################################################################################################################################
#      getters
#############################################################################################################################################

    def get_tuplaTareasDejadas(self):
        '''
        Retornara una lista de los datos de todas las tarea que han sido dejadas en la
        clase de classroom y topic de classroom que fueron seleccionados en el apartado
        de: 'Mis configuraciones'.

        Returns:
            dato de tipo 'list': La lista que retornara dicho metodo, tendra el siguiente
            formato:
                [  [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
                   [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
                   [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
                                                    .
                                                    .
                                                    .
                ]
        '''

        # obteniendo de la base de atos local la lista de las tareas que pertenecen a la clase
        # de classroom y topic de classroom seleccionados en el apartado: 'Mis configuraciones'.
        # La lista obtenida seguira el siguiente formato:
        #                 [
        #                    [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
        #                    [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
        #                    [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
        #                                                     .
        #                                                     .
        #                                                     .
        #                 ]
        listaTareas=self.classroom_control.get_listaTareasTopic(
            self.configuracionCalificador.curso_idApi,
            self.configuracionCalificador.topic_idApi
        )
        return listaTareas


    def get_datosCurso(self):
        '''
        Returns:
            dato de tipo: 'tuple': Retornara una tupla de dos elementos.
                - el primer elemento (str): Representara el ID de la clase de classroom
                que fue seleccionada por el usuario en el apartado de: 'Mis configuraciones'
                - el segundo elemento (str): Representara el NOMBRE de la clase de classroom
                que fue seleccionada por el usuario en el apartado de: 'Mis configuraciones'
        '''

        return (self.configuracionCalificador.curso_idApi, self.configuracionCalificador.curso_nombre)

    def get_datosTopic(self):
        '''
        Returns
            dato de tipo: 'tuple': Retornara una tupla de dos elementos.
                - el primer elemento (str): Representara el ID del topic de classroom
                que fue seleccionado por el usuario en el apartado de: 'Mis configuraciones'
                - el segundo elemento (str): Representara el NOMBRE del topic de classroom
                que fue seleccionado por el usuario en el apartado de: 'Mis configuraciones'
        '''
        return (self.configuracionCalificador.topic_idApi, self.configuracionCalificador.topic_nombre)

    def get_courseWorksLibres_baseDatosLocal(self):
        '''
        Returns:
            dato de tipo: 'tuple': Retornara una tupla que contendra los datos
            de todas las tareas que cumplan con lo siguiente:
                - Se encuentran registradas en la clase de classroom y topic de classroom
                que fueron seleccionados en el apartado de: 'Mis configuraciones'
                - Son tareas que aun NO HAN sido registradas por el usuario como tareas
                calficables.

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

        # obteniendo de la base de atos local la tupla de datos de las tareas que pertenecen a la clase
        # de classroom y topic de classroom seleccionados en el apartado: 'Mis configuraciones'
        # y que no han sido registradas como tareas calificables.
        # La tupla obtenida seguira el siguiente formato:
        #                 [
        #                    [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
        #                    [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
        #                    [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
        #                                                     .
        #                                                     .
        #                                                     .
        #                 ]
        tuplaDatosCourseWorks=self.baseDatosLocalClassRoom.get_courseWorksLibres(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi
        )
        return tuplaDatosCourseWorks


    def get_courseWorksCalificables_baseDatosLocal(self):
        '''
        Returns:
            dato de tipo: 'tuple': Retornara una tupla que contendra los datos
            de todas las tareas que cumplan con lo siguiente:
                - Se encuentran registradas en la clase de classroom y topic de classroom
                que fueron seleccionados en el apartado de: 'Mis configuraciones'
                - Son tareas que ACTUALMENTE ESTAN registradas por el usuario como tareas
                calficables, es decir que pertenecen a la tabla de tareas calificables

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

        # obteniendo de la base de atos local la tupla de datos de las tareas que pertenecen a la clase
        # de classroom y topic de classroom seleccionados en el apartado: 'Mis configuraciones'
        # y que estan registradas como tareas calificables.
        # La tupla obtenida seguira el siguiente formato:
        #                 [
        #                    [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
        #                    [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
        #                    [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
        #                                                     .
        #                                                     .
        #                                                     .
        #                 ]
        tuplaDatosCourseWorks=self.baseDatosLocalClassRoom.get_courseWorksAgregados(
            curso_id=self.configuracionCalificador.curso_idApi,
            topic_id=self.configuracionCalificador.topic_idApi
        )
        return tuplaDatosCourseWorks



    def get_informacionEntregasDeTareas(self, courseWork_id):
        '''

        Returns:
            dato de tipo 'dict': Este metodo retornara en un diccionario los datos
            de las entregas que han realizado los estudiantes de la tarea(coursework)
            cuyo ID es igual al valor que almacena el parametro: 'courseWork_id' y
            que se encuentra en la clase de classroom y topic de classroom seleccionados
            en el apartado de: 'Mis configuraciones'

            El formato del diccionario sera el siguiente:

            {
                ID_estudiante_1 :  [ attachments_estudiante_1, ID_deLaEntrega_estudiante_1  ],
                ID_estudiante_2 :  [ attachments_estudiante_2, ID_deLaEntrega_estudiante_2  ],
                ID_estudiante_3 :  [ attachments_estudiante_3, ID_deLaEntrega_estudiante_3  ],
                                                    .
                                                    .
                                                    .
            }

            ¿Que son los  attachments ? Representan a los materiales que adjunto el estudiante
            a google classroom en el apartado de la tarea.
        '''


        # obteniendo de la API de google classroom el diccionario que contiene los datos  de las
        # entregas que han realizado los estudiantes de la tarea(coursework), el diccionario
        # retornado seguira el siguiente formato
        #             {
        #                 ID_estudiante_1 :  [ attachments_estudiante_1, ID_deLaEntrega_estudiante_1  ],
        #                 ID_estudiante_2 :  [ attachments_estudiante_2, ID_deLaEntrega_estudiante_2  ],
        #                 ID_estudiante_3 :  [ attachments_estudiante_3, ID_deLaEntrega_estudiante_3  ],
        #                                                     .
        #                                                     .
        #                                                     .
        #             }
        datosEntragas=self.classroom_control.getEntregasDeEstudiantes(
            course_id=self.configuracionCalificador.curso_idApi,
            coursework_id=courseWork_id
        )

        return datosEntragas

    def getDatosCourseWork(self, courseWork_id):
        '''

        Este metodo obtendra de:  la tarea(coursework) cuyo ID es igual al valor que almacena el parametro:
        'courseWork_id' y que se encuentra en la clase de classroom y topic de classroom seleccionados
        en el apartado de: 'Mis configuraciones' LO SIGUIENTE:
            - Cuantas entregas de dicha tarea ya han sido calificadas
            - Cuantas entregas de dicha tarea han sido entregadas pero NO calificadas
            - Cuantas entregas de dicha tarea faltan por entregar

        Una vez obtenidos esos datos los retorna contenidos en un diccionario

        Returns:
            - Dato de tipo: 'dict': Diccionario que contiene informacion acerca de las entregas que han realizado
            los alumnos de la tarea que selecciono el usuario.Dicho diccionario contiene las siguientes llaves:
                * 'porCalificar' : El value de esta llave sera el numero de alumnos que ya entrego la tarea, pero
                aun no han sido calificados
                * 'calificadas' : El value de esta llave sera el numero de alumnos que ya fueron calificados en
                la tarea que entregaron
                * 'porEntregar': El value de esta llave representa el numero de alumnos que aun no realizan la
                entrega de la tarea que el usuario selecciono
        '''

        # obteniendo el diccionario que contiene las siguientes llaves:
        #      * 'porCalificar' : El value de esta llave sera el numero de alumnos que ya entrego la tarea, pero
        #      aun no han sido calificados
        #      * 'calificadas' : El value de esta llave sera el numero de alumnos que ya fueron calificados en
        #      la tarea que entregaron
        #      * 'porEntregar': El value de esta llave representa el numero de alumnos que aun no realizan la
        #      entrega de la tarea que el usuario selecciono
        dictDatosEntrega= self.classroom_control.get_datosEntregas(
            course_id=self.configuracionCalificador.curso_idApi,
            coursework_id=courseWork_id
        )

        return dictDatosEntrega


    def get_LinkAccesoClaseClassroom(self):
        '''
        Este metodo generar el link que permite acceder con el navegador web
        a la clase de classroom seleccionada, despues de generar dicho link
        lo retorna

        Returns:
             Dato de tipo 'str' : Representa el link que permite acceder con
             un navegador web a la clase de classroom seleccionada
        '''


        idCurso = self.configuracionCalificador.getIdApi_cursoClassroom()

        if idCurso!=None:
            datosClaseClassroom = self.classroom_control.service_classroom.courses().get(
                id=idCurso
            ).execute()

            if datosClaseClassroom != None:
                linkAcceso = datosClaseClassroom.get("alternateLink")
                return linkAcceso
        return None

    def getErrorEn_idDelColabQueSeDiceSerQueEsUnIdDeUnArchivoValidoDeTarea(self, idDelColab):
        '''
        Revisa si  el ID que representa el valor que tome el parámetro 'idDelColab' corresponde al
        ID de  un archivo que se encuentre en el google drive del usuario y sea de tipo jupyter o colab
        ya que  esos son los formatos de los archivos con los que  el usuario debera asignar las tareas
        de programación a sus alumnos.

        Para validar lo anteriormente mencionado el archivo que correponda ID que representa el valor que
        tome el  parámetro 'idDelColab' DEBEBERA CORRESPONDER A UN ARCHIVO DEL GOOGLE DRIVE DEL USUARIO y
        debera cumplir solo  alguna de las siguientes validaciones:
            * ¿el archivo es de tipo: 'application/json' ?
            * ¿el archivo es de tipo: 'application/vnd.google.colaboratory'?
            * ¿el archivo tiene una terminación: '.ipynb'

        Si se cumple con lo anteriormente mencionado, el metodo retornara 'None', en caso contrario retornara
        un dato de tipo 'str' el cual contendra el error detectado que presento el archivo que representa el
        ID.

        Parámetros:
            - idDelColab (str): Representa el ID del archivo que se quiere comprobar si es un archivo
            valido para ser asignado como tarea de programación y si dicho archivo existe en el google
            drive del usuario.

        Returns
            Dato 'None' : Si no existio ningun error no hay ningun error que retornar
            Dato de tipo 'str'  : Si existio un error se retorna el error presentado
        '''

        if idDelColab != "":
            try:
                # obteniendo el archivo de google drive al que le corresponde
                # el ID que ingreso el usuario
                response = self.classroom_control.service_drive.files().get(
                    fileId=idDelColab,
                    fields='name,mimeType'
                ).execute()

                mimeType = response.get('mimeType')
                nombreArchivo = response.get('name')
                if type(nombreArchivo) != str:
                    nombreArchivo = ""

                # ¿el ID ingresado  NO es el ID de un colab?
                if mimeType != 'application/vnd.google.colaboratory' and mimeType != 'application/json' and nombreArchivo.endswith(
                        ".ipynb") != True:
                    mensajeDeError = f"El ID que ingresaste corresponde a un archivo cuyo nombre es: <<{nombreArchivo}>> y cuyo tipo es:" \
                                     f"<<{mimeType}>>, sin embargo, DICHO ARCHIVO NO CORRESPONDE A UN ARCHIVO VALIDO, ya que no paso las pruebas " \
                                     f"que validan que es un archivo de un google colab o un jupyter notebook pues su tipo no coincide con: " \
                                     f"<<application/vnd.google.colaboratory>> y ni tampoco con: <<application/json>> y ni siquiera el archivo " \
                                     f"tiene la terminacion: <<.ipynb>>"
                    return mensajeDeError

                # significa que el archivo que correspone al ID cumplio por lo menos con alguna restriccion que se valida en el
                # anterior condicional
                else:
                    return None

            except Exception as e:
                return str(e)

        else:
            mensajeDeError = "no se ingreso ningun ID en el colab de la tarea"

            return mensajeDeError

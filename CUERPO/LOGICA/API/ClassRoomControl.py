'''
ClassRoomControl.py :
        Contiene una sola  clase, la clase 'ClassRoomControl',la cual a grosso modo sirve
        para hacer todas las consultas a la API de google classroom con el objetivo de
        obtener datos de las clases de classroom, de los courseworks, de los topics,etc.
'''

from __future__ import print_function

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"



# librerias estandar
import os.path
import shutil
import os

# Paquetes de terceros
#from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import rfc3339
import iso8601

# fuente local
import recursos




def get_date_object(date_string):
  return iso8601.parse_date(date_string)

def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)



class ClassRoomControl:
    '''
    Sirve para hacer todas las consultas a la API de google classroom con el objetivo de
    obtener datos de las clases de classroom, de los courseworks, de los topics,etc.


    '''

    # Permisos que se le solicitaran al usuario para poder generar el token respectivo
    # https://console.cloud.google.com/apis/credentials
    SCOPES = [

        'https://www.googleapis.com/auth/classroom.topics',

        # Ver cursos de Classroom
        'https://www.googleapis.com/auth/classroom.courses.readonly',

        # Ver listas de clases, agregar e invitar personas a clases,
        # eliminar personas de las clases
        'https://www.googleapis.com/auth/classroom.rosters',

        # Ver y modificar tareas y preguntas, y el trabajo y las
        # calificaciones del usuario actual.
        'https://www.googleapis.com/auth/classroom.coursework.me',

        # Ver y modificar asignaciones y preguntas y el trabajo y
        # calificaciones de los cursos que enseña el usuario actual
        # y ver lo mismo para los cursos que administra el usuario actual.
        'https://www.googleapis.com/auth/classroom.coursework.students',

        # Ver y modificar anuncios para el usuario actual.
        'https://www.googleapis.com/auth/classroom.announcements',

        # Ver y administrar los tutores de los alumnos en sus clases de
        # Google Classroom.
        'https://www.googleapis.com/auth/classroom.guardianlinks.students',

        # Ver fotos de perfil de usuario visibles para el usuario autenticado
        'https://www.googleapis.com/auth/classroom.profile.photos',

        # Ver las direcciones de correo electrónico de los usuarios visibles para el usuario autenticado
        'https://www.googleapis.com/auth/classroom.profile.emails',

        # DRIVE
        'https://www.googleapis.com/auth/drive.activity.readonly',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self):
        self.service_classroom=None
        self.service_drive=None


    def cargarArchivoCredenciales(self,nombreArchivo):
        '''
        CACPY necesita  de un archivo de credenciales para poder pedir los permisos al usuario y posteriormente
        generar el token el cual permitira a CACPY interactuar con el google drive y google classroom del usuario.

        CACPY guardara en una ruta en especifica al: ARCHIVO DE CREDENCIALES, ya que este  se usa cuando un usuario
        inicia sesión con CACPY.Lo que hace este metodo es generar una copia del archivo: 'nombreArchivo' y despues
        almacenar dicha copia en la ruta respectiva en donde CACPY guarda al archivo de credenciales, sin embargo si
        ya existia registrado un archivo de credenciales en esa ruta, entonces CACPY eliminara el archivo que ya existia,
        ya que en dicha ruta solo puede existir un  archivo de credenciales.

        Parametros:
            nombreArchivo (str): Nombre del archivo de credenciales que CACPY copiara y almacenara en una ruta en donde
            solo guarda al archivo de credenciales
        '''

        archivo_crendencialesExite = os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)
        archivo_tokenExiste=os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)


        if archivo_tokenExiste:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)

        if archivo_crendencialesExite:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

        shutil.copyfile(nombreArchivo,recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)


    def eliminarArchivoCredenciales(self):
        '''
        Eliminara el archivo de credenciales que CACPY tiene almacenado en la ruta en
        donde guarda al archivo de credenciales.
        '''

        archivo_crendencialesExite = os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

        if archivo_crendencialesExite:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

    def eliminarArchivoToken(self):
        '''
        Eliminara el token que CACPY tiene almacenado en la ruta en donde guarda al token
        '''

        archivo_tokenExiste=os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)

        if archivo_tokenExiste:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)

    def obtenerValor_service_classroom_and_drive(self):
        """
        Obtendra los objetos que permitiran a CACPY hacer peticiones a la API de google classroom
        y a la API de google drive del usuario  y dichos objetos los almacenara en los
        atributos de instancia: 'self.service_classroom' y 'self.service_drive'

        Cabe mencionar que para hacer lo anterior, este metodo buscara primero si existe el token
        y si aun es valido en caso de ser asi, entonces procedera a crear los objetos antes mencionados,
        sin embargo si se detecta que el token no es valido o no existe entonces se le pediran los permisos
        al usuario para generarlo y despues se obtendran los objetos antes mencionados.
        """

        SCOPES=self.SCOPES
        creds = None

        # ¿existe ya el token?
        if os.path.exists(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN):
            creds = Credentials.from_authorized_user_file(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN, SCOPES)

        # ¿el token no existe o el token no es valido?
        if not creds or not creds.valid:
            # ¿ el token si existe pero ya expiro?
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            # el token no existe por lo se le pediran los permisos respectivos al usuario con ayuda del archivo
            # de credenciales que se cuenta,lo anterior se realiza con el objetivo de generar el token
            else:
                flow = InstalledAppFlow.from_client_secrets_file(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES,SCOPES)
                creds = flow.run_local_server(port=0)

            # guardando el token generado en la ruta respectiva
            with open(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN, 'w') as token:
                token.write(creds.to_json())

        # obteniendo los objetos que permitiran a CACPY interactuar con la API de google classroom y google drive
        self.service_classroom = build('classroom', 'v1', credentials=creds)
        self.service_drive = build('drive', 'v3', credentials=creds)


    def get_listaDatosCursos(self):
        """
        Hara la consulta respectiva  a la API de google classroom del usuario con el objetivo
        de obtener los datos de las clases de classroom que el usuario tiene, posteriormente
        dichos datos los retonara

        Returns:
            dato de tipo 'list' el cual contendra los datos de las clases de google classroom
            que el usuario tiene registradas, la forma de la lista que se retornara sera
            el siguiente:
             (
                    (id_api_1,nombre_1),
                    (id_api_2,nombre_2),
                    (id_api_3,nombre_3),
                             .
                             .
                             .
            )
        """

        listaDatosClasesClassroom_retornoAPI= []
        page_token = None

        while True:
            response = self.service_classroom.courses().list(pageToken=page_token,
                                              pageSize=100).execute()
            listaDatosClasesClassroom_retornoAPI.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        listaDatosClasesClassroom_queSeRetornaran=[]

        # ¿la API retorno almenos el dato de una clase de google classroom?
        if listaDatosClasesClassroom_retornoAPI:
            for curso in listaDatosClasesClassroom_retornoAPI:
                listaDatosClasesClassroom_queSeRetornaran.append( ( curso.get('id'), curso.get('name') )  )

        return listaDatosClasesClassroom_queSeRetornaran

    def get_listaDatosTopicsCurso(self,curso_id):
        """
        Hara la consulta respectiva  a la API de google classroom del usuario con el objetivo
        de obtener los datos de los topics de la clase de google classroom cuyo id es igual
        a: 'curso_id'  posteriormente dichos datos los retonara

        Returns:
            dato de tipo 'list' el cual contendra los datos de los topics de la clase  de google
            classroom cuyo id es igual  a: 'curso_id', la forma de la lista que se retornara sera
            el siguiente:
             (
                    (idApi_topic_1,nombre_topic_1),
                    (idApi_topic_2,nombre_topic_2),
                    (idApi_topic_3,nombre_topic_3),
                             .
                             .
                             .
            )
        """

        listaDatosTopics_retornoAPI=[]
        page_token = None

        while True:
            response = self.service_classroom.courses().topics().list(
                pageToken=page_token,
                courseId=curso_id,
                pageSize=10).execute()
            listaDatosTopics_retornoAPI.extend(response.get('topic', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        listaDatosTopics_queSeRetornaran = []

        # ¿la API retorno almenos los datos de un topic de google classroom?
        if listaDatosTopics_retornoAPI:
            for topic in listaDatosTopics_retornoAPI:
                 listaDatosTopics_queSeRetornaran.append( [ topic.get('topicId'), topic.get('name') ] )

        return listaDatosTopics_queSeRetornaran



    def get_listaTareasTopic(self, curso_id,topic_id):
        """
        Hara la consulta respectiva  a la API de google classroom del usuario con el objetivo
        de obtener los datos de los Courseworks(tarea) de la clase de google classroom cuyo id es igual
        a: 'curso_id'  y que se encuentran almacenadas en el topic cuyo id es igual a: 'topic_id', una
        vez obtenidos dichos datos solo seleccionara algunos  de ellos de cada CourseWork(tarea) y
        los retornara

        Parámetros:
            curso_id (str) : Representa el ID de la clase de google classroom que tiene almacenadas las
            tareas cuyos datos se retornaran
            topic_id (str): Representa el ID del topic de google classroom que tiene almacenadas las tareas
            cuyos datos se retornaran

        Returns:
            Dato de tipo 'list' el cual contendra datos especificos de cada Tarea(CourseWork) que pertenezca
            a la clase de classroom con id igual a: 'curso_id' y topic con id igual a: 'topic_id', el formato
            en el que tendran almacenados los datos la lista sera el siguiente:

                [
                [id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1],
                [id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2],
                [id_tarea_3,nombre_tarea_3,descripccion_tarea_3,fechaCreacion_tarea_3],
                                                 .
                                                 .
                                                 .
                ]
        """

        listaDatosCourseWorks_retornoAPI = []
        page_token = None

        while True:
            response = self.service_classroom.courses().courseWork().list(
                pageToken=page_token,
                courseId=curso_id
            ).execute()
            listaDatosCourseWorks_retornoAPI.extend(response.get('courseWork', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        listaDatosCourseWorks_queSeRetornaran = []

        # ¿la API retorno almenos los datos de un CourseWork de google classroom?
        if listaDatosCourseWorks_retornoAPI:
            for datosTarea in listaDatosCourseWorks_retornoAPI:
                tarea_topic=datosTarea.get('topicId')

                # ¿los datos de la tarea corresponden al topic cuyo id es igual a: topic_id ?
                if topic_id==tarea_topic:

                    # fecha de creacion en formato iso8601
                    fechaCreacion = get_date_object(  datosTarea.get('creationTime')   )

                    # formato de cadena ISO8601:  YYYY-MM-DD HH:MM:SS.SSS para compatibilidad con sqlite3
                    fechaCreacion=fechaCreacion.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                    datos = [
                        datosTarea.get('id'),datosTarea.get('title'),datosTarea.get('description'), fechaCreacion
                    ]

                    listaDatosCourseWorks_queSeRetornaran.append(datos)

        return listaDatosCourseWorks_queSeRetornaran


    def get_datosProfesor(self,nombreCompletoFoto_guardar=None):
        """
        Hara la consulta respetiva a la API de google classroom del usuario con el objetivo de
        obtener los datos del profesor, y rescartara especificamente 3 datos esenciales:
            - nombre completo del profesor
            - correo electronico del profesor
            - url de la foto de perfil del profesor

        Si se asigna un valor al parametro 'direccionCopiaraFoto',este metodo descargara la foto
        del profesor atraves de la url de la foto obtenida, y la guardara con el nombre y direccion
        que tenga el parametro 'direccionCopiaraFoto'.Si no se le asigna valor alguno al parametro
        'direccionCopiaraFoto' entonces no se descargara la foto.

        Parámetros:
            nombreCompletoFoto_guardar: Nombre completo(que incluya la ruta tambien), de la foto
            del profesor

        Returns:
            Dato de tipo: 'tuple' que representa a una tupla de  2 elementos:
            - primer elemento (str) :Representa el nombre completo del profesor
            - segundo elemento (str): Representa el correo electronico del profesor
        """

        profesor_userProfile= self.service_classroom.userProfiles().get(userId="me").execute()
        profesor_nombre = profesor_userProfile.get("name").get('fullName')
        profesor_email=profesor_userProfile.get('emailAddress')

        if nombreCompletoFoto_guardar:
            if os.path.isfile(nombreCompletoFoto_guardar):
                os.remove(nombreCompletoFoto_guardar)

            profesor_photoUrl = profesor_userProfile.get("photoUrl")


            # un error en la API es que NO siempre incluye al inicio: 'https:', por tal motivo
            # si no se detecta que se incluyo se procede a incluirlo
            if not profesor_photoUrl.startswith('https:'):
                profesor_photoUrl='https:'+profesor_photoUrl


            r = requests.get(profesor_photoUrl)

            # guardando la foto del profesor
            with open(nombreCompletoFoto_guardar, 'wb') as f:
                f.write(r.content)

        return (profesor_email,profesor_nombre)


    def get_datosAlumno(self,idAlumno):
        """
        Hara la consulta respetiva a la API de google classroom del usuario con el objetivo de
        obtener los datos del alumno cuyo id es igual a: 'idAlumno', y rescartara especificamente
        3 datos esenciales:
            - nombre completo
            - correo electronico

        Parámetros:
            idAlumno (str): Representa el ID del alumno del cual se desea obtener sus datos

        Returns:
            Dato de tipo: 'tuple' que representa a una tupla de  2 elementos:
            - primer elemento (str) :Representa el nombre completo del alumno
            - segundo elemento (str): Representa el correo electronico del  alumno
        """

        estudiante_userProfile= self.service_classroom.userProfiles().get(userId=idAlumno).execute()
        estudiante_nombre = estudiante_userProfile.get("name").get('fullName')
        estudiante_email=estudiante_userProfile.get('emailAddress')

        return (estudiante_email,estudiante_nombre)


    def get_listaAlumnos(self, course_id):
        '''
        Hara la consulta respetiva a la API de google classroom del usuario con el objetivo de
        de obtener el nombre y correo electronico de cada alumno inscrito a su clase de google
        classroom cuyo id es igual a: 'course_id'

        Parámetros:
            course_id (str): Representa el ID de la clase de google classroom de la cual se quieren
            obtener los datos de sus alumnos

        Returns:
            Dato de tipo 'list' que contiene todos los nombres y correos electronicos de todos los alumnos
            inscritos a la clase de google classroom cuyo id es igual: 'course_id'.El el formato en el que
            tendran almacenados los datos la lista sera el siguiente:

                (   (idEstudiante_1,nombreCompleto_1,correoElectronico_1),
                    (idEstudiante_2,nombreCompleto_2,correoElectronico_2),
                                           .
                                           .
                                           .
                )
        '''

        listaDatosAlumnos_retornoAPI=[]
        listaDatosAlumnos_queSeRetornaran=[]

        page_token = None
        while True:
            response = self.service_classroom.courses().students().list(
                pageToken=page_token,
                courseId=course_id,
                pageSize=10).execute()
            listaDatosAlumnos_retornoAPI.extend(response.get('students', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break


        # ¿la API retorno almenos los datos de un Alumno
        if listaDatosAlumnos_retornoAPI:
            for datosAlumno_x in listaDatosAlumnos_retornoAPI:
                idEstudiante = datosAlumno_x.get('userId')
                nombreCompleto = datosAlumno_x.get('profile').get('name')['fullName']
                correoElectronico=datosAlumno_x.get('profile').get('emailAddress')

                listaDatosAlumnos_queSeRetornaran.append(
                    (idEstudiante, nombreCompleto, correoElectronico)
                )

        return listaDatosAlumnos_queSeRetornaran


    def create_asignacionPrograma(self, course_id,topic_programas_id,colab_id,titulo,description):
        '''
        Creara una tarea en la clase y topic de classroom cuyos IDs corresponden a: 'course_id' y
        'topics_programas_id', sin embargo dicha tarea la creara como borrador, es decir no la podran
        ver los alumnos del usuario, unicamente la podra ver el usuario.

        La tarea la crea con los datos de los parametros de este metodo: 'titulo', 'description',
        'colab_id'

        Parámetros:
            course_id (str): Representa el ID de la clase de classroom en donde se creara la tarea
            topic_programas_id (str ): Representa el ID del topic de classroom en donde se creara
            la tarea
            titulo (str): Nombre de la tarea que se creara
            descripccion (str): Instrucciones de la tarea que se creara
            colab_id (str): ID que le asigna google drive al archivo de tarea que deberan
            resolver los alumnos.

        Returns:
            idTarea (str): ID que le asigno google classroom a la tarea que se crea este metodo
        '''

        coursework = {
            'title': titulo,
            'description': description,
            'topicId':topic_programas_id,
            'workType': 'ASSIGNMENT',
            'state': 'DRAFT',  # 'PUBLISHED', 'DRAFT'
            'maxPoints':100, # puntos de esta tarea
            'materials': [
                {
                    'driveFile': {
                        'driveFile':{
                            'id':colab_id,
                            'title': titulo
                        },
                        'shareMode': 'STUDENT_COPY'
                    },
                }
                # {       }
                # {       }
            ]
        }

        coursework = self.service_classroom.courses().courseWork().create(
            courseId=course_id,
            body=coursework).execute()

        idCoursework=coursework.get('id')

        return idCoursework


##################################################################################################################################################################################################
#
##################################################################################################################################################################################################

    def get_datosEntregas(self, course_id, coursework_id):
        """

        Para entender la logica de operacion de este metodo, es importante recordar los estados
        de las tareas en google classroom:

            A) SUBMISSION_STATE_UNSPECIFIED	Ningún estado especificado. Esto nunca debe devolverse.
            B) NEW	El alumno nunca ha accedido a este envío. Los archivos adjuntos no se devuelven
                y las marcas de tiempo no se establecen.
            C) CREATED	Ha sido creado.
            D) TURNED_IN Ha sido entregado al maestro.
            E) RETURNED	Ha sido devuelto al alumno.
            F) RECLAIMED_BY_STUDENT	El estudiante eligió "anular la entrega" de la tarea.


        submissionHistory  ==> Contiene el historial de entrega de cada alumno, es importante
        recalcar que duando recien se le deja una tarea a un estudiante el historial se ve asi:

                [
                    {
                        'stateHistory':
                        {
                            'state': 'CREATED',
                            'stateTimestamp': '2021-08-29T17:46:54.744Z',
                            'actorUserId': '104545356553078923308'
                        }
                    },

                ]

        Cuando un alumno sube la tarea que se dejo el historial se ve asi:
                [
                    {
                        'stateHistory':
                        {
                            'state': 'CREATED',
                            'stateTimestamp': '2021-08-29T17:46:54.744Z',
                            'actorUserId': '104545356553078923308'
                        }
                    },

                    {
                     'stateHistory':
                         {'state': 'TURNED_IN',
                         'stateTimestamp': '2021-08-29T17:47:09.343Z',
                         'actorUserId': '114283316418743255552'
                         }
                    }
                ]

        Cuando la tarea de alumno se califica asi se ve su historial:

                [
                    {
                        'stateHistory':
                        {
                            'state': 'CREATED',
                            'stateTimestamp': '2021-08-29T17:46:54.744Z',
                            'actorUserId': '104545356553078923308'
                        }
                    },

                    {
                     'stateHistory':
                         {'state': 'TURNED_IN',
                         'stateTimestamp': '2021-08-29T17:47:09.343Z',
                         'actorUserId': '114283316418743255552'
                         }
                    },

                    {
                    'gradeHistory':
                        {
                            'maxPoints': 100,
                            'gradeTimestamp': '2021-08-29T18:12:45.271Z',
                            'actorUserId': '105070726429141696472',
                            'gradeChangeType': 'ASSIGNED_GRADE_POINTS_EARNED_CHANGE'
                        }
                    }
                ]

        Se puede apreciar claramente como en el historial se muestran todas las acciones hechas en una
        tarea de un estudiante, en forma de una lista.Mi programa por tal motivo para saber si debe
        o no debe calificar a una tarea checara el historial y vera cual fue la ultima accion, si la
        ultima accion del estudiante fue:  { 'stateHistory': {'state': 'TURNED_IN',.... } significara
        que dicha tarea quiere ser nuevamente calificada, sin embargo si la ultima accion fue:
        { 'gradeHistory': { 'maxPoints': 100,...} significa que el estudiante no ha repetido su entrega
        y por lo tanto no desea que se vuelva a repetir por que ya esta conforme con la calificacion
        asignada.


        Lo que hara este metodo es clasificar las entregas realizadas por los estudiantes de la tarea
        cuyo id es igual a: 'coursework_id' que pertenece a la clase de classroom cuyo id es igual a:
        'course_id' ¿como las clasificara? atraves de un diccionario llevara un conteo de a que categoria
        pertence cada entrega realizada por los estudiantes, las llaves del diccionario seran las siguientes:


            'porCalificar' : El value de esta llave sera el numero de alumnos que ya entrego la tarea, pero
                             aun no han sido calificados
            'calificadas' : El value de esta llave sera el numero de alumnos que ya fueron calificados en
                            la tarea que entregaron
            'porEntregar':   El value de esta llave representa el numero de alumnos que aun no realizan la
                            entrega de la tarea que el usuario selecciono

        Una vez obtenido dicho diccionario con los datos respectivos, este metodo procedera a retornar dicho diccionario

        Returns:
            Dato de tipo: 'dict' el cual representara el conteo que obtuvo de cada  categoria a la que
            pertenece cada entrega realizada por los estudiantes.
        """


        listaDatosEntregasDeLosAlumnos_retornoAPI=[]
        page_token = None

        while True:
            coursework = self.service_classroom.courses().courseWork()
            response = coursework.studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                states=['NEW','CREATED','RETURNED','TURNED_IN','RECLAIMED_BY_STUDENT'],
                courseWorkId=coursework_id,
                pageSize=10).execute()
            listaDatosEntregasDeLosAlumnos_retornoAPI.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break


        dictDatosEntrega = {
            'calificados': 0,  # RETURNED
            'porCalificar': 0,  # TURNED_IN
            'porEntregar': 0,
        }


        # ¿la API retorno almenos los datos de una entrega de un alumno?
        if listaDatosEntregasDeLosAlumnos_retornoAPI:

            for c,datosEntregaAlumno_x in enumerate(listaDatosEntregasDeLosAlumnos_retornoAPI):

                # si ".get('state')" retorna 'NEW' significa que el usuario ni siquiera ha abierto
                # la asignacion por lo tanto no existe un 'submissionHistory', por tal motivo este
                # condicional pregunta si  ".get('state')" es diferente de: 'NEW'
                if datosEntregaAlumno_x.get('state')!='NEW':

                    # ¿la ultima accion fue un 'gradeHistory' o  un 'stateHistory' ?
                    # si no es un 'stateHistory' la variable 'ultimaAccion' valdra None
                    ultimaAccion=datosEntregaAlumno_x.get('submissionHistory')[-1].get('stateHistory')

                    # si  la variable 'ultimaAccion' fue un 'gradeHistory'  significa que la ultima accion que se
                    # realizo con la tarea es que fue calificada por el profesor por lo tanto significa
                    # que ya fue retornada su calificacion o esta por retornarse por lo tanto el valor
                    # de la variable 'ultimoEstadoTarea' sera igual a 'RETURNED' y solo cambiara si y solo
                    # si  la variable 'ultimaAccion' fue un 'stateHistory'
                    ultimoEstadoTarea='RETURNED'

                    # ¿ la ultima accion fue un 'stateHistory' ?
                    if ultimaAccion!=None:

                        # como la ultima accion fue un 'stateHistory' significa que el estudiante pudo:
                        # hacer lo siguiente: 'TURNED_IN'  o 'RECLAIMED_BY_STUDENT' es decir significa que
                        # la ultima accion que se hizo con la tarea es que el estudian o la entrego o cancelo
                        # su entrega
                        ultimoEstadoTarea=ultimaAccion.get('state')

                # el estudiante ni si quiera ha abierto la tarea
                else:
                    ultimoEstadoTarea='NEW'

                if ultimoEstadoTarea=='RETURNED':
                    dictDatosEntrega['calificados']+=1
                elif ultimoEstadoTarea=='TURNED_IN':
                    dictDatosEntrega['porCalificar']+=1
                else:
                    dictDatosEntrega['porEntregar']+=1

        return dictDatosEntrega



    def getEntregasDeEstudiantes(self, course_id, coursework_id):
        """
        Returns:
            dato de tipo 'dict': Este metodo retornara en un diccionario los datos
            de las entregas que han realizado los estudiantes de la tarea(coursework)
            cuyo ID es igual al valor que almacena el parametro: 'courseWork_id' y
            que se encuentra en la clase de classroom cuyo ID es igual al valor que
            almacena el parametro: 'course_id'

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
            a google classroom en el apartado de la tarea.Como CACPY asigna tareas de programacion
            mediante google colabs, entonces se espera en el attachments el contenido del colab,
            por lo tanto para obtener el link de acceso a ese colab bastaria con hacer lo
            siguiente:

            url = tarea['attachments'][0]['driveFile']['alternateLink']

        """

        listaDatosEntregasDeLosAlumnos_retornoAPI = []
        page_token = None

        while True:
            response= self.service_classroom.courses().courseWork().studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                states=['TURNED_IN'],
                courseWorkId=coursework_id,
                pageSize=10).execute()
            listaDatosEntregasDeLosAlumnos_retornoAPI.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        dictEntregas = {}  # keys= userId  values= link

        # ¿la API retorno almenos los datos de una entrega de un alumno?
        if listaDatosEntregasDeLosAlumnos_retornoAPI:

            for c,datosEntregaAlumno_x in enumerate(listaDatosEntregasDeLosAlumnos_retornoAPI):
                user_id = datosEntregaAlumno_x.get('userId')
                state = datosEntregaAlumno_x.get('state')
                asignacion_id = datosEntregaAlumno_x.get('id')


                # si ".get('state')" retorna 'NEW' significa que el usuario ni siquiera ha abierto
                # la asignacion por lo tanto no existe un 'submissionHistory', por tal motivo este
                # condicional pregunta si  ".get('state')" es diferente de: 'NEW'
                if datosEntregaAlumno_x.get('state')!='NEW':

                    # ¿la ultima accion fue un 'gradeHistory' o  un 'stateHistory' ?
                    # si no es un 'stateHistory' la variable 'ultimaAccion' valdra None
                    ultimaAccion=datosEntregaAlumno_x.get('submissionHistory')[-1].get('stateHistory')

                    # si  la variable 'ultimaAccion' fue un 'gradeHistory'  significa que la ultima accion que se
                    # realizo con la tarea es que fue calificada por el profesor por lo tanto significa
                    # que ya fue retornada su calificacion o esta por retornarse por lo tanto el valor
                    # de la variable 'ultimoEstadoTarea' sera igual a 'RETURNED' y solo cambiara si y solo
                    # si  la variable 'ultimaAccion' fue un 'stateHistory'
                    ultimoEstadoTarea='RETURNED'

                    # ¿ la ultima accion fue un 'stateHistory' ?
                    if ultimaAccion!=None:

                        # como la ultima accion fue un 'stateHistory' significa que el estudiante pudo:
                        # hacer lo siguiente: 'TURNED_IN'  o 'RECLAIMED_BY_STUDENT' es decir significa que
                        # la ultima accion que se hizo con la tarea es que el estudian o la entrego o cancelo
                        # su entrega
                        ultimoEstadoTarea=ultimaAccion.get('state')

                # el estudiante ni si quiera ha abierto la tarea
                else:
                    ultimoEstadoTarea='NEW'

                # ¿el usuario a entregado la tarea?
                if ultimoEstadoTarea != 'RETURNED':
                    try:
                        listaAttachments = datosEntregaAlumno_x.get('assignmentSubmission').get('attachments')
                        dictEntregas[user_id] = [listaAttachments, asignacion_id]

                    except:
                        # el usuario NO entrego nada como archivo de tarea, por lo tanto se omite su entrega
                        continue

        return dictEntregas



    def list_todasEntregasEstudiante(self, course_id, user_id):
        """

        Parámetros:
            course_id (str): Representa el ID de la clase de classroom de la cual se quieren
            obtener las tareas existentes y las calificaciones de un estudiante en especifico
            user_id (str): Representa el ID  del estudiante del cual es quieren obtener sus
            calificaciones de cada tarea que se ha dejado en la clase de classroom cuyo id
            es igual a: 'course_id'

        Returns:
            Retornara un diccionario  que contendra de forma ordenada todas las tareas que se han dejado
            en la clase de classroom cuyo id es igual a: 'course_id' junto con las calificaciones que
            saco el estudiante cuyo id es igual a: 'user_id', la forma en que ordenara los datos el
            diccionario sera la siguiente:

               {
               'topic_1': (  (nombre_tarea1,calif_tarea1), (nombre_tarea2,calif_tarea2) ...  )
               'topic_2': (  (nombre_tarea1,calif_tarea1), (nombre_tarea2,calif_tarea2) ...  )
                                                 .
                                                 .
                                                 .
               }
         """

        page_token = None

        listaDatos_tareasEstudianteX_retornoAPI=[]

        while True:
            response= self.service_classroom.courses().courseWork().studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                courseWorkId="-",
                userId=user_id).execute()
            listaDatos_tareasEstudianteX_retornoAPI.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        datosDict = {}

        # ¿la API retorno almenos los datos de una tarea del estudiante?
        if listaDatos_tareasEstudianteX_retornoAPI:
            for datosTareaX in listaDatos_tareasEstudianteX_retornoAPI:
                calificacion=datosTareaX.get('assignedGrade')
                coursework_id=datosTareaX.get('courseWorkId')

                nombreTopicyCoursework=self.get_nombreTopicyCourseWork(
                    curso_id=course_id,
                    courseWork_id=coursework_id
                )

                if nombreTopicyCoursework!=None:
                    topic_nombre,courseWork_nombre=nombreTopicyCoursework

                    if not(topic_nombre in datosDict):
                        datosDict[topic_nombre] = []

                    datosDict[topic_nombre].append(  (courseWork_nombre,calificacion) )

        return datosDict



    def get_nombreTopicyCourseWork(self, curso_id,courseWork_id):
        """
        Parámetros:
            curso_id (str): Representa el ID de lc clase de classroom en donde
            se encuentra el coursework cuyo ID es igual a: 'courseWork_id'
            courseWork_id (str): Representa el ID del courseWork del cual se
            desea hallar el nombre del topic al que pertence asi como su
            propio nombre.

        Returns:
                Una tupla de dos elementos en donde:
                    - el primer elemento (str): Representa el nombre del topic
                      al que pertence el coursework cuyo id es igual a:
                     'courseWork_id'

                    - el segundo elemento (str): Representa el nombre del courseWork
                    cuyo id es igual a: 'courseWork_id'
        """


        datosCourseWork = self.service_classroom.courses().courseWork().get(
            courseId=curso_id,
            id=courseWork_id
        ).execute()


        if datosCourseWork != None:
            courseWork_nombre = datosCourseWork.get("title")
            courseWork_topicId=datosCourseWork.get("topicId")

            datosTopic = self.service_classroom.courses().topics().get(
                courseId=curso_id,
                id=courseWork_topicId
            ).execute()

            if datosTopic != None:
                topic_nombre = datosTopic.get("name")

                return topic_nombre,courseWork_nombre
        return None






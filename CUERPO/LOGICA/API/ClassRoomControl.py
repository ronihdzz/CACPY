from __future__ import print_function
import os.path
from subprocess import check_output
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

import datetime     # for general datetime object handling
import rfc3339      # for date object -> date string
import iso8601

def get_date_object(date_string):
  return iso8601.parse_date(date_string)

def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)


class AdministradorProgramasClassRoom:
    def __init__(self,classroom_control,curso_id,tareasProgramas_topic_id,retroProgramas_topic_id):
        self.classroom_control=classroom_control
        self.curso_nombre=None
        self.curso_id=curso_id
        self.tareasProgramas_topic_id=tareasProgramas_topic_id
        self.retroProgramas_topic_id=retroProgramas_topic_id


    def get_dictTareasDejadas(self):
        dictTareas=self.classroom_control.get_dictTareasTopic(self.curso_id,self.tareasProgramas_topic_id)
        print(dictTareas)
        return dictTareas

    def crearTarea(self,titulo,descripccion,colab_link,colab_id):

        idTarea= self.classroom_control.create_asignacionPrograma(
                    course_id=self.curso_id,
                    topic_programas_id=self.tareasProgramas_topic_id,
                    colab_link=colab_link,
                    colab_id=colab_id,
                    titulo=titulo,
                    description=descripccion
        )
        return idTarea


class CalificadorConfiguracion:
    def __init__(self,curso_nombre=None,curso_api_id=None,programTopic_nombre=None,programTopic_id=None,retroTopic_nombre=None,retroTopic_id=None):

        self.curso_nombre=curso_nombre
        self.curso_api_id=curso_api_id

        self.programTopic_id=programTopic_id
        self.programTopic_nombre=programTopic_nombre

        self.retroTopic_nombre=retroTopic_nombre
        self.retroTopic_id=retroTopic_id


    def reiniciarValores(self):
        self.curso_nombre = None
        self.curso_api_id = None
        self.programTopic_nombre = None
        self.programTopic_id=None
        self.retroTopic_nombre = None
        self.retroTopic_id = None

    def cargarDatosCurso(self,id,nombre):
        self.reiniciarValores()
        self.curso_api_id = id
        self.curso_nombre=nombre

    def cargarDatosTopic(self,programaTopic_id,programaTopic_nombre):
        self.programTopic_id=programaTopic_id
        self.programTopic_nombre=programaTopic_nombre

    def datosListosApartadoTareas(self):
        if self.curso_api_id!=None and self.programTopic_id!=None:
            return True
        else:
            return False

    def respaldarDatos(self,nombreArchivo):
        seDebeRespaldar= (self.curso_api_id!=None and self.programTopic_id!=None)
        archivoDatosExiste=os.path.isfile(nombreArchivo)

        if seDebeRespaldar:
            with open(nombreArchivo,'w') as archivo:
                archivo.write(  '\n'.join(  (self.curso_api_id,self.programTopic_id)  )   )

        elif archivoDatosExiste:
            os.remove(nombreArchivo)








class ClassRoomControl:

    # If modifying these scopes, delete the file token.json.
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

    def __init__(self,credenciales_direc=None,token_direc=None):
        self.credenciales_direc=credenciales_direc
        self.token_direc=token_direc
        self.obtenerValor_service_classroom_and_drive()


    def obtenerValor_service_classroom_and_drive(self):
        """
        Shows basic usage of the Classroom API.
        Prints the names of the first 10 courses the user has access to.
        """

        SCOPES=self.SCOPES
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service_classroom = build('classroom', 'v1', credentials=creds)
        self.service_drive = build('drive', 'v3', credentials=creds)
        # service = build('driveactivity', 'v2', credentials=creds)


    def refrescarValor_service_classroom_and_drive(self):
        # borrar el token

        # obtener el token
        #self.obtenerValor_service_classroom_and_drive()

        pass

    def get_listaDatosCursos(self):
        """
        Obtiene las clases del PROFESOR

        :returns
            dict_cursos: dato de tipo lista donde cada elemento de ella
            es una tupla con 2 elementos cada una:
                - primer elemento de la tupla es el id del curso
                - segundo elemento de la tupla es el nombre del curso
        """

        service = self.service_classroom
        listaCursos= []
        page_token = None

        while True:
            response = service.courses().list(pageToken=page_token,
                                              pageSize=100).execute()
            listaCursos.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        listaDatos=[]
        if not listaCursos:
            print('No courses found.')
        else:
            print('Courses:')
            for curso in listaCursos:
                listaDatos.append( ( curso.get('id'), curso.get('name') )  )
        return listaDatos

    def get_listaDatosTopicsCurso(self,curso_id):
        """ Returnara un diccionario en donde:
                - Los keys son los id de los topic
                - Los values  son los nombres de los topic
        """

        service = self.service_classroom
        # [START classroom_list_submissions]
        curso_topics = []
        page_token = None

        while True:

            response = service.courses().topics().list(
                pageToken=page_token,
                courseId=curso_id,
                pageSize=10).execute()
            curso_topics.extend(response.get('topic', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        lista_tuplasDatos = []
        if not curso_topics:
            print('No student submissions found.')
            return lista_tuplasDatos
        else:
            print('Student Submissions:******************************************************')

            for topic in curso_topics:
                 lista_tuplasDatos.append( [ topic.get('topicId'), topic.get('name') ] )
            return lista_tuplasDatos


    def get_listaTareasTopic(self, curso_id,topic_id):
        """
        Obtendra los datos de todas las tareas asignadas hasta este
        momento, posteriormente

        """

        service = self.service_classroom
        # [START classroom_list_submissions]
        submissions = []
        page_token = None

        while True:
            coursework = service.courses().courseWork()
            response = coursework.list(
                courseId=curso_id
            ).execute()
            submissions.extend(response.get('courseWork', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        listaDatos = []
        if not submissions:
            print('Ninguna asignación encontrada')
        else:
            print('Lista de asignaciones:')

            for tarea in submissions:
                tarea_topic=tarea.get('topicId')
                if topic_id==tarea_topic:
                    # fecha de creacion en formato iso8601
                    fechaCreacion = get_date_object(  tarea.get('creationTime')   )
                    # formato de cadena ISO8601:  YYYY-MM-DD HH:MM:SS.SSS para compatibilidad con sqlite3
                    fechaCreacion=fechaCreacion.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                    datos=[
                        tarea.get('id'), curso_id, topic_id, tarea.get('title'),
                        tarea.get('description'), fechaCreacion
                    ]

                    listaDatos.append(datos)

        return listaDatos


    def get_datosProfesor(self,nombreCompletoFoto_guardar=None):
        """
        Obtendra los datos del profesor, y rescartara especificamente
        3 datos esenciales:
            - nombre completo del profesor
            - correo electronico del profesor
            - url de la foto de perfil del profesor

        Y si se asigna un valor al parametro 'direccionCopiaraFoto',este
        metodo descargara la foto del profesor atraves de la url de la foto
        obtenida, y la guardara con el nombre y direccion que tenga el parametro
        'direccionCopiaraFoto'.Si no se le asigna valor alguno al parametro
        'direccionCopiaraFoto' entonces no se descargara la foto.

        :param direccionCopiaraFoto:
        :return: una tupla con 2 elementos:
            - nombre completo del profesor
            - correo electronico del profesor
        """

        service = self.service_classroom

        profesor_userProfile= service.userProfiles().get(userId="me").execute()
        profesor_nombre = profesor_userProfile.get("name").get('fullName')
        profesor_email=profesor_userProfile.get('emailAddress')

        if nombreCompletoFoto_guardar:
            if os.path.isfile(nombreCompletoFoto_guardar):
                os.remove(nombreCompletoFoto_guardar)

            profesor_photoUrl = profesor_userProfile.get("photoUrl")
            # PROCESO PARA DESCARGAR ARCHIVO:
            print('Beginning file download with requests')
            r = requests.get(profesor_photoUrl)
            with open(nombreCompletoFoto_guardar, 'wb') as f:
                f.write(r.content)

        return (profesor_email,profesor_nombre)



    def get_listaAlumnos(self, course_id):

        """ Returnar la lista de estudiantes """

        service = self.service_classroom
        # [START classroom_list_submissions]
        submissions = []
        page_token = None

        while True:

            response = service.courses().students().list(
                pageToken=page_token,
                courseId=course_id,
                pageSize=10).execute()
            submissions.extend(response.get('students', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not submissions:
            print('No student submissions found.')
        else:
            print('Student Submissions:******************************************************')
            dictDatos = {}
            for submission in submissions:
                idEstudiante = submission.get('userId')
                nombreCompleto = submission.get('profile').get('name')['fullName']
                # print()
                # print(idEstudiante,nombreCompleto)

                dictDatos[idEstudiante] = nombreCompleto
            return dictDatos



    def create_asignacionPrograma(self, course_id,topic_programas_id,colab_link,colab_id,titulo,description):
        """ Creates a coursework. """
        service = self.service_classroom
        # [START classroom_create_coursework]
        coursework = {
            'title': titulo,
            'description': description,
            'topicId':topic_programas_id,
            'workType': 'ASSIGNMENT',
            'state': 'DRAFT',  # 'PUBLISHED'
            'maxPoints':100, # puntos de esta tarea
            'materials': [
                {
                    'driveFile': {
                        'driveFile':{
                            'id':colab_id,
                            'title': titulo,
                            'alternateLink': colab_link
                        },
                        'shareMode': 'STUDENT_COPY'
                    },
                }
                # {       }
                # {       }
            ]
        }
        coursework = service.courses().courseWork().create(
            courseId=course_id, body=coursework).execute()
        print('Assignment created with ID {%s}' % coursework.get('id'))

        idCoursework=coursework.get('id')

        return idCoursework


##################################################################################################################################################################################################
#
##################################################################################################################################################################################################

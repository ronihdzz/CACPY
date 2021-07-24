from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

import rfc3339      # for date object -> date string
import iso8601
import recursos

import os


def get_date_object(date_string):
  return iso8601.parse_date(date_string)

def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)



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
        #if os.path.exists('token.json'):
        print("EXISTE??{}".format(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN))
        if os.path.exists(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN):

            creds = Credentials.from_authorized_user_file(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN, SCOPES)
            #creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                #flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                flow = InstalledAppFlow.from_client_secrets_file(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES,SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            #with open('token.json', 'w') as token:
            with open(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN, 'w') as token:
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

                    #datos=[
                    #    tarea.get('id'), curso_id, topic_id, tarea.get('title'),
                    #    tarea.get('description'), fechaCreacion
                    #]

                    datos = [
                        tarea.get('id'),tarea.get('title'),tarea.get('description'), fechaCreacion
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

        print("curso",course_id)
        print("topicProgramas",topic_programas_id)
        print("colab",colab_link)
        print("colab_id", colab_id)
        print("titulo:",titulo)
        print("descripccion",description)

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

    def get_datosEntregas(self, course_id, coursework_id):
        """ Lists all student submissions for a given coursework.
         Poner atencion a los estados:
         RETURNED

        SUBMISSION_STATE_UNSPECIFIED	Ningún estado especificado. Esto nunca debe devolverse.
        NEW	El alumno nunca ha accedido a este envío. Los archivos adjuntos no se devuelven
            y las marcas de tiempo no se establecen.
        CREATED	Ha sido creado.
        TURNED_IN	Ha sido entregado al maestro.
        RETURNED	Ha sido devuelto al alumno.
        RECLAIMED_BY_STUDENT	El estudiante eligió "anular la entrega" de la tarea.


         """
        service = self.service_classroom

        # dictEstudiantes=self.get_listaAlumnos(course_id=course_id)

        # [START classroom_list_submissions]
        submissions = []
        page_token = None

        while True:
            coursework = service.courses().courseWork()
            response = coursework.studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                states=['NEW','CREATED','RETURNED','TURNED_IN','RECLAIMED_BY_STUDENT'],
                courseWorkId=coursework_id,
                pageSize=10).execute()
            submissions.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        dictEntregas = {}  # keys= userId  values= link
        if not submissions:
            print('No student submissions found.')
            return dictEntregas
        else:
            print('Student Submissions:******************************************************')

            dictDatosEntrega={
                'calificados':0, #RETURNED
                'porCalificar':0, # TURNED_IN
                'porEntregar':0,
            }

            for submission in submissions:
                state = submission.get('state')

                if state=='RETURNED':
                    dictDatosEntrega['calificados']+=1
                elif state=='TURNED_IN':
                    dictDatosEntrega['porCalificar']+=1
                else:
                    dictDatosEntrega['porEntregar']+=1

            return dictDatosEntrega


    def list_submissions(self, course_id, coursework_id):
        """ Lists all student submissions for a given coursework.
         Poner atencion a los estados:
         RETURNED

        SUBMISSION_STATE_UNSPECIFIED	Ningún estado especificado. Esto nunca debe devolverse.
        NEW	El alumno nunca ha accedido a este envío. Los archivos adjuntos no se devuelven
            y las marcas de tiempo no se establecen.
        CREATED	Ha sido creado.
        TURNED_IN	Ha sido entregado al maestro.
        RETURNED	Ha sido devuelto al alumno.
        RECLAIMED_BY_STUDENT	El estudiante eligió "anular la entrega" de la tarea.


         """
        service = self.service_classroom

        # dictEstudiantes=self.get_listaAlumnos(course_id=course_id)

        # [START classroom_list_submissions]
        submissions = []
        page_token = None

        while True:
            coursework = service.courses().courseWork()
            response = coursework.studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                states=['TURNED_IN'],
                courseWorkId=coursework_id,
                pageSize=10).execute()
            submissions.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        dictEntregas = {}  # keys= userId  values= link
        if not submissions:
            print('No student submissions found.')
            return dictEntregas
        else:
            print('Student Submissions:******************************************************')

            for submission in submissions:
                user_id = submission.get('userId')
                state = submission.get('state')
                asignacion_id = submission.get('id')

                # nombreAlumno=dictEstudiantes[user_id]

                print('Alumno:', user_id)
                print('Estado:', state)



                # url = tarea['attachments'][0]['link']['url']
                try:
                    #print(tarea['attachments'])
                    tarea = submission.get('assignmentSubmission')
                    url = tarea['attachments'][0]['driveFile']['alternateLink']
                    # Si el usuario entrego pero no entrego nada...
                except:
                    continue

                print(url)
                dictEntregas[user_id] = [url, asignacion_id]
            return dictEntregas
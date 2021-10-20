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
import shutil
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
        #self.obtenerValor_service_classroom_and_drive()


    def cargarArchivoCredenciales(self,nombreArchivo):


        print("Operando FUNCION cargarArchivoCredenciales...")
        archivo_crendencialesExite = os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

        archivo_tokenExiste=os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)

        if archivo_tokenExiste:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)

        if archivo_crendencialesExite:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

        cadena=f"{nombreArchivo} ---- {recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES}"
        print(cadena)

        shutil.copyfile(nombreArchivo,recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)



    def eliminarArchivoCredenciales(self):
        archivo_crendencialesExite = os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

        if archivo_crendencialesExite:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_CREDENCIALES)

    def eliminarArchivoToken(self):

        archivo_tokenExiste=os.path.isfile(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)

        if archivo_tokenExiste:
            os.remove(recursos.App_Principal.NOMBRE_COMPLETO_TOKEN)




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
            print("URL OBTENIDA:", profesor_photoUrl)

            # error en la API, ya que no siempre incluye al inicio: 'https:'
            if not profesor_photoUrl.startswith('https:'):
                profesor_photoUrl='https:'+profesor_photoUrl

            print("URL OBTENIDA:", profesor_photoUrl)
            r = requests.get(profesor_photoUrl)

            with open(nombreCompletoFoto_guardar, 'wb') as f:
                f.write(r.content)

        return (profesor_email,profesor_nombre)




    def get_datosAlumno(self,idAlumno):
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

        estudiante_userProfile= service.userProfiles().get(userId=idAlumno).execute()
        estudiante_nombre = estudiante_userProfile.get("name").get('fullName')
        estudiante_email=estudiante_userProfile.get('emailAddress')

        return (estudiante_email,estudiante_nombre)




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
            tuplaDatos = []
            for submission in submissions:
                idEstudiante = submission.get('userId')
                nombreCompleto = submission.get('profile').get('name')['fullName']
                correoElectronico=submission.get('profile').get('emailAddress')
                # print()
                # print(idEstudiante,nombreCompleto)

                tuplaDatos.append( (idEstudiante,nombreCompleto,correoElectronico) )
            return tuple(tuplaDatos)


    def create_asignacionPrograma(self, course_id,topic_programas_id,colab_id,titulo,description):

        """ Creates a coursework. """
        service = self.service_classroom
        # [START classroom_create_coursework]
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
        coursework = service.courses().courseWork().create(
            courseId=course_id, body=coursework).execute()
        print('Assignment created with ID {%s}' % coursework.get('id'))

        print()

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



        submissionHistory  ==> Contiene el historial de entrega de cada alumno, es importante
        recalcar que

        Cuando recien se le deja una tarea a un estudiante el historial se ve asi:

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

            dictDatosEntrega={
                'calificados':0, #RETURNED
                'porCalificar':0, # TURNED_IN
                'porEntregar':0,
            }
            #print("DATOS DE LA TAREA")
            #print('*****************************************************')
            c=0
            #print(submissions)
            for submission in submissions:

                # ¿la ultima accion fue un 'gradeHistory' o  un 'stateHistory' ?
                # si no es un 'stateHistory' la variable 'ultimaAccion' valdra None
                #print(submission.get('submissionHistory'),submission.get('state'))

                if submission.get('state')!='NEW':
                    ultimaAccion=submission.get('submissionHistory')[-1].get('stateHistory')
                    ultimoEstadoTarea='RETURNED'
                    if ultimaAccion!=None:
                        ultimoEstadoTarea=ultimaAccion.get('state')
                else:
                    ultimoEstadoTarea='NEW'

                c+=1
                #print("Alumno numero:",c)
                #print("*" * 100)
                #print("Alumno estado:",state,end=' ')
                #print("ultimoEstadoTarea:",ultimoEstadoTarea)
                #print("DraftGrade=",draftGrade,end=' ')
                #print('assignedGrade',assignedGrade)

                if ultimoEstadoTarea=='RETURNED': # or draftGrade!=None or assignedGrade!=None:
                    dictDatosEntrega['calificados']+=1
                elif ultimoEstadoTarea=='TURNED_IN':
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
            #print('Student Submissions:******************************************************')

            for submission in submissions:
                user_id = submission.get('userId')
                state = submission.get('state')
                asignacion_id = submission.get('id')

                # ¿la ultima accion fue un 'gradeHistory' o  un 'stateHistory' ?
                # si no es un 'stateHistory' la variable 'ultimaAccion' valdra None
                ultimaAccion = submission.get('submissionHistory')[-1].get('stateHistory')

                ultimoEstadoTarea = 'RETURNED'
                if ultimaAccion != None:
                    ultimoEstadoTarea = ultimaAccion.get('state')

                # nombreAlumno=dictEstudiantes[user_id]

                #print('Alumno:', user_id)
                #print('Estado:', state)

                # url = tarea['attachments'][0]['link']['url']
                draftGrade=submission.get('draftGrade')
                assignedGrade=submission.get('assignedGrade')

                #if draftGrade==None and assignedGrade==None:
                if ultimoEstadoTarea!='RETURNED':
                    try:
                        #print(tarea['attachments'])
                        #tarea = submission.get('assignmentSubmission')
                        #url = tarea['attachments'][0]['driveFile']['alternateLink']


                        listaAttachments=submission.get('assignmentSubmission').get('attachments')
                        dictEntregas[user_id] = [listaAttachments, asignacion_id]
                        # Si el usuario entrego pero no entrego nada...
                    except:
                        continue

            return dictEntregas


    def list_todasEntregasEstudiante(self, course_id, user_id):
        """ Lists all coursework submissions for a given student. """
        service = self.service_classroom
        # [START classroom_list_submissions]
        submissions = []
        page_token = None

        while True:
            coursework = service.courses().courseWork()
            response = coursework.studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                courseWorkId="-",
                userId=user_id).execute()
            submissions.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not submissions:
            print('No student submissions found.')
        else:
            datosDict={}
            print('Complete list of student Submissions:')
            for submission in submissions:
                calificacion=submission.get('assignedGrade')
                coursework_id=submission.get('courseWorkId')

                nombreTopicyCoursework=self.get_nombreTopicyCourseWork(
                    curso_id=course_id,
                    courseWork_id=coursework_id
                )

                topic_nombre=None
                courseWork_nombre=None

                if nombreTopicyCoursework!=None:
                    topic_nombre,courseWork_nombre=nombreTopicyCoursework

                if not(topic_nombre in datosDict):
                    datosDict[topic_nombre] = []

                datosDict[topic_nombre].append(  (courseWork_nombre,calificacion) )

            return datosDict



    def get_nombreTopicyCourseWork(self, curso_id,courseWork_id):
        """ Returnara un diccionario en donde:
                - Los keys son los id de los topic
                - Los values  son los nombres de los topic
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






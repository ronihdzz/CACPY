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

import recursos

from nbgrader.apps import NbGraderAPI
from traitlets.config import Config

import os
import io
from googleapiclient.http import MediaIoBaseDownload


# para convertir a pdf y para saber el sistema operativo
import pdfkit
import platform

from apiclient.http import MediaFileUpload


def get_date_object(date_string):
  return iso8601.parse_date(date_string)

def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)


class AdministradorProgramasClassRoom:
    def __init__(self,classroom_control,baseDatosLocalClassRoom,configuracionCalificador):
        self.classroom_control=classroom_control
        self.configuracionCalificador=configuracionCalificador
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.nbGrader_control=None



    def get_datosCurso(self):
        return (self.configuracionCalificador.curso_api_id,self.configuracionCalificador.curso_nombre)

    def get_datosTopic(self):
        return (self.configuracionCalificador.programTopic_id,self.configuracionCalificador.programTopic_nombre)


    def seleccionarBaseLocal_coursework(self,idCourseWork):
        self.baseDatosLocalClassRoom.cambiarEstadoEleccion(
            curso_id=self.configuracionCalificador.curso_api_id,
            topic_id=self.configuracionCalificador.programTopic_id,
            idCourseWorkElegido=idCourseWork
        )


    def get_dictTareasDejadas(self):
        listaTareas=self.classroom_control.get_listaTareasTopic(
            self.configuracionCalificador.curso_api_id,
            self.configuracionCalificador.programTopic_id
        )
        #datos = [
        #    tarea.get('id'), curso_id, topic_id, tarea.get('title'),
        #    tarea.get('description'), fechaCreacion
        #]

        print(listaTareas)
        return listaTareas

    def crearTarea(self,titulo,descripccion,colab_link,colab_id):

        idTarea= self.classroom_control.create_asignacionPrograma(
                    course_id=self.configuracionCalificador.curso_api_id,
                    topic_programas_id=self.configuracionCalificador.programTopic_id,
                    colab_link=colab_link,
                    colab_id=colab_id,
                    titulo=titulo,
                    description=descripccion
        )
        # formato de cadena ISO8601:  YYYY-MM-DD HH:MM:SS.SSS para compatibilidad con sqlite3
        fechaCreacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # tuplaDatos=(id,title,description,fechaCreacion)
        self.agregarCourseWorks_baseDatosLocal(
            tuplaDatos=(  (idTarea,titulo,descripccion,fechaCreacion),   )
        )

        # registrar como ya agregada
        self.seleccionarBaseLocal_coursework(idCourseWork=idTarea)

        return idTarea,fechaCreacion


    def get_courseWorksLibres_baseDatosLocal(self):

        tuplaDatosCourseWorks=self.baseDatosLocalClassRoom.get_courseWorksLibres(
            curso_id=self.configuracionCalificador.curso_api_id,
            topic_id=self.configuracionCalificador.programTopic_id
        )
        return tuplaDatosCourseWorks

    def get_courseWorksAgregados_baseDatosLocal(self):

        tuplaDatosCourseWorks=self.baseDatosLocalClassRoom.get_courseWorksAgregados(
            curso_id=self.configuracionCalificador.curso_api_id,
            topic_id=self.configuracionCalificador.programTopic_id
        )
        return tuplaDatosCourseWorks


    def agregarCourseWorks_baseDatosLocal(self,tuplaDatos):
        self.baseDatosLocalClassRoom.agregar_soloNuevosCourseWorks(
            tuplaDatos=tuplaDatos,
            curso_id=self.configuracionCalificador.curso_api_id,
            topic_id=self.configuracionCalificador.programTopic_id
        )

    def eliminarCourseWork_baseDatosLocal(self,courseWork_id):
        self.baseDatosLocalClassRoom.eliminarCourseWork(
            curso_id=self.configuracionCalificador.curso_api_id,
            topic_id=self.configuracionCalificador.programTopic_id,
            coursework_id=courseWork_id
        )


    def get_informacionTareasEntregadas(self,courseWork_id):

        #dictEntregas[user_id] = [url, asignacion_id]

        datosEntraga=self.classroom_control.list_submissions(
            course_id=self.configuracionCalificador.curso_api_id,
            coursework_id=courseWork_id
        )

        print(datosEntraga)

    def get_rutaAsignaciones(self):
        if self.nbGrader_control:
            ubicacionCurso=self.nbGrader_control.config.CourseDirectory.root
            print("UBICACION DEL CURSO...",ubicacionCurso)
            ubicacionCurso+='submitted/'
            return ubicacionCurso

    def get_rutaRetroalimentacion(self):
        if self.nbGrader_control:
            ubicacionCurso=self.nbGrader_control.config.CourseDirectory.root
            print("UBICACION DEL CURSO...",ubicacionCurso)
            ubicacionCurso+='feedback/'
            return ubicacionCurso


    def calificarEstudiantes(self, courseWork_id,courseWork_name,noMaxEstudiantesCalificar=5):

        ############################################################################################
        # DATOS DE LA CARPETA EN DONDE SE ADJUNTARAN LAS RETROALIMENTACIONES
        ###########################################################################################

        folder_id = '1W5StOtU4tJERcsRtUjj2lLhkJ8ybdbW1'
        nombreCarpetaCurso = 'israel_mejia'  # sera el id del curso

        drive_service=self.classroom_control.service_drive
        page_token=None

        ############################################################################################################################################
        # SI EXISTE EN DRIVE LA CARPETA DEL CURSO, AHI SE SUBIRAN LAS TAREAS DEL ESTUDIANTE PERO SI NO EXISTE SE VA A CREAR
        ############################################################################################################################################

        # Lo que se busca es una CARPETA, la carpeta que se busca NO SE ENCUENTRA en la papelera de reciclaje
        # la carpeta que se busca se encuentra dentro de la carpeta  cuyo id es igual a un id especifico
        query = "trashed=False and mimeType='application/vnd.google-apps.folder' and name='{}'   and  '{}' in parents".format(
            nombreCarpetaCurso, folder_id)
        # print("QUERY=",query)
        listaResultados = []
        while True:
            response = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token).execute()

            for file in response.get('files', []):
                # Process change
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                listaResultados.append([file.get('name'), file.get('id')])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        if listaResultados != []:
            # Si solo existe una carpeta con dicho nombre y especificaciones se obtiene su ID
            if len(listaResultados) == 1:
                print("Si existe la carpeta")
                ID_SUPREMO = listaResultados[0][1]
            # Si existe mas de una carpeta con dicho nombre y especificaciones entonces hay un error
            else:
                print("ERROR de repeticion de dos carpeta, arreglar cuanto antes")

        # Si no existe ninguna carpeta con dicho nombre y especificaciones entonces se crea y posteriormente
        # se obtiene su ID
        else:
            print("No existe la carpeta")
            file_metadata = {
                'name': nombreCarpetaCurso,
                'parents': [folder_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = drive_service.files().create(body=file_metadata,
                                                fields='id').execute()
            print('Folder ID: %s' % file.get('id'))
            ID_SUPREMO = file.get('id')
            print("")


        # YA QUE SE TIENE EL ID DE LA CARPETA EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES...



        #formato del diccionario: dictEntregas[user_id] = [url, asignacion_id]
        dictEntregas=self.classroom_control.list_submissions(
            course_id=self.configuracionCalificador.curso_api_id,
            coursework_id=courseWork_id,
        )

        RUTA_ASIGNACIONES=self.get_rutaAsignaciones()


        if len(dictEntregas)>0:
            for user_id, url_or_idAsignacion in dictEntregas.items():
                url, idAsignacion = url_or_idAsignacion

                ####################################################################################
                #  OBTENIENDO EL NOMBRE EN DONDE SE DESCARGARA LA TAREA ENTREGADA POR EL USUARIO
                ####################################################################################

                RUTA_TAREA = RUTA_ASIGNACIONES + user_id + '/' + courseWork_name + '/'
                os.makedirs(RUTA_TAREA, exist_ok=True)
                nombreArchivo = RUTA_TAREA + courseWork_name + '.ipynb'

                ####################################################################################
                #  DESCARGANDO LA ASIGNACION DEL ESTUDIANTE EN LA RUTA DEBIDA
                ####################################################################################

                # FORMATO DE LINK: 'https://drive.google.com/file/d/1m-LNYFiQeNKeeGRxo03dPg5HMrzQI3Wl/view?usp=drive_web'
                # si el archivo ya existe en la ruta debida, se eliminara de ahi
                archivo_id = url.split('/')[-2]
                if os.path.exists(nombreArchivo):
                    print("YA EXISTE :DDDD")
                    os.remove(nombreArchivo)

                # Descargando el archivo en la ruta debida
                request = self.classroom_control.service_drive.files().get_media(fileId=archivo_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))

                fh.seek(0)
                with open(nombreArchivo, 'wb') as f:
                    f.write(fh.read())
                    f.close()

                ####################################################################################
                #  CALIFICANDO LA TAREA CON NBGRADER
                ####################################################################################

                resultadoAlCalificar = self.nbGrader_control.autograde(assignment_id=courseWork_name,student_id=user_id)

                calificacionFinal=0
                puntosTotales=0
                if resultadoAlCalificar['success'] is True:
                    calif =self.nbGrader_control.get_submission(assignment_id=courseWork_name, student_id=user_id)
                    puntosObtenidos = calif['score']
                    puntosTotales = calif['max_score']
                    print(puntosObtenidos, '/', puntosTotales)
                    calificacionFinal=puntosObtenidos/puntosTotales

                    #Si hubo exito al calificar la tarea entonces se puede crear la reotroalimentacion
                    #estatus_retroalimentacion=self.nbGrader_control.generate_feedback(assignment_id=courseWork_name,student_id=user_id,force=True)

                    nombreCopletoRetro=self.get_rutaRetroalimentacion()+ user_id + '/' + courseWork_name + '/'+courseWork_name
                    huboExito_crearRetro=self.generarRetraolimentacionTarea_pdf(courseWork_name=courseWork_name,
                                                           idEstudiante=user_id,
                                                           nombreCompletoRetro=nombreCopletoRetro)

                    if huboExito_crearRetro:

                        ############################################################################################################################################
                        # SUBIENDO EL ARCHIVO A LA CARPETA DEL CURSO, OBTENIENDO SU LINK DE ACCESO Y POSTERIORMENTE MODIFICANDO SUS PERMISOS PARA UN ACCESO PUBLICO
                        ############################################################################################################################################

                        print("ID_SUPREMO:", ID_SUPREMO)
                        nombreGuardaraArchivo = '{}_{}'.format(user_id,courseWork_id)  # Id de los archivos   alumnoId_topicId_courseworkId_numeroVersion

                        #############################################################################################
                        # ADJUNTANDO EL NUMERO DE VERSION AL NOMBRE DEL ARCHIVO QUE SE DESEA SUBIR
                        #############################################################################################

                        # Se busca la existencia de archivos con la palabra 'nombreGuardaraArchivo' contenida
                        #trashed=False and mimeType!='application/vnd.google-apps.folder' and
                        #fullText contains 'hello'
                        query = "trashed=False and mimeType!='application/vnd.google-apps.folder' and fullText contains '{}'  and  '{}' in parents".format(
                            nombreGuardaraArchivo, ID_SUPREMO)
                        print("QUERY=", query)
                        listaResultados = []
                        while True:
                            # " mimeType = 'application/vnd.google-apps.folder'    '{}' in parents ".format(folder_id)
                            response = drive_service.files().list(
                                q=query,
                                spaces='drive',
                                fields='nextPageToken, files(id, name)',
                                pageToken=page_token).execute()

                            for file in response.get('files', []):
                                # Process change
                                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                                listaResultados.append([file.get('name'), file.get('id')])
                            page_token = response.get('nextPageToken', None)
                            if page_token is None:
                                break

                        numeroVersionArchivo = len(listaResultados)
                        nombreGuardaraArchivo += ('_{}.pdf'.format(numeroVersionArchivo))

                        #############################################################################################
                        # SUBIENDO EL ARCHIVO Y OBTENIENDO SU LINK DE VISTA
                        #############################################################################################

                        file_metadata = {
                            'name': nombreGuardaraArchivo,  # nombre que tendra en el archivo que se subira
                            'parents': [ID_SUPREMO]
                        }
                        media = MediaFileUpload(nombreCopletoRetro+'.pdf',  # nombre completo en donde se encuentra el archivo
                                                mimetype='application/pdf',
                                                # pdf=application/pdf   jpg=image/jpeg   html=application/json
                                                resumable=True)
                        file = drive_service.files().create(body=file_metadata,
                                                            media_body=media,
                                                            fields='id,name,webContentLink,webViewLink'
                                                            ).execute()

                        # caracteristicas: https://developers.google.com/drive/api/v3/reference/files
                        print('File ID: %s' % file.get('id'))
                        print('File webView: %s' % file.get('webViewLink'))

                        URL_RETROALIMENTACION=file.get('webViewLink')

                        ID_RETROALIMENTACION = file.get('id')

                        #############################################################################################
                        # DANDOLE ACCESO PUBLICO AL ARCHIVO COMPARTIDO
                        #############################################################################################

                        ID_ARCHIVO_COMPARTIR = ID_RETROALIMENTACION

                        def callback(request_id, response, exception):
                            if exception:
                                # Handle error
                                print(exception)
                            else:
                                print("Permission Id: %s " % response.get('id'))
                                print('File webView: %s' % response.get('webViewLink'))
                                print(response)
                                print(request_id)

                        batch = drive_service.new_batch_http_request(callback=callback)
                        user_permission = {
                            'type': 'anyone',  # compartir para cualquier persona
                            'role': 'reader',  # los permisos compartidos seran unicamente de lector
                        }
                        batch.add(drive_service.permissions().create(
                            fileId=ID_ARCHIVO_COMPARTIR,
                            body=user_permission,
                            fields='id'
                        ))
                        batch.execute()


                        #############################################################################################
                        # SUBIENDO LOS RESULTADOS AL USUARIO
                        #############################################################################################

                        # RESPUESTA AL USUARIO
                        studentSubmission = {
                            'assignedGrade': puntosObtenidos,
                            'draftGrade':puntosObtenidos,
                            'state': 'RETURNED',
                        }


                        print("Id sudmision:", idAsignacion)
                        self.classroom_control.service_classroom.courses().courseWork().studentSubmissions().patch(
                            courseId=self.configuracionCalificador.curso_api_id,
                            courseWorkId=courseWork_id,
                            id=idAsignacion,
                            updateMask='assignedGrade,draftGrade',
                            # updateMask='assignedGrade,draftGrade',
                            body=studentSubmission).execute()


                        request = {
                            'addAttachments': [
                                {
                                    'link': {
                                        "url": URL_RETROALIMENTACION
                                    }
                                }
                            ]
                        }
                        coursework =  self.classroom_control.service_classroom.courses().courseWork()
                        coursework.studentSubmissions().modifyAttachments(
                            courseId=self.configuracionCalificador.curso_api_id,
                            courseWorkId=courseWork_id,
                            id=idAsignacion,
                            body=request).execute()


                        print("ESTUDIANTE: ",user_id," TEMRINADO DE CALIFICAR")


                # no hubo exito al calificar...
                else:
                    print("PROBLEMAS AL CALIFICAR AUTOMATICAMENTE")
                    print('ERROR:\n','\t',resultadoAlCalificar['error'] )
                    print('LOG:\n',  '\t', resultadoAlCalificar['log'] )






    def generarRetraolimentacionTarea_pdf(self,courseWork_name,idEstudiante,nombreCompletoRetro):
        estatus_retroalimentacion=self.nbGrader_control.generate_feedback(assignment_id=courseWork_name, student_id=idEstudiante, force=True)

        # hubo exito al crear el feedbak
        if estatus_retroalimentacion['success']:

            sistema = platform.system()
            #print("Estamos en {}".format(sistema))

            urlpath = nombreCompletoRetro+'.html'
            pdffilepath = nombreCompletoRetro+'.pdf'
            print("RUTA DEL ARCHIVO A COPIAR...",urlpath)
            print("RUTA DEL ARCHIVO A CREAR...",pdffilepath)


#C:\Users\ronal\Desktop\proyectos\calificadorRoni\NB_GRADER\course_1\feedback\114283316418743255552\tarea_2
            if sistema == 'Windows':
                path_wkthmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
                pdfkit.from_url(url=urlpath, output_path=pdffilepath, configuration=config)
                return True

            elif sistema == 'Linux':
                pdfkit.from_url(url=urlpath, output_path=pdffilepath)
                return True
            elif sistema == 'Darwin':  # sistema operativo mac
                return False

        else:
            print("PROBLEMAS AL GENERAR LA RETROALIMENTACION")
            print('ERROR:\n', '\t', resultadoAlCalificar['error'])
            print('LOG:\n', '\t', resultadoAlCalificar['log'])
            return False




    def actualizar_nbGraderControl(self):
        '''
        Cuando el valor de la clase es cambio, debera ser llamado este metodo
        ya que este metodo renueva la nueva ruta en donde se encuentra ubicada el
        nbGrader control.


        :param nombreNuevaClase:
        :return:
        '''

        nombreNuevaClase=self.configuracionCalificador.clase_nombreNbGrader

        # create a custom config object to specify options for nbgrader
        config = Config()
        config.CourseDirectory.course_id = nombreNuevaClase
        config.CourseDirectory.root =recursos.App_Principal.RUTA_NB_GRADER+nombreNuevaClase+'/'
        self.nbGrader_control = NbGraderAPI(config=config)

        print("Tareas:",self.nbGrader_control.get_source_assignments())

    def existeEsaTarea_cursoNbGrader(self,nombreTarea):


        if self.nbGrader_control!=None:
            tareasExistentes=self.nbGrader_control.get_source_assignments()
            print(tareasExistentes)
            if nombreTarea in tareasExistentes:
                return True
            else:
                return False







class CalificadorConfiguracion:
    def __init__(self,curso_nombre=None,curso_api_id=None,programTopic_nombre=None,
                 programTopic_id=None,retroTopic_nombre=None,retroTopic_id=None,
                 clase_nombreNbGrader=None):

        self.curso_api_id = curso_api_id
        self.curso_nombre=curso_nombre

        self.programTopic_id=programTopic_id
        self.programTopic_nombre=programTopic_nombre

        self.retroTopic_nombre=retroTopic_nombre
        self.retroTopic_id=retroTopic_id

        self.clase_nombreNbGrader=clase_nombreNbGrader


    def get_id_nombre_cursoClassroom(self):
        return self.curso_api_id,self.curso_nombre

    def get_id_nombre_topicClassroom(self):
        return self.programTopic_id,self.programTopic_nombre

    def get_nombre_cursoNbGrader(self):
        return self.clase_nombreNbGrader




    def reiniciarValores(self):
        self.curso_nombre = None
        self.curso_api_id = None
        self.programTopic_nombre = None
        self.programTopic_id=None
        self.retroTopic_nombre = None
        self.retroTopic_id = None
        self.clase_nombreNbGrader=None

    def cargarDatosCurso(self,id,nombre):
        self.reiniciarValores()
        self.curso_api_id = id
        self.curso_nombre=nombre

    def cargarDatosTopic(self,programaTopic_id,programaTopic_nombre):
        self.programTopic_id=programaTopic_id
        self.programTopic_nombre=programaTopic_nombre


    def datosListosApartadoTareas(self):
        if self.curso_api_id!=None and self.programTopic_id!=None and self.clase_nombreNbGrader!=None:
            return True
        else:
            return False

    def set_clase_nombreNbGrader(self,nuevoValor):
        self.clase_nombreNbGrader=nuevoValor


    def respaldarDatos(self,nombreArchivo):
        seDebeRespaldar= (self.curso_api_id!=None and self.programTopic_id!=None)
        archivoDatosExiste=os.path.isfile(nombreArchivo)

        datosRespaldar=(
            self.curso_api_id,
            self.programTopic_id
        )

        if seDebeRespaldar:
            with open(nombreArchivo,'w') as archivo:
                archivo.write(  '\n'.join( datosRespaldar )   )

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


    def list_submissions(self, course_id, coursework_id):
        """ Lists all student submissions for a given coursework.
         Poner atencion a los estados:
         RETURNED


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

                tarea = submission.get('assignmentSubmission')
                # url = tarea['attachments'][0]['link']['url']
                url = tarea['attachments'][0]['driveFile']['alternateLink']
                print('Alumno:', user_id)
                print('Estado:', state)
                print(tarea['attachments'])
                print(url)
                dictEntregas[user_id] = [url, asignacion_id]
            return dictEntregas
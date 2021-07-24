from PyQt5.QtCore import QThread
import os.path
import os
import io
from googleapiclient.http import MediaIoBaseDownload


# para convertir a pdf y para saber el sistema operativo

from apiclient.http import MediaFileUpload
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana




class HiloCalificadorTarea(QThread):

    senal_unAlumnoCalificado=pyqtSignal(tuple) # se emitira un señal cuando se cierre
                                                   # el calificador para que se desbloque
                                                   # el programa
    senal_terminoCalificar=pyqtSignal(bool)

    # Errores de red...
    senal_errorRed=pyqtSignal(tuple )
    # 1) error al buscar la carpeta en donde se suben las retroalimentaciones y obtener su id
    # 2) error al crear la carpeta en caso de no existir y posteriormente obtener su id
    # 3) error al obtener la informacion de los alumnos que han entregado tareas
    # 4) error al descargar el colab del alumno
    # 5) error al obtener la version de la retraolimentacion
    # 6) error al subir a drive la retroalimentacion del alumno
    # 7) error al obtener el link de acceso publico con permisos de solo vista de la
    # retroalimentacion del alumno
    # 8) error al subir el link de la retroalimentacion al alumno
    # 9) error al subir la calificacion del alumno

    LISTA_ERRORES_RED=[
        "1) error al buscar la carpeta en donde se suben las retroalimentaciones y obtener su id",
        "2) error al crear la carpeta en caso de no existir y posteriormente obtener su id",
        "3) error al obtener la informacion de los alumnos que han entregado tareas",
        "4) error al descargar el colab del alumno",
        "5) error al obtener la version de la retraolimentacion",
        "6) error al subir a drive la retroalimentacion del alumno",
        "7) error al obtener el link de acceso publico con permisos de solo vista de la retroalimentacion del alumno",
        "8) error al subir el link de la retroalimentacion al alumno",
        "9) error al subir la calificacion del alumno"
    ]




    def __init__(self,configuracionCalificador,nbGrader_control,classroom_control):
        super().__init__()

        self.configuracionCalificador=configuracionCalificador
        self.nbGrader_control=nbGrader_control
        self.classroom_control=classroom_control

        self.courseWork_id=None
        self.courseWork_name=None

        self.noMaxEstudiantesCalificar=5 # valor default


        # variable bandera
        self.HILO_ACTIVO=True



    def setDatosTareaCalificar(self,nuevoCourseWork_id,nuevoCourseWork_name):

        self.courseWork_id=nuevoCourseWork_id
        self.courseWork_name=nuevoCourseWork_name



    def setNoMaxEstudiantesCalificar(self,nuevoValor):
        self.noMaxEstudiantesCalificar=nuevoValor

# def calificarEstudiantes(self, courseWork_id, courseWork_name, noMaxEstudiantesCalificar=5):

    def run(self):

        RECURSO_EXPLICACION_ERROR = 'https://www.youtube.com/watch?v=S6hidGAjSIY&t=58s'
        NUMERO_TAREAS_CALIFICAR=self.noMaxEstudiantesCalificar

        if self.HILO_ACTIVO:
            if self.courseWork_name and self.courseWork_id:

                courseWork_name = self.courseWork_name
                courseWork_id = self.courseWork_id

                print("Coursework_name", courseWork_name)
                print("Coursework_id", courseWork_id)

                # DATOS DE LA CARPETA EN DONDE SE ADJUNTARAN LAS RETROALIMENTACIONES
                folder_id = '1W5StOtU4tJERcsRtUjj2lLhkJ8ybdbW1'
                nombreCarpetaCurso = 'israel_mejia'  # sera el id del curso
                drive_service = self.classroom_control.service_drive
                page_token = None

                ############################################################################################################################################
                #   POSIBLE ERROR POR CONEXION DE RED 1:
                #   SI EXISTE EN DRIVE LA CARPETA EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES
                ############################################################################################################################################
                try:
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
                except Exception as e:
                    # 1) error al buscar la carpeta en donde se suben las
                    # retroalimentaciones y obtener su id
                    self.senal_errorRed.emit((self.LISTA_ERRORES_RED[0], e))
                    self.HILO_ACTIVO=False

                if self.HILO_ACTIVO:
                    if listaResultados != []:
                        # Si solo existe una carpeta con dicho nombre y especificaciones se obtiene su ID
                        if len(listaResultados) == 1:
                            print("Si existe la carpeta")
                            ID_SUPREMO = listaResultados[0][1]
                        # Si existe mas de una carpeta con dicho nombre y especificaciones entonces hay un error
                        else:
                            print("ERROR de repeticion de dos carpeta, arreglar cuanto antes")

                    ############################################################################################################################################
                    #   POSIBLE ERROR POR CONEXION DE RED 2:
                    #   SI  NO EXISTE EN DRIVE LA CARPETA EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES
                    #   SE CREARA LA CARPETA Y SE OBTENDRA SU ID
                    ############################################################################################################################################

                    else:
                        try:
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
                        except Exception as e:
                            self.senal_errorRed.emit((self.LISTA_ERRORES_RED[1], e))
                            self.HILO_ACTIVO=False

                    if self.HILO_ACTIVO:

                        # YA QUE SE TIENE EL ID DE LA CARPETA EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES..
                        ############################################################################################################################################
                        #   POSIBLE ERROR POR CONEXION DE RED 3:
                        #   SE OBTENDRA LA INFORMACION DE TODOS LOS ALUMNOS QUE HAN ENTREGADO LA TAREA
                        ############################################################################################################################################

                        try:

                            # formato del diccionario: dictEntregas[user_id] = [url, asignacion_id]
                            dictEntregas = self.classroom_control.list_submissions(
                                course_id=self.configuracionCalificador.curso_api_id,
                                coursework_id=courseWork_id,
                            )
                        except Exception as e:
                            self.senal_errorRed.emit((self.LISTA_ERRORES_RED[2], e))
                            self.HILO_ACTIVO=False

                        if self.HILO_ACTIVO:

                            RUTA_ASIGNACIONES = self.get_rutaAsignaciones()

                            datosTareas= (tuple(dictEntregas.items())[:NUMERO_TAREAS_CALIFICAR])
                            print("TAREAS A CALIFICAR: ",len(datosTareas) )
                            print("NUMERO DE TAREAS DESEADAS:",NUMERO_TAREAS_CALIFICAR)

                            if len(dictEntregas) > 0:
                                for user_id, url_or_idAsignacion in datosTareas:
                                    if self.HILO_ACTIVO is False:
                                        break

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
                                    ############################################################################################################################################
                                    #   POSIBLE ERROR POR CONEXION DE RED 4:
                                    #   DESCARGAR EL COLAB DEL ALUMNO
                                    ############################################################################################################################################
                                    try:

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
                                    except Exception as e:
                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[3], e))
                                        self.HILO_ACTIVO=False
                                        break


                                    ####################################################################################
                                    #  CALIFICANDO LA TAREA CON NBGRADER
                                    ####################################################################################

                                    resultadoAlCalificar = self.nbGrader_control.autograde(assignment_id=courseWork_name,
                                                                                           student_id=user_id)

                                    calificacionFinal = 0
                                    puntosTotales = 0
                                    exitoCalificar_conNbgrader = False

                                    if resultadoAlCalificar['success'] is True:
                                        exitoCalificar_conNbgrader = True
                                        calif = self.nbGrader_control.get_submission(assignment_id=courseWork_name,
                                                                                     student_id=user_id)
                                        puntosObtenidos = calif['score']
                                        puntosTotales = calif['max_score']
                                        print(puntosObtenidos, '/', puntosTotales)

                                        calificacionFinal=puntosObtenidos
                                        if puntosObtenidos > 100:
                                            calificacionFinal = 100

                                        # Si hubo exito al calificar la tarea entonces se puede crear la reotroalimentacion
                                        # estatus_retroalimentacion=self.nbGrader_control.generate_feedback(assignment_id=courseWork_name,student_id=user_id,force=True)

                                        nombreCopletoRetro = self.get_rutaRetroalimentacion() + user_id + '/' + courseWork_name + '/' + courseWork_name

                                        estatus_retroalimentacion = self.nbGrader_control.generate_feedback(
                                            assignment_id=courseWork_name,
                                            student_id=user_id, force=True)

                                        if estatus_retroalimentacion['success']:

                                            ############################################################################################################################################
                                            # SUBIENDO EL ARCHIVO A LA CARPETA DEL CURSO, OBTENIENDO SU LINK DE ACCESO Y POSTERIORMENTE MODIFICANDO SUS PERMISOS PARA UN ACCESO PUBLICO
                                            ############################################################################################################################################

                                            print("ID_SUPREMO:", ID_SUPREMO)
                                            nombreGuardaraArchivo = '{}_{}'.format(user_id,
                                                                                   courseWork_id)  # Id de los archivos   alumnoId_topicId_courseworkId_numeroVersion

                                            #############################################################################################
                                            # ADJUNTANDO EL NUMERO DE VERSION AL NOMBRE DEL ARCHIVO QUE SE DESEA SUBIR
                                            #############################################################################################

                                            ############################################################################################################################################
                                            #   POSIBLE ERROR POR CONEXION DE RED 5:
                                            #   OBTENER LA VERSION DEL ARCHIVO DE RETROALIMENTACION
                                            ############################################################################################################################################

                                            # Se busca la existencia de archivos con la palabra 'nombreGuardaraArchivo' contenida
                                            # trashed=False and mimeType!='application/vnd.google-apps.folder' and
                                            # fullText contains 'hello'
                                            query = "trashed=False and mimeType!='application/vnd.google-apps.folder' and fullText contains '{}'  and  '{}' in parents".format(
                                                nombreGuardaraArchivo, ID_SUPREMO)
                                            print("QUERY=", query)
                                            listaResultados = []

                                            try:
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
                                            except Exception as e:
                                                self.senal_errorRed.emit((self.LISTA_ERRORES_RED[4], e))
                                                self.HILO_ACTIVO=False
                                                break


                                            numeroVersionArchivo = len(listaResultados)
                                            nombreGuardaraArchivo += ('_{}.html'.format(numeroVersionArchivo))

                                            #############################################################################################
                                            # POSIBLE ERROR POR CONEXION DE RED 6:
                                            # SUBIENDO EL ARCHIVO Y OBTENIENDO SU LINK DE VISTA
                                            #############################################################################################

                                            file_metadata = {
                                                'name': nombreGuardaraArchivo,  # nombre que tendra en el archivo que se subira
                                                'parents': [ID_SUPREMO]
                                            }
                                            media = MediaFileUpload(nombreCopletoRetro + '.html',  # '.pdf',
                                                                    # nombre completo en donde se encuentra el archivo
                                                                    # mimetype='application/pdf',
                                                                    mimetype='application/json',
                                                                    # pdf=application/pdf   jpg=image/jpeg   html=application/json
                                                                    resumable=True)
                                            try:
                                                file = drive_service.files().create(body=file_metadata,
                                                                                    media_body=media,
                                                                                    fields='id,name,webContentLink,webViewLink'
                                                                                    ).execute()
                                            except Exception as e:
                                                self.senal_errorRed.emit((self.LISTA_ERRORES_RED[5], e))
                                                self.HILO_ACTIVO=False
                                                break


                                            # caracteristicas: https://developers.google.com/drive/api/v3/reference/files
                                            print('File ID: %s' % file.get('id'))
                                            print('File webView: %s' % file.get('webViewLink'))

                                            URL_RETROALIMENTACION = file.get('webViewLink')

                                            ID_RETROALIMENTACION = file.get('id')

                                            #############################################################################################
                                            # POSIBLE ERROR POR CONEXION DE RED 7:
                                            # DANDOLE ACCESO PUBLICO AL ARCHIVO COMPARTIDO
                                            #############################################################################################

                                            ID_ARCHIVO_COMPARTIR = ID_RETROALIMENTACION

                                            try:
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
                                            except Exception as e:
                                                self.senal_errorRed.emit((self.LISTA_ERRORES_RED[6], e))
                                                self.HILO_ACTIVO=False
                                                break

                                        else:
                                            # ocurrio un error al generar el reporte...
                                            continue


                                    if exitoCalificar_conNbgrader is False:
                                        calificacionFinal = 0
                                        URL_RETROALIMENTACION = RECURSO_EXPLICACION_ERROR

                                    #############################################################################################
                                    # SUBIENDO LOS RESULTADOS AL USUARIO
                                    #############################################################################################

                                    # RESPUESTA AL USUARIO
                                    studentSubmission = {
                                        'assignedGrade': calificacionFinal,
                                        'draftGrade': calificacionFinal,
                                        'state': 'RETURNED',
                                    }

                                    print("Id sudmision:", idAsignacion)

                                    #############################################################################################
                                    # POSIBLE ERROR POR CONEXION DE RED 9:
                                    # SUBIR LA CALIFICACION AL ALUMNO
                                    #############################################################################################
                                    try:
                                        pass
                                        # self.classroom_control.service_classroom.courses().courseWork().studentSubmissions().patch(
                                        #    courseId=self.configuracionCalificador.curso_api_id,
                                        #    courseWorkId=courseWork_id,
                                        #    id=idAsignacion,
                                        #    updateMask='assignedGrade,draftGrade',
                                        #    # updateMask='assignedGrade,draftGrade',
                                        #    body=studentSubmission).execute()
                                    except Exception as e:
                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[8], e))
                                        self.HILO_ACTIVO=False
                                        break


                                    request = {
                                        'addAttachments': [
                                            {
                                                'link': {
                                                    "url": URL_RETROALIMENTACION
                                                }
                                            }
                                        ]
                                    }
                                    coursework = self.classroom_control.service_classroom.courses().courseWork()

                                    #############################################################################################
                                    # POSIBLE ERROR POR CONEXION DE RED 8:
                                    # SUBIR EL LINK DE RETROALUMENTACION
                                    #############################################################################################
                                    try:
                                        pass
                                        # coursework.studentSubmissions().modifyAttachments(
                                        #    courseId=self.configuracionCalificador.curso_api_id,
                                        #    courseWorkId=courseWork_id,
                                        #    id=idAsignacion,
                                        #    body=request).execute()
                                    except Exception as e:
                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[7], e))
                                        self.HILO_ACTIVO=False
                                        break


                                    tuplaDatosEstudianteCalficado = (
                                        exitoCalificar_conNbgrader,
                                        user_id,  # id del estudiante
                                        user_id,  # id del estudiante
                                        calificacionFinal  # los puntos obtenidos
                                    )

                                    self.senal_unAlumnoCalificado.emit(tuplaDatosEstudianteCalficado)
                                    print("ESTUDIANTE: ", user_id, " TEMRINADO DE CALIFICAR")

                                    # no hubo exito al calificar...
                                    # else:
                                    #    print("PROBLEMAS AL CALIFICAR AUTOMATICAMENTE")
                                    #    print('ERROR:\n', '\t', resultadoAlCalificar['error'])
                                    #    print('LOG:\n', '\t', resultadoAlCalificar['log'])

                                print("TERMINANDO DE CALIFICAR A TODOS")
                                # solo si el hilo termino naturalmente
            self.senal_terminoCalificar.emit(self.HILO_ACTIVO)

    def activarHiloParaCalificar(self):
        self.HILO_ACTIVO=True

    def terminarHilo(self):
        self.HILO_ACTIVO=False


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


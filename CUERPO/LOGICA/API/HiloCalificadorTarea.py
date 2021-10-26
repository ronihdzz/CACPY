'''
HiloCalificadorTarea.py :
        Contiene una sola  clase, la clase 'HiloCalificadorTarea',la cual a grosso modo sirve
        para calificar las entregas de las tareas de los estudiantes
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"



# librerias estandar
import os.path
import os
import io

# Paquetes de terceros
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from googleapiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload

# fuente local
from CUERPO.LOGICA.API import FuncionesDrive


class HiloCalificadorTarea(QThread):
    '''
    Sirve para calificar las entregas de las tareas de los estudiantes
    '''


    senal_unAlumnoCalificado=pyqtSignal(tuple)     # se emitira un señal cuando se cierre
                                                   # el calificador para que se desbloque
                                                   # el programa
    senal_terminoCalificar=pyqtSignal(bool)

    # Errores de red...
    senal_errorRed=pyqtSignal(tuple )


    LISTA_ERRORES_RED=[
        "1) error al buscar la carpeta de la clase de classroom en donde se suben las retroalimentaciones,"
        "con el objetivo de obtener su id o crearla",

        "2) error al obtener la informacion de todas las asignaciones que han realizado los alumnos en la "
        "tarea respectiva",
        
        "3) error al obtener el correo electronico y nombre del alumno cuya tarea se esta calificando ",
        
        "4) error al buscar o crear la carpeta que contiene todas retroalimentaciones de todas las tareas "
        "de  un alumno en especifico",

        "5) error al buscar o crear la carpeta que contendra la retroalimentacion del estudiante de la tarea "
        " que se esta calificando",
        
        "6) error al descargar el colab de la tarea  del alumno",

        "7) error al obtener la version de la retroalimentacion de la tarea",

        "8) error al subir a drive la retroalimentacion del alumno",

        "9) error al compartir al estudiante el acceso a la vista de la carpeta de drive que almacena las "
        "retroalimetaciones de la tarea que se esta calificando ",

        "10) error al subir la calificacion de la tarea del alumno a classroom",

        "11) error al adjuntar el link para que accedan a la carpeta de retroalimentaciones de classroom"

    ]




    def __init__(self,configuracionCalificador,nbGrader_control,classroom_control):
        '''
        nbGrader_control : dicho objeto permitira calificar tareas de python que
        hayan sido creadas en la clase de NbGrader que se selecciono en el apartado:
        'Mis configuraciones'

        classRoomControl (objeto de la clase: ClassRoomControl): dicho objeto es una capa
        de abstracción para poder hacer algunas peticiones al ClassRoom del profesor, asi
        como al GoogleDrive del profesor

        configuracionCalificador (objeto de la clase: CalificadorConfiguracion): dicho objeto
        contiene ordenados los datos de configuracion que necesitara el programa, asi como tambien
        contiene metodos que serviran para obtener o editar dichos datos
        '''

        super().__init__()

        self.configuracionCalificador=configuracionCalificador
        self.nbGrader_control=nbGrader_control
        self.classroom_control=classroom_control

        self.courseWork_id=None
        self.courseWork_name=None

        self.noMaxEstudiantesCalificar=5 # valor default

        # variable bandera para determinar si el HILO seguira calificando o no tareas
        self.HILO_ACTIVO=True


    def setDatosTareaCalificar(self,nuevoCourseWork_id,nuevoCourseWork_name):
        '''
        Carga los datos de la tarea cuyas entregas que ha realizado los estudiantes desean
        ser calificadas.

        Parámetros:
            nuevoCourseWork_id (str): Representa el ID del courseWork cuyas entregas que han
            realizados los estudiantes desean ser calificadas
            nuevoCourseWork_name (str): Representa el NOMBRE del courseWork cuyas entregas que han
            realizados los estudiantes desean ser calificadas
        '''

        self.courseWork_id=nuevoCourseWork_id
        self.courseWork_name=nuevoCourseWork_name


    def setNoMaxEstudiantesCalificar(self,nuevoValor):
        '''
        Cambia el valor del numero de entregas maximas que se calificaran

        Parámetros:
            nuevoValor (int): Representa el numero maximo
            de entregas que se desean calificar
        '''

        self.noMaxEstudiantesCalificar=nuevoValor


    def activarHiloParaCalificar(self):
        '''
        Cuando se va a calificar entregas de tareas en el metodo 'run()' se pregunta si
        'self.HILO_ACTIVO' vale True, en caso de valer True, procedera a calificar, pero
        si vale False no calificara nada es decir no funcionara el metodo: 'run()'
        '''


        self.HILO_ACTIVO=True

    def terminarHilo(self):
        '''
        Cada vez que se califica una nueva entrega en el metodo 'run()' se pregunta si
        'self.HILO_ACTIVO' sigue valiendo True, en caso de no ser asi la calificacion
        de dichas tareas se detendra, y este es el objetivo de dicho metodo, cambiar
        el valor de: 'self.HILO_ACTIVO' para que este pueda ocacionar la detencion
        prematura de la calificancion de entregas que se este realizando en el metodo
        'run()'
        '''

        self.HILO_ACTIVO=False


    def get_rutaAsignaciones(self):
        '''
        Returns:
            Dato de tipo: 'str' que representara la ruta especifica en donde deberan
            adjuntarse todas las  entregas de todos los estudiantes.Es importante
            mencionar que para que: NbGrader pueda calificar las entregas estan deberan
            ubicarse en dicha direccion.
        '''


        if self.nbGrader_control:
            ubicacionCurso=self.nbGrader_control.config.CourseDirectory.root
            print("UBICACION DEL CURSO...",ubicacionCurso)
            ubicacionCurso+='submitted/'
            return ubicacionCurso

    def get_rutaRetroalimentacion(self):
        '''
        Returns:
            Dato de tipo: 'str' que representa la ruta especifica en donde NbGrader
            alojara las retroalimentaciones de los estudiante cuyas entregas vaya
            calificando
        '''

        if self.nbGrader_control:
            ubicacionCurso=self.nbGrader_control.config.CourseDirectory.root
            print("UBICACION DEL CURSO...",ubicacionCurso)
            ubicacionCurso+='feedback/'
            return ubicacionCurso




    def run(self):
        '''
        Calificara las entregas de los estudiantes de la tarea cuyo ID es  igual al valor del atributo de
        instancia: 'self.courseWork_id' tarea la cual se encuentra dentro de la clase de google classroom
        y topic de google classroom que el usuario selecciono en el apartado de: 'Mis configuraciones'.

        Es importante mencionar que solo calificara un determinado numero de entregas y dicho determinado
        numero correspondera al valor del atributo de instancia: 'self.noMaxEstudiantesCalificar'

        El objetivo de realizar la calificacion de las entregas por medio de este hilo es evitar que se
        congele la GUI mientras se estan calificando las entregas de la tarea.


        Es importante mencionar lo siguiente:

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

        Es importante mencionar que:
            * Si al calificar se presenta algun error, el hilo mandara una señal con el
              error presentado, y automaticamente dejara de calificar las tareas de programación.
            * Por cada entrega que califica exitosamente se emitira una señal con el objetivo de informar
            cual alumno fue calificado y cuanto obtuvo de calificacion
            * Si se detecta que un alumno entrego un material que no era el de la tarea se emitira una señal
            con el objetivo de informar que  alumno fue el que presento el error.
            * Cuando se termine de ejecutarse este metodo, se emitira una señal
        '''

        NUMERO_TAREAS_CALIFICAR=self.noMaxEstudiantesCalificar

        if self.HILO_ACTIVO:
            if self.courseWork_name and self.courseWork_id:

                courseWork_name = self.courseWork_name
                courseWork_id = self.courseWork_id

                # OBTENIENDO EL ID DE LA CARPETA EN DONDE SE ADJUNTARAN TODAS LAS RETROALIMENTACIONES
                folder_id = self.configuracionCalificador.getIdApiCarpetaRetro()
                idClase,nombreClase=self.configuracionCalificador.get_id_nombre_cursoClassroom()

                # obteniendo el nombre de la carpeta en donde se adjuntaran UNICAMENTE las retroalimentaciones
                # de los alumnos que pertenecen a la clase de classroom que el usuario selecciono en el apartado
                # de: 'Mis configuraciones'
                nombreCarpetaCurso = "{}_{}".format(nombreClase,idClase)  # sera el id del curso

                drive_service = self.classroom_control.service_drive
                page_token = None

                ############################################################################################################################################
                #   POSIBLE ERROR POR CONEXION DE RED 1:
                #   ¿EXISTE EN DRIVE LA CARPETA DE LA CLASE DE CLASSROOM EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES?
                ############################################################################################################################################

                print("*" * 100)
                print("PASO 1: ¿EXISTE EN DRIVE LA CARPETA DE LA CLASE DE CLASSROOM EN DONDE SE SUBIRAN LAS RETROALIMENTACIONES?")

                # obteniendo el id o creando la carpeta donde se guardara las retroalimentaciones
                # de la clase de classroom que el usuario selecciono en el apartado de: 'Mis configuraciones'
                respuesta=FuncionesDrive.getId_carpeta(nombre=nombreCarpetaCurso,
                                                       idCarpetaAlmacena=folder_id,
                                                       intermediarioAPI_drive=drive_service)

                if respuesta['exito'] is False:
                    errorPresentado=respuesta['resultado']
                    self.HILO_ACTIVO = False
                    self.senal_errorRed.emit((self.LISTA_ERRORES_RED[0],errorPresentado))

                else:
                    id_carpetaRetroClase=respuesta['resultado']['id']


                    ############################################################################################################################################
                    #   POSIBLE ERROR POR CONEXION DE RED 2:
                    #   OBTENIENDO LA INFORMACIÓN DE TODAS LAS ENTREGAS HECHAS POR LOS ALUMNOS EN LA TAREA RESPECTIVA
                    ############################################################################################################################################

                    try:
                        print("*" * 100)
                        print("PASO 2: OBTENIENDO LA INFORMACIÓN DE TODAS  LAS ENTREGAS HECHAS POR LOS ALUMNOS EN LA TAREA RESPECTIVA")

                        # formato del diccionario: dictEntregasEstudiantes_deTarea[user_id] = [listaAttachments, asignacion_id]
                        dictEntregasEstudiantes_deTarea = self.classroom_control.getEntregasDeEstudiantes(
                            course_id=self.configuracionCalificador.curso_idApi,
                            coursework_id=courseWork_id,
                        )

                    except Exception as e:
                        self.HILO_ACTIVO = False
                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[1], e))


                    if self.HILO_ACTIVO:
                        ruta_asignaciones_nbgrader = self.get_rutaAsignaciones()

                        # ¿hay por lo menos una entrega de un estudiante que calificar?
                        if len(dictEntregasEstudiantes_deTarea) > 0:
                            for user_id, listaAttachments_y_idAsginacion in tuple(dictEntregasEstudiantes_deTarea.items())[:NUMERO_TAREAS_CALIFICAR]:

                                # se parte de que el estudiante entrego la tarea de forma correcta
                                sin_errorEntregaTareaPorEstudiante=True

                                # calificacion de la tarea del estudiante
                                calificacionFinal=0

                                listaAttachments,idAsignacion = listaAttachments_y_idAsginacion


                                ############################################################################################################################################
                                #   POSIBLE ERROR POR CONEXION DE RED 3
                                #   Obteniendo el correo y el nombre del alumno que se esta calificando
                                ############################################################################################################################################

                                print("*" * 100)
                                print("PASO 3: Obteniendo el correo y el nombre del alumno que se esta calificando")
                                try:
                                    correoAlumno, nombreAlumno = self.classroom_control.get_datosAlumno(
                                        idAlumno=user_id)
                                    print(f"Calificando a: {nombreAlumno} cuyo correo es: {correoAlumno} la tarea: {courseWork_name}")
                                    print("id estudiante:",user_id)
                                
                                except Exception as e:
                                    self.HILO_ACTIVO = False
                                    self.senal_errorRed.emit((self.LISTA_ERRORES_RED[2], e))
                                    break

                                ############################################################################################################################################
                                #
                                #   3.1) OBTENIENDO EL LINK DE LA ENTREGA DE LA TAREA DEL ALUMNO
                                ############################################################################################################################################

                                print("*" * 100)
                                print("PASO 3.1: OBTENIENDO EL LINK DE LA ENTREGA DE LA TAREA DEL ALUMNO")

                                try:

                                    # cada entrega del estudiante debe tener solo  un archivo adjunto
                                    # el cual  debe ser el colab
                                    numeroAttachmentsRegistrados = len(listaAttachments)

                                    assert (numeroAttachmentsRegistrados==1)

                                    # de cada entrega de cada estudiante se espera un documento de google colab
                                    # al inicio de la entrega por ende a continuacion se obtienE su link para
                                    # posteriormente poder descargarlo
                                    url_colabEntregadoPorEstudiante=listaAttachments[0]['driveFile']['alternateLink']

                                    # FORMATO DE LINK: 'https://drive.google.com/file/d/1m-LNYFiQeNKeeGRxo03dPg5HMrzQI3Wl/view?usp=drive_web'
                                    id_colabEntregadoPorEstudiante = url_colabEntregadoPorEstudiante.split('/')[-2]

                                except:
                                    # el alumno entrego una cosa diferente a un documento colab, entre otras cosas
                                    sin_errorEntregaTareaPorEstudiante=False


                                if sin_errorEntregaTareaPorEstudiante:

                                    ############################################################################################################################################
                                    #   POSIBLE ERROR POR CONEXION DE RED 4
                                    #   Buscando o creando la carpeta que contiene todas retroalimentaciones de todas las tareas de  un alumno en especifico
                                    ############################################################################################################################################

                                    print("*" * 100)
                                    print("PASO 4: Buscando o creando la carpeta que contiene todas retroalimentaciones de todas las "
                                          "tareas de  un alumno en especifico")

                                    # Buscando si ya existe una carpeta con el id del estudiante la cual es donde
                                    # se almacenan todas las retroalimentaciones de sus tareas entregadas
                                    respuesta=FuncionesDrive.getId_carpeta(
                                        nombre=user_id,
                                        idCarpetaAlmacena=id_carpetaRetroClase,
                                        intermediarioAPI_drive=drive_service
                                    )

                                    if respuesta['exito'] is False:
                                        errorPresentado = respuesta['resultado']
                                        self.HILO_ACTIVO = False
                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[1], errorPresentado))
                                        break

                                    else:
                                        id_carpetaRetroEstudiante=respuesta['resultado']['id']

                                        ############################################################################################################################################
                                        #   POSIBLE ERROR POR CONEXION DE RED 5
                                        #   Buscando o creando la carpeta que contendra la retroalimentacion de la tarea que se esta calificando
                                        ############################################################################################################################################

                                        print("*" * 100)
                                        print("PASO 5: Buscando o creando la carpeta que contendra la retroalimentacion del estudiante de la tarea que se esta calificando")

                                        # Buscando o creando la carpeta que contendra la retroalimentacion
                                        # de la tarea que se esta calificando
                                        respuesta = FuncionesDrive.getId_carpeta(
                                            nombre=courseWork_name,
                                            idCarpetaAlmacena=id_carpetaRetroEstudiante,
                                            intermediarioAPI_drive=drive_service
                                        )

                                        if respuesta['exito'] is False:
                                            errorPresentado = respuesta['resultado']
                                            self.HILO_ACTIVO = False
                                            self.senal_errorRed.emit((self.LISTA_ERRORES_RED[4], errorPresentado))
                                            break


                                        id_carpetaRetroTareaEstudiante= respuesta['resultado']['id']
                                        webViewLink_carpetaRetroTareaEstudiante= respuesta['resultado']['webViewLink']

                                        ####################################################################################
                                        #  OBTENIENDO EL NOMBRE EN DONDE SE DESCARGARA LA TAREA ENTREGADA POR EL USUARIO
                                        ####################################################################################

                                        ruta_descargaraColabTareaEntregada = ruta_asignaciones_nbgrader + user_id + '/' + courseWork_name + '/'
                                        os.makedirs(ruta_descargaraColabTareaEntregada, exist_ok=True)
                                        nombreCompleto_colabEntregado = ruta_descargaraColabTareaEntregada + courseWork_name + '.ipynb'

                                        ####################################################################################
                                        #  DESCARGANDO LA ASIGNACION DEL ESTUDIANTE EN LA RUTA DEBIDA
                                        ####################################################################################

                                        if os.path.exists(nombreCompleto_colabEntregado):
                                            os.remove(nombreCompleto_colabEntregado)

                                        # Descargando el archivo en la ruta debida
                                        ############################################################################################################################################
                                        #   POSIBLE ERROR POR CONEXION DE RED 6:
                                        #   DESCARGAR EL COLAB DEL ALUMNO
                                        ############################################################################################################################################
                                        try:
                                            print("*" * 100)
                                            print("PASO 6: Descargando el colab entregado por el estudiante")

                                            request = self.classroom_control.service_drive.files().get_media(fileId=id_colabEntregadoPorEstudiante)
                                            fh = io.BytesIO()
                                            downloader = MediaIoBaseDownload(fh, request)
                                            done = False
                                            while done is False:
                                                status, done = downloader.next_chunk()
                                                print("Download %d%%." % int(status.progress() * 100))

                                            fh.seek(0)
                                            with open(nombreCompleto_colabEntregado, 'wb') as f:
                                                print("Archivo descargado en:",nombreCompleto_colabEntregado)
                                                f.write(fh.read())
                                                f.close()
                                        except Exception as e:
                                            #self.HILO_ACTIVO = False
                                            #self.senal_errorRed.emit( (self.LISTA_ERRORES_RED[5],e)  )
                                            #break
                                            sin_errorEntregaTareaPorEstudiante=False
                                            print("ERROR AL DESCARGAR LA ENTREGA DEL ESTUDIANTE:")
                                            print(e)

                                        if sin_errorEntregaTareaPorEstudiante:

                                            ####################################################################################
                                            #  CALIFICANDO LA TAREA CON NBGRADER
                                            ####################################################################################

                                            print("*" * 100)
                                            print("PASO 6.1: CALIFICANDO TAREA ")
                                            resultadoAlCalificar = self.nbGrader_control.autograde(assignment_id=courseWork_name,
                                                                                                   student_id=user_id)

                                            if resultadoAlCalificar['success'] != True:
                                                sin_errorEntregaTareaPorEstudiante=False

                                                print("ERROR AL CALIFICAR LA TAREA DE PROGRAMACION..")
                                                print(resultadoAlCalificar['error'])
                                                print(resultadoAlCalificar['log'])

                                            else:


                                                calif = self.nbGrader_control.get_submission(assignment_id=courseWork_name,
                                                                                             student_id=user_id)
                                                puntosObtenidos = calif['score']

                                                # todas las tareas que se califiquen se calificaran baja 100 puntos
                                                # por ende si hay tareas que al calificarlas dan mas de 100 puntos
                                                # la calificacion sera 100 puntos
                                                calificacionFinal=puntosObtenidos
                                                if puntosObtenidos > 100:
                                                    calificacionFinal = 100.0
                                                
                                                print("Calificacion obtenida:",calificacionFinal)

                                                # Si hubo exito al calificar la tarea entonces se puede crear la reotroalimentacion
                                                # estatus_retroalimentacion=self.nbGrader_control.generate_feedback(assignment_id=courseWork_name,student_id=user_id,force=True)
                                                nombre_completoRetro = self.get_rutaRetroalimentacion() + user_id + '/' + courseWork_name + '/' + courseWork_name

                                                print("*" * 100)
                                                print("PASO 6.2: OBTENIENDO RETROALIMENTACION DE LA TAREA")

                                                # obteniendo la retroalimentacion de la tarea
                                                estatus_retroalimentacion = self.nbGrader_control.generate_feedback(
                                                    assignment_id=courseWork_name,
                                                    student_id=user_id, force=True)

                                                if estatus_retroalimentacion['success'] != True:

                                                    # si es obtuvo un error al caliciar con NbGrader o al obtener
                                                    # la retroalimentacion del alumno, lo mas probable es que se
                                                    # debe a una entrega de la tarea del estudiante
                                                    sin_errorEntregaTareaPorEstudiante = False

                                                    print("ERROR AL OBTENER LA RETROALIMENTACION...")
                                                    print(estatus_retroalimentacion['error'])
                                                    print(estatus_retroalimentacion['log'])

                                                else:
                                                    # nombre con el cual se guardara la retroalimentacion en google drive
                                                    nombreRetro_drive=courseWork_name


                                                    ############################################################################################################################################
                                                    #   POSIBLE ERROR POR CONEXION DE RED 7:
                                                    #   OBTENER LA VERSION DEL ARCHIVO DE RETROALIMENTACION
                                                    ############################################################################################################################################

                                                    # Se busca la existencia de archivos con la palabra que almacena la variable: 'nombreRetro_drive'
                                                    # en la carpeta con id igual al valor que almacena en la variable: 'id_carpetaRetroTareaEstudiante'
                                                    # los archivos que se buscan se indican que no estan en la papelera de reciclaje del drive
                                                    query = "trashed=False and '{}' in parents".format(id_carpetaRetroTareaEstudiante)
                                                    listaResultados = []

                                                    try:
                                                        print("*" * 100)
                                                        print("PASO 7: OBTENIENDO LA VERSION DEL ARCHIVO DE RETROALIMENTACION", id_carpetaRetroClase)
                                                        print("QUERY=", query)
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
                                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[6], e))
                                                        self.HILO_ACTIVO=False
                                                        break

                                                    # como se dejara que los alumnos entregen mas de una vez una misma tarea,
                                                    # entonces en la carpeta en donde se suben las retroalimentaciones de una
                                                    # tarea y estudiante especifico, podra tener mas de un archivo, lo cual
                                                    # indirectamente indicara cuantas veces ha intentado una misma tarea un
                                                    # alumno
                                                    numeroVersionArchivo = len(listaResultados)
                                                    nombreRetro_drive += ('_intento_{}.html'.format(numeroVersionArchivo+1))

                                                    #############################################################################################
                                                    # POSIBLE ERROR POR CONEXION DE RED 8:
                                                    # SUBIENDO LA RETROALIMENTACION DEL ESTUDIANTE A LA CARPETA DE DRIVE
                                                    #############################################################################################

                                                    file_metadata = {
                                                        'name': nombreRetro_drive,  # nombre que tendra en el archivo que se subira
                                                        'parents': [id_carpetaRetroTareaEstudiante]
                                                    }
                                                    media = MediaFileUpload(nombre_completoRetro + '.html',  # '.pdf',
                                                                            # nombre completo en donde se encuentra el archivo
                                                                            # mimetype='application/pdf',
                                                                            mimetype='application/json',
                                                                            # pdf=application/pdf   jpg=image/jpeg   html=application/json
                                                                            resumable=True)
                                                    try:
                                                        print("*" * 100)
                                                        print("PASO 8: SUBIENDO LA RETROALIMENTACION DEL ESTUDIANTE EN DRIVE")
                                                        file = drive_service.files().create(body=file_metadata,
                                                                                            media_body=media,
                                                                                            fields='id,name,webContentLink,webViewLink'
                                                                                            ).execute()
                                                    except Exception as e:
                                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[7], e))
                                                        self.HILO_ACTIVO=False
                                                        break


                                                    #############################################################################################
                                                    # POSIBLE ERROR POR CONEXION DE RED 9:
                                                    # COMPARTIR EL ACCESO A VISTA A LA CARPETA QUE ALMACENA LAS RETROALIMENTACIONES
                                                    #############################################################################################

                                                    print("*" * 100)
                                                    print("PASO 9: COMPARTIR EL ACCESO A VISTA A LA CARPETA QUE ALMACENA LAS RETROALIMENTACIONES ")
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
                                                            'type': 'user',   # compartir a un usuario en especifico
                                                            'role': 'reader', # los permisos compartidos seran unicamente de lector
                                                            'emailAddress': correoAlumno # correo electronico del usuario que tendra acceso a esta carpeta
                                                        }
                                                        batch.add(drive_service.permissions().create(
                                                            fileId=id_carpetaRetroTareaEstudiante,
                                                            body=user_permission,
                                                            fields='id'
                                                        ))
                                                        batch.execute()
                                                    except Exception as e:
                                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[8], e))
                                                        self.HILO_ACTIVO=False
                                                        break


                                                    #############################################################################################
                                                    # POSIBLE ERROR POR CONEXION DE RED 10:
                                                    # SUBIR LA CALIFICACION AL ALUMNO
                                                    #############################################################################################

                                                    # Respuesta que le dara al estudiante
                                                    studentSubmission = {
                                                        'assignedGrade': calificacionFinal,
                                                        'draftGrade': calificacionFinal
                                                    }

                                                    try:
                                                        print("*" * 100)
                                                        print("PASO 10: SUBIENDO CALIFICAION AL ALUMNO ")
                                                        self.classroom_control.service_classroom.courses().courseWork().studentSubmissions().patch(
                                                            courseId=self.configuracionCalificador.curso_idApi,
                                                            courseWorkId=courseWork_id,
                                                            id=idAsignacion,
                                                            updateMask='draftGrade,assignedGrade',
                                                            body=studentSubmission).execute()
                                                    except Exception as e:
                                                        print(e)
                                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[9], e))
                                                        self.HILO_ACTIVO=False
                                                        break



                                                    #############################################################################################
                                                    # POSIBLE ERROR POR CONEXION DE RED 11:
                                                    # SUBIR EL LINK DE RETROALUMENTACION
                                                    #############################################################################################

                                                    # Mensaje de retroalimentacion que se le adjuntara al estudiante
                                                    request = {
                                                        'addAttachments': [
                                                            {
                                                                'link': {
                                                                    "url": webViewLink_carpetaRetroTareaEstudiante
                                                                }
                                                            }
                                                        ]
                                                    }

                                                    try:
                                                        print("*" * 100)
                                                        print("PASO 11: ADJUNTANDO RETROALIMENTACION AL ALUMNO")
                                                        self.classroom_control.service_classroom.courses().courseWork().studentSubmissions().modifyAttachments(
                                                            courseId=self.configuracionCalificador.curso_idApi,
                                                            courseWorkId=courseWork_id,
                                                            id=idAsignacion,
                                                            body=request).execute()
                                                    except Exception as e:
                                                        print(e)
                                                        self.senal_errorRed.emit((self.LISTA_ERRORES_RED[10], e))
                                                        self.HILO_ACTIVO=False
                                                        break


                                tuplaDatosEstudianteCalficado = (
                                    sin_errorEntregaTareaPorEstudiante,
                                    nombreAlumno,  # id del estudiante
                                    correoAlumno,  # id del estudiante
                                    calificacionFinal  # los puntos obtenidos
                                )

                                self.senal_unAlumnoCalificado.emit(tuplaDatosEstudianteCalficado)
                                print(f"ESTUDIANTE: nombre:{nombreAlumno} con correo:{correoAlumno} TEMRINADO DE CALIFICAR")

                            print("TERMINANDO DE CALIFICAR A TODOS")
                            # solo si el hilo termino naturalmente

            # si el hilo termina naturalmente el valor de: 'self.HILO_ACTIVO' sera igual a True
            self.senal_terminoCalificar.emit(self.HILO_ACTIVO)


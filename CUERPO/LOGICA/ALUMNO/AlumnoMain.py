'''
AlumnoMain.py :
                    Contiene una sola  clase, la clase 'Alumno',  la cual a grosso
                    modo sirve para mostrar las lista de correos y nombres de los
                    alumnos inscritos a la clase de classroom seleccionada,y tambien
                    sirve para poder las califaciones de todas las tareas de cada
                    estudiantes asi como tambien sirve para ver todas las
                    retroalimentaciones de los ejercicios de programacion de cada alumno.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import Qt

###########################################################################################################################################
# fuente local
###########################################################################################################################################

import recursos
from CUERPO.LOGICA.API import FuncionesDrive
from CUERPO.DISENO.ALUMNO.AlumnoMain_d import Ui_Form


class AlumnoMain(QtWidgets.QWidget,Ui_Form,recursos.HuellaAplicacion):
    '''
    Sirve para mostrar las lista de correos y nombres de los
    alumnos inscritos a la clase de classroom seleccionada,y tambien
    sirve para poder ver las califaciones de todas las tareas de cada
    estudiante asi como tambien sirve para ver todas las
    retroalimentaciones de los ejercicios de programacion de cada alumno.
    '''



    def __init__(self,baseDatosLocalClassRoom,classRoomControl,configuracionCalificador):
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

        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)

        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador

        self.btn_refrescarListaAlumnos.clicked.connect(self.cargarEstudiantes_claseClassroomSelec)
        self.tableWidget_alumnos.installEventFilter(self)

        self.configurarTablasApartadoMisAlumnos()

        self.tableWidget_alumnos.itemDoubleClicked.connect(self.verDetallesEstudiante)
        self.btn_regresar.clicked.connect(lambda : self.listWidget.setCurrentIndex(0) )
        self.listaIdsEstudiantes=[]


        self.mostrarDatosCurso()


        self.textBrowser_datosEstudiante.setOpenExternalLinks(True)
        self.textBrowser_datosEstudiante.setOpenLinks(True)
        self.textBrowser_datosEstudiante.setReadOnly(True)

##################################################################################################################################################
# ESTUDIANTE SELECCIONADO
##################################################################################################################################################

    def actuarAnteCambio_claseClassroom(self):
        '''
        Por cada clase de classroom hay diferentes alumnos inscritos a estas, por tal
        motivo cuando el usuario cambia de clase de classroom se debe llamar a este
        metodo ya que lo que hace este metodo es:
            - Si tenia cargados en la tabla los nombres y correos de los alumnos
             de la clase de classroom que antes estaba seleccionada, los borrara
            - Mostrara el nombre de la clase de classroom nueva seleccionada en la
            label respectiva de la GUI
        '''

        self.borrarListaAlumnos()
        self.mostrarDatosCurso()

    def borrarListaAlumnos(self):
        '''
        Borrara todos los datos contenidos en la tabla en donde se muestran los nombres y correos
        electronicos de los alumnos de la clase de classroom seleccionada.
        '''

        self.tableWidget_alumnos.setRowCount(0)
        self.listaIdsEstudiantes = []

    def mostrarDatosCurso(self):
        '''
        Mostrara el nombre de la clase de classroom selecciona en la label respectiva
        de la GUI.
        '''

        nombreCurso=self.configuracionCalificador.getNombre_cursoClassroom()
        self.bel_numeroAlumnos.setText("0")

        if nombreCurso!=None:
            self.bel_nombreCurso.setText(nombreCurso)


    def cargarEstudiantes_claseClassroomSelec(self):
        '''
        Hara una consulta a la API de google classroom para saber cuales son los datos
        de los alumnos inscritos a la clase de classroom seleccionada, posteriormente
        mostrara en una tabla los nombres y correos electronicos de los alumnos inscritos
        a la clase de classroom seleccionada.
        '''


        seDeseaCargarListaAlumnos=self.msg_preguntarAcercaRefrescarListaEstudiantes()

        if seDeseaCargarListaAlumnos:
            claseClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

            # el metodo 'get_listaAlumnos' retorna los datos de cada alumno de la siguiente
            # forma:
            # (   (idEstudiante_1,nombreCompleto_1,correoElectronico_1),
            #     (idEstudiante_2,nombreCompleto_2,correoElectronico_2),
            #                           .
            #                           .
            #                           .
            #  )
            datosAlumnosInscritosClase=self.classRoomControl.get_listaAlumnos(claseClassroom_id)
            self.listaIdsEstudiantes=[]
            numeroAlumnosInscritos=len(datosAlumnosInscritosClase)

            if numeroAlumnosInscritos>0:
                self.tableWidget_alumnos.setRowCount(numeroAlumnosInscritos)
                self.bel_numeroAlumnos.setText(str(numeroAlumnosInscritos))

            for r,datosAlumno in enumerate(datosAlumnosInscritosClase):

                idAlumno,nombreAlumno,correoAlumno=datosAlumno
                self.listaIdsEstudiantes.append(idAlumno)

                # nombre del alumno
                a = QtWidgets.QTableWidgetItem(nombreAlumno)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_alumnos.setItem(r, 0, a)

                # correo electronico del alumno
                a = QtWidgets.QTableWidgetItem(correoAlumno)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_alumnos.setItem(r, 1, a)

            self.msg_exitoAlRefrescar()

    def eventFilter(self, source, event):
        """
        Este metodo se encarga de mostrar un menu  con la leyenda: 'eliminar',
        cuando  el usuario le de clic derecho a algun renglon de la tabla de
        la lista de alumnos inscritos a la clase de classroom seleccionada.
        Si el usuario da clic izquierdo sobre la leyenda 'eliminar' este metodo
        se encargara de iniciar el proceso de eliminacion del alumno que se encuentra
        en el renglon en donde el usuario dio clic derecho.
        """


        if event.type() == QtCore.QEvent.ContextMenu and source is self.tableWidget_alumnos:

            try:
                # La excepccion se adjunta por que si el usuario da clic derecho sobre cualquier parte
                # de la tabla que no se es un renglon, entonces la variable: 'item' tomara el valor
                # de: 'None', y cuando se realice: 'item.row()' habra un error por que el
                # valor None no tiene el metodo 'row()', por tal motivo se coloca la excepccion

                item = source.itemAt(event.pos())
                indiceEliminar = item.row()

                menu = QtWidgets.QMenu()
                menu.addAction("eliminar")  # menu.addAction("eliminar",metodoA_llamar)

                if menu.exec_(event.globalPos()):
                    self.eliminarEstudiante(indiceEliminar)

            except Exception as e:
                pass

            return True
        return super().eventFilter(source, event)

    def eliminarEstudiante(self,numeroRenglon):
        '''
        Se encargara de eliminar el estudiante que se encuentra en la posicion: 'numeroRenglon'
        de la tabla de estudiantes inscritos a la clase de classroom seleccionada.

        Al eliminar al estudiante que se encuentra en la posicion: 'numeroRenglon' de la tabla
        de estudiantes inscritos a la clase de classroom seleccionada.
            * Se eliminara eliminara unicamente de la tabla, por tal motivo si se diera clic en
            el boton de refrescar volverian a aparecer los estudiantes eliminados
        '''

        # primero se pregunta si en realidad se desea eliminar al estudiante seleccionado
        respuestaPositiva=self.msg_preguntarEleccionBorrarEstudiante(
            estudianteEliminar=self.tableWidget_alumnos.item(numeroRenglon, 0).text()
        )

        if respuestaPositiva:
            self.tableWidget_alumnos.removeRow(numeroRenglon)
            self.listaIdsEstudiantes.pop(numeroRenglon)


##################################################################################################################################################
# ESTUDIANTE SELECCIONADO
##################################################################################################################################################

    def verDetallesEstudiante(self,index):
        '''
        Este metodo se llamara cuando el usuario haya dado doble clic izquierdo sobre el renglon
        en donde se encuentran almacenados los datos de un alumno en especifico.
        Lo que hara este metodo es mostrar los datos del alumno seleccionado, es decir mostrara:
            * El nombre del alumno
            * El correo del alumno
            * El link para acceder a la carpeta de retroalimentaciones del alumno
            * Las calificaciones de todas las tareas del alumno seleccionado
        '''

        # obteniendo el numero de renglon en el cual se encuentra
        # almacenado el nombre del alumno seleccionado
        index = index.row()


        # obteniendo el nombre del alumno seleccionado
        nombre = self.tableWidget_alumnos.item(index,0).text()

        # obteniendo el correo del alumno seleccionado
        correo=self.tableWidget_alumnos.item(index, 1).text()

        # obteniendo el ID del alumno seleccionado
        idEstudiante = self.listaIdsEstudiantes[index]

        # obteniendo el link de acceso a la carpeta de google drive
        # en donde se almacenan todas las retroalimentaciones del alumno
        # seleccionado
        linkCarpetaRetroalimentacion=self.getLinkCarpetaRetroAlumno(
            user_id=idEstudiante
        )

        # agrupando los datos del alumno en un formato de html
        htmlEstudiante=self.generarHtmlEstudianteMostrar(
            nombre=nombre,
            correo=correo,
            linkCarpetaRetroalimentacion=linkCarpetaRetroalimentacion,
        )

        # mostrando los datos del alumno
        self.textBrowser_datosEstudiante.setHtml(htmlEstudiante)

        # cargando en una  tabla las calificaciones de las tareas del alumno
        # seleccionado
        self.cargarCalificacionesAlumnoSelec(idEstudiante=idEstudiante)


        # cambiando a la ventana en donde se mostraran los datos del alumno seleccionado
        self.listWidget.setCurrentIndex(1)

    def getLinkCarpetaRetroAlumno(self,user_id):
        '''
        Este metodo retornara el link de acceso a la carpeta de google drive en donde
        se suben todas las retroaliemntaciones del estudiante cuyo ID es igual al valor
        que almacena el parametro: 'user_id'

        Returns:
            Dato de tipo: 'str' que representa el link de acceso a la carpeta de google drive en donde
            se suben todas las retroaliemntaciones del estudiante cuyo ID es igual al valor
            que almacena el parametro: 'user_id'
        '''



        ID_carpetaAlmacenadoraRetro = self.configuracionCalificador.getIdApiCarpetaRetro()
        ID_claseClassroom, nombre_claseClassroom = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        # obteniendo el nombre de la carpeta en donde se almacenan todas las retroalimentaciones de todos los alumnos
        # de la clase de classroom seleccionada
        nombre_carpetaAlmacenaRetro_cursoClassroom = "{}_{}".format(nombre_claseClassroom,ID_claseClassroom)

        # obteniendo el ID de la carpeta que almacena donde se almacenan todas las retroalimentaciones de todos los alumnos
        # de la clase de classroom seleccionada, en caso de que la carpeta no existe entonces se creara y despues se retornara
        # el ID
        respuesta = FuncionesDrive.getId_carpeta(nombre=nombre_carpetaAlmacenaRetro_cursoClassroom,
                                                 idCarpetaAlmacena=ID_carpetaAlmacenadoraRetro,
                                                 intermediarioAPI_drive=self.classRoomControl.service_drive)

        if respuesta['exito'] is False:
            errorPresentado = respuesta['resultado']
            print(errorPresentado)

        else:
            ID_carpetaAlmacenaRetro_cursoClassroom = respuesta['resultado']['id']

            #   Buscando o creando la carpeta que contiene todas retroalimentaciones de todas las tareas de  un alumno en especifico
            # Buscando si ya existe una carpeta con el id del estudiante la cual es donde
            # se almacenan todas las retroalimentaciones de sus tareas entragadas
            respuesta = FuncionesDrive.getId_carpeta(
                nombre=user_id,
                idCarpetaAlmacena=ID_carpetaAlmacenaRetro_cursoClassroom,
                intermediarioAPI_drive=self.classRoomControl.service_drive
            )

            if respuesta['exito'] is False:
                errorPresentado = respuesta['resultado']
                print(errorPresentado)
            else:
                # obteniendo el link de acceso a la carpeta de google drive en donde estan todas
                # las retroalimentaciones del estuiante seleccionao
                link_carpetaEstudiante=respuesta['resultado']['webViewLink']
                return link_carpetaEstudiante

        return None

    def generarHtmlEstudianteMostrar(self, nombre, correo, linkCarpetaRetroalimentacion):
        '''
        Este metodo generara el html que agrupa los datos del alumno que el usuario quiere
        ver, es decir agrupa en formato html:
            * El nombre del alumno
            * El correo del alumno
            * Y el link para acceder a la carpeta de retroalimentaciones del alumno

        Una vez creada el html con dichos datos, proseguira a retornar dicho html

        Parámetros:
            - nombre (str) : Nombre del alumno que el usuario selecciono para ver
            - correo (str) : Correo electronico del alumno que el usuario selecciono
            para ver
            - linkRetroalimentacion (str): Link que da acceso a la carpeta de google
            drive en donde se almacenan todas las retroalimentaciones de todas las
            tareas de programacion que ha entregado el alumno que el usuario selecciono

        Returns:
            - Este metodo retorna un dato de tipo 'str' el cual representa el codigo
            que contiene agrupados todos los datos mencionados anteriormente
        '''

        htmlEstudiante = f'''
        <p>
            <span style=" font-size:16px;font-family: TamilSangamMN;"> 
            Estudiante: {nombre}
            </span>
            <br>
            <br>

            <span style=" font-size:12px;font-family: TamilSangamMN;"> 
            Correo: {correo}
            </span>
            <br>
            <br>

            <span style=" font-size:12px;font-family: TamilSangamMN;"> 
             Retroalimentaciones:
            </span>

            <span style=" font-size:12px;font-family: TamilSangamMN;">
                <a href="{linkCarpetaRetroalimentacion}"  style="color:black;"> 
                    <strong>carpeta de todas las retrolimentaciones<\strong> 
                </a>
            </span>
        <p>  
        '''

        return htmlEstudiante


    def cargarCalificacionesAlumnoSelec(self, idEstudiante):
        '''
        Cargara las calificaciones de todas las tareas del alumno seleccionado
        en una tabla

        Parámetros:
            idEstudiante (str) : Representa el ID del alumno que el usuario
            selecciono para poder ver sus datos respectivos
        '''


        claseClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()


        # obteniendo la lista de calificaciones de todas las tareas del alumno seleccionado
        # el dict obtenido retornara los datos agrupados de la siguiente forma:
        #   {
        #   'topic_1': (  (nombre_tarea1,calif_tarea1), (nombre_tarea2,calif_tarea2) ...  )
        #   'topic_2': (  (nombre_tarea1,calif_tarea1), (nombre_tarea2,calif_tarea2) ...  )
        #                                      .
        #                                      .
        #                                      .
        #   }
        dict_califAlumnoSelec=self.classRoomControl.list_todasEntregasEstudiante(
            course_id=claseClassroom_id,
            user_id=idEstudiante
        )

        self.tableWidget_tareasAlumno.setRowCount(0)
        numeroRenglones=0

        for cadaLlave in dict_califAlumnoSelec.keys():
            nombreTopic=cadaLlave

            for nombreCourseWork,calificacion in dict_califAlumnoSelec[nombreTopic]:
                self.tableWidget_tareasAlumno.insertRow(numeroRenglones)

                print(nombreCourseWork,nombreTopic,calificacion)

                # nombre coursework...
                a = QtWidgets.QTableWidgetItem(nombreCourseWork)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                self.tableWidget_tareasAlumno.setItem(numeroRenglones,0, a)

                # nombre topic...
                b = QtWidgets.QTableWidgetItem(nombreTopic)
                b.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                self.tableWidget_tareasAlumno.setItem(numeroRenglones,1,b)

                # calificacion...
                c = QtWidgets.QTableWidgetItem(str(calificacion))
                c.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                self.tableWidget_tareasAlumno.setItem(numeroRenglones,2, c)

                numeroRenglones += 1

##################################################################################################################################################
# OTRAS COSAS
##################################################################################################################################################

    def configurarTablasApartadoMisAlumnos(self):
        '''
        Se encargara de darle un formato a las tablas del apartado 'Mis Alumnos',
        es decir:
         - Se encargara de definir el numero de columnas de cada tabla
         - Se encargara de definirla interaccion que se tendra con cada tabla
         - Se encargara de definir el diseño de cada tabla(color de tabla, color de renglones,etc)
        '''

        # Configuracion de la tabla en donde se muestra la lista de los nombres y correos
        # de los alumnos inscritos a la clase de classroom seleccionada.

        self.tableWidget_alumnos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_alumnos.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_alumnos.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.COLOR_TABLA = "#EEF2F3"
        self.COLOR_RESPUESTA = "#9AE5E0"
        stylesheet = f"""
        QTableView{{selection-background-color:{recursos.App_Principal.COLOR_TOPIC_SELECCIONADO};
        background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }};
        """
        self.tableWidget_alumnos.setStyleSheet(stylesheet)
        self.tableWidget_alumnos.verticalHeader().setDefaultSectionSize(70)

        # la tabla tiene 2 columnas: Nombre, Correo
        header = self.tableWidget_alumnos.horizontalHeader()
        for columna in range(0, 2):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)


        # Configuracion de la tabla en donde se muestran las calificaciones del alumno seleccionado

        self.tableWidget_tareasAlumno.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_tareasAlumno.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_tareasAlumno.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget_tareasAlumno.setStyleSheet(stylesheet)

        # la tabla tiene 3 columnas: Topic,Nombre tarea, calificacion
        header = self.tableWidget_tareasAlumno.horizontalHeader()
        for columna in range(0,3):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)


####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################


    def msg_preguntarEleccionBorrarEstudiante(self,estudianteEliminar):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer eliminar al estudiante  cuyo nombre es el valor que almacena el
        parametro: 'estudianteEliminar'

        Parámetros:
            - estudianteEliminarr (str) : Nombre del estudiante que se desea eliminar de la tabla
            donde se muestran los datos de tdos los estudiantes inscritos a la clase de classroom
            seleccionada

        Returns:
            - True (bool) : Si el usuario confirmo positivamente de querer eliminar
            - False (bool): Si el usuario respondio que NO desea eliminar
        '''

        mensaje = "¿Seguro de querer ELIMINAR al estudiante <<{}>> ?".format(estudianteEliminar)

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado



    def msg_preguntarAcercaRefrescarListaEstudiantes(self):
        '''
        Mostrara un cuadro de dialogo al usuario para preguntarle si
        en realidad desea refrescar.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente que si
            desea  refrescar
            - False (bool): Si el usuario dijo que NO desea refrescar
        '''

        mensaje = "Solo es recomendable refrescar la lista de estudiantes " \
                  "si eliminaste a un estudiante por accidente o si no vez " \
                  "la lista de nombres de tus estudiantes"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_exitoAlRefrescar(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        ha refrescado exitosamente.
        '''

        mensaje = "Se ha refrescado con exito la lista de estudiantes inscritos en la clase de  "
        mensaje+= "classroom seleccionada"

        self.ventanaEmergenteDe_informacion(mensaje)



if __name__ == '__main__':
    app = QApplication([])
    application = AlumnoMain()
    application.show()
    app.exit(app.exec())
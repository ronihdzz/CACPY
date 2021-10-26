
'''
TareaMain.py:
    Contine una sola  clase, la clase 'TareaMain', cuyo funcionamiento
    es el unificar todas las ventanas que conforman el apartado de: 'Mis tareas'
    y ser el representante de dichas ventanas ante el codigo principal del programa CACPY.
'''


__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import Qt,pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.TAREA.TareaMain_d import  Ui_Form
from CUERPO.LOGICA.TAREA.AgregadorCourseWork import AgregadorCourseWorks
from CUERPO.LOGICA.TAREA.CreadorTarea import CreadorTareas
from CUERPO.LOGICA.TAREA.CalificadorTareas import CalificadorTareas

import recursos


class TareaMain(QWidget,Ui_Form,recursos.HuellaAplicacion):
    '''
    Esta clase se encargara de unificar todas las ventanas que conforman el apartado de 'Mis tareas'
    del programa, es decir esta clase es como un Main que agrupa todas las ventanas que conforman al
    apartado 'Mis tareas'.Atraves de esta clase todas las ventanas que conforman el apartado
    de 'Mis tareas' tienen comunicación con el resto de los apartados.
    Basicamente gracias a esta clase funciona el apartado 'Mis tareas' el cual esta diseñado
    para que el usuario pueda calificar o ver la informacion de las entregas de las tareas de programacion
    que haya asignado a sus estudiantes, tambien gracias a esta clase el usuario podra asignar tareas
    de google classroom
    '''


    senal_operacionCompleja=pyqtSignal(bool) # señal que se emitira para que desactiven o activen todos los
                                             # apartados del programa

    def __init__(self,baseDatosLocalClassRoom,administradorProgramasClassRoom):
        '''
        - administradorProgramasClassroom (objeto de la clase: AdministradorProgramasClassRoom): dicho
        objeto permite calificar tareas de los estudiantes  del classroom seleccionado por el usuario, este
        objeto tambien permite obtener informacion de una manera mas sencilla acerca de las tareas del classroom
        y topic seleccionadas por el usuario

        - baseDatosLocalClassRoom (objeto de la clase: BaseDatos_ClassRoomProgramas): dicho
        objeto permitira acceder a la base de datos local, la cual almacena los datos de
        los 'CourseWork' asi como los 'Topics' y 'Clases' del ClassRoom del profesor que ha
        iniciado sesión
        '''


        QWidget.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # BREVES CONFIGURACIONES DE DISEÑO DE LA TABLA...
        self.configurarTabla()


        self.administradorProgramasClassRoom=administradorProgramasClassRoom
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom

        self.listaIds_courseworks = []

        # Creando las diferentes ventanas que contiene el apartado: 'Mis tareas'

        self.ventanaAgregadoraTareas = AgregadorCourseWorks(
            administradorProgramasClassRoom=self.administradorProgramasClassRoom
        )

        self.ventanaCreadoraTareas=CreadorTareas(
            administradorProgramasClassRoom=self.administradorProgramasClassRoom
        )

        self.ventanaCalificadoraTareas=CalificadorTareas(
            administradorProgramasClassRoom=self.administradorProgramasClassRoom)


        # conectando señales de las ventanas:
        self.ventanaAgregadoraTareas.senal_courseWork_selec.connect(self.agregarUnCourseWork_tablaTareasCalificables)
        self.ventanaCalificadoraTareas.senal_calificadorTareas_cerro.connect(self.actuarAnteCierreDe_ventanaCalificadora)

        # conectando señales de los objetos:
        self.tableWidget.itemDoubleClicked.connect(self.verDetallesTarea)
        self.btn_crearTarea.clicked.connect(lambda : self.ventanaCreadoraTareas.show() )
        self.btn_importarTarea.clicked.connect( self.mostrarVentana_agregadoraTareas )

        self.btn_regresar.clicked.connect(self.regresarMenu)

        # si el usuario desea calificar las entregas de la tarea seleccionada, entonces se abrira
        # la ventana respectiva que permite hacer eso
        self.btn_calificarPendientes.clicked.connect(self.mostrarVentana_calificadoraEntregasTareas)


        # estableciendo opciones a partir del clic derecho a los items de la tabla
        # con la finalidad de que aparezca la opcion de eliminar objetos
        self.tableWidget.installEventFilter(self)


    def regresarMenu(self):
        '''
        Regresara al apartado en donde se muestra la tabla de tareas calificables
        '''
        self.listWidget.setCurrentIndex(0)


    def verDetallesTarea(self, index):
        '''
        Este metodo es llamado cuando el usuario haga doble clic izquierdo sobre el nombre de
        una tarea(courseWork), contenida en la tabla de tareas calificables.

        ¿Que hara este metodo?
            - Preguntara si  a lo que se le dio doble clic izquierdo es la tarea que se deseaba
            seleccionar para ver sus datos o para calificarla las entregas hechas en esta tarea,
            si el usuario responde afirmativamente este metodo  mostrara una apartado del programa
            en donde se prodra apreciar:
                    - El nombre de la tarea que se selecciono
                    - La fecha en la cual fue creada dicha tarea
                    - Cuantas entregas de dicha tarea ya han sido calificadas
                    - Cuantas entregas de dicha tarea han sido entregadas pero NO calificadas
                    - Cuantas entregas de dicha tarea faltan por entregar
                    - Un boton con imagen de un icono de notas el cual debera se presionado
                    cuando se desee abrir la ventana calificadora de entregas de tareas con
                    el objetivo de calificar las entregas de la tarea seleccionada

        Parámetros:
            item (QTableWidgetItem) : Es un objeto de de PyQt5 y es proveniente de la clase:
            QTableWidgetItem, este objeto contiene información acerca del item al cual se le
            dio doble clic izquierdo dentro de la tabla de topics seleccionables
        '''

        # la tarea  que se selecciono se encuentra dentro de la tabla de tareas calificables
        # en un renglon en especifico, con lo siguiente se obtiene dicho numero de renglon
        # en donde se encuentra la tarea  que se selecciono
        index_tareaSeleccionada = index.row()

        # Cargando los datos de la tarea(coursework)
        nombre_tareaSeleccionada = self.tableWidget.item(index_tareaSeleccionada, 0).text()
        fecha_tareaSeleccionada = self.tableWidget.item(index_tareaSeleccionada, 1).text()

        # ¿existe la tarea que se selecciono en la clase de NbGrader seleccionada?
        if self.administradorProgramasClassRoom.existeEsaTarea_cursoNbGrader(nombreTarea=nombre_tareaSeleccionada):

            # cargando los datos de la tarea seleccionada
            self.nombreTareaSeleccionada=nombre_tareaSeleccionada
            self.indexTareaSeleccionada=index_tareaSeleccionada

            id_tareaSeleccionada = self.listaIds_courseworks[index_tareaSeleccionada]


            # obteniendo los datos las entregas realizados por los alumnos de la tarea
            # seleccionada
            dictDatosEntrega=self.administradorProgramasClassRoom.getDatosCourseWork(
                courseWork_id=id_tareaSeleccionada
            )
            numeroTareasCalificar=dictDatosEntrega['porCalificar']
            numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
            numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

            # mostrando los datos de la tarea seleccionada  en las respectivas label de la GUI
            self.bel_nombre.setText(nombre_tareaSeleccionada)
            self.bel_fechaCreacion.setText(fecha_tareaSeleccionada)
            self.bel_noTareasPorCalificar.setText( str(numeroTareasCalificar) )
            self.bel_noTareasCalificadas.setText( str(numeroTareasCalificadasTotales) )
            self.bel_noTareasPorEntregar.setText( str(numeroTareasPorEntregar) )


            # preparando a la ventana calificadora de entregas de tareas, para que este lista
            # para ser llamada para calificar entregas de la tarea seleccionada
            self.ventanaCalificadoraTareas.prepararParaMostrar(
                cousework_id=id_tareaSeleccionada,
                coursework_name=self.nombreTareaSeleccionada,
                coursework_fechaCreacion=self.tableWidget.item(self.indexTareaSeleccionada,1).text(),
                dictDatosEntrega=dictDatosEntrega
            )

            # mostrando al usuario el apartado del programa en donde se muestran los datos
            # de las tareas seleccionadas y en donde se pueden calificar las entregas de
            # dichas tareas
            self.listWidget.setCurrentIndex(1)

        else:
            # explicandole al usuario que no existe ninguna tarea en la clase de NbGrader, con el nombre
            # de la tarea que seleccion y que por tal motivo no se le muestra el apartado del programa
            # que permite calificar las entregas de las tareas seleccionadas, asi como ver los datos
            # de dichas entregas de tareas.
            nombreClaseNbGrader = self.administradorProgramasClassRoom.configuracionCalificador.get_nombre_cursoNbGrader()
            self.msg_tareaNoRegistradaNbGrader(
                nombreClaseNbGrader=nombreClaseNbGrader,
                nombreTarea=nombre_tareaSeleccionada
            )



    def actuarAnteCambio_claseClassroom(self):
        '''
        Este metodo es llamado cuando se selecciona una clase de classroom diferente a la seleccionada
        ¿Que hara este metodo?
            -   En la GUI mostrara el nombre de la nueva clase de classroom seleccionada
            -   Limpiara la tabla de las tareas calificables ya que cuando el usuario cambio de clase
            de classroom seleccionada significa que dicha tabla debera mostrar otras tareas, ya que
            dos clases de classroom distintas no contienen las mismas tareas, sin embargo hasta este  momento
            aun no se cargara ningun nombre en la tabla ya que el usuario cuando cambia de clase de classroom
            ahora debera seleccionar el topic en donde se encuentran las tareas de programacion, cuando
            el usuario seleccione el topic, ahora si ya se mostraran los datos de las tareas respectivas que
            corresponde al topic y clase de classroom seleccionadas
            -  Si esta clase se encontraba en el apartado en donde se muestran los datos de las tareas seleccionadas
            se cambiara al apartado en donde se muestra la tabla de tareas calificables
        '''

        id_nuevaClaseClassroom,nombre_nuevaClaseClassroom=self.administradorProgramasClassRoom.get_datosCurso()

        if nombre_nuevaClaseClassroom!=None:
            self.bel_nombreCurso.setText(nombre_nuevaClaseClassroom)
            # limpiando la tabla de tareas calificables
            self.tableWidget.setRowCount(0)
            # limpiando la lista que almacena los IDS de las tareas que se encontraban
            # en la tabla de tareas calificables
            self.listaIds_courseworks = []

        # regresando al apartado del programa en donde se encuentra la tabla de tareas calificables
        self.regresarMenu()


    def actuarAnteCambio_topicClassroom(self):
        '''
        Este metodo es llamado cuando se selecciona un topic de classroom diferente al que estaba
        seleccionado
        ¿Que hara este metodo?
            - En la GUI mostrara el nombre del topic de classroom seleccionado
            - Revisara en la base datos local si existen tareas que cumplan con lo siguiente:
                    - Pertenezcan al topic y classroom seleccionados en el apartado 'Mis configuraciones'
                    - Son tareas que fueron registradas en la tabla de tareas calificables y no fueron
                    eliminadas de ahi
              Si encuentra tareas que cumplan con lo anteriormente mencionado entonces se mostraran sus
              datos en la tabla de tareas calificables.
        '''

        id_nuevoTopicSelec,nombre_nuevoTopicSelec=self.administradorProgramasClassRoom.get_datosTopic()
        if id_nuevoTopicSelec!=None:
            self.bel_nombreTopic.setText(nombre_nuevoTopicSelec)
            self.cargarTareas_tablaTareasCalificables()
        # regresando al apartado del programa en donde se muestra la tabla de tareas calificables
        self.regresarMenu()


    def mostrarVentana_agregadoraTareas(self):
        '''
        Mostrara la ventana que permite agregar tareas a la tabla de tareas
        calificables para que sus entregas de estas puedan ser calificadas
        '''

        self.ventanaAgregadoraTareas.prepararParaMostrar()
        self.ventanaAgregadoraTareas.show()


    def mostrarVentana_calificadoraEntregasTareas(self):
        '''
        Este metodo se llamara cuando el usuario desee abrir la ventana calificadora de entregas
        de tareas.

        Este metodo  se encarga de mandar la señal respectiva para que se INABILITEN todos
        los apartados del programa con el objetivo de  que el usuario solo pueda interactar con la
        la ventana calificadora de entregas de tareas.
        Este metodo tambien se encargara de mostrar la ventana calificadora de entregas de tareas
        '''

        self.senal_operacionCompleja.emit(True)

        self.ventanaCalificadoraTareas.show()


    def actuarAnteCierreDe_ventanaCalificadora(self, dictDatosEntrega):
        '''
        Este metodo se llamara cuando la ventana calificadora de entregas de tareas se
        haya cerrado.
        Cuando el usuario habre la ventana calificadora de entregas de tareas, puede que haya
        calificado algunas entregas por lo cual los siguientes datos pudieron cambiar:
            - Cuantas entregas de dicha tarea ya han sido calificadas
            - Cuantas entregas de dicha tarea han sido entregadas pero NO calificadas
            - Cuantas entregas de dicha tarea faltan por entregar

        Y dichos datos se muestran en esta clase, por tal motivo este metodo  actualizar dichos valores
        en esta clase, y se muestran dichos valores en las respectivas label de esta clase

        Este metodo tambien se encarga de mandar la señal respectiva para que se vuelva  a habilitar todos
        los apartados del programa ya que  ya que cuando se abre la ventana calificadora de entregas de tareas,
        el programa inabilita todos los apartados del programa para que el usuario solo pueda interactar con lo
        que hay en la ventana calificadora de entregas de tareas

        Parámetros:
            - dictDatosEntrega (dict): Diccionario que contiene informacion acerca de las entregas que han realizado
            los alumnos de la tarea que selecciono el usuario.Dicho diccionario contiene las siguientes llaves:
                * 'porCalificar' : El value de esta llave sera el numero de alumnos que ya entrego la tarea, pero
                aun no han sido calificados
                * 'calificadas' : El value de esta llave sera el numero de alumnos que ya fueron calificados en
                la tarea que entregaron
                * 'porEntregar': El value de esta llave representa el numero de alumnos que aun no realizan la
                entrega de la tarea que el usuario selecciono
        '''

        numeroTareasCalificar=dictDatosEntrega['porCalificar']
        numeroTareasCalificadasTotales=dictDatosEntrega['calificados']
        numeroTareasPorEntregar=dictDatosEntrega['porEntregar']

        # actualizando los valores que se muestran en las label de esta clase
        self.bel_noTareasPorCalificar.setText( str(numeroTareasCalificar) )
        self.bel_noTareasCalificadas.setText( str(numeroTareasCalificadasTotales) )
        self.bel_noTareasPorEntregar.setText( str(numeroTareasPorEntregar) )

        # emitiendo esta señal para avisar que ya se vuelvan a habilitar todos los apartados del programa,
        # ya que cuando se abre la ventana calificadora de entregas de tareas, el programa inabilita todos
        # los apartados del programa para que el usuario solo pueda interactar con lo que hay en la ventana
        # calificadora de entregas de tareas.
        self.senal_operacionCompleja.emit(False)


##################################################################################################################################################
# TABLA DE TAREAS CALIFICABLES
##################################################################################################################################################

    def cargarTareas_tablaTareasCalificables(self):
        '''
        - Revisara en la base datos local si existen tareas que cumplan con lo siguiente:
                - Pertenezcan al topic y classroom seleccionados en el apartado 'Mis configuraciones'
                - Son tareas que fueron registradas en la tabla de tareas calificables y no fueron
                eliminadas de ahi
          Si encuentra tareas que cumplan con lo anteriormente mencionado entonces mostra  sus
          datos de dichas tareas en la tabla de tareas calificables.
        '''

        # Haciendo consultado en la base de datos local, si hay tareas que cumplan con lo siguiente:
        #   - Pertenezcan al topic y classroom seleccionados en el apartado 'Mis configuraciones'
        #   - Son tareas que fueron registradas en la tabla de tareas calificables y no fueron
        #   eliminadas de ahi
        # En caso de existir alguna  tarea  los datos de la tarea o tareas obtenidas vendran en
        # el siguiente formato:
        # (
        #       (id_tarea_1,nombre_tarea_1,descripccion_tarea_1,fechaCreacion_tarea_1),
        #       (id_tarea_2,nombre_tarea_2,descripccion_tarea_2,fechaCreacion_tarea_2) ,
        #       ....
        #   )
        tuplaDatosCourseWorks= self.administradorProgramasClassRoom.get_courseWorksCalificables_baseDatosLocal()

        tuplaDatosMostrar=[]
        self.listaIds_courseworks=[]
        self.tableWidget.setRowCount(0)

        numeroCourseworks = len(tuplaDatosCourseWorks)


        if tuplaDatosCourseWorks != () and numeroCourseworks != 0:
            self.tableWidget.setRowCount(numeroCourseworks)
            for r,tuplaDatos_unCoursework in enumerate(tuplaDatosCourseWorks):
                courseWork_api_id, titulo, descripccion, fechaCreacion= tuplaDatos_unCoursework

                self.listaIds_courseworks.append(courseWork_api_id)

                # Cargando datos de los coursworks en la tabla:

                # nombre de la tarea(coursework)
                a = QtWidgets.QTableWidgetItem(titulo)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(r, 0, a)

                # fecha de creacion de la tarea(coursework)
                a = QtWidgets.QTableWidgetItem(fechaCreacion)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(r, 1, a)


    def agregarUnCourseWork_tablaTareasCalificables(self, tuplaDatos):
        '''
        Este metodo se llamara cuando el usuario haya completado el tramite para agregar
        una tarea(coursework) a la tabla de tareas calificables  con ayuda de la ventana:
        'AgregadorCourseWork'.Este metodo a grosso modo se encarga de agregar la tarea que el
         usuario quiere agregar en la tabla de tareas calificables, por lo tanto este
         metodo hace lo siguiente:
            1) Mostrar el nombre y la fecha de creacion de la tarea en la tabla de tareas
            seleccionables
            2) Agregar el ID de la tarea en la lista que registra todos los ID de todas las
            tareas que se encuentran dentro de la tabla de tareas calificables

        Parametros:
                1) El primer elemento (str): Representa el ID de la tarea(coursework)
                que el usuario quiere agregar a la tabla de tareas calificables
                2) El segundo elemento (str): Representa el nombre de la tarea(coursework)
                que el usuario quiere agregar a la tabla de tareas calificables
                3) El tercer elemento (str): Representa la fecha de creacion de la tarea
                (coursework) que el usuario quiere agregar a la tabla de tareas calificables
        '''

        # se inserta un renglon que mostrara los datos de la tarea que se agregara a la tabla
        # de tareas calificables en la posicion: 'noRenglones' de la tabla
        noRenglones = self.tableWidget.rowCount()
        self.tableWidget.insertRow(noRenglones)

        # Guardando el id de la tarea  en la lista que almacena los IDs de las
        # tareas que se encuentran en la tabla de tareas calificables
        self.listaIds_courseworks.append(tuplaDatos[0])

        # Mostrando el nombre de la tarea en el renglon respectivo
        celda=QtWidgets.QTableWidgetItem(tuplaDatos[1])
        celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setItem(noRenglones, 0,celda )

        # Mostrando la fecha de creacion de la tarea en el renglon respectivo
        celda=QtWidgets.QTableWidgetItem(tuplaDatos[2])
        celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setItem(noRenglones, 1,celda )


    def eliminarRenglon_tablaTareasCalificables(self,numeroRenglonEliminar):
        '''
        Se encargara de eliminar la tarea(coursewrok)  que se encuentra en la posicion:
        'numeroRenglon' de la tabla de tareas calificables.

        Al eliminar la tarea que se encuentra en la posicion: 'numeroRenglon'
        de la tabla de tareas calificables se hara tambien lo siguiente:
            * Se eliminara los datos de ese tarea de la base de datos local, por
            tal motivo ya no aparecera en la ventana: 'AgregadorCourseworks', sin embargo
            si se desea ver nuevamente en la ventana: 'AgregadorCourseworks' podra lograrse
            refrescando los valores dentro de dicha ventana.
        '''

        respuestaPositiva=self.msg_preguntarEleccionBorrarCourseWork(
            nombreCourseWork_eliminar=self.tableWidget.item(numeroRenglonEliminar, 0).text()
        )

        if respuestaPositiva:
            courseWork_id=self.listaIds_courseworks[numeroRenglonEliminar]
            # se elimina la tarea de la tabla de tareas calificables
            self.tableWidget.removeRow(numeroRenglonEliminar)
            # se elimina el id de la tarea
            self.listaIds_courseworks.pop(numeroRenglonEliminar)
            # se elimina los datos de la tarea de la base de datos local
            self.administradorProgramasClassRoom.eliminarCourseWork_baseDatosLocal(
                courseWork_id=courseWork_id
            )


    def eventFilter(self, source, event):
        """
        Este metodo se encarga de mostrar un menu  con la leyenda: 'eliminar',
        cuando  el usuario le de clic derecho a algun renglon de la tabla de
        tareas calificables.Si el usuario da clic izquierdo sobre la leyenda
        'eliminar' este metodo se encargara de iniciar el proceso de eliminacion
        de la tarea que se encuentra en el renglon en donde el usuario dio clic derecho.
        """


        if event.type() == QtCore.QEvent.ContextMenu and source is self.tableWidget:

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
                    self.eliminarRenglon_tablaTareasCalificables(numeroRenglonEliminar=indiceEliminar)

            except Exception as e:
                pass

            return True
        return super().eventFilter(source, event)


    def configurarTabla(self):
        '''
        Se encargara de darle un formato a la tabla de tareas(coursework) que el usuario
        puede agregar a la tabla de tareas calificables, es decir:
         - Se encargara de definir el numero de columnas de la tabla
         - Se encargara de definirla interaccion que se tendra con dicha tabla.
         - Se encargara de definir el diseño de la tabla(color de tabla, color de renglones,etc)
        '''


        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        header = self.tableWidget.horizontalHeader()

        self.COLOR_TABLA = "#EEF2F3"
        self.COLOR_RESPUESTA = "#9AE5E0"
        stylesheet = "QTableView{selection-background-color: " + self.COLOR_RESPUESTA + "};"
        self.tableWidget.setStyleSheet(stylesheet)


        # la tabla tiene 2 columnas
        # ("NOMBRE","FECHA CREACION")
        header = self.tableWidget.horizontalHeader()
        for columna in range(0,2):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.verticalHeader().setDefaultSectionSize(60)


##################################################################################################################################################
# MENSAJES
##################################################################################################################################################


    def msg_preguntarEleccionBorrarCourseWork(self, nombreCourseWork_eliminar):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer eliminar la tarea de la tabla de tareas calificables  cuyo
        nombre es el valor que almacena el parametro: 'nombreCourseWork_eliminar'

        Parámetros:
            - nombreCourseWork_eliminar (str) : Nombre de la tarea(coursework) que se desea eliminar de
            la tabla de tareas calificables

        Returns:
            - True (bool) : Si el usuario confirmo positivamente de querer eliminar
            - False (bool): Si el usuario respondio que NO desea eliminar
        '''

        mensaje = "¿Seguro de querer ELIMINAR al CourseWork: programa:<<{}>> ".format(nombreCourseWork_eliminar)

        respuesta=self.ventanaEmergenteDe_pregunta(mensaje)

        return respuesta


    def msg_tareaNoRegistradaNbGrader(self, nombreClaseNbGrader, nombreTarea):
        '''
        Ventana emergente informativa que se le mostrara al usuario cuando se quieran ver
        los detalles de una tarea que no existe en la clase de NbGrader seleccionada
        y que por lo tanto no pudiera ser calificada.

        Parámetros:
            nombreClaseNbGrader (str) : Nombre de la clase de NbGrader en la cual no
            se encuentra la tarea de la cual se quieren ver sus detalles

            nombreTarea (str): Nombre de la tarea de la cual se quieren ver sus detalles
        '''

        mensaje = f"No existe ninguna tarea registrada con el nombre de: <<{nombreTarea}>> " \
                  f"en la clase NbGrader:<<{nombreClaseNbGrader}>> que tu escogiste como calificadora"

        self.ventanaEmergenteDe_error(mensaje)



if __name__ == '__main__':
    app = QApplication([])
    application = TareaMain()
    application.show()
    app.exit(app.exec())

'''
ConfiguracionMain.py :  Contiene una sola  clase, la clase 'ConfiguracionMain' cuyo funcionamiento
                        es el unificar todas las ventanas que conforman el apartado de configuracion
                        y ser el representante de dichas ventanas ante el codigo principal del
                        programa CACPY.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import Qt,pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################
# diseño de este apartado de la aplicación
from CUERPO.DISENO.CONFIGURACION.ConfiguracionMain_d import Ui_Form  

import recursos
from CUERPO.LOGICA.CONFIGURACION.CambiadorClases import CambiadorClases
from CUERPO.LOGICA.CONFIGURACION.CambiadorClasesNbGrader import CambiadorClases_NbGrader
from CUERPO.LOGICA.CONFIGURACION.AgregadorTopcis import AgregadorTopics
from CUERPO.LOGICA.CONFIGURACION.CambiadorCarpetaDrive import CambiadorCarpetaDrive


class ConfiguracionMain(QtWidgets.QWidget,Ui_Form,recursos.HuellaAplicacion):
    '''
    Esta clase se encargara de unificar todas las ventanas que conforman el apartado de 'Mis configuraciones'
    del programa, es decir esta clase es como un Main que agrupa todas las ventanas que conforman al
    apartado 'Mis configuraciones'.Atraves de esta clase todas las ventanas que conforman el apartado
    de 'Mis configuraciones' tienen comunicación con el resto de los apartados.
    Basicamente gracias a esta clase funciona el apartado 'Mis configuraciones' el cual esta diseñado
    para que el usuario pueda escoger la clase de classroom, el topic de classroom, la clase NbGrader y
    la carpeta de google drive.
    '''


    NO_COLUMNAS_TABLA_TOPICS_SELEC=1

    # Señales que se emitiran solo cuando se realicen cambios en los valores de:
    # la clase de classroom seleccionada, el topic de classroom seleccionado
    # o la clase de NbGrader seleccionada, es importante mencionae que el unico
    # valor que emitiran es el valor de True y que son de vital importancia para
    # avisarle al resto del programa que actue en consecuencia a partir de los
    # cambios de valores
    senal_eligioUnCurso = pyqtSignal(bool)
    senal_eligioTopic=pyqtSignal(bool)
    senal_claseNbGrader_cambio=pyqtSignal(bool)


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

        QtWidgets.QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)
        

        # Objetos que ayudaran a la clase a cargar los datos
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador

        # Atributos muy importantes
        self.idApi_topic_sele = self.configuracionCalificador.topic_idApi
        self.indice_topic_sele=None
        self.listaIds_topicsClaseClassroom=[]


        # Breves configuraciones a la tabla
        self.configurarTabla()


        # Creando ventanas

        # Este ventana permitira elegir al profesor la clase de classroom en la
        # que se encuentran los ejercicios de programacion que desea calificar
        self.ventana_cambiadorClases=CambiadorClases(
            configuracionCalificador=self.configuracionCalificador,
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoom,
            classRoomControl=self.classRoomControl
        )

        # Esta ventana permitiria elergir al profesor la carpeta de clase
        # de NbGrader en la cual se encuentran las tareas que desea calificar
        # de sus alumnons
        self.ventana_cambiadorClases_NbGrader=CambiadorClases_NbGrader(
            configuracionCalificador=self.configuracionCalificador
        )

        # Esta ventana permitirar agregar los  topics a la tabla de topics calificables
        # es decir permitira agregar los topics en los cuales se encuentran los ejercicios
        # de programación.
        self.ventana_agredadorTopics=AgregadorTopics(
            configuracionCalificador=self.configuracionCalificador,
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoom,
            classRoomControl=self.classRoomControl
        )


        # Esta ventana permitira elegir la carpeta de GoogleDrive en la
        # que se almacenaran las retroalimentaciones de las tareas de los
        # estudiantes.
        self.ventana_cambiadorCarpetaDrive =CambiadorCarpetaDrive(
            classRoomControl=self.classRoomControl,
            configuracionCalificador=self.configuracionCalificador
        )

        # Conectando señales de cada ventana
        self.ventana_cambiadorClases.senal_eligioUnCurso.connect(self.actuarAnteCambio_claseClassroom)
        self.ventana_cambiadorClases_NbGrader.senal_eligioUnCurso.connect(self.actuarAnteCambio_claseNbGrader)
        self.ventana_agredadorTopics.senal_agregoUnTopic.connect(self.agregarUnTopic_tablaTopics_selec)
        self.ventana_cambiadorCarpetaDrive.senal_eligioUnaCarpetaDrive.connect(self.actuarAnteCambio_carpetaDriveRetro)


        # Conectando las señales de los objetos de la clase 
        self.tablaWidget_topics_selec.doubleClicked.connect(self.cambiar_topicClassroom)
        self.btn_agregarApartado.clicked.connect( self.mostrarVentana_agregadoraTopcis )
        self.btn_editarClase_classroom.clicked.connect(self.iniciarProcesoCambiarClaseClassroom)
        self.btn_editarClase_NbGrader.clicked.connect(self.iniciarProcesoCambiarClaseNbGrader)
        self.btn_editarCarpetaMadre.clicked.connect(self.iniciarProcesoCambiarCarpetaDrive)


        # haciendo que la tabla  a partir del clic derecho muestre un 
        # menu que permita eliminar renglones
        self.tablaWidget_topics_selec.installEventFilter(self)



##################################################################################################################################################
# METODOS QUE CAMBIAN EL CONTENIDO DE LOS VALORES DE LA CLASE: NBGRADER, CLASSROOM Y CARPETA DE GOOGLE DRIVE DE RETROALIMENTACIONES
##################################################################################################################################################

    def iniciarProcesoCambiarClaseClassroom(self):
        '''
        Pregunta si en realidad se desea cambiar el valor de la clase de classroom seleccionada,
        de ser afirmativa la respuesta abre la ventana que permite elegir la clase de classroom
        deseada.
        '''

        respuestaAfirmativa=self.msg_preguntarAcercaCambioClase()
        if respuestaAfirmativa:
            # se mostrara la clase de classroom que esta seleccionada para que
            # el usuario pueda ver en la ventana que se desplegara cual es la
            # clase de classroom que tiene como seleccionada
            self.ventana_cambiadorClases.prepararMostrar()
            self.ventana_cambiadorClases.show()

    def iniciarProcesoCambiarClaseNbGrader(self):
        '''
        Pregunta si en realidad se desea cambiar el valor de la clase de NbGrader seleccionada,
        de ser afirmativa la respuesta abre la ventana que permite elegir la clase de NbGrader
        deseada.
        '''

        respuestaAfirmativa=self.msg_preguntarAcercaCambioClase_NbGrader()
        if respuestaAfirmativa:
            self.ventana_cambiadorClases_NbGrader.show()

    def iniciarProcesoCambiarCarpetaDrive(self):
        '''
        Pregunta si en realidad se desea cambiar el valor de la carpeta de google drive en donde
        se almacenan todas las retroalimentaciones, de ser afirmativa la respuesta abre la ventana
        que permite elegir la carpeta de google drive deseada.
        '''

        respuestaAfirmativa=self.msg_preguntarAcercaCambioCarpetaDrive()
        if respuestaAfirmativa:
            self.ventana_cambiadorCarpetaDrive.show()



    def actuarAnteCambio_claseNbGrader(self):
        '''
        Este metodo es llamado cuando se selecciona una  clase NbGrader diferente a la seleccionada
        ¿Que hara este metodo?
            -   En la GUI realizara el cambio de nombre correspondiente a la nueva clase NbGrader
                seleccionada
            -   Mandara una señal a la clase 'Main' de la aplicacion, para informarle que
                se cambio de  clase NbGrader seleccionada.
        '''

        nombreClaseNbGrader=self.configuracionCalificador.get_nombre_cursoNbGrader()


        # Mostrando el nombre de la clase NbGrader seleccionada
        self.bel_clase_nombreNbGrader.setText(nombreClaseNbGrader)

        # Avisando al resto del programa que la clase de NbGrader ha sido cambiada para que se actue
        # en consecuente
        self.senal_claseNbGrader_cambio.emit(True)


    def actuarAnteCambio_claseClassroom(self):
        '''
        Este metodo es llamado cuando se selecciona una clase de classroom diferente a la seleccionada
        ¿Que hara este metodo?
            -   En la GUI mostrara el nombre de la nueva clase de classroom seleccionada
            -   Mandara una señal a la clase 'Main' de la aplicacion, para informarle que
                se cambio la clase de Classroom.

        '''

        _,cursoClassroom_nombre=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        # Mostrando el nombre de la clase classroom seleccionada
        self.bel_nombreClase_classroom.setText(cursoClassroom_nombre)

        # Cuando se selecciona una clase de classroom diferente a la actual, el valor
        # del topic seleccionado cambiara a None
        self.idApi_topic_sele=None
        self.indice_topic_sele=None


        # Cada clase de classroom tiene diferentes topics con diferentes id, por lo tanto la
        # lista que almacenaba todos los ids de los topics de la clase de classroom anterior
        # debere incilizarse a una lista vacia
        self.listaIds_topicsClaseClassroom=[]


        # Es probable que la clase de classroom seleccionada ya habia sido seleccionada con anterioridad,
        # de ser asi, entonces se mostraran en la tabla de topics seleccionables, los topcis que ya habian
        # sido importados en dicha tabla, entre otras cosas mas
        self.cargarDatos_claseClassroom_topicClassroom_claseNbGrader()

        # avisando al resto del programa que ha sido cambiada la clase de classroom seleccionada.
        self.senal_eligioUnCurso.emit(True)

        self.bel_clase_nombreNbGrader.setText(
            "Ninguna clase NbGrader seleccionada"
        )

    def actuarAnteCambio_carpetaDriveRetro(self):
        '''
        Este metodo se llamara cuando se sepa que el usuario realizo un cambio
        en la seleccion de la carpeta de google drive de retroimentaciones, lo
        que hara este metodo sera mostrar en el apartado respectivo de la GUI
        el valor actualizado de la carpeta de google drive seleccionada
        '''

        nombreCarpeta=self.configuracionCalificador.getNombreCarpetaRetro()
        self.bel_nombreCarpetaDriveMadre.setText(nombreCarpeta)



##################################################################################################################################################
# TOPICS
##################################################################################################################################################

    def cambiar_topicClassroom(self, item):
        '''
        Este metodo es llamado cuando el usuario haga doble clic izquierdo sobre el nombre de
        un topic contenido en la tabla de topics seleccionables
        ¿Que hara este metodo?
            - Preguntara si se desea seleccionar el topic al que se le dio doble clic izquerdo,
            de ser afirmativa la respuesta:
                -  En la GUI en la tabla de topcis seleccionables coloreara el renglon correspondiente
                al topic seleccionado
                -  Registrara el cambio en el objeto 'self.configuracionCalificador'
                -  Mandara una señal a la clase 'Main' de la aplicacion, para informarle que
                se cambio el topic de classroom

        Parámetros:
            item (QTableWidgetItem) : Es un objeto de de PyQt5 y es proveniente de la clase:
            QTableWidgetItem, este objeto contiene información acerca del item al cual se le
            dio doble clic izquierdo dentro de la tabla de topics seleccionables
        '''

        cursoClassroom_id, _ = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        # ¿existe una clase de classroom seleccionada Y existe mas de un topic contenido dentro
        # de la tabla de topics seleccionables?
        if cursoClassroom_id and len(self.listaIds_topicsClaseClassroom) > 0:

            # el topic que se selecciono se encuentra dentro de la tabla de topics seleccionables
            # en un renglon en especifico, con lo siguiente se obtiene dicho numero de renglon
            # en donde se encuentra el topic que se selecciono
            noRenglon = item.row()

            # preguntandole al usuario si  el topic que se selecciono si sea el que se queria elegir
            respuetaPositiva = self.msg_preguntarAcercaCambioTopic(
                nombreTopicA_seleccionar=self.tablaWidget_topics_selec.item(noRenglon, 0).text(),
            )
            if respuetaPositiva:

                # descoloreando el renglon que corresponde al topic que antes estaba seleccionado en la tabla de
                # topics seleccionables
                if self.indice_topic_sele != None:
                    renglon_prev = self.indice_topic_sele
                    self.colorearRenglon_tablaTopics_selec(renglon_prev, recursos.App_Principal.COLOR_TABLA_TOPICS)

                # coloreando el renglon que corresponde al topic que se acaba de seleccionar en la tabla de
                # topics seleccionables
                self.colorearRenglon_tablaTopics_selec(noRenglon, recursos.App_Principal.COLOR_TOPIC_SELECCIONADO)
                self.indice_topic_sele = noRenglon

                # guardando información del topic seleccionado en el objeto de configuraciones
                self.configuracionCalificador.cargarDatosTopic(
                    programaTopic_id=self.listaIds_topicsClaseClassroom[noRenglon],
                    programaTopic_nombre=self.tablaWidget_topics_selec.item(noRenglon, 0).text()
                )

                # avisando al resto del programa que ha sido cambiada la clase de classroom seleccionada.
                self.senal_eligioTopic.emit(True)


    def mostrarVentana_agregadoraTopcis(self):
        '''
        Mostrara la ventana que permite agregar topics a la tabla de topics
        seleccionables
        '''

        cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if cursoClassroom_id!=None:
            # se prepara a la ventana con los datos respectivos antes de ser mostrada
            self.ventana_agredadorTopics.prepararParaMostrar()
            self.ventana_agredadorTopics.show()
        else:
            # no puedes agregar un topic si no tienes ninguna clase de classroom seleccionada
            self.msg_necesitasUnaClaseAntesAgregarTopic()

##################################################################################################################################################
# TABLA DE TOPICS SELECCIONABLES
##################################################################################################################################################


    def cargarTopics_tablaSelec(self):
        '''
        Este metodo obtendra de la base de datos local los nombres y ids de lo topics que
        han sido agregados a la tabla de topics seleccionables y que son parte de la clase
        de classroom seleccionada, posteriormente mostrara los nombres de dichos topics
        en la tabla de topics seleccionables
        '''


        claseClassroom_idApi,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if claseClassroom_idApi != None:

            # carga los topics que han sido agregados a la tabla de topics seleccionables y que pertencen
            # a la clase de classroom seleccionada
            topicsAgregados = self.baseDatosLocalClassRoom.get_topicsAgregados(course_id_api=claseClassroom_idApi)

            self.listaIds_topicsClaseClassroom = []
            self.tablaWidget_topics_selec.setRowCount(0)  # Eliminando todas las filas de la tabla


            numeroTopics_selec=len(topicsAgregados)
            if topicsAgregados!=() and numeroTopics_selec>0:
                self.tablaWidget_topics_selec.setRowCount(numeroTopics_selec)


                for f,datosTopic in enumerate(topicsAgregados):
                    topicClassroom_idApi, topicClassroom_nombre=datosTopic

                    self.listaIds_topicsClaseClassroom.append(topicClassroom_idApi)

                    a = QtWidgets.QTableWidgetItem( topicClassroom_nombre)
                    a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tablaWidget_topics_selec.setItem(f, 0, a)

    def agregarUnTopic_tablaTopics_selec(self, tuplaDatosTopic):
        '''
        Este metodo se llamara cuando el usuario haya completado el tramite para agregar
        un topic a la tabla de topics seleccionables con ayuda de la ventana:
        'AgregadorTopics'.Este metodo a grosso modo se encarga de agregar el topic que el
         usuario quiere agregar en la tabla de topics seleccionables, por lo tanto este
         metodo hace lo siguiente:
            1) Mostrar el nombre del topic en la tabla de topics seleccionables.
            2) Agregar el ID del topic en la lista que registra todos los ID de los topics
            contenido en la tabla de topics seleccionables.

        Parametros:
            - tuplaDatosTopic (tuple) : Es una tupla que contiene dos elementos:
                1) El primer elemento (str): Representa el ID del topic
                que el usuario quiere agregar a la tabla de topics seleccionables
                2) El segundo elemento (str): Representa el nombre del topic
                que el usuario quiere agregar a la tabla de topics seleccionables
        '''

        id_topicClassroom, nombre_topicClassroom = tuplaDatosTopic

        noRenglones = self.tablaWidget_topics_selec.rowCount()

        # insertando un renglon en la posicion: 'noRenglones' de la tabla
        self.tablaWidget_topics_selec.insertRow(noRenglones)

        # Insertado el nombre del topic a la tabla de topics seleccionables
        celda = QtWidgets.QTableWidgetItem(nombre_topicClassroom)
        celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tablaWidget_topics_selec.setItem(noRenglones, 0, celda)

        # Agregando el ID del topics a la lista que almacena todos los topics de la
        # tabla de topics seleccionables
        self.listaIds_topicsClaseClassroom.append(id_topicClassroom)

    def colorearRenglon_tablaTopics_selec(self, noRenglon, color):
        '''
        Coloreara en la tabla de topic seleccionables: el renglon cuyo valor
        es igual al parametro 'noRenglon'  de color cuyo valor de igual parametro 'color'

        Parámetros:
            - noRenglon (int): Dato de tipo entero que representa el numero renglon de la
            tabla topics seleccionables que se desea colorear
            - color (str) : Representa el color al cual se desea colorear el renglon, cabe
            aclarar que se espera que el color se defina en su valor hexadecimal,
            ejemplo: "#0DDEFF"
        '''

        for c in range(self.NO_COLUMNAS_TABLA_TOPICS_SELEC):
            self.tablaWidget_topics_selec.item(noRenglon, c).setBackground(QtGui.QColor(color))


    def eliminarRenglon_tablaTopics_selec(self, numeroRenglon):
        '''
        Se encargara de eliminar el topic que se encuentra en la posicion: 'numeroRenglon'
        de la tabla de topics seleccionables.Sin embargo solo podra eliminar dicho topic
        si el topic que se desea eliminar no es el topic seleccionado.

        Al eliminar el topic que se encuentra en la posicion: 'numeroRenglon'
        de la tabla de topics seleccionables se hara tambien lo siguiente:
            * Se eliminara los datos de ese topic de la base de datos local, por
            tal motivo ya no aparecera en la ventana: 'AgregadorTopics', sin embargo
            si se desea ver nuevamente en la ventana: 'AgregadorTopics' podra lograrse
            refrescando los valores dentro de dicha ventana.
        '''

        # ¿el topic que se desea eliminar es el topic seleccionado actualmente?
        if numeroRenglon != self.indice_topic_sele:
            respuestaPositiva = self.msg_preguntarEleccionBorrarTopic(
                nombreTopicA_eliminar=self.tablaWidget_topics_selec.item(numeroRenglon, 0).text()
            )

            if respuestaPositiva:
                cursoClassroom_id, _ = self.configuracionCalificador.get_id_nombre_cursoClassroom()
                # eliminando topic de la base de datos local
                self.baseDatosLocalClassRoom.eliminarTopic(curso_id=cursoClassroom_id,
                                                           topicProgramas_id=self.listaIds_topicsClaseClassroom[
                                                               numeroRenglon])
                # eliminando topic de la tabla de topics seleccionables
                self.tablaWidget_topics_selec.removeRow(numeroRenglon)
                # eliminando topic de la lista que almacena todos los ID de los
                # topics que se encuentran en la tabla de topics seleccionables
                self.listaIds_topicsClaseClassroom.pop(numeroRenglon)

                # ¿al eliminar el topic ya existia algun topic seleccionado?
                if self.indice_topic_sele != None:
                    # ¿la posicion del renglon en donde se encuentra el topic seleccionado
                    # es mayor en posicion del renglon donde se encontraba el topic eliminado?
                    if self.indice_topic_sele > numeroRenglon:
                        self.indice_topic_sele -= 1
        else:
            self.msg_noPuedesEliminarTopicSelec()

    def eventFilter(self, source, event):
        """
        Este metodo se encarga de mostrar un menu  con la leyenda: 'eliminar',
        cuando  el usuario le de clic derecho a algun renglon de la tabla de
        topics seleccionables.Si el usuario da clic izquierdo sobre la leyenda
        'eliminar' este metodo se encargara de iniciar el proceso de eliminacion
        del topic que se encuentra en el renglon en donde el usuario dio clic derecho.
        """

        if event.type() == QtCore.QEvent.ContextMenu and source is self.tablaWidget_topics_selec:

            try:
                # La excepccion se adjunta por que si el usuario da clic derecho sobre cualquier parte
                # de la tabla que no se es un renglon, entonces la variable: 'item' tomara el valor
                # de: 'None', y cuando se realice: 'item.row()' habra un error por que el
                # valor None no tiene el metodo 'row()', por tal motivo se coloca la excepccion
                item = source.itemAt(event.pos())
                indiceEliminar = item.row()

                menu = QtWidgets.QMenu()
                menu.addAction("eliminar")
                if menu.exec_(event.globalPos()):
                    self.eliminarRenglon_tablaTopics_selec(indiceEliminar)
            except Exception as e:
                pass

            return True
        return super().eventFilter(source, event)


    def configurarTabla(self):
        '''
        Se encargara de darle un formato a la tabla de topics seleccionables,es
        decir:
         - Se encargara de definir el numero de columnas de la tabla
         - Se encargara de definirla interaccion que se tendra con dicha tabla.
         - Se encargara de definir el diseño de la tabla(color de tabla, color de renglones,etc)
        '''

        self.tablaWidget_topics_selec.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tablaWidget_topics_selec.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tablaWidget_topics_selec.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tablaWidget_topics_selec.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.COLOR_TABLA = "#EEF2F3"
        self.COLOR_RESPUESTA = "#9AE5E0"

        stylesheet = f"""QTableView{{ background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }}; """
        self.tablaWidget_topics_selec.setStyleSheet(stylesheet)

        self.tablaWidget_topics_selec.verticalHeader().setDefaultSectionSize(70)

        # la tabla contiene una sola columna, la cual muestra los nombres de los topics
        # seleccionables
        header = self.tablaWidget_topics_selec.horizontalHeader()
        for columna in range(0, self.NO_COLUMNAS_TABLA_TOPICS_SELEC):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)


##################################################################################################################################################
# PROCESAMIENTO DE LOS DATOS QUE EL USUARIO DEFINIO LA ULTIMA VEZ QUE ABRIO EL PROGRAMA
##################################################################################################################################################

    def cargarDatos_objetoConfigurador(self):
        '''
        Se encargara de procesar  todos los  datos que tiene registrado en
        el  objeto: 'self.configuracionCalificador'
        '''

        self.cargarDatos_claseClassroom_topicClassroom_claseNbGrader()
        self.cargarDatos_carpetaDrive()


    def cargarDatos_carpetaDrive(self):
        '''
        Se revisara si se tiene registrado que: el usuario tiene definida la carpeta de
        Google Drive donde se almacenaran las retroalimentaciones en caso de ser esto
        cierto se mostrara en la label respectiva de la GUI el nombre de la carpeta de
        google drive.
        '''

        # Se muestra el nombre de la carpeta elegida en caso de existir
        if self.configuracionCalificador.getNombreCarpetaRetro() != None and self.configuracionCalificador.getIdApiCarpetaRetro()!=None:
            self.bel_nombreCarpetaDriveMadre.setText(
                self.configuracionCalificador.getNombreCarpetaRetro()
            )
            self.ventana_cambiadorCarpetaDrive.bel_nombreCarpetaActual.setText(
                self.configuracionCalificador.getNombreCarpetaRetro()
            )
        else:
            self.bel_nombreCarpetaDriveMadre.setText("Sin ninguna carpeta drive seleccionada")


    def cargarDatos_claseClassroom_topicClassroom_claseNbGrader(self):
        '''
        ¿Que es lo que hace exactamente?
         - Si se tiene registrado que el usuario tiene una clase de classroom seleccionada, entonces:
             - Se cargaran en la tabla de topics seleccionables los nombres de los topics que pertenecen
             a dicha clase de classroom y que pertenecen  a la tabla de topics seleccionables
             - Se mostrara el nombre de la clase de classroom seleccionada, en la respectiva label de
             la GUI
             - Se revisara si  se tiene registrado que el usuario tiene  un topic de classroom
             seleccionado de la tabla de topic seleccionables, de ser asi entonces se coloreara
             el renglon de la tabla de topics seleccionables que muestra el nombre de dicho topic

             - Se revisara si se tiene registrado que el usuario tiene una clase de NbGrader, de
             ser asi de mostrara el nombre de dicha clase de NbGrader
        '''


        # obteniendo los datos de la CLASE de classroom seleccionada(si es que hay una clase de classroom seleccionada)
        claseClassroom_idApi,claseClassroom_nombre = self.configuracionCalificador.get_id_nombre_cursoClassroom()

        # obteniendo los datos del TOPIC de classroom seleccionado (si es que hay un TOPIC de classroom
        # seleccionado)
        topicClassroom_idApi,topicClassroom_nombre = self.configuracionCalificador.get_id_nombre_topicClassroom()

        # ¿hay una clase de classroom seleccionada?
        if claseClassroom_idApi!=None :
            self.cargarTopics_tablaSelec()
            self.bel_nombreClase_classroom.setText( claseClassroom_nombre )
            self.senal_eligioUnCurso.emit(True)

            # ¿hay un topic de classroom seleccionado?
            if topicClassroom_idApi!=None:
                # obteniendo el numero de renglon al que petenece el topic seleciconado
                renglonSeleccionar=self.listaIds_topicsClaseClassroom.index(topicClassroom_idApi)
                self.colorearRenglon_tablaTopics_selec(renglonSeleccionar, recursos.App_Principal.COLOR_TOPIC_SELECCIONADO)
                self.indice_topic_sele=renglonSeleccionar
                self.senal_eligioTopic.emit(True)

            # ¿hay una clase de NbGrader seleccionada?
            if self.configuracionCalificador.get_nombre_cursoNbGrader() != None:
                # Revisando si la clase de NbGrader seleccionada es valida
                respuestaPositiva = self.ventana_cambiadorClases_NbGrader.cargarClaseNbGrader(
                    self.configuracionCalificador.get_nombre_cursoNbGrader()
                )


                # ¿es la clase de NbGrader seleccionada valida?
                if respuestaPositiva is False:
                    self.configuracionCalificador.set_nombre_cursoNbGrader(
                        nombre=None
                    )
                    self.bel_clase_nombreNbGrader.setText(
                        "Ninguna clase NbGrader seleccionada"
                    )

                else:
                    self.bel_clase_nombreNbGrader.setText(
                        self.configuracionCalificador.get_nombre_cursoNbGrader()
                    )
                    self.senal_claseNbGrader_cambio.emit(True)

        else:
            self.bel_nombreClase_classroom.setText(
                recursos.App_Principal.LEYENDA_SIN_CURSO_SELECCIONADO
            )

            self.bel_clase_nombreNbGrader.setText(
                "Ninguna clase NbGrader seleccionada"
            )

##################################################################################################################################################
# MENSAJES
##################################################################################################################################################

    def msg_preguntarAcercaCambioClase(self):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer editar la clase de classroom actualmente seleccionada

        Returns:
            - True (bool) : Si el usuario confirmo positivamente
            - False (bool): Si el usuario respondio que NO desea
        '''

        mensaje = "¿Seguro que quieres cambiar de clase?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_preguntarAcercaCambioClase_NbGrader(self):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer editar la clase de NbGrader actualmente seleccionada

        Returns:
            - True (bool) : Si el usuario confirmo positivamente
            - False (bool): Si el usuario respondio que NO desea
        '''

        mensaje = "¿Seguro que quieres cambiar de la clase NbGrader seleccionada?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_preguntarAcercaCambioCarpetaDrive(self):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer editar la carpeta de google drive seleccionada como carpeta guardadora
        de retroalimentacines

        Returns:
            - True (bool) : Si el usuario confirmo positivamente
            - False (bool): Si el usuario respondio que NO desea
        '''

        mensaje = "¿Seguro que quieres cambiar la carpeta de drive en donde se almacenan todas "
        mensaje += "las retroalimentaciones de tus cursos de programacion?"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_preguntarEleccionBorrarTopic(self,nombreTopicA_eliminar):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer eliminar el topic de la tabla de topics seleccionable el topic cuyo
        nombre es el valor que almacena el parametro: 'nombreTopicA_eliminar'

        Parámetros:
            - nombreTopicA_eliminar (str) : Nombre del topic que se desea eliminar de la tabla
            de topics seleccionables

        Returns:
            - True (bool) : Si el usuario confirmo positivamente de querer eliminar el
            topic de la tabla de topics seleccionables
            - False (bool): Si el usuario respondio que NO desea eliminar el topic de
            la tabla de topics seleccionables
        '''

        mensaje = "¿Seguro de querer ELIMINAR el topic: <<{}>> ?".format(nombreTopicA_eliminar)

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


    def msg_noPuedesEliminarTopicSelec(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que
        no puede eliminar el topic que actualmente esta seleccionado de la tabla de
        topics seleccionables.
        '''

        mensaje = "No puedes eliminar los topics seleccionados"

        self.ventanaEmergenteDe_informacion(mensaje)


    def msg_necesitasUnaClaseAntesAgregarTopic(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que
        no puede agregar un topic a la tabla de topics seleccionables, por que
        no ha seleccionado ninguna clase de classroom
        '''

        mensaje = "Para agregar un topic primero debes escoger una clase de classroom"

        self.ventanaEmergenteDe_informacion(mensaje)

    def msg_preguntarAcercaCambioTopic(self,nombreTopicA_seleccionar):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer seleccionar el topic  cuyo nombre es el valor que almacena el parametro:
        'nombreTopicA_seleccionar'

        Parámetros:
            - nombreTopicA_seleccionar (str) : Nombre del topic que el usuario desea seleccionar

        Returns:
            - True (bool) : Si el usuario confirmo positivamente de querer seleccionar el topic
            - False (bool): Si el usuario respondio que NO querer seleccionar el topic
        '''

        mensaje = "¿Seguro de querer cambiar al apartado: <<{}>> ?".format(nombreTopicA_seleccionar)

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado


if __name__ == '__main__':
    app = QApplication([])
    application = ConfiguracionMain()
    application.show()
    app.exit(app.exec())

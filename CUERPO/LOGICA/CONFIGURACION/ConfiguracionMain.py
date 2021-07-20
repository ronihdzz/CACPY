from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import  QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5 import QtCore,QtGui


from CUERPO.LOGICA.CONFIGURACION.CambiadorClases import CambiadorClases
from CUERPO.LOGICA.CONFIGURACION.CambiadorClasesNbGrader import CambiadorClases_NbGrader
from CUERPO.LOGICA.CONFIGURACION.AgregadorTopcis import AgregadorTopics


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.CONFIGURACION.ConfiguracionMain_d import Ui_Form
import recursos



class ConfiguracionMain(QtWidgets.QWidget,Ui_Form,recursos.HuellaAplicacion):
    #DATOS_MOSTRAR='Topic programacion, Topic de retrolimentacion'
    NO_COLUMNAS=1

    #senal_verDetallesTarea = pyqtSignal(int)  # id de tarea
    senal_operacionImportante = pyqtSignal(bool)
    senal_eligioUnCurso = pyqtSignal(bool)
    senal_eligioTopic=pyqtSignal(bool)


    senal_claseNbGrader_cambio=pyqtSignal(bool)




    def __init__(self,baseDatosLocalClassRoom,classRoomControl,configuracionCalificador):

        QtWidgets.QWidget.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # ATRIBUTOS DE LA CLASE

        # Objetos que ayudaran a la clase a cargar los datos
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador

        # Atributos muy importantes
        self.programas_topic_id = self.configuracionCalificador.programTopic_id
        self.indice_topic_sele=None
        self.listaIds_apartadosProgramas=[]

        # Breves configuraciones a la tabla
        self.configurarTabla()



        # VENTANAS:

        # Creando ventanas
        self.ventana_cambiadorClases=CambiadorClases(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoom,
            classRoomControl=self.classRoomControl
        )

        self.ventana_cambiadorClases_NbGrader=CambiadorClases_NbGrader()

        self.ventana_agredadorTopics=AgregadorTopics(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoom,
            classRoomControl=self.classRoomControl
        )




        # Conectando señales de ventana
        self.ventana_cambiadorClases.senal_eligioUnCurso.connect(self.cambiar_claseClassroom)
        self.ventana_cambiadorClases_NbGrader.senal_eligioUnCurso.connect(self.cambiar_claseNbGrader)
        self.ventana_agredadorTopics.senal_agregoUnTopic.connect(self.agregarUnTopic)



        # SEÑALES DE LOS OBJETOS DE LA CLASE:

        self.tableWidget.doubleClicked.connect(self.cambiar_topicClassroom)
        self.btn_agregarApartado.clicked.connect( self.mostrarVentana_agregadoraTopcis )
        self.btn_editarClase_classroom.clicked.connect(self.procesoCambiarClase)
        self.btn_editarClase_NbGrader.clicked.connect(lambda : self.ventana_cambiadorClases_NbGrader.show())

        # estableciendo opciones a partir del clic derecho a los items de la tabla
        # con la finalidad de que aparezca la opcion de eliminar objetos
        self.tableWidget.installEventFilter(self)


        # Cargando los datos que se mostraran
        #self.cargarDatos()



##################################################################################################################################################
# CLASES
##################################################################################################################################################

    def cambiar_claseNbGrader(self,nuevoNombre):
        self.configuracionCalificador.set_clase_nombreNbGrader(nuevoNombre)
        self.bel_clase_nombreNbGrader.setText(nuevoNombre)
        self.senal_claseNbGrader_cambio.emit(True)


    def editarValor_clase_nombreNbGrader(self,nuevoNombre):
        self.configuracionCalificador.set_clase_nombreNbGrader(nuevoNombre)
        self.bel_clase_nombreNbGrader.setText(nuevoNombre)


    def cambiar_claseClassroom(self, clase_tuplaDatos):
        '''
        tuplaDatos
            primer elemento - api id del curso
            segundo elemetno - nombre del curso

        :param clase_tuplaDatos:
        :return:
        '''

        # Solo si el valor de id escogido es diferente entonces se procedera
        # a actuar
        id, nombre = clase_tuplaDatos

        cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if cursoClassroom_id!=id:

            self.bel_nombreClase_classroom.setText(nombre)
            self.programas_topic_id=None
            self.indice_topic_sele=None
            self.listaIds_apartadosProgramas=[]

            # Cargando los datos del curso
            self.configuracionCalificador.cargarDatosCurso(
                id=id,
                nombre=nombre,
            )

            print("QUE PASA AQUI")
            self.ventana_agredadorTopics.curso_id=cursoClassroom_id
            self.cargarDatos()

            # cargar los topic agregados de esa clase..
            self.senal_eligioUnCurso.emit(True)


    def procesoCambiarClase(self):

        respuestaAfirmativa=self.msg_preguntarAcercaCambioClase()
        if respuestaAfirmativa:
            cursoClassroom_id,cursoClassroom_nombre=self.configuracionCalificador.get_id_nombre_cursoClassroom()
            if cursoClassroom_id!=None:
                self.ventana_cambiadorClases.prepararMostrar(
                    curso_tuplaDatos=(cursoClassroom_id,cursoClassroom_nombre)
                )
            self.ventana_cambiadorClases.show()



##################################################################################################################################################
# TOPICS
##################################################################################################################################################


    def cambiar_topicClassroom(self, item):

        # mensaje de no puedes editar si no hay ningun curso esocogido
        # o si no hay ningun topic agregado

        cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if cursoClassroom_id and len(self.listaIds_apartadosProgramas)>0:
            noRenglon = item.row()

            respuetaPositiva=self.msg_preguntarAcercaCambioTopic(
                apartadoProgram_nombre=self.tableWidget.item(noRenglon,0).text(),
            )
            if respuetaPositiva:
                if self.indice_topic_sele!=None:
                    renglon_prev=self.indice_topic_sele
                    self.colorearRenglon(renglon_prev, recursos.App_Principal.COLOR_TABLA_TOPICS)

                self.colorearRenglon(noRenglon,recursos.App_Principal.COLOR_TOPIC_SELECCIONADO)

                self.indice_topic_sele=noRenglon

                self.configuracionCalificador.cargarDatosTopic(
                    programaTopic_id=self.listaIds_apartadosProgramas[noRenglon],
                    programaTopic_nombre=self.tableWidget.item(noRenglon, 0).text()
                )
                self.senal_eligioTopic.emit(True)


    def colorearRenglon(self,noRenglon,color):
        for c in range(self.NO_COLUMNAS):
            self.tableWidget.item(noRenglon,c).setBackground(QtGui.QColor(color))


    def mostrarVentana_agregadoraTopcis(self):

        cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if cursoClassroom_id!=None:
            self.ventana_agredadorTopics.cargarDatosTopics(cursoClassroom_id)
            self.ventana_agredadorTopics.show()
        else:
            # no puedes agregar un topic si no tienes ningun curso agregado
            self.msg_necesitasUnaClaseAntesAgregarTopic()


    def agregarUnTopic(self, tuplaTopics):
        '''
        listaTopics:
            - 1 elemento(programas):
                id_api
                nombre
            - 2 elemento(retroalimentacion):
                id_api
                nombre


        :return:
        '''
        tupla_topic_programas = tuplaTopics


        noRenglones=self.tableWidget.rowCount()
        self.tableWidget.insertRow(noRenglones)

        # Insertado el nombre del topic en donde se pondran los programas

        #Agregando nombre
        celda=QtWidgets.QTableWidgetItem(tupla_topic_programas[1])
        celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setItem(noRenglones,0,celda )


        self.listaIds_apartadosProgramas.append( tupla_topic_programas[0] )


    def eliminarRenglonTopic(self,numeroRenglon):
        if numeroRenglon != self.indice_topic_sele:
            respuestaPositiva=self.msg_preguntarEleccionBorrarTopic(
                apartadoProgram_nombre=self.tableWidget.item(numeroRenglon, 0).text()
            )

            if respuestaPositiva:
                cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()
                self.baseDatosLocalClassRoom.eliminarTopic(curso_id=cursoClassroom_id,
                                                           topicProgramas_id=self.listaIds_apartadosProgramas[numeroRenglon])
                self.tableWidget.removeRow(numeroRenglon)
                self.listaIds_apartadosProgramas.pop(numeroRenglon)

                if self.indice_topic_sele!=None:
                    if self.indice_topic_sele>numeroRenglon:
                        self.indice_topic_sele-=1
                print("INDICE SELECCIONADO:",self.indice_topic_sele)
        else:
            self.msg_noPuedesEliminarTopicSelec()



    def eventFilter(self, source, event):
        """
        Cada vez que alguien haga click derecho sobre algun item de la
        'listWid_soniMio' significara que probablemente quiera borrar
        esa canción asi que debe  mostrar la opcion de borrar, y en caso
        de ser seleccionada dicha opcion se mandara a borrar a dicha cancion
        """

        if event.type() == QtCore.QEvent.ContextMenu and source is self.tableWidget:

            try:
                item = source.itemAt(event.pos())
                print("objeto=",item)
                print("indice a eliminar:",item.row())
                indiceEliminar = item.row()

                menu = QtWidgets.QMenu()
                menu.addAction("eliminar")  # menu.addAction("eliminar",metodoA_llamar)
                print("Clic derecho")


            # indice=self.listWid_soniMio.currentIndex().row()
            # cancionEliminar=self.listWid_soniMio.item(indice).text()
            # print(f"Indice {indice} indice{event.pos()}  cancionEliminar{cancionEliminar}")

                if menu.exec_(event.globalPos()):

                    self.eliminarRenglonTopic(indiceEliminar)

                    #if self.indice_topic_sele!=indiceEliminar:
                    #    print("DEBEMOS ELIMINAR")
                    #    self.eliminarRenglonTopic(indiceEliminar)
                    #else:
                    #    print("NO DEBEMOS ELIMINAR")
                    #self.eliminarCancion()
            except Exception as e:
                print(e)

            return True
        return super().eventFilter(source, event)



##################################################################################################################################################
# OTRAS COSAS
##################################################################################################################################################


    def configurarTabla(self):

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)


        header = self.tableWidget.horizontalHeader()

        self.COLOR_TABLA = "#EEF2F3"
        self.COLOR_RESPUESTA = "#9AE5E0"
        #stylesheet = f"""
        #QTableView{{selection-background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS};
        #background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }};
        #"""

        stylesheet = f"""QTableView{{ background-color:{recursos.App_Principal.COLOR_TABLA_TOPICS}; }}; """

        # stylesheet += "background-color:" + self.COLOR_TABLA + ";}"
        self.tableWidget.setStyleSheet(stylesheet)

        self.tableWidget.verticalHeader().setDefaultSectionSize(70)

        # la tabla tiene 3 columnas
        # ("NOMBRE","DATA_TIME", "PREGUNTAS")
        header = self.tableWidget.horizontalHeader()
        for columna in range(0,self.NO_COLUMNAS):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
            #header.setSectionResizeMode(columna, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)


    def cargarDatos(self):
        '''
        Esta diseñado para funcionar cuando recien se inicia el programa...


        Cargara los datos, en funcion del valor de los atributos de instancia:
            - self.curso_id
            - self.topic_id

        Posteriormente cargar los datos de los topics del curso seleccionado en
        la tabla


        (
        program_topic_id,programas_topic_nombre,
        retro_topic_id,retro_topic_nombre
        ),
        (
        program_topic_id,programas_topic_nombre,
        retro_topic_id,retro_topic_nombre
        ),

        '''


        cursoClassroom_id,cursoClassroom_nombre = self.configuracionCalificador.get_id_nombre_cursoClassroom()
        topicClassroom_id,topicClassroom_nombre = self.configuracionCalificador.get_id_nombre_topicClassroom()
        cursoNbGrader_nombre= self.configuracionCalificador.get_nombre_cursoNbGrader()

        if cursoClassroom_id!=None :
            self.cargarTopicsCurso()
            self.bel_nombreClase_classroom.setText( cursoClassroom_nombre )
            self.senal_eligioUnCurso.emit(True)

            # Seleccionar renglon...
            if topicClassroom_id!=None:
                renglonSeleccionar=self.listaIds_apartadosProgramas.index(topicClassroom_id)
                self.colorearRenglon(renglonSeleccionar,recursos.App_Principal.COLOR_TOPIC_SELECCIONADO)
                self.indice_topic_sele=renglonSeleccionar
                self.senal_eligioTopic.emit(True)

            # Colocando el nombre al curso nbgrader
            if cursoNbGrader_nombre!=None:
                self.bel_clase_nombreNbGrader.setText(cursoNbGrader_nombre)
            else:
                self.bel_clase_nombreNbGrader.setText(
                    recursos.App_Principal.LEYENDA_SIN_CURSO_SELECCIONADO
                )

        else:
            self.bel_nombreClase_classroom.setText(
                recursos.App_Principal.LEYENDA_SIN_CURSO_SELECCIONADO
            )

            self.bel_clase_nombreNbGrader.setText(
                recursos.App_Principal.LEYENDA_SIN_CURSO_SELECCIONADO
            )


    def cargarTopicsCurso(self):


        topicClassroom_id,_=self.configuracionCalificador.get_id_nombre_topicClassroom()
        cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if cursoClassroom_id != None:
            topicsAgregados = self.baseDatosLocalClassRoom.get_topicsAgregados(course_id_api=cursoClassroom_id)
            self.listaIds_apartadosProgramas = []
            tuplaDatos = []
            self.tableWidget.setRowCount(0)  # Eliminando todas las filas de la tabla
            if topicsAgregados != () and len(topicsAgregados) > 0:
                for apartadoProgram_id, apartadoProgram_nombre in topicsAgregados:
                    self.listaIds_apartadosProgramas.append(apartadoProgram_id)
                    tuplaDatos.append( (apartadoProgram_nombre,)  )

            self.cargarDatosEnTabla(tuplaDatos=tuplaDatos)



    def cargarDatosEnTabla(self,tuplaDatos):
        '''
        Cargara los datos de los cuestionarios en la tabla, los datos que cargara
        son los que  vienen en el parametro cuyo nombre es: 'tuplaDatos'

        :param tuplaDatos:
         ¿Como vendran los datos?
         (
            ( Nombre,Calificadas,Por calificar,Fecha emision,Promedio ),
            ( Nombre,Calificadas,Por calificar,Fecha emision,Promedio ),
                                    .
                                    .
                                    .
            ( Nombre,Calificadas,Por calificar,Fecha emision,Promedio )
        )

        :return:
        '''

        # Si tan siquiera hay un dato...

        if len(tuplaDatos)>0:

            # Nombre,Calificadas,Por calificar,Fecha emision,Promedio
            FILAS = len(tuplaDatos)
            COLUMNAS = self.NO_COLUMNAS

            self.noCuestionarios = FILAS
            self.tableWidget.setRowCount(FILAS)

            for f in range(FILAS):
                for c in range(COLUMNAS):
                    dato_celda_string = str(tuplaDatos[f][c])
                    a = QtWidgets.QTableWidgetItem(dato_celda_string)
                    a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                    self.tableWidget.setItem(f, c, a)



##################################################################################################################################################
# MENSAJES
##################################################################################################################################################

    def msg_preguntarEleccionBorrarTopic(self,apartadoProgram_nombre):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro de querer ELIMINAR el topic: <<{}>> ?".format(apartadoProgram_nombre)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton() == btn_yes:
            return True
        return False


    def msg_noPuedesEliminarTopicSelec(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "No puedes eliminar los topics seleccionados"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_necesitasUnaClaseAntesAgregarTopic(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Para agregar un topic primero debes escoger una clase"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_preguntarAcercaCambioClase(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro que quieres cambiar de clase?"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton() == btn_yes:
            return True
        return False


    def msg_preguntarAcercaCambioTopic(self,apartadoProgram_nombre):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro de querer cambiar al apartado: <<{}>> ?".format(apartadoProgram_nombre)

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton() == btn_yes:
            return True
        return False



if __name__ == '__main__':
    app = QApplication([])
    application = ConfiguracionMain()
    application.show()
    app.exit(app.exec())

"""

####################################################################################################################
# APARTADO SELECCIONADO
####################################################################################################################



"""
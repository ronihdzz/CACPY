from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import  QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5 import QtCore,QtGui


from CUERPO.LOGICA.CONFIGURACION.CambiadorClases import CambiadorClases
from CUERPO.LOGICA.CONFIGURACION.CambiadorClasesNbGrader import CambiadorClases_NbGrader
from CUERPO.LOGICA.CONFIGURACION.AgregadorTopcis import AgregadorTopics
from CUERPO.LOGICA.CONFIGURACION.CambiadorCarpetaDrive import CambiadorCarpetaDrive

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


        # Objetos que ayudaran a la clase a cargar los datos
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom
        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador

        # Atributos muy importantes
        self.programas_topic_id = self.configuracionCalificador.topic_idApi
        self.indice_topic_sele=None
        self.listaIds_topicsClaseClassroom=[]

        # Breves configuraciones a la tabla
        self.configurarTabla()



        # Creando ventanas
        # Este ventana permitira elegir al profesor la clase de classroom en la
        # que se encuentran los ejercicios de programacion que desea calificar
        self.ventana_cambiadorClases=CambiadorClases(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoom,
            classRoomControl=self.classRoomControl
        )

        # Esta ventana permitiria elergir al profesor la carpeta de clase
        # de NbGrader en la cual se encuentran las tareas que desea calificar
        # de sus alumnons
        self.ventana_cambiadorClases_NbGrader=CambiadorClases_NbGrader()


        # Esta ventana permite elegir un topic de la clase de classrom seleccinada
        self.ventana_agredadorTopics=AgregadorTopics(
            baseDatosLocalClassRoom=self.baseDatosLocalClassRoom,
            classRoomControl=self.classRoomControl
        )

        self.ventana_cambiadorCarpetaDrive =CambiadorCarpetaDrive(
            classRoomControl=self.classRoomControl,
            configuracionCalificador=self.configuracionCalificador
        )


        # Mostramos el nombre de la carpeta elegida en caso de existir
        if self.configuracionCalificador.getNombreCarpetaRetro() != None and self.configuracionCalificador.getIdApiCarpetaRetro()!=None:
            self.bel_nombreCarpetaDriveMadre.setText(
                self.configuracionCalificador.getNombreCarpetaRetro()
            )
            self.ventana_cambiadorCarpetaDrive.bel_nombreCarpetaActual.setText(
                self.configuracionCalificador.getNombreCarpetaRetro()
            )
        else:
            self.bel_nombreCarpetaDriveMadre.setText("Sin ninguna carpeta drive seleccionada")






        # Conectando señales de ventana
        self.ventana_cambiadorClases.senal_eligioUnCurso.connect(self.cambiar_claseClassroom)
        self.ventana_cambiadorClases_NbGrader.senal_eligioUnCurso.connect(self.cambiar_claseNbGrader)
        self.ventana_agredadorTopics.senal_agregoUnTopic.connect(self.agregarUnTopic)
        self.ventana_cambiadorCarpetaDrive.senal_eligioUnaCarpetaDrive.connect(self.mostrarNuevaCarpetaDriveElegida)




        # SEÑALES DE LOS OBJETOS DE LA CLASE:
        self.tableWidget.doubleClicked.connect(self.cambiar_topicClassroom)
        self.btn_agregarApartado.clicked.connect( self.mostrarVentana_agregadoraTopcis )
        self.btn_editarClase_classroom.clicked.connect(self.procesoCambiarClase)
        self.btn_editarClase_NbGrader.clicked.connect(lambda : self.ventana_cambiadorClases_NbGrader.show())
        self.btn_editarCarpetaMadre.clicked.connect(lambda : self.ventana_cambiadorCarpetaDrive.show() )




        # estableciendo opciones a partir del clic derecho a los items de la tabla
        # con la finalidad de que aparezca la opcion de eliminar objetos
        self.tableWidget.installEventFilter(self)


        # Cargando los datos que se mostraran
        #self.cargarDatos()



##################################################################################################################################################
# CLASES
##################################################################################################################################################
    def mostrarNuevaCarpetaDriveElegida(self):
        nombreCarpeta=self.configuracionCalificador.getNombreCarpetaRetro()
        self.bel_nombreCarpetaDriveMadre.setText(nombreCarpeta)


    def cambiar_claseNbGrader(self,nuevoNombre):
        '''
        Este metodo es llamado cuando se selecciona una  clase NbGrader diferente a la seleccionada
        ¿Que hara este metodo?
            -   En la GUI realizara el cambio de nombre correspondiente a la nueva clase NbGrader
                seleccionada
            -   Registrara el cambio en el objeto 'self.configuracionCalificador'
            -   Mandara una señal a la clase 'Main' de la aplicacion, para informarle que
                se cambio de  clase NbGrader seleccionada.

        Parametros:
            nuevoNombre (str): Representa el nuevo nombre de la clase NbGrader seleccionada
        '''

        self.configuracionCalificador.set_clase_nombreNbGrader(nuevoNombre)

        # Renovando en nombre de la clase NbGrader seleccionada
        self.bel_clase_nombreNbGrader.setText(nuevoNombre)

        self.senal_claseNbGrader_cambio.emit(True)


    def cambiar_claseClassroom(self, clase_tuplaDatos):
        '''
        Este metodo es llamado cuando se selecciona una clase de classroom diferente a la seleccionada
        ¿Que hara este metodo?

        tuplaDatos
            primer elemento - api id del curso
            segundo elemetno - nombre del curso

        :param clase_tuplaDatos:
        :return:
        '''

        # Solo si el valor de id escogido es diferente entonces se procedera
        # a actuar
        clase_idApi, clase_nombre = clase_tuplaDatos

        cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()


        # ¿la clase que se selecciono es diferente a la acutal seleccionada?
        if cursoClassroom_id!=id:
            # Renovando en nombre de la clase classroom seleccionada
            self.bel_nombreClase_classroom.setText(clase_nombre)

            # Cuando se selecciona una clase de classroom diferente a la actual, el valor
            # del topic seleccionado cambiara a None
            self.programas_topic_id=None
            self.indice_topic_sele=None

            # Cada clase de classroom tiene diferentes topics con diferentes id, por lo tanto la
            # lista que almacenaba todos los ids de los topics de la clase de classroom anterior
            # debere incilizarse a una lista vacia
            self.listaIds_topicsClaseClassroom=[]

            # Avisando al objeto 'configuracionCalificador' que la clase de classroom seleccionada ahora
            # es una diferente
            self.configuracionCalificador.cargarDatosClaseClassroom_seleccionada(
                clase_idApi=clase_idApi,
                clase_nombre=clase_nombre,
            )
            
            
            self.ventana_agredadorTopics.curso_id=cursoClassroom_id
            self.cargarDatos()

            # cargar los topic agregados de esa clase..
            self.senal_eligioUnCurso.emit(True)
            self.bel_clase_nombreNbGrader.setText(
                "Ninguna clase NbGrader seleccionada"
            )


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

        if cursoClassroom_id and len(self.listaIds_topicsClaseClassroom)>0:
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
                    programaTopic_id=self.listaIds_topicsClaseClassroom[noRenglon],
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


        self.listaIds_topicsClaseClassroom.append(tupla_topic_programas[0])


    def eliminarRenglonTopic(self,numeroRenglon):
        if numeroRenglon != self.indice_topic_sele:
            respuestaPositiva=self.msg_preguntarEleccionBorrarTopic(
                apartadoProgram_nombre=self.tableWidget.item(numeroRenglon, 0).text()
            )

            if respuestaPositiva:
                cursoClassroom_id,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()
                self.baseDatosLocalClassRoom.eliminarTopic(curso_id=cursoClassroom_id,
                                                           topicProgramas_id=self.listaIds_topicsClaseClassroom[numeroRenglon])
                self.tableWidget.removeRow(numeroRenglon)
                self.listaIds_topicsClaseClassroom.pop(numeroRenglon)

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
        Este metodo es diseñado para cargar los datos de la clase de classroom seleccionada.
        ¿Que datos carga?
        -   Carga los topics de la clase de classroom con ayuda de  la base de datos local
            que los almacena.
                    - En la tabla muestra los topics que el profesor ha elegido con anterioridad
                    - En la ventana que sirve para agregar los topcis a la tabla carga los topcis
                    faltantes
        '''

        claseClassroom_idApi,claseClassroom_nombre = self.configuracionCalificador.get_id_nombre_cursoClassroom()
        topicClassroom_idApi,topicClassroom_nombre = self.configuracionCalificador.get_id_nombre_topicClassroom()


        if claseClassroom_idApi!=None :
            self.cargarTopicsCurso()
            self.bel_nombreClase_classroom.setText( claseClassroom_nombre )
            self.senal_eligioUnCurso.emit(True)

            # Seleccionar renglon...
            if topicClassroom_idApi!=None:
                renglonSeleccionar=self.listaIds_topicsClaseClassroom.index(topicClassroom_idApi)
                self.colorearRenglon(renglonSeleccionar,recursos.App_Principal.COLOR_TOPIC_SELECCIONADO)
                self.indice_topic_sele=renglonSeleccionar
                self.senal_eligioTopic.emit(True)

            # Colocando el nombre al curso nbgrader
            if self.configuracionCalificador.get_nombre_cursoNbGrader() != None:
                respuestaPositiva = self.ventana_cambiadorClases_NbGrader.cargarClaseNbGrader(
                    self.configuracionCalificador.get_nombre_cursoNbGrader()
                )

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


    def cargarTopicsCurso(self):
        '''
        Este metodo carga los topics que fueron agregados con anterioridad a la tabla
        por parte del profesor.
        ¿De que clase de classroom carga los topics?
            R= De la clase de classroom seleccionada
        Este metodo es usualmente llamado cuando se cambia de clase de classroom seleccionada
        '''


        claseClassroom_idApi,_=self.configuracionCalificador.get_id_nombre_cursoClassroom()

        if claseClassroom_idApi != None:

            # carga los topics que han sido agregados con anteriodidad por parte del profesor
            topicsAgregados = self.baseDatosLocalClassRoom.get_topicsAgregados(course_id_api=claseClassroom_idApi)

            self.listaIds_topicsClaseClassroom = []
            tuplaDatos = []
            self.tableWidget.setRowCount(0)  # Eliminando todas las filas de la tabla

            if topicsAgregados != () and len(topicsAgregados) > 0:
                for topicClassroom_idApi, topicClassroom_nombre in topicsAgregados:
                    self.listaIds_topicsClaseClassroom.append(topicClassroom_idApi)
                    tuplaDatos.append( (topicClassroom_nombre,)  )

            self.cargarDatosEnTabla(tuplaDatos=tuplaDatos)



    def cargarDatosEnTabla(self,tuplaDatos):
        '''
        Cargara los nombre de los topcis que vienen inmerso en el valor que tomara el
        parametro con nombre de: 'tuplaDatos'

        Parametros:
            tuplaDatos (tuple): Es una tupla de n elementos donde cada elemento de ellas
            representa el nombre de un topic de la clase de classroom seleccionada.
        '''

        if len(tuplaDatos)>0:
            FILAS = len(tuplaDatos)
            self.tableWidget.setRowCount(FILAS)

            for f in range(FILAS):
                dato_celda_string = str(tuplaDatos[f][0])
                a = QtWidgets.QTableWidgetItem(dato_celda_string)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                self.tableWidget.setItem(f,0, a)



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
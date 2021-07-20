from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5 import QtCore,QtGui

from CUERPO.DISENO.TAREA.TareaMain_d import  Ui_Form
from CUERPO.LOGICA.TAREA.AgregadorCourseWork import AgregadorCourseWorks
from CUERPO.LOGICA.TAREA.CreadorTarea import CreadorTareas
import recursos

class TareaMain(QWidget,Ui_Form,recursos.HuellaAplicacion):

    #DATOS_MOSTRAR='Nombre,Calificadas,Por calificar,Fecha emision,Promedio'
    NO_COLUMNAS=5

    senal_verDetallesTarea = pyqtSignal(int)  # id de tarea
    senal_crearTarea=pyqtSignal(bool)
    senal_cambiarDeClase=pyqtSignal(bool)

    def __init__(self,baseDatosLocalClassRoom,administradorProgramasClassRoom):
        QWidget.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

        # BREVES CONFIGURACIONES DE DISEÑO DE LA TABLA...
        self.configurarTabla()

        # Cargando y mostrando todas las tareas de programación creadas

        self.administradorProgramasClassRoom=administradorProgramasClassRoom
        #self.cargarDatosEnTabla(self.datosTareas)
        self.baseDatosLocalClassRoom=baseDatosLocalClassRoom



        # SENALES DE LOS OBJETOS DE ESTA VENTANA...
        # self.btn_verCuestionarios.clicked.connect(self.verCuestionariosCreador)

        self.ventanaAgregadoraTareas = AgregadorCourseWorks(
            administradorProgramasClassRoom=self.administradorProgramasClassRoom
        )

        self.ventanaCreadoraTareas=CreadorTareas(
            listaNombresTareasYaCreadas=[],
            administradorProgramasClassRoom=self.administradorProgramasClassRoom
        )




        self.tableWidget.itemDoubleClicked.connect(self.verDetallesTarea)
        self.btn_crearTarea.clicked.connect(lambda : self.ventanaCreadoraTareas.show() )
        self.btn_importarTarea.clicked.connect( self.mostrarVentanaAgregadora_tareas )
        self.btn_regresar.clicked.connect(self.regresarMenu)

        self.ventanaAgregadoraTareas.senal_courseWork_selec.connect(self.agregarCouseWork_aTabla)
        self.ventanaCreadoraTareas.senalUsuarioCreoTarea.connect(self.agregarCouseWork_aTabla)

        self.listaIds_courseworks=[]

        # estableciendo opciones a partir del clic derecho a los items de la tabla
        # con la finalidad de que aparezca la opcion de eliminar objetos
        self.tableWidget.installEventFilter(self)


        self.btn_calificarPendientes.clicked.connect(self.calificarTareas)


    def calificarTareas(self):
        self.administradorProgramasClassRoom.calificarEstudiantes(
            courseWork_id=self.listaIds_courseworks[self.indexTareaSeleccionada],
            courseWork_name=self.nombreTareaSeleccionada,
        )


    def verDetallesTarea(self, index):
        index = index.row()

        # Cargando los datos del coursework
        nombre = self.tableWidget.item(index, 0).text()
        fecha = self.tableWidget.item(index, 1).text()

        if self.administradorProgramasClassRoom.existeEsaTarea_cursoNbGrader(nombreTarea=nombre):
            self.btn_calificarPendientes.setEnabled(True)
            self.nombreTareaSeleccionada=nombre
            self.indexTareaSeleccionada=index

        else:
            self.btn_calificarPendientes.setEnabled(False)

        coursework_id = self.listaIds_courseworks[index]

        self.bel_nombre.setText(nombre)
        self.bel_fechaCreacion.setText(fecha)

        self.listWidget.setCurrentIndex(1)

        #self.administradorProgramasClassRoom.get_informacionTareasEntregadas(courseWork_id=coursework_id)



    def eliminarRenglonTopic(self,numeroRenglon):
        respuestaPositiva=self.msg_preguntarEleccionBorrarCourseWork(
            nombreCourseWork=self.tableWidget.item(numeroRenglon, 0).text()
        )

        if respuestaPositiva:

            courseWork_id=self.listaIds_courseworks[numeroRenglon]
            self.tableWidget.removeRow(numeroRenglon)
            self.listaIds_courseworks.pop(numeroRenglon)
            self.administradorProgramasClassRoom.eliminarCourseWork_baseDatosLocal(
                courseWork_id=courseWork_id
            )


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

                if menu.exec_(event.globalPos()):
                    self.eliminarRenglonTopic(indiceEliminar)

            except Exception as e:
                print(e)

            return True
        return super().eventFilter(source, event)




    def agregarCouseWork_aTabla(self,tuplaDatos):
        '''
        tuplaDatos:
            - 1er elemento=id coursework
            - 2do elemento=nombre coursework
            - 3er elemento=fecha coursework

        :param tuplaDatos:
        :return:
        '''


        noRenglones = self.tableWidget.rowCount()
        self.tableWidget.insertRow(noRenglones)

        # Guardando el id en la lista
        self.listaIds_courseworks.append(tuplaDatos[0])

        #Agregando nombre
        celda=QtWidgets.QTableWidgetItem(tuplaDatos[1])
        celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setItem(noRenglones, 0,celda )

        #Agregando fecha
        celda=QtWidgets.QTableWidgetItem(tuplaDatos[2])
        celda.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget.setItem(noRenglones, 1,celda )



    def mostrarVentanaAgregadora_tareas(self):
        self.ventanaAgregadoraTareas.cargarDatos_courseWorks()
        self.ventanaAgregadoraTareas.show()
        pass



    def actuarCambioCurso(self):
        id,nombre=self.administradorProgramasClassRoom.get_datosCurso()
        print("blaaaaaaaaaaaaaaaaaaaaaaaa",id,nombre)
        if nombre!=None:
            self.bel_nombreCurso.setText(nombre)
            self.tableWidget.setRowCount(0)


    def actuarCambioTopic(self):
        id,nombre=self.administradorProgramasClassRoom.get_datosTopic()
        print("blaaaaaaaaaaaaaaaaaaaaaaaa", id, nombre)
        if nombre!=None:
            self.bel_nombreTopic.setText(nombre)
            self.tableWidget.setRowCount(0)
            self.cargarDatos()




    def preguntarAcercaCambioClase(self):

        ventanaDialogo = QMessageBox()
        #ventanaDialogo.setIcon(QMessageBox.Question)
        #ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        #ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText("¿Seguro que quieres cambiar de clase?")
        ventanaDialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton() == btn_yes:
            self.senal_cambiarDeClase.emit(True)



    def regresarMenu(self):
        self.listWidget.setCurrentIndex(0)






    def configurarTabla(self):

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        header = self.tableWidget.horizontalHeader()

        self.COLOR_TABLA = "#EEF2F3"
        self.COLOR_RESPUESTA = "#9AE5E0"
        stylesheet = "QTableView{selection-background-color: " + self.COLOR_RESPUESTA + "};"
        # stylesheet += "background-color:" + self.COLOR_TABLA + ";}"
        self.tableWidget.setStyleSheet(stylesheet)

        # la tabla tiene 3 columnas
        # ("NOMBRE","DATA_TIME", "PREGUNTAS")
        header = self.tableWidget.horizontalHeader()
        for columna in range(0, 3):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.verticalHeader().setDefaultSectionSize(60)


    def cargarDatos(self):
        '''
        Cuando se detecte un cambio de topic es por que ya se eligio un curso y un topic...
        :return:
        '''

        tuplaDatosCourseWorks= self.administradorProgramasClassRoom.get_courseWorksAgregados_baseDatosLocal()
        tuplaDatosMostrar=[]
        self.listaIds_courseworks=[]
        self.tableWidget.setRowCount(0)
        if tuplaDatosCourseWorks != () and len(tuplaDatosCourseWorks) != 0:
            for courseWork_api_id, titulo, descripccion, fechaCreacion in tuplaDatosCourseWorks:
                tuplaDatosMostrar.append((titulo, fechaCreacion))
                self.listaIds_courseworks.append(courseWork_api_id)
            self.cargarDatosEnTabla(tuplaDatos=tuplaDatosMostrar)


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

        # Nombre,Calificadas,Por calificar,Fecha emision,Promedio
        FILAS = len(tuplaDatos)
        #COLUMNAS = self.NO_COLUMNAS
        COLUMNAS=2

        self.noCuestionarios = FILAS
        self.tableWidget.setRowCount(FILAS)

        for f in range(FILAS):
            for c in range(COLUMNAS):
                dato_celda_string = str(tuplaDatos[f][c])
                a = QtWidgets.QTableWidgetItem(dato_celda_string)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                self.tableWidget.setItem(f, c, a)
        self.tableWidget.selectRow(0)

##################################################################################################################################################
# MENSAJES
##################################################################################################################################################

    def msg_preguntarEleccionBorrarCourseWork(self,nombreCourseWork):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Seguro de querer ELIMINAR al CourseWork: programa:<<{}>> ".format(nombreCourseWork)
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
    application = TareaMain()
    application.show()
    app.exit(app.exec())
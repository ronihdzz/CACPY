from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana


from CUERPO.DISENO.TAREA.VisualizadorTareas_d import  Ui_Form



class VisualizadorTareas(QWidget,Ui_Form):

    #DATOS_MOSTRAR='Nombre,Calificadas,Por calificar,Fecha emision,Promedio'
    NO_COLUMNAS=5

    senal_verDetallesTarea = pyqtSignal(int)  # id de tarea
    senal_crearTarea=pyqtSignal(bool)
    senal_cambiarDeClase=pyqtSignal(bool)

    def __init__(self,datosTareas):
        Ui_Form.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)

        # BREVES CONFIGURACIONES DE DISEÑO DE LA TABLA...
        self.configurarTabla()

        # Cargando y mostrando todas las tareas de programación creadas

        self.datosTareas=datosTareas
        self.cargarDatosEnTabla(self.datosTareas)

        # SENALES DE LOS OBJETOS DE ESTA VENTANA...
        # self.btn_verCuestionarios.clicked.connect(self.verCuestionariosCreador)
        self.tableWidget.itemDoubleClicked.connect(self.verDetallesTarea)
        self.btn_agregarTarea.clicked.connect(lambda : self.senal_crearTarea.emit(True) )
        self.btn_editarClase.clicked.connect(self.preguntarAcercaCambioClase)


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



    def verDetallesTarea(self,index):
        index = index.row()
        self.senal_verDetallesTarea.emit(index)


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
        COLUMNAS = self.NO_COLUMNAS

        self.noCuestionarios = FILAS
        self.tableWidget.setRowCount(FILAS)

        for f in range(FILAS):
            for c in range(COLUMNAS):
                dato_celda_string = str(tuplaDatos[f][c])
                a = QtWidgets.QTableWidgetItem(dato_celda_string)
                a.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # change the alignment
                self.tableWidget.setItem(f, c, a)
        self.tableWidget.selectRow(0)




if __name__ == '__main__':
    app = QApplication([])
    application = VisualizadorTareas()
    application.show()
    app.exit(app.exec())
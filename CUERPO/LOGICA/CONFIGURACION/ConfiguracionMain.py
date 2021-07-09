from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.CONFIGURACION.ConfiguracionMain_d import Ui_Form




class ConfiguracionMain(QtWidgets.QWidget,Ui_Form):
    #DATOS_MOSTRAR='Topic programacion, Topic de retrolimentacion'
    NO_COLUMNAS=2

    #senal_verDetallesTarea = pyqtSignal(int)  # id de tarea

    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        # BREVES CONFIGURACIONES DE DISEÑO DE LA TABLA...
        self.configurarTabla()

        # Cargando y mostrando todas las apartados de  programación

        #self.datosTareas=datosTareas
        self.datosApartados=(
            ('P_1','R_1'),
            ('P_2', 'R_2'),
            ('P_3', 'R_3'),
            ('P_4', 'R_4')
        )
        self.cargarDatosEnTabla(self.datosApartados)

        # SENALES DE LOS OBJETOS DE ESTA VENTANA...
        # self.btn_verCuestionarios.clicked.connect(self.verCuestionariosCreador)

        self.tableWidget.itemDoubleClicked.connect(self.seleccionarApartado)


        self.btn_edit_or_cancelEdit_aparSelec.clicked.connect(self.edit_or_cancelEdit_aparSelec)
        self.btn_agregar_or_guardar_apar.clicked.connect(self.add_or_save_apar)

        #self.btn_editarApartadoSeleccionado.clicked.connect(self.apartado_cambiar_elegir)


        # Configuraciones iniciales
        self.tableWidget.setEnabled(False)
        #self.btn_agregarApartado.clicked.connect()


        self.MODO_CAMBIAR_APARTADO=False



####################################################################################################################
# APARTADO SELECCIONADO
####################################################################################################################

    def preparar_posibleEdicion_aparSelec(self):

        self.tableWidget.setEnabled(True)
        # Boton en modo de guardar apartado seleccionado
        self.btn_agregar_or_guardar_apar.setStyleSheet(
            '''
            QPushButton{border-image: url(:/main/IMAGENES/guardar_off.png);}
            QPushButton:hover {border-image: url(:/main/IMAGENES/guardar_on.png);}
            QPushButton:pressed {border-image: url(:/main/IMAGENES/guardar_off.png);}
            ''')
        self.bel_agregar_or_guardar_apar.setText('Guardar')

        # Boton en modo de cancelar edicion
        self.btn_edit_or_cancelEdit_aparSelec.setStyleSheet(
            '''
            QPushButton{border-image: url(:/main/IMAGENES/tache_off.png);}
            QPushButton:hover {border-image: url(:/main/IMAGENES/tache_on.png);}
            QPushButton:pressed {border-image: url(:/main/IMAGENES/tache_off.png);}
            ''')
        self.bel_edit_or_cancelEdit_aparSelec.setText('Cancelar\nedicion')

    def restaurar_posibleEdicion_aparSelec(self):

        self.tableWidget.setEnabled(False)
        # Boton modo agregar apartado
        self.btn_agregar_or_guardar_apar.setStyleSheet('''
        QPushButton{border-image: url(:/main/IMAGENES/plus_off.png);}
        QPushButton:hover {border-image: url(:/main/IMAGENES/plus_on.png);}
        QPushButton:pressed {border-image: url(:/main/IMAGENES/plus_off.png);}
        ''')
        self.bel_agregar_or_guardar_apar.setText("Agregar\npartado")

        # Boton modo editar
        self.btn_edit_or_cancelEdit_aparSelec.setStyleSheet('''
        QPushButton{border-image: url(:/main/IMAGENES/edit_off.png);}
        QPushButton:hover {border-image: url(:/main/IMAGENES/edit_off.png);}
        QPushButton:pressed {border-image: url(:/main/IMAGENES/edit_off.png);}
        ''')
        self.bel_edit_or_cancelEdit_aparSelec.setText("Editar")

    # editar o cancelar apartado seleccionado
    def edit_or_cancelEdit_aparSelec(self):

        self.MODO_CAMBIAR_APARTADO=not(self.MODO_CAMBIAR_APARTADO)
        if self.MODO_CAMBIAR_APARTADO:
            self.preparar_posibleEdicion_aparSelec()
        else:
            self.restaurar_posibleEdicion_aparSelec()

    def add_or_save_apar(self):

        # Si se esta en modo de edicion de apartado este boton
        # funcionara como guardador de cambios
        if self.MODO_CAMBIAR_APARTADO:
            self.MODO_CAMBIAR_APARTADO=False # como ya se guardo el cambio ya no se esta en modo
                                             # de editar apartado

            # Guardar cambios y regresar a la normalidad
            self.restaurar_posibleEdicion_aparSelec()


        # Si no esta en modo de edicion este boton funcionara como
        # agregador de apartados
        else:
            # Iniciar proceso de agregar
            pass





####################################################################################################################
# APARTADO SELECCIONADO
####################################################################################################################

        #    self.tableWidget.setEnabled(True)



        ventanaDialogo = QMessageBox()
        #ventanaDialogo.setIcon(QMessageBox.Question)
        #ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        #ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)





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
            pass



    def seleccionarApartado(self,index):
        index = index.row()


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
        for columna in range(0,self.NO_COLUMNAS):
            header.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
            #header.setSectionResizeMode(columna, QtWidgets.QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)


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
    application = ConfiguracionMain()
    application.show()
    app.exit(app.exec())
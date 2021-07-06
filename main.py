from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel,QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana



from VisualizadorTareas import VisualizadorTareas
from MostradorDetallesTarea import MostradorDetallesTareas
from CalificadorEnDirecto import CalificadorEnDirecto
from CreadorTarea import CreadorTareas
from CUERPO.DISENO.main_d import  Ui_MainWindow



class Main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)



        # Nombre,Calificadas,Por calificar,Fecha emision,Promedio
        datos_prueba=(
            ('Tararea_1',10,50,'20/08/30 5:40 pm',9.5),
            ('Tararea_1', 10, 50, '20/08/30 5:40 pm', 9.5),
            ('Tararea_1', 10, 50, '20/08/30 5:40 pm', 9.5),
            ('Tararea_1', 10, 50, '20/08/30 5:40 pm', 9.5),
            ('Tararea_1', 10, 50, '20/08/30 5:40 pm', 9.5),
        )

        # Creacion de las ventanas
        self.ventana_visualizadorTareas=VisualizadorTareas(datosTareas=datos_prueba)
        self.ventana_mostradorDetallesTarea = MostradorDetallesTareas()
        self.ventana_calificadorEnDirecto=CalificadorEnDirecto()
        self.ventana_creadorTareas=CreadorTareas(listaNombresTareasYaCreadas=[])

        self.listWidget.addWidget(self.ventana_visualizadorTareas)
        self.listWidget.addWidget(self.ventana_mostradorDetallesTarea)


        # Enlazano las señales de las ventanas

        self.ventana_visualizadorTareas.senal_crearTarea.connect(self.mostrarCreadorTareas)


        self.ventana_visualizadorTareas.senal_verDetallesTarea.connect(self.verDetalleTarea)

        self.ventana_mostradorDetallesTarea.senal_regresar.connect(self.mostrarMenuTodasTareas)
        self.ventana_mostradorDetallesTarea.senal_calificarDirecto.connect(self.mostrarCalificadorEnVivo)
        self.ventana_calificadorEnDirecto.senal_calificadorEnDirecto_termino.connect(self.desbloquearAplicacionCentral)

        self.ventana_creadorTareas.senalUsuarioSoloCerroVentana.connect(self.desbloquearAplicacionCentral)
        self.ventana_creadorTareas.senalUsuarioCreoTarea.connect(self.registrarTareaCreada)


        # VENTANA CON LA QUE SE INICIA POR DEFAULT...
        self.listWidget.setCurrentIndex(0)
        self.listWidget.showFullScreen()


    def mostrarCreadorTareas(self):
        self.setEnabled(False)
        self.ventana_creadorTareas.show()

    def registrarTareaCreada(self):
        pass

    def verDetalleTarea(self,tuplaDatosTarea):
        self.listWidget.setCurrentIndex(1)

    def mostrarMenuTodasTareas(self):
        self.listWidget.setCurrentIndex(0)

    def mostrarCalificadorEnVivo(self):
        self.setEnabled(False)
        self.ventana_calificadorEnDirecto.show()

    def desbloquearAplicacionCentral(self):
        self.setEnabled(True)




    def closeEvent(self, event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerra el programa, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa.
        '''

        ventanaDialogo = QMessageBox()
        #ventanaDialogo.setIcon(QMessageBox.Question)
        #ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        #ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        ventanaDialogo.setText("¿Seguro que quieres salir?")
        ventanaDialogo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btn_yes = ventanaDialogo.button(QMessageBox.Yes)
        btn_yes.setText('Si')
        btn_no = ventanaDialogo.button(QMessageBox.No)
        btn_no.setText('No')
        ventanaDialogo.exec_()
        if ventanaDialogo.clickedButton() == btn_yes:
            event.accept()
        else:
            event.ignore()  # No saldremos del evento




if __name__ == '__main__':
    app = QApplication([])
    application = Main()
    application.show()
    app.exit(app.exec())
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana


from CUERPO.DISENO.MostradorDetallesTareas_d import  Ui_Form



class MostradorDetallesTareas(QWidget,Ui_Form):

    senal_regresar= pyqtSignal(bool)  # id de tarea
    senal_calificarDirecto=pyqtSignal(bool)

    def __init__(self):
        Ui_Form.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)

        self.btn_regresar.clicked.connect(lambda : self.senal_regresar.emit(True)  )
        self.btn_calificarVivo.clicked.connect(lambda : self.senal_calificarDirecto.emit(True) )



if __name__ == '__main__':
    app = QApplication([])
    application = MostradorDetallesTareas()
    application.show()
    app.exit(app.exec())
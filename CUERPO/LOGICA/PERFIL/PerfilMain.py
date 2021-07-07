from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5.QtWidgets import QApplication


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.PERFIL.PerfilMain_d import Ui_Form




class PerfilMain(QtWidgets.QMainWindow,Ui_Form):

    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication([])
    application = PerfilMain()
    application.show()
    app.exit(app.exec())
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5.QtWidgets import QApplication


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.CONFIGURACION.ConfiguracionMain_d import Ui_Form




class ConfiguracionMain(QtWidgets.QMainWindow,Ui_Form):

    def __init__(self):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication([])
    application = ConfiguracionMain()
    application.show()
    app.exit(app.exec())
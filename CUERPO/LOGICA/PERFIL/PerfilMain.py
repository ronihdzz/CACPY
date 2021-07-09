from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5.QtWidgets import QApplication
from PyQt5 import  Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import  QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from os import getcwd

from datetime import datetime



###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.PERFIL.PerfilMain_d import Ui_Form
import recursos



class PerfilMain(QtWidgets.QWidget,Ui_Form):

    def __init__(self,profesor_correo,profesor_nombre,profesor_imagenPerfil):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.profesor_correo=profesor_correo
        self.profesor_nombre=profesor_nombre
        self.profesor_imagenPerfil=profesor_imagenPerfil



    def cargarPerfilProfesor(self):

        # Cargando los datos de correo y nombre del profesor.
        self.bel_profesor_correo.setText(self.profesor_correo)
        self.bel_profesor_nombre.setText(self.profesor_nombre)

        # Cargando la imagen
        imagen=self.profesor_imagenPerfil
        ancho=self.bel_imagenPerfilProfesor.width()
        alto=self.bel_imagenPerfilProfesor.height()

        pixmapImagen = QPixmap(imagen).scaled(ancho * 0.95, alto * 0.95, Qt.IgnoreAspectRatio,
                                              Qt.SmoothTransformation)
        self.bel_imagenPerfilProfesor.setAlignment(Qt.AlignCenter)
        self.bel_imagenPerfilProfesor.setPixmap(pixmapImagen)


if __name__ == '__main__':
    app = QApplication([])
    application = PerfilMain()
    application.show()
    app.exit(app.exec())
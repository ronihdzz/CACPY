from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5.QtWidgets import QApplication
from PyQt5 import  Qt
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import  QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from os import getcwd

from datetime import datetime


from CUERPO.LOGICA.PERFIL.ConfirmadorAccion import ConfirmadorAccion

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.PERFIL.PerfilMain_d import Ui_Form
import recursos



class PerfilMain(QtWidgets.QWidget,Ui_Form,recursos.HuellaAplicacion):
    senal_cerrarAplicacion = pyqtSignal(bool)

    def __init__(self,profesor_correo,profesor_nombre,profesor_imagenPerfil):
        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        recursos.HuellaAplicacion.__init__(self)

        self.setupUi(self)
        self.profesor_correo=profesor_correo
        self.profesor_nombre=profesor_nombre
        self.profesor_imagenPerfil=profesor_imagenPerfil

        self.btn_cerrarSesion.clicked.connect(self.confirmarAccionCerrarSesion)

        self.ventanaConfirmadorCerrarSesion=ConfirmadorAccion(
            indicaciones="Al cerrar sesión se borrara el token, por lo tanto si quieres "
                         "volver a usar el programa se te volveran a pedir los permisos, sin embargo si solo "
                         "deseas salir del programa y evitar nuevamente tener que conceder los permisos entonces  NO "
                         "cerrar sesión, y solo cerrar el programa dando clic izquierdo sobre el tache superior "
                         "derecho de la ventana de la aplicación. "
                         "Una vez explicado lo anterior ¿que deseas hacer? ¿sigues queriendo cerrar sesion?"
                         " de ser afirmativa tu respuesta escribe la frase  que se de indica a continuación",
            palabraConfirmacion='cerrar sesion'
        )
        self.ventanaConfirmadorCerrarSesion.accionConfirmada.connect(self.cerrarSesion)

    def confirmarAccionCerrarSesion(self):
        self.ventanaConfirmadorCerrarSesion.prepararMostrar()
        self.ventanaConfirmadorCerrarSesion.show()

    def cerrarSesion(self):

        recursos.App_Principal.borrarDatosSesionProfesor()
        self.senal_cerrarAplicacion.emit(True)











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
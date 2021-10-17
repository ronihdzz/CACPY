
'''
PerfilMain.py :
                    Contiene una sola  clase, la clase ' PerfilMain', la cual a grosso
                    modo sirve para mostrar los datos del usuario, es decir: correo electronico,
                    nombre y foto de perfil, asi como tambien ofrecce una opccion para cerrar sesión
                    al usuario con la finalidad de que este pueda iniciar sesión con otro
                    correo de gmail.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"

###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.LOGICA.PERFIL.ConfirmadorAccion import ConfirmadorAccion
from CUERPO.DISENO.PERFIL.PerfilMain_d import Ui_Form
import recursos



class PerfilMain(QtWidgets.QWidget,Ui_Form,recursos.HuellaAplicacion):
    '''
    El objetivo de esta clase es mostrar los datos del usuario que inicio sesion
    en CACPY, es decir esta clase:
        * Mostrara el correo electronico del usuario
        * Mostrara el nombre completo del usuario
        * Mostrara la imagen de perfil del usuario

    Otro de sus objetivos de esta clase es permitirle al usuario cerrar sesion
    en CACPY con el correo de gmail ingresado, con el objetivo que despues de
    cerrar sesión pueda inciar sesion con otro correo de gmail si asi lo desea.
    Es importante menccionar que si el usuario cierra sesión esta clase emitira
    la señal: 'senal_cerrarAplicacion'
    '''


    senal_cerrarAplicacion = pyqtSignal(bool)

    def __init__(self,profesor_correo,profesor_nombre,profesor_imagenPerfil):
        '''
        Parámetros:
            - profesor_correo (str): Correo electronico del profesor
            - profesor_nombre (str): Nombre completo del profesor
            - profesor_-imagenPerfil (str): Nombre completo de la imagen
            de perfil del profesor ¿a que me refiero por nombre completo?
            me refieron que el nombre abarca el nombre de la imagen asi
            como el nombre de la ruta en donde se encuentra ubicada,
            ejemplo: 'BLA/BLA/BLA/imagen.jpg'
        '''

        Ui_Form.__init__(self)
        QtWidgets.QWidget.__init__(self)
        recursos.HuellaAplicacion.__init__(self)

        self.setupUi(self)
        self.profesor_correo=profesor_correo
        self.profesor_nombre=profesor_nombre
        self.profesor_imagenPerfil=profesor_imagenPerfil

        self.btn_cerrarSesion.clicked.connect(self.mostrarVentana_cerrarSesion)

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

    def mostrarVentana_cerrarSesion(self):
        '''
        Este metodo mostrara la ventana que le permitira al usuario cerrar sesión
        si repite una frase respectiva
        '''

        self.ventanaConfirmadorCerrarSesion.prepararMostrar()
        self.ventanaConfirmadorCerrarSesion.show()

    def cerrarSesion(self):
        '''
        Este metodo se llamara cuando el usuario haya confirmado correctamente que desea
        cerrar sesion.
        Es importante mencionar que lo que conlleva cerrar sesion es la eliminacion de los siguientes
        archivos:
            - El token que se genero localmente para acceder a la API de Classroom
            y la API de Drive
            - La base de datos local que se genero para respaldar datos del Classroom
            del profesor
            - Los ficheros locales que contienen el nombre y correo electronico del profesor
            - La foto de gmail del profesor

        Es importante mencionar que es recomendable cerrar sesion cuando se desea inicar sesion
        con otro correo de gmail, ya que de esa forma cuando se vuelva a iniciar el programa
        se volvera a pedir un correo de gmail asi como los permisos respectivos
        '''

        recursos.App_Principal.borrarDatosSesionProfesor()
        self.senal_cerrarAplicacion.emit(True)

    def cargarPerfilProfesor(self):
        '''
        Mostrara los datos del profesor en las respectivas label
        de la GUI
        '''

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
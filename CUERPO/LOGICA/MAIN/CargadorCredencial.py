
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import (QMessageBox,QFileDialog)
from PyQt5.QtGui import QIcon
import os
###############################################################
#  IMPORTACION DEL LOGICA...
##############################################################


###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.MAIN.CargadorCrendencial_d import Ui_MainWindow
import recursos


class CargadorCrendencial(QtWidgets.QMainWindow, Ui_MainWindow, recursos.HuellaAplicacion):


    def __init__(self,classRoomControl):
        '''

        '''

        self.classRoomControl=classRoomControl

        QtWidgets.QMainWindow.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_cargarArchivos.clicked.connect(self.cargarArchivo)
        self.btn_finalizar.clicked.connect(self.generarToken)


        self.nombreArchivoElegido=None

        self.ARCHIVO_VALIDO=False




    def cargarArchivo(self):
        '''
        Este metodo abrira el explorador de archivos para que  el usuario pueda elegir el archivo  que
        contiene las credenciales.
        '''

        print("Agregando una cancion")
        archivoCredenciales_nombre, _ = QFileDialog.getOpenFileName(self, "Archivo de credenciales", "c://",
                                                 "Formatos validos (*.json)")
        if archivoCredenciales_nombre:
            archivoCredenciales_nombreFull = os.path.normpath(archivoCredenciales_nombre)  # normalizando la ruta

            self.nombreArchivoElegido=archivoCredenciales_nombreFull
            archivoCredenciales_soloNombre = archivoCredenciales_nombreFull.split(os.sep)[-1]

            # Copiando el archivo de credenciales
            self.bel_nombreArchivoSelec.setText(archivoCredenciales_soloNombre)


    def generarToken(self):

        if self.nombreArchivoElegido!=None:

            respuestaPositiva=self.msg_asegurarEleccion(self.nombreArchivoElegido)

            if respuestaPositiva:
                try:
                    self.ARCHIVO_VALIDO=False
                    self.classRoomControl.cargarArchivoCredenciales(self.nombreArchivoElegido)
                    self.classRoomControl.obtenerValor_service_classroom_and_drive()
                    self.msg_exitoCargarArchivo()
                    self.ARCHIVO_VALIDO=True

                except Exception as e:
                    self.classRoomControl.eliminarArchivoCredenciales()
                    self.msg_errorEnArchivoElegido(
                        nombreArchivoElegido=self.nombreArchivoElegido,
                        exception_presentada=e
                    )
        else:
            self.msg_debesCargarUnArchivo()


    def closeEvent(self, event):
        '''
        Cuando el usuario le de clic izquierdo sobre el boton de cerra el programa, el metodo
        que se llamara es este, el cual le preguntara al usuario si esta seguro de cerrar el
        programa, en caso de que su respuesta sea afirmativa se cerrara el programa.
        '''


        if self.ARCHIVO_VALIDO:
            event.accept()
        else:
            respuestaAfirmativa = self.msg_cerrarVentana()
            if respuestaAfirmativa:
                event.accept()
            else:
                event.ignore()




####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_cerrarVentana(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Esta seguro que quieres cerrar la ventana, recuerda que aun no has elegido un " \
                  "archivo de credenciales valido?"
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




    def msg_asegurarEleccion(self,nombreArchivoElegido):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = f"¿Esta seguro que el archivo cuyo nombre es: <<{nombreArchivoElegido}>> es el archivo " \
                  f"que contiene las credenciales?"
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

    def msg_debesCargarUnArchivo(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Debes cargar un archivo"
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)
        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



    def msg_exitoCargarArchivo(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "El archivo de credenciales cargado es valido y el token ya se ha generado " \
                  ",por favor cierra la aplicacion y vuelve a ejecutar el programa, y ya podras " \
                  "trabajar."


        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)
        ventanaDialogo.setText(mensaje)

        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')

        ventanaDialogo.exec_()

    def msg_errorEnArchivoElegido(self,nombreArchivoElegido,exception_presentada):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = f"El nombre del archivo: <<{nombreArchivoElegido}>> el cual fue el que elegiste " \
                  f"NO es correcto, por favor "
        mensaje+=f" elige un archivo valido ya que al cargar dicho archivo ocurrio el siguiente error: << " \
                 f"{exception_presentada}>>"
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)
        ventanaDialogo.setText(mensaje)

        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()







if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = CargadorCrendencial()
    application.show()
    app.exec()
    #sys.exit(app.exec())
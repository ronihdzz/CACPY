from PyQt5.QtWidgets import QDialog
import sys, re
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana
from PyQt5.QtGui import QIcon

###############################################################
#  IMPORTACION DEL DISEÑO...
##############################################################
from CUERPO.DISENO.PERFIL.ConfirmacionAccion_d import Ui_Dialog
import recursos
###############################################################
#  MIS LIBRERIAS...
##############################################################

class ConfirmadorAccion(QDialog, Ui_Dialog,recursos.HuellaAplicacion):
    # Metodo constructor:
    accionConfirmada = pyqtSignal(bool) #dira si la accion se confirmo bien...

    def __init__(self,indicaciones="",palabraConfirmacion=""):
        Ui_Dialog.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)


        self.reiniciar(indicaciones=indicaciones,palabraConfirmacion=palabraConfirmacion)


        self.lineEdit_wordRepetir.setReadOnly(True)
        self.textBrowser_indicaciones.setReadOnly(True)

        self.lineEdit_firma.textChanged.connect(self.validarFirma)
        self.btn_aceptar.clicked.connect(self.concretarAccion)


        self.firmaEscritaCorrectamente =False
        self.validarFirma()#para que se ponga en rojo...
        self.textBrowser_indicaciones.setOpenExternalLinks(True)
        self.textBrowser_indicaciones.setOpenLinks(True)



    def prepararMostrar(self):
        self.lineEdit_firma.setText("")
        self.firmaEscritaCorrectamente=False
        self.validarFirma()


    def reiniciar(self,indicaciones,palabraConfirmacion,esHtmlIndicaciones=False):
        if esHtmlIndicaciones:
            self.textBrowser_indicaciones.setHtml(indicaciones)
        else:
            self.textBrowser_indicaciones.setPlainText(indicaciones)

        self.palabraConfirmacion = palabraConfirmacion
        self.lineEdit_wordRepetir.setText(self.palabraConfirmacion)
        self.lineEdit_firma.setText("")

        self.prepararMostrar()



    def cargarIndicaciones(self,indicaciones,esHtml=False):
        if esHtml:
            self.textBrowser_indicaciones.setHtml(indicaciones)
        else:
            self.textBrowser_indicaciones.setPlainText(indicaciones)


    def concretarAccion(self):
        if self.palabraConfirmacion!=self.lineEdit_firma.text():
            self.msg_lasPalabrasNoCoinciden()
        else:
            resultado=self.msg_cersiorarDesicion()
            if resultado:
                self.firmaEscritaCorrectamente=True
                self.close()

    # primer metodo para validar el dato nombre
    def validarFirma(self):
        if self.palabraConfirmacion!=self.lineEdit_firma.text():  # si la validacion no es correcta  (si  no es True)
            # modifcando el estilo del objeto etiqueta llamado 'nombre'
            self.lineEdit_firma.setStyleSheet("border-radius:5px; border:5px solid red;")
        else:  # no pasa ningun error
            self.lineEdit_firma.setStyleSheet("border-radius:5px; border: 5px solid green;")

    def closeEvent(self, event):
        if self.firmaEscritaCorrectamente:
            self.accionConfirmada.emit(True) # mandando nombre

        event.accept()

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_cersiorarDesicion(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: preguntarle el profesor
        si en realidad desea cerrar la aplicacion

        Returns:
            True : En caso de que el profesor presione el boton de 'Si'
            False: En caso de que el profesor presione el boton de 'No'
        '''
        
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "¿Estas seguro de lo que haras?"
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




    def msg_lasPalabrasNoCoinciden(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: informarle al
        profesor la razon por la cual no puede acceder al apartado de
        alumnos.
        '''

        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Critical)
        ventanaDialogo.setWindowIcon(QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Las palabras no coinciden"
        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()





########################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogo = ConfirmadorAccion("BLABLABLABLABLA","acepto los terminos")
    dialogo.show()
    app.exec_()


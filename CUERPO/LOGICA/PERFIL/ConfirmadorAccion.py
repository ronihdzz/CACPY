from PyQt5.QtWidgets import QDialog
import sys, re
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana

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
            QMessageBox.critical(self, "Atencion", "Las palabras no coinciden", QMessageBox.Ok)
        else:
            resultado = QMessageBox.warning(self,"Atencion",f"¿Estas seguro de lo que haras?",
                                             QMessageBox.Yes | QMessageBox.No)
            if resultado == QMessageBox.Yes:
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

########################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogo = ConfirmadorAccion("BLABLABLABLABLA","acepto los terminos")
    dialogo.show()
    app.exec_()


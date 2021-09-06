from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox,QHeaderView
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import  QMessageBox,QAction,QActionGroup,QWidget,QVBoxLayout,QTabWidget,QLabel
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QCompleter
#from PyQt5.QtGui import Qt

from PyQt5 import QtCore,QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   #mandas senales a la otra ventana


from CUERPO.DISENO.CONFIGURACION.CambiadorCarpetaDrive_d import Ui_Dialog
from CUERPO.LOGICA.PERFIL.ConfirmadorAccion import ConfirmadorAccion

import recursos
import os


class CambiadorCarpetaDrive(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):

    senal_eligioUnaCarpetaDrive=pyqtSignal(bool) #  curso_nombre

    def __init__(self,configuracionCalificador,classRoomControl):
        QtWidgets.QDialog.__init__(self)
        recursos.HuellaAplicacion.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador




        self.btn_realizarCambio.clicked.connect(self.comprobarExistenciaCarpeta)

        self.ventanaConfirmadorAccion=ConfirmadorAccion()

        self.ventanaConfirmadorAccion.accionConfirmada.connect(self.notificarCambiosCarpetaElegida)


        self.nombreCarpetaPropone=None
        self.idCarpetaPropone=None



    def notificarCambiosCarpetaElegida(self):
        if self.nombreCarpetaPropone:
            self.bel_nombreCarpetaActual.setText(self.nombreCarpetaPropone)

            self.configuracionCalificador.setDatosCarpetaRetroalimentacion(
                nombre=self.nombreCarpetaPropone,
                idApi=self.idCarpetaPropone
            )

            self.plainText_idCarpeta.setPlainText("")
            self.msg_exitoSeleccionarCarpeta()

            self.senal_eligioUnaCarpetaDrive.emit(True)


    def comprobarExistenciaCarpeta(self):
        idCarpeta=self.plainText_idCarpeta.toPlainText()

        if idCarpeta!="":
            try:
                response = self.classRoomControl.service_drive.files().get(
                    fileId=idCarpeta,
                    fields='name,webViewLink,mimeType'
                ).execute()

                nombre=response.get('name'),
                linkView=response.get('webViewLink')
                mimeType=response.get('mimeType')
                nombre = nombre[0]
                print(nombre)
                print(linkView)
                print(mimeType)

                # si el id del archivo que se ingreso no es el de una carpeta...
                if mimeType!='application/vnd.google-apps.folder':
                    self.msg_errorPorNoPonerIdCarpeta(
                        idArchivo=idCarpeta,
                        nombreArchivo=nombre,
                        tipoArchivo=mimeType
                    )

                else:
                    self.nombreCarpetaPropone=nombre
                    self.idCarpetaPropone=idCarpeta

                    self.mostrarMensajeConfirmacion(
                        nombreCarpeta=nombre,
                        idCarpeta=idCarpeta,
                        linkAccesoCarpeta=linkView,
                        nombre_linkAccesoCarpeta=nombre,
                    )


            except Exception as e:
                self.msg_errorIdCarpeta(idCarpeta=idCarpeta,excepccion=e)
        else:
            self.msg_noHayIdsBlancos()




    def mostrarMensajeConfirmacion(self,nombreCarpeta,idCarpeta,linkAccesoCarpeta,nombre_linkAccesoCarpeta):

#<p style="color:red;">This is a red paragraph.</p>
        mensajeAdvertencia = f'''

             <span style=" font-size:13px;font-family: TamilSangamMN;"> 
                El id que ingresaste fue: "{idCarpeta}" y la carpeta con dicho id 
                tiene el nombre de: "{nombreCarpeta}", por favor ingresa al siguiente link:
            </span>

            <span style=" font-size:13px;font-family: TamilSangamMN;">
                <a href="{linkAccesoCarpeta}"  style="color:black;"> 
                    <strong>{nombre_linkAccesoCarpeta}<\strong> 
                </a><
            /span>

             <span style=" font-size:13px;font-family: TamilSangamMN;"> 
                para corraborar que es la carpeta deseada.Una vez hecho lo anterior 
                ¿estas seguro que es la carpeta correcta?, si la respuesta es afirmativa 
                por favor haz lo que se indica a continuacion: 
            </span>            
            '''

        self.ventanaConfirmadorAccion.reiniciar(
            indicaciones=mensajeAdvertencia,
            palabraConfirmacion="acepto el cambio de carpeta",
            esHtmlIndicaciones=True
        )
        self.ventanaConfirmadorAccion.show()




##########################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################
    def msg_exitoSeleccionarCarpeta(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "La carpeta que elegiste ha sido guardada correctamente, " \
                  "ya puedes cerrar esta ventana y tus cambios habran sido " \
                  "guardados"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()








    def msg_noHayIdsBlancos(self):
        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "No puedes dejar el apartado de Id en blanco,debes ingresar el id de " \
                  "la carpeta en donde deseas que se guarden las retroalimentaciones " \
                  "de tus cursos"

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()


    def msg_errorIdCarpeta(self,idCarpeta,excepccion):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Critical)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = f"El id: <<{idCarpeta}>> que fue el que  ingresaste como id de la carpeta, " \
                      f"no es valido por que ocaciono, el siguiente error: <<{excepccion}>> " \
                      f"por favor revisa que el id ingresado haya sido el correcto"

            mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()

    def msg_errorPorNoPonerIdCarpeta(self,idArchivo,nombreArchivo,tipoArchivo):
            ventanaDialogo = QMessageBox()
            ventanaDialogo.setIcon(QMessageBox.Critical)
            ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
            ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

            mensaje = f"El id: <<{idArchivo}>> que fue el que  ingresaste como id de la carpeta, " \
                      f"NO resulto ser el id de una carpeta de drive, si no resulto ser el id de un " \
                      f"archivo de tipo: <<{tipoArchivo}>> cuyo nombre es: <<{nombreArchivo}>>, por favor " \
                      f"ingresa un id de una carpeta de drive "

            mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

            ventanaDialogo.setText(mensaje)
            ventanaDialogo.setStandardButtons(QMessageBox.Ok)
            btn_ok = ventanaDialogo.button(QMessageBox.Ok)
            btn_ok.setText('Entendido')
            ventanaDialogo.exec_()


if __name__ == '__main__':
    app = QApplication([])
    application = CambiadorClases_NbGrader()
    application.show()
    app.exit(app.exec())
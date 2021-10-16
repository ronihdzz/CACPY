
'''
CambiadorCarpetaDrive.py :  Contiene una sola  clase, la clase 'CambiadorCarpetaDrive', la cual  es una clase
                            que a grosso modo se encarga de hacer posible que el usuario pueda seleccionar la
                            carpeta de google drive en donde desea que se almacenen las retroalimentaciones de
                            sus estudiantes
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.CONFIGURACION.CambiadorCarpetaDrive_d import Ui_Dialog
from CUERPO.LOGICA.PERFIL.ConfirmadorAccion import ConfirmadorAccion
import recursos



class CambiadorCarpetaDrive(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Dicha clase permite al usuario establecer la carpeta de google drive en donde
    se almacenaran todas las retroalimentaciones de sus estudiantes, sin embargo
    para lograr ello se encarga de hacer  validaciones de los datos que ingresa
    el usuario con el objetivo de cersiorar de que se eliga la carpeta de google
    drive de forma correcta.Si el usuario elige una carpeta de google drive de
    forma correcta esta clase emitira una señal.
    '''

    senal_eligioUnaCarpetaDrive=pyqtSignal(bool) # Mandara el valor de: True cuando
                                                 # el usuario haya seleccionado una
                                                 # carpeta de google drive.

    def __init__(self,configuracionCalificador,classRoomControl):
        '''
        Parámetros:
            - configuracionCalificador (objeto de la clase: CalificadorConfiguracion): dicho objeto
            contiene ordenados los datos de configuracion que necesitara el programa, asi como tambien
            contiene metodos que serviran para obtener o editar dichos datos

            - classRoomControl (objeto de la clase: ClassRoomControl): dicho objeto es una capa
            de abstracción para poder hacer algunas peticiones al ClassRoom del profesor, asi
            como al GoogleDrive del profesor
        '''

        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)
        

        self.classRoomControl=classRoomControl
        self.configuracionCalificador=configuracionCalificador


        self.btn_realizarCambio.clicked.connect(self.procesar_IDdeCarpetaIngresado)
        self.ventanaConfirmadorAccion=ConfirmadorAccion()
        self.ventanaConfirmadorAccion.accionConfirmada.connect(self.notificarCambiosCarpetaElegida)


        self.nombreCarpetaPropone=None  # nombre de la carpeta de google drive que el usuario selecciono
        self.idCarpetaPropone=None  # nombre de la carpeta de google drive que el usuario selecciono




    def procesar_IDdeCarpetaIngresado(self):
        '''
        Cuando el usuario haya ingresado el id de la carpeta en donde
        desea que se guarden todas las retroalimentaciones, y despues de
        ingresar dicho ID, haya dado clic sobre el boton 'Realizar cambio'
        se llamara a este metodo con el objetivo de:
           - Validar si el ID ingresado por el usuario es un ID valido es decir,
             corroborara que el ID ingresado corresponda al ID de una  carpeta de google drive
             del usuario, en caso de que el ID si coincida con el de un ID de una carpeta de google
             drive del usuario, ahora se le preguntara al usuario si en realidad desea establecer
             dicha carpeta como la carpeta guardadora de las las retroalimentaciones de sus alumnos,
             si el usuario responde afirmativamente entonces se proseguira a guardar dichos cambios
             y cerrar la ventana.
        '''


        # obteniendo el id ingresado por el usuario
        idCarpeta=self.plainText_idCarpeta.toPlainText()


        if idCarpeta!="":
            try:
                # obteniendo el archivo de google drive al que le corresponde
                # el ID que ingreso el usuario
                response = self.classRoomControl.service_drive.files().get(
                    fileId=idCarpeta,
                    fields='name,webViewLink,mimeType'
                ).execute()

                nombre=response.get('name')
                linkView=response.get('webViewLink')
                mimeType=response.get('mimeType')


                # si el ID ingresado  no es el ID de una carpeta...
                if mimeType!='application/vnd.google-apps.folder':
                    self.msg_errorPorNoPonerIdCarpeta(
                        idArchivo=idCarpeta,
                        nombreArchivo=nombre,
                        tipoArchivo=mimeType
                    )

                # el ID ingresado si corresponde al ID de una carpeta de google drive
                # del usuario
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
        '''
        * Mostrara el nombre de la carpeta del ID que ingreso el usuario
        * Permitira acceder a la carpeta del ID que ingreso el usuario, si el usuario da  un clic izquierdo
        sobre un link.

        La ventana hace todo lo anterior por que su función principal es mostrarle al usuario cual es
        la carpeta del ID que ingreso, para  que el usuario tome una desición mas confiada acerca de
        si si es la carpeta de google drive en donde desea que se almacenen todas las retroalimentaciones
        de sus estudiantes, en caso de que asi sea, esta ventana le hara escribir una frase especifica al usuario,
        para poder confirmar, si el usuario acompleta la frase, esta ventana emitira una señal
        para que se guarden los datos de la carpeta de google drive.

        Parámetros:
            - nombreCarpeta (str) : Nombre de la carpeta de google drive cuyo ID corresponde al
              ID que el usuario ingreso
            - idCarpeta (str) : El ID de la carpeta de google drive que ingreso el usuario
            - linksAccesoCarpeta (str): El link de acceso a la carpeta cuyo ID corresponde al
              ID que el usuario ingreso
            - nombre_linkAccesoCarpeta (str): El nombre con el que se ocultara el link de acceso
              a la carpeta cuyo ID corresponde al ID que el usuario ingreso
        '''

        # Mensaje en HTML de lo que se le mostrara al usuario.
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



    def notificarCambiosCarpetaElegida(self):
        '''
        Este metodo se encargara de guardar los datos de la carpeta de google drive
        que el usuario decidio elegir, posteriormente le notificara al usuario
        que los datos fueron cargados exitosamente despues mandara una señal
        para avisar que el usuario selecciono una carpeta de google drive y finalmente
        cerrara la ventana.
        '''

        if self.nombreCarpetaPropone:
            self.bel_nombreCarpetaActual.setText(self.nombreCarpetaPropone)

            self.configuracionCalificador.setDatosCarpetaRetroalimentacion(
                nombre=self.nombreCarpetaPropone,
                idApi=self.idCarpetaPropone
            )

            self.plainText_idCarpeta.setPlainText("")
            self.msg_exitoSeleccionarCarpeta()

            self.senal_eligioUnaCarpetaDrive.emit(True)

            self.close()



##########################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################
    def msg_exitoSeleccionarCarpeta(self):
        '''
        Ventana emergente informativa que se le mostrara al usuario
        cuando este haya realizado con exito la seleccion de la
        carpeta de google drive en donde se almacenaran las retroalimentaciones
        de sus estudiantes.
        '''


        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "La carpeta que elegiste ha sido guardada correctamente, " \
                  "a continuación se cerraran las ventanas y podras ver "
        mensaje+="nuevamente el apartado de: 'Mis configuraciones' "

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



    def msg_noHayIdsBlancos(self):
        '''
        Ventana emergente informativa que se le mostrara al usuario
        cuando este quiere validar un ID vacio, es decir cuando este
        le da clic sobre el boton: 'Realizar cambio' y no puso nada
        en el aparto de ID de la ventana.
        '''

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
        '''
        Ventana emergente informativa que se le mostrara al usuario
        cuando se detecte que el ID ingresado por el usuario no es
        un ID valido.

        Parámetros:
            - idCarpeta (str) : El ID que el usuario ingreso
            - excepccion (str): La excepccion que surgio cuando el usuario
            trato de validar el ID que ingreso y que resulto erroneo
        '''

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
        '''
        Ventana emergente informativa que se le mostrara al usuario cuando este quiere validar
        un ID que no corresponde a una carpeta de google drive.

        Parámetros:
            - idArchivo (str): El ID que el usuario ingreso
            - nombreArchivo (str) : Nombre del archivo al cual pertence al ID que el usuario
            ingreso
            - tipoArchivo (str): El tipo de arhivo  al cual pertence el archivo cuyo  ID es el que
             el usuario ingreso
        '''

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
    application = CambiadorCarpetaDrive()
    application.show()
    app.exit(app.exec())
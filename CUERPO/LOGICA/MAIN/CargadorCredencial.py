
'''
CargadorCredenciales.py :   Contiene una sola  clase, la clase 'CargadorCrendencial', la cual a grosso
                            modo se encarga de hacer posible que el usuario seleccione el archivo de
                            crendeciales respectivo para que se pueda iniciar el programa CACPY.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# librerias estandar
###########################################################################################################################################
import os

###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtGui import QIcon

###########################################################################################################################################
# fuente local
###########################################################################################################################################
from CUERPO.DISENO.MAIN.CargadorCrendencial_d import Ui_MainWindow
import recursos


class CargadorCrendencial(QtWidgets.QMainWindow, Ui_MainWindow, recursos.HuellaAplicacion):
    '''
    El objetivo principal de esta clase es cargar el archivo respectivo de credenciales del
    usuario, y con este perdile los permisos al usuario para poder generar el token que
    permitira a CACPY interactuar con el classroom y google drive del usuario.

    Es importante mencionar genera una ventana totalmente independiente a la de la ventana del
    programa CACPY, el unico objetivo de esta ventana es cargar el archivo de credenciales y procesarlo,
    despues de hacer lo anteriormente mencionado este programa ya no se volvera a abrir y unicamente
    se abrira la vetana que contiene todos los apartados de CACPY.
    '''


    TOKEN_GENERADO_EXITOSAMENTE=True # variable de bandera que nos permitira saber fuera de esta
                                     # clase, si el usuario genero el token o no.

    def __init__(self,classRoomControl):
        '''

        - classRoomControl (objeto de la clase: ClassRoomControl): dicho objeto es una capa
        de abstracción para poder hacer algunas peticiones al ClassRoom del profesor, asi
        como al GoogleDrive del profesor

        '''

        self.classRoomControl=classRoomControl

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)
        

        self.btn_abrirExploradorArchivos.clicked.connect(self.abrirExploradorArchivos_y_procesarArchivoElegido)
        self.btn_finalizar.clicked.connect(self.procesarArchivoCrendenciales_y_generarToken)


        self.nombreArchivoElegido=None # nombre del archivo de credenciales seleccionado
                                       # por el usuario

        CargadorCrendencial.TOKEN_GENERADO_EXITOSAMENTE=False  # su valor sera igual a True unicamente cuando
                                                               # se haya generado el token por el usuario


    def abrirExploradorArchivos_y_procesarArchivoElegido(self):
        '''
        Este metodo abrira el explorador de archivos para que el usuario pueda
        seleccionar el archivo de credenciales.Si el usuario elige un archivo
        de credenciales este metodo almacenara el nombre y  ubicacion de dicho
        archivo asi como tambien mostrara el nombre del archivo de credenciales
        en la label respectiva de la GUI
        '''

        archivoCredenciales_nombre, _ = QFileDialog.getOpenFileName(self, "Archivo de credenciales", "c://",
                                                 "Formatos validos (*.json)")
        if archivoCredenciales_nombre:
            archivoCredenciales_nombreFull = os.path.normpath(archivoCredenciales_nombre) # normalizando la ruta

            self.nombreArchivoElegido=archivoCredenciales_nombreFull
            archivoCredenciales_soloNombre = archivoCredenciales_nombreFull.split(os.sep)[-1]

            # Mostrando el archivo de credenciales elegido en la label respectiva de
            # la GUI
            self.bel_nombreArchivoSelec.setText(archivoCredenciales_soloNombre)


    def procesarArchivoCrendenciales_y_generarToken(self):
        '''
        Para que el programa pueda interactuar con el classroom y google drive
        del usuario se necesita un token que lo permita, y para generar dicho
        token se necesita procesar el archivo un archivo de  crendeciales y
        que el usuario conceda ciertos permisos.LO QUE HARA ESTE METODO SERA
        cargar el archivo de credenciales que el usuario a escogido y solicitar
        los permisos al usuario para que se genere el token, si todo sale bien
        y el usuario hace todo lo anteriormente mencionado este metodo proseguira
        a cerrar esta aplicación.
        '''

        # ¿ya escogio un archivo de crendenciales el usuario?
        if self.nombreArchivoElegido!=None:

            # preguntarle al usuario si en realidad el archivo de credenciales que
            # escogio es el correcto
            respuestaPositiva=self.msg_asegurarEleccion(self.nombreArchivoElegido)

            if respuestaPositiva:
                try:

                    # copea el archivo de credenciales que adjunto el usuario en una ruta
                    # especifica, si ya existian un archivo de credenciales en esa ruta,
                    # entonces lo elimina y lo sustituye por el archivo de credenciales que
                    # el usuario selecciono
                    self.classRoomControl.cargarArchivoCredenciales(self.nombreArchivoElegido)

                    # procesa el archivo de credenciales que adjunto el usuario y solicita los
                    # permisos respectivos al usuario
                    self.classRoomControl.obtenerValor_service_classroom_and_drive()
                    self.msg_exitoCargarArchivo()
                    CargadorCrendencial.TOKEN_GENERADO_EXITOSAMENTE = True
                    self.close()

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
        Este metodo se llamara en dos cirscuntancias distintas y actuara
        de diferente forma dependiendo las cinscunstancias:
            - Si el usuario le de clic izquierdo sobre el boton
            de cerrar el programa, el metodo que se llamara es este,
            y lo que hara este metodo es preguntar al usuario si esta
            seguro de cerrar  el programa, en caso de que su respuesta
            sea afirmativa  se cerrara el programa.
            - Si el usuario a cargado el archivo de credenciales y generado
            el token, se llamara a este metodo, lo que hara hara este metodo
            es cerrar el programa.
        '''


        if CargadorCrendencial.TOKEN_GENERADO_EXITOSAMENTE:
            CargadorCrendencial.TOKEN_GENERADO_EXITOSAMENTE=True
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
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de querer cerrar la ventana del programa.

        Returns:
            - True (bool) : Si el usuario confirmo positivamente
            - False (bool): Si el usuario respondio que NO desea
        '''

        mensaje = "¿Esta seguro que quieres cerrar la ventana, recuerda que aun no has elegido un " \
                  "archivo de credenciales valido?"
        resultado=self.ventanaEmergenteDe_pregunta(mensaje)
        return resultado



    def msg_asegurarEleccion(self,nombreArchivoElegido):
        '''
        Ventana emergente que se le mostrara al usuario en la cual  se le preguntara si en realidad
        esta seguro de que el archivo que adjunto como archivo de credenciales es el correcto para
        ser procesado pedir los permisos y generar el token

        Parámetros:
            - nombreArchivoElegido (str): Nombre del archivo que el usuario selecciono
            como archivo de credenciales

        Returns:
            - True (bool) : Si el usuario confirmo positivamente
            - False (bool): Si el usuario respondio que NO desea
        '''

        mensaje = f"¿Esta seguro que el archivo cuyo nombre es: <<{nombreArchivoElegido}>> es el archivo " \
                  f"que contiene las credenciales?"
        resultado=self.ventanaEmergenteDe_pregunta(mensaje)
        return resultado

    def msg_debesCargarUnArchivo(self):
        '''
        Ventana emergente informativa que se le mostrara al usuario cuando
        este quiere procesar un archivo de credenciales que aun no ha sido
        elegido por el.
        '''

        mensaje = "Debes cargar un archivo"
        self.ventanaEmergenteDe_error(mensaje)

    def msg_exitoCargarArchivo(self):
        '''
        Ventana emergente informativa que se le mostrara al usuario para informarle
        que se ha creado con exito el token y que en un momento de abrira el programa
        principal
        '''

        mensaje = "Felicidades, el archivo de credenciales cargado es valido y el token ya se ha generado " \
                  ",a continuacion se cerrara esta ventana y se ejecutara el programa para que ya " \
                  "puedas comenzar a utilizarlo."
        self.ventanaEmergenteDe_informacion(mensaje)

    def msg_errorEnArchivoElegido(self,nombreArchivoElegido,exception_presentada):
        '''
        Ventana emergente informativa que se le mostrara al usuario para informarle
        que se ha producido un error al querer procesar el archivo de credenciales
        que adjunto y tambien para informarle que tipo de error se presento

        Parámetros:
            - nombreArchivoElegido (str): Nombre del archivo que el usuario
            escogio como archivo de credenciales
            - exception_presentada (str) : Excepccion que se presento al
            querer procesar el archivo que adjunto el usuario como archivo
            de credenciales
        '''

        mensaje = f"El nombre del archivo: <<{nombreArchivoElegido}>> el cual fue el que elegiste " \
                  f"NO es correcto, por favor "
        mensaje+=f" elige un archivo valido ya que al cargar dicho archivo ocurrio el siguiente error: << " \
                 f"{exception_presentada}>>"

        self.ventanaEmergenteDe_error(mensaje)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = CargadorCrendencial()
    application.show()
    app.exec()
    #sys.exit(app.exec())
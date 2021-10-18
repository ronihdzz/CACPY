'''
ConfirmadorAccion.py :
                    Contiene una sola  clase, la clase ' ConfirmadorAccion', la cual sirve
                    para mostrarle unas indicaciones al usuario y si esta el deacuerdo con
                    ellas deba repetir una frase de confirmacion para validar que esta
                    de acuerdo o entiende las indicaciones.
'''

__author__      = "David Roni Hernández Beltrán"
__email__ = "roni.hernandez.1999@gmail.com"


###########################################################################################################################################
# librerias estandar
###########################################################################################################################################
import sys

###########################################################################################################################################
# Paquetes de terceros
###########################################################################################################################################

from PyQt5.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.PERFIL.ConfirmacionAccion_d import Ui_Dialog
import recursos



class ConfirmadorAccion(QDialog, Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Esta clase sirve para hacerle tomar una desicion al usuario de la forma
    mas segura posible, es decir esta clase sirve para mostrarle al usuario
    un mensaje donde se le explica detalladamente que pasara si acepta, y
    esta clase le pedira al usuario repetir una frase para confirmar que
    esta de acuerdo con las indicaciones que le dieron a leer.Si el usuario
    repite la frase de confirmación y valida que esta seguro de tomar la desicion
    esta clase mandara una señal de que el usuario acepto y posteriormente
    proseguira a cerrarse.
    '''


    # Metodo constructor:
    accionConfirmada = pyqtSignal(bool) # esta señal solo se mandara el valor de True y solo
                                        # se enviara  si el usuario acepto las indicaciones
                                        # que se le mostraron

    def __init__(self,indicaciones="SIN INDICACIONES",palabraConfirmacion="SIN PALABRA DE CONFIRMACION"):
        '''
        Parámetros:
            -indicaciones (str): Representan el texto de las indicaciones que se le
            mostraran al usuario, las cuales deberan explicar claramente en que
            pasa si el usuario confirma la accion.
            -palabraConfirmacion (str): Representa la palabra que el usuario debera
            repetir para validar que esta deacuerdo con las indicaciones que leyo.
        '''

        Ui_Dialog.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)


        # El line edit en el que se mostrara la frase a repetir no podra
        # editar su contenido el usuario, solo podra verla
        self.lineEdit_wordRepetir.setReadOnly(True)

        # El textBrowser en el que se mostraran las indicaciones no podra
        # editar su contenido el usuario, solo podra verlo
        self.textBrowser_indicaciones.setReadOnly(True)

        # El textBrowser que mostrara las indicaciones tambien podra abrir links
        # que tiene adjuntos a el, si el usuario les da clic izquierdo sobre ellos
        self.textBrowser_indicaciones.setOpenExternalLinks(True)
        self.textBrowser_indicaciones.setOpenLinks(True)


        self.lineEdit_firma.textChanged.connect(self.validarFirma)
        self.btn_aceptar.clicked.connect(self.concretarAccion)
        self.firmaEscritaCorrectamente =False


        self.reiniciar(indicaciones=indicaciones, palabraConfirmacion=palabraConfirmacion)
        self.validarFirma()#para que se ponga en rojo...


    def prepararMostrar(self):
        '''
        El objetivo principal de este metodo sera preparar a esta clase
        para que el usuario pueda repetir la frase de validacion de accion
        como si nunca lo hubiera hecho antes, es decir este metodo:
            - Se encargara de eliminar el contenido del lineEdit, en donde el usuario
            escribe  la repeticion de la palabra de confirmacion.
            - Reseteara el valor de la variable bandera para que esta entienda
            que aun no se escribe la palabra de confirmacion
        '''

        self.lineEdit_firma.setText("")
        self.firmaEscritaCorrectamente=False
        self.validarFirma()


    def reiniciar(self,indicaciones,palabraConfirmacion,esHtmlIndicaciones=False):
        '''
        Cambiara el contenido de las indicaciones que se muestra por el valor contenido
        en el parametro: 'indicaciones', cambiara la palabra de confirmacion por el valor
        contenido en el parametro 'palabraConfirmacion'.
        Si el valor del parametro 'esHtmlIndicaciones' es igual a True las indicaciones
        las adjuntara en formato html, sin embargo si el valor del parametro 'esHtmlIndicaciones'
        es igual a False las indicaciones las adjuntara como texto normal.

        Parámetros:
            - indicaciones (str) : Representa a las indicaciones que se le presentaran al usuario
            las cuales explican que pasara si se repite la frase se confirmacion.
            - palabraConfirmacion (str): Representa la frase que el usuario debera escribir para
            confirmar la accion que quiere hacer.
            - esHtmlInidicaciones (bool): Si dicho parametro adquiere un valor de True, significara
            que las indicaciones vienen en formato de html, si  dicho parametro adquiere el valor de
            False significara que las indicaciones vienen en formato de texto normal
        '''

        if esHtmlIndicaciones:
            self.textBrowser_indicaciones.setHtml(indicaciones)
        else:
            self.textBrowser_indicaciones.setPlainText(indicaciones)

        self.palabraConfirmacion = palabraConfirmacion
        self.lineEdit_wordRepetir.setText(self.palabraConfirmacion)
        self.lineEdit_firma.setText("")

        self.prepararMostrar()



    def cargarIndicaciones(self,indicaciones,esHtml=False):
        '''
        Cambiara el contenido de las indicaciones que se muestra por el valor contenido
        en el parametro: 'indicaciones'.
        Si el valor del parametro 'esHtmlIndicaciones' es igual a True las indicaciones
        las adjuntara en formato html, sin embargo si el valor del parametro 'esHtmlIndicaciones'
        es igual a False las indicaciones las adjuntara como texto normal.

        Parámetros:
            - indicaciones (str) : Representa a las indicaciones que se le presentaran al usuario
            las cuales explican que pasara si se repite la frase se confirmacion.
            - esHtmlInidicaciones (bool): Si dicho parametro adquiere un valor de True, significara
            que las indicaciones vienen en formato de html, si  dicho parametro adquiere el valor de
            False significara que las indicaciones vienen en formato de texto normal
        '''

        if esHtml:
            self.textBrowser_indicaciones.setHtml(indicaciones)
        else:
            self.textBrowser_indicaciones.setPlainText(indicaciones)


    def concretarAccion(self):
        '''
        Una vez que el usuario repita la frase de confirmación debera dar clic sobre un boton
        para validar que en realidad esta seguro, cuando esto suceda este metodo le preguntara
        a travez de una cuadro emergente si en realidad desea hacer dicha accion, si el usuario
        confirma positivamente se cerrara esta ventana y se emitira una señal que significara
        de que el usuario ha confirmado la accion y esta seguro de aceptar las consecuencias.
        '''

        if self.palabraConfirmacion!=self.lineEdit_firma.text():
            self.msg_lasPalabrasNoCoinciden()
        else:
            resultado=self.msg_cersiorarDesicion()
            if resultado:
                self.firmaEscritaCorrectamente=True
                self.close()

    # primer metodo para validar el dato nombre
    def validarFirma(self):
        '''
        Cada vez que el usuario escriba algo en el lineEdit en donde se debe escribir la
        frase de confirmación, este metodo revisara si ya se cumple con la repeticion
        exacta de la frase de repeticion, si este metodo detecta que la frase que escribio
        el usuario es exactamente igual a la frase de repeticion el contorno del lineEdit
        en donde debe escribir la frase de confirmacion el usuario cambiara a color verde,
        en caso contrario sera de color rojo.
        '''


        if self.palabraConfirmacion!=self.lineEdit_firma.text():
            self.lineEdit_firma.setStyleSheet("border-radius:5px; border:5px solid red;")
        else:
            self.lineEdit_firma.setStyleSheet("border-radius:5px; border: 5px solid green;")

    def closeEvent(self, event):
        '''
        Este metodo se sobreescribio para que tenga dos comportamientos diferentes
        que dependeran del valor de atributo de instancia: 'self.firmaEscritaCorrectamente'.

        Los comportamientos son los siguientes:
            * Si se manda a llamar este metodo atraves de: 'self.close()' y la
            variable de instancia: 'self.firmaEscritaCorrectamente' es igual a True,
            este metodo emitira la señal: 'self.accionConfirmada' antes de cerrar
            esta ventana
            * Si se cierra la ventana dando clic izquierdo sobre el tache superior derecho
            de esta ventana unicamente se cerrar la ventana sin emitir ninguna señal
        '''


        if self.firmaEscritaCorrectamente:
            self.accionConfirmada.emit(True)

        event.accept()

####################################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################

    def msg_cersiorarDesicion(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de preguntarle el profesor
        si en realidad desea aceptar los terminos que se explican en las indicaciones

        Returns:
            True : En caso de que el profesor presione el boton de 'Si'
            False: En caso de que el profesor presione el boton de 'No'
        '''

        mensaje = "¿Estas seguro de lo que haras?¿Leiste correctamente las indicaciones"

        resultado=self.ventanaEmergenteDe_pregunta(mensaje)

        return resultado

    def msg_lasPalabrasNoCoinciden(self):
        '''
        Mostrara un cuadro de dialogo con el objetivo de: informarle al
        profesor que la frase o palabra que escribio no coinciden con
        la frase de confirmación
        '''

        mensaje = "Las palabras no coinciden"

        self.ventanaEmergenteDe_error(mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogo = ConfirmadorAccion("BLABLABLABLABLA","acepto los terminos")
    dialogo.show()
    app.exec_()


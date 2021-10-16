
'''
CambiadorClasesNbGrader.py :    Contine una sola  clase, la clase 'CambiadorClases_NbGrader', la cual  es una clase
                                que a grosso modo se encarga de hacer posible que el usuario pueda seleccionar la
                                clase de NbGrader que desee.
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

from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

###########################################################################################################################################
# fuente local
###########################################################################################################################################

from CUERPO.DISENO.CONFIGURACION.CambiadorClases_d import Ui_Dialog
import recursos


class CambiadorClases_NbGrader(QtWidgets.QDialog,Ui_Dialog,recursos.HuellaAplicacion):
    '''
    Se encarga de hacer posible que el usuario pueda seleccionar la clase de NbGrader
    que desee, por ende le muestra todas las clases de NbGrader entre las que puede
    elegir, si el usuario no ve las clase de NbGrader que desea, le ofrece la opccion
    de actualizar las clases de NbGrader que puede elegir.
    Si el usuario se decanta por seleccionar una clase de NbGrader, esta clase emitira
    una señal.
    '''

    senal_eligioUnCurso=pyqtSignal(bool) # Mandara solo  el valor de: True, y este se mandara solo
                                         # cuando el usuario haya escogido una clase de NbGrader

    def __init__(self,configuracionCalificador):
        '''
        Parámetros:
            - configuracionCalificador (objeto de la clase: CalificadorConfiguracion): dicho objeto
            contiene ordenados los datos de configuracion que necesitara el programa, asi como tambien
            contiene metodos que serviran para obtener o editar dichos datos
        '''


        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        recursos.HuellaAplicacion.__init__(self)
        self.bel_tipoClase.setText("Clase Nb-grader")

        self.configuracionCalificador=configuracionCalificador

        self.btn_refrescarLasClases.clicked.connect(self.refrescarClasesNbGrader)
        self.btn_realizarCambio.clicked.connect(self.realizarCambioClase)

        self.listaClases=[]
        self.cargarDatosClasesNbGrader()



    def refrescarClasesNbGrader(self):
        '''
        Primera pregunta si se desea refrescar las clases de NbGrader que se muestran,en caso
        de que el usuario de una respuesta positiva, se hara exactamente lo mismo que el metodo
        'self.cargarDatosClasesNbGrader' y le avisara al usuario cuando esta acción haya sido realizada.
        '''

        respuestaPositiva=self.msg_preguntarAcercaRefrescarClases()

        if respuestaPositiva:
            self.cargarDatosClasesNbGrader()
            self.msg_exitoAlRefrescar()


    def cargarClaseNbGrader(self,nombreClase):
        '''
        Buscara si el valor del parametro: 'nombreClase' corresponde
        a una clase NbGrader existente, de ser afirmativo: seleccionara
        dicha clase en el combox de esta ventana y aparte retornara True,
        en caso contrario unicamente retornara False.

        Parámetros:
            - nombreClase (str): Nombre de la clase NbGrader el cual se desea
            saber si es un nombre existente.

        Returns:
            True (bool) : Si el parametro: 'nombreClase' corresponde
            a una clase NbGrader existente.
            False (bool): Si el parametro: 'nombreClase' NO corresponde
            a una clase de NbGrader existente.
        '''

        if nombreClase in self.listaClases:
            self.comboBox_clases.setCurrentText(nombreClase)
            return True
        return False


    def cargarDatosClasesNbGrader(self):
        '''
        Revisara la ruta respectiva en donde se deben crear las clases de NbGrader,y
        vera cuales existen, posteriormente cargara sus nombres y las mostrara en el
        combo box para que el usuario pueda elegir alguna de ellas.
        '''

        self.listaClases=[]
        self.listaClases=os.listdir(recursos.App_Principal.RUTA_NB_GRADER)
        self.comboBox_clases.clear()
        self.comboBox_clases.addItems( self.listaClases )


    def realizarCambioClase(self):
        '''
        Preguntara acera de si en realidad se desea cambiar a la clase de NbGrader
        seleccionada, de ser positiva la respuesta entonces guardara el nuevo valor
        de la clase de NbGrader en el objeto: 'self.configuracionCalificador' y
        finalmente mandara una señal indicando que se ha cambiado de clase de NbGrader
        y cerrara la ventana.
        '''

        if len(self.listaClases)>0:
            cursoElegido_nombre=self.comboBox_clases.currentText()
            respuestaPositiva=self.msg_confirmarEleccionClaseNbGrader(nombreClaseNbGraderSelec=cursoElegido_nombre)
            if respuestaPositiva:

                # Guardando en el objeto de configuraciones el nuevo nombre de la clase
                # NbGrader seleccionada
                self.configuracionCalificador.set_clase_nombreNbGrader(cursoElegido_nombre)

                # Mostrara la clase de NbGrader elegida en la label respetiva
                self.bel_nombreClaseActual.setText(cursoElegido_nombre)

                self.senal_eligioUnCurso.emit(True)

                self.close()

        # no puedes elegir cuando no hay ninguna clase de NbGrader registrada
        else:
            self.msg_noPuedesElegirClase_siNoHay()


##########################################################################################################################
# M E N S A J E S     E M E R G E N T E S :
####################################################################################################################################


    def msg_confirmarEleccionClaseNbGrader(self, nombreClaseNbGraderSelec):
        '''
        Mostrar una ventana emergente con la finalidad de preguntarle al usuario
        si en realidad desea elegir la clase de NbGrader seleccionada.

        Parámetros:
            nombreClaseNbGraderSelec (str) : Nombre de la clase de NbGrader que el
            usuario selecciono

        Returns:
            True (bool) : En caso de que la respuesta del usuario haya sido afirmativa
            False (bool): En caso de que la respuesta del usuario haya sido negativa
        '''


        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = f"¿En verdad la clase de NbGrader con el nombre de: <<{nombreClaseNbGraderSelec}>> "
        mensaje += " es la clase de NbGrader que deseas elegir? "
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


    def msg_noPuedesElegirClase_siNoHay(self):
        '''
        Mostrara una cuadro de dialogo con el objetivo de informarle
        al usuario que no puede seleccionar ninguna clase de NbGrader
        por que no hay ninguna clase de NbGrader registrada.
        '''


        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Warning)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "No puedes seleccionar ninguna clase de NbGrader, ya que no tienes "
        mensaje+= "ninguna clase NbGrader registrada, "
        mensaje += "en caso de que si tengas una clase de NbGrader registrada y no se visualice aqui, "
        mensaje += "por favor da clic sobre el boton refrescar para que apare<ca entre las  "
        mensaje += "clases de NbGrader elegibles."

        mensaje = self.huellaAplicacion_ajustarMensajeEmergente(mensaje)

        ventanaDialogo.setText(mensaje)
        ventanaDialogo.setStandardButtons(QMessageBox.Ok)
        btn_ok = ventanaDialogo.button(QMessageBox.Ok)
        btn_ok.setText('Entendido')
        ventanaDialogo.exec_()



    def msg_preguntarAcercaRefrescarClases(self):
        '''
        Mostrar una ventana emergente con la finalidad de preguntarle al usuario
        si en realidad desea refrescar

        Returns:
            True (bool) : En caso de que la respuesta del usuario haya sido afirmativa
            False (bool): En caso de que la respuesta del usuario haya sido negativa
        '''


        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Question)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Solo es recomendable refrescar cuando no vez la clase que deseas "
        mensaje+="¿en verdad la clase que deseas no se encuentra en la lista? "
        mensaje+="¿en verdad necesitas refrescar?"
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

    def msg_exitoAlRefrescar(self):
        '''
        Mostrara un cuadro de dialogo al usuario con la finalidad de  informarle que se
        ha refrescado exitosamente.
        '''


        ventanaDialogo = QMessageBox()
        ventanaDialogo.setIcon(QMessageBox.Information)
        ventanaDialogo.setWindowIcon(QtGui.QIcon(self.ICONO_APLICACION))
        ventanaDialogo.setWindowTitle(self.NOMBRE_APLICACION)

        mensaje = "Ya se reviso en la ruta debida en donde se encuentra las clases de NbGrader creadas "
        mensaje+= "y ya se cargaron  para que usted puede visualizarlas y elegir alguna de ellas, sin embargo "
        mensaje+= "es importante recalcar que si no vez ningun cambio es por que no  "
        mensaje+= "se encontraron clases de NbGrader nuevas registradas."

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